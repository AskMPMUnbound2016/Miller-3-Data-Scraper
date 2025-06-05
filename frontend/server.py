"""
Flask server for Data Axle Scraper
This serves the frontend and handles API requests
"""
import os
import sys
import yaml
import time
import threading
from flask import Flask, request, jsonify, send_from_directory, after_this_request
from flask_cors import CORS

# Get the base directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Import ReferenceUSA scraper
sys.path.append(base_dir)
from reference_usa_scraper import ReferenceUSAScraper

# Setup paths
frontend_dir = os.path.join(base_dir, "frontend")
config_dir = os.path.join(base_dir, "config")
config_file = os.path.join(config_dir, "referenceusa_config.yaml")

# Make sure directories exist
os.makedirs(config_dir, exist_ok=True)
os.makedirs(os.path.join(base_dir, "downloads"), exist_ok=True)

# Create Flask app
app = Flask(__name__, static_folder=frontend_dir)
# Enable CORS
CORS(app)

# Global variables
scraper = None
is_running = False
scraper_thread = None
log_data = []

# Create a default config if one doesn't exist
def create_default_config():
    """Create a default configuration file"""
    # Create the downloads directory
    download_dir = os.path.join(base_dir, "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    config = {
        "download_dir": download_dir,
        "auth_url": "https://login.openathens.net/auth/cobbcounty.org/o/72388178",
        "library_credentials": {
            "Cobb County Library": {
                "username": "202124402",
                "password": "3353"
            }
        },
        "search_parameters": {
            "state": "New Mexico",
            "include_unverified": True,
            "include_closed": False
        },
        "pages_per_batch": 10,
        "pages_to_download": "all",
        "state_file": os.path.join(config_dir, "reference_usa_state.json")
    }
    
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"Created default configuration file: {config_file}")
    return config_file

# Routes
@app.route('/')
def index():
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(frontend_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(frontend_dir, path)

# API Routes
@app.route('/api/config', methods=['GET', 'OPTIONS'])
def get_config():
    try:
        # Create default config if it doesn't exist
        if not os.path.exists(config_file):
            create_default_config()
            
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        response = jsonify(config)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        import traceback
        error_msg = f"Error loading config: {str(e)} - {traceback.format_exc()}"
        print(error_msg)
        response = jsonify({"error": error_msg})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/api/config', methods=['POST'])
def save_config():
    try:
        config_data = request.json
        
        # Create backup of the current config file
        if os.path.exists(config_file):
            backup_file = config_file + '.bak'
            with open(config_file, 'r') as src, open(backup_file, 'w') as dst:
                dst.write(src.read())
        
        # Save the new config
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False)
        
        return jsonify({"success": True, "message": "Configuration saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/run', methods=['POST'])
def run_scraper():
    global scraper_thread, is_running
    
    if is_running:
        return jsonify({"error": "Scraper is already running"}), 400
    
    data = request.json
    start_batch = data.get('startBatch', 1)
    end_batch = data.get('endBatch', 10)
    
    # Start the scraper in a new thread
    scraper_thread = threading.Thread(
        target=run_scraper_thread, 
        args=(start_batch, end_batch)
    )
    scraper_thread.daemon = True
    scraper_thread.start()
    
    return jsonify({"success": True, "message": "Scraper started"})

def run_scraper_thread(start_batch, end_batch):
    global is_running, scraper
    
    try:
        is_running = True
        log_data.clear()
        add_log(f"=== ReferenceUSA Scraper ===")
        add_log(f"Starting batch: {start_batch}")
        add_log(f"Ending batch: {end_batch}")
        
        # Initialize the scraper
        scraper = ReferenceUSAScraper(config_file)
        
        # Override the scraper's print function to capture logs
        def log_capture(message):
            add_log(message)
        scraper.print_function = log_capture
        
        # Run the scraper
        scraper.run(start_batch, end_batch)
        
        add_log("Scraper completed successfully")
    except Exception as e:
        add_log(f"Error: {str(e)}", "error")
    finally:
        is_running = False

@app.route('/api/stop', methods=['POST'])
def stop_scraper():
    global scraper_thread, is_running, scraper
    
    if not is_running:
        return jsonify({"error": "Scraper is not running"}), 400
    
    # Attempt to stop the scraper
    try:
        if scraper and hasattr(scraper, 'browser_manager'):
            scraper.browser_manager.close()
        
        is_running = False
        add_log("Scraper stopped by user", "warning")
        return jsonify({"success": True, "message": "Scraper stopped"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify(log_data)

def add_log(message, level="info"):
    timestamp = time.strftime("%H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "message": message,
        "level": level
    }
    log_data.append(log_entry)
    print(f"[{timestamp}] {message}")

if __name__ == "__main__":
    # Make sure the config file exists
    if not os.path.exists(config_file):
        create_default_config()
    
    # Start the Flask app
    app.run(debug=False, port=5000)
