#!/usr/bin/env python3
"""
Configuration Helper for Miller 3 Data Scraper
Helps users easily set up download directories and other preferences
"""

import os
import yaml
from pathlib import Path

def create_custom_config():
    """Interactive config file creation"""
    print("🔧 Miller 3 Data Scraper - Configuration Setup")
    print("=" * 50)
    
    config = {}
    
    # Download Directory
    print("\n📁 Download Directory Configuration")
    print("-" * 35)
    print("Where would you like to save downloaded files?")
    print("1. Current directory/downloads (default)")
    print("2. Desktop/Miller3Downloads")
    print("3. Documents/Miller3Downloads") 
    print("4. Custom location")
    
    while True:
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == "1":
            config['download_dir'] = os.path.join(os.getcwd(), "downloads")
            break
        elif choice == "2":
            desktop = os.path.join(os.path.expanduser("~"), "Desktop", "Miller3Downloads")
            config['download_dir'] = desktop
            break
        elif choice == "3":
            documents = os.path.join(os.path.expanduser("~"), "Documents", "Miller3Downloads")
            config['download_dir'] = documents
            break
        elif choice == "4":
            custom_path = input("Enter full path: ").strip()
            if custom_path:
                config['download_dir'] = os.path.expanduser(custom_path)
                break
            else:
                print("❌ Please enter a valid path")
                continue
        else:
            print("❌ Invalid choice")
            continue
    
    # Create the directory
    try:
        os.makedirs(config['download_dir'], exist_ok=True)
        print(f"✅ Created download directory: {config['download_dir']}")
    except Exception as e:
        print(f"⚠️ Warning: Could not create directory: {e}")
    
    # State Selection
    print("\n🗺️  State Configuration")
    print("-" * 25)
    
    states = [
        "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
        "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
        "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
        "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
        "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
        "New Hampshire", "New Jersey", "New Mexico", "New York",
        "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
        "West Virginia", "Wisconsin", "Wyoming"
    ]
    
    print("Select state to scrape (or press Enter for Alabama):")
    for i, state in enumerate(states[:10], 1):
        print(f"{i:2d}. {state}")
    print("    ... (type state name for others)")
    
    state_input = input("\nState name or number: ").strip()
    
    if not state_input:
        selected_state = "Alabama"
    elif state_input.isdigit():
        idx = int(state_input) - 1
        if 0 <= idx < len(states):
            selected_state = states[idx]
        else:
            selected_state = "Alabama"
    else:
        # Try to match state name
        state_input = state_input.title()
        if state_input in states:
            selected_state = state_input
        else:
            print(f"⚠️ State '{state_input}' not found, using Alabama")
            selected_state = "Alabama"
    
    config['search_parameters'] = {
        'geography_type': 'state',
        'state': selected_state,
        'include_closed': False,
        'include_unverified': True
    }
    
    print(f"✅ Selected state: {selected_state}")
    
    # Batch Configuration
    print("\n📦 Batch Configuration")
    print("-" * 23)
    print("How many pages per batch? (default: 10)")
    print("Smaller batches = more frequent downloads, easier to resume")
    print("Larger batches = fewer files, faster overall")
    
    batch_input = input("Pages per batch (5-50): ").strip()
    try:
        pages_per_batch = int(batch_input)
        if 5 <= pages_per_batch <= 50:
            config['pages_per_batch'] = pages_per_batch
        else:
            config['pages_per_batch'] = 10
            print("⚠️ Using default: 10 pages per batch")
    except ValueError:
        config['pages_per_batch'] = 10
        print("⚠️ Using default: 10 pages per batch")
    
    # Library Credentials (optional)
    print("\n📚 Library Credentials (Optional)")
    print("-" * 35)
    print("If you have library access credentials, enter them here.")
    print("Otherwise, press Enter to skip.")
    
    library_name = input("Library name (e.g., 'Cobb County Library'): ").strip()
    if library_name:
        username = input("Username/Card Number: ").strip()
        password = input("Password/PIN: ").strip()
        
        if username and password:
            config['library_credentials'] = {
                library_name: {
                    'username': username,
                    'password': password
                }
            }
            print(f"✅ Added credentials for {library_name}")
        else:
            print("⚠️ Incomplete credentials, skipping")
    
    # Default values
    config.update({
        'auth_url': 'http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Quick/497be73bf9a94fe3aebb7eb4857b584f',
        'pages_to_download': 'all',
        'state_file': 'reference_usa_state.json'
    })
    
    # Save config
    config_dir = "config"
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, "my_referenceusa_config.yaml")
    
    try:
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
        
        print(f"\n✅ Configuration saved to: {config_file}")
        print("\n📋 Your Configuration Summary:")
        print(f"   📁 Download Directory: {config['download_dir']}")
        print(f"   🗺️  State: {config['search_parameters']['state']}")
        print(f"   📦 Pages per Batch: {config['pages_per_batch']}")
        
        print("\n🚀 Ready to run! Use one of these commands:")
        print(f"   python3 reference_usa_scraper_enhanced.py --config={config_file}")
        print(f"   python3 reference_usa_scraper_enhanced.py")
        
        return config_file
        
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return None

def show_existing_configs():
    """Show existing configuration files"""
    config_locations = [
        "config/referenceusa_config.yaml",
        "config/my_referenceusa_config.yaml", 
        "referenceusa_config.yaml"
    ]
    
    found_configs = []
    for location in config_locations:
        if os.path.exists(location):
            found_configs.append(location)
    
    if found_configs:
        print("📋 Existing Configuration Files:")
        for i, config_path in enumerate(found_configs, 1):
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                state = config.get('search_parameters', {}).get('state', 'Unknown')
                download_dir = config.get('download_dir', 'Unknown')
                
                print(f"{i}. {config_path}")
                print(f"   State: {state}")
                print(f"   Download Dir: {download_dir}")
                print()
                
            except Exception as e:
                print(f"{i}. {config_path} (Error reading: {e})")
    else:
        print("📋 No existing configuration files found")
    
    return found_configs

def main():
    """Main configuration helper"""
    print("🔧 Miller 3 Data Scraper - Configuration Helper")
    print("=" * 55)
    
    # Show existing configs
    existing = show_existing_configs()
    
    print("\nWhat would you like to do?")
    print("1. Create new configuration")
    print("2. Use existing configuration")
    print("3. Show download directory options")
    print("4. Exit")
    
    while True:
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == "1":
            create_custom_config()
            break
        elif choice == "2":
            if existing:
                print("\nSelect configuration to use:")
                for i, config_path in enumerate(existing, 1):
                    print(f"{i}. {config_path}")
                
                try:
                    selection = int(input("Choice: ")) - 1
                    if 0 <= selection < len(existing):
                        selected_config = existing[selection]
                        print(f"\n✅ Using configuration: {selected_config}")
                        print(f"Run: python3 reference_usa_scraper_enhanced.py --config={selected_config}")
                    else:
                        print("❌ Invalid selection")
                except ValueError:
                    print("❌ Invalid selection")
            else:
                print("❌ No existing configurations found")
            break
        elif choice == "3":
            print("\n📁 Common Download Directory Options:")
            print(f"   Current directory: {os.getcwd()}/downloads")
            print(f"   Desktop: {os.path.expanduser('~/Desktop')}/Miller3Downloads")
            print(f"   Documents: {os.path.expanduser('~/Documents')}/Miller3Downloads")
            print(f"   External drive: /Volumes/YourDrive/Miller3Downloads")
            print("\n💡 Tips:")
            print("   - Use absolute paths for external drives")
            print("   - Ensure the directory has enough space")
            print("   - Test write permissions before running")
            continue
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")
            continue

if __name__ == "__main__":
    main()
