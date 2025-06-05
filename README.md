# Data Axle Scraper

A web scraping tool for retrieving business information from Data Axle (previously ReferenceUSA) through library access.

## Overview

This tool automates the process of:
1. Authenticating to Data Axle through your library credentials
2. Navigating to the business database
3. Setting search criteria
4. Downloading business data in batches

The scraper includes a web interface for easy configuration and control.

## Requirements

- Python 3.7 or higher
- Google Chrome browser
- Valid library card credentials for a library that offers Data Axle access

## Quick Start

### Windows
1. Double-click `Quick_Start.bat`
2. The server will start and open the web interface in your browser
3. Configure your library credentials and search parameters
4. Click "Run Scraper" to start

### Mac
1. Double-click `Quick_Start.command` (you may need to make it executable first with `chmod +x Quick_Start.command`)
2. The server will start and open the web interface in your browser
3. Configure your library credentials and search parameters
4. Click "Run Scraper" to start

### Manual Start
1. Open a terminal or command prompt
2. Navigate to the DataAxleScraper directory
3. Run `python start_server.py`
4. Open a browser and go to http://localhost:5000

## Multiple Connection Options

If you experience connection issues, try one of these alternatives:

### Alternate Port (If port 5000 is blocked or in use)
Run the server on a different port:
```
python start_server.py --port 8080
```
Then access at http://localhost:8080

### Proxy Server (For CORS issues)
Run the proxy server:
```
python proxy_server.py
```
Then access at http://localhost:8000

### Offline Mode (No web interface)
Run directly from command line:
```
python offline_mode.py --start 1 --end 10
```

## Configuration

Edit the configuration through the web interface or directly modify `config/referenceusa_config.yaml`:

```yaml
download_dir: "./downloads"
auth_url: "https://login.openathens.net/auth/yourlibrary.org/..."
library_credentials:
  Your Library Name:
    username: "YOUR_LIBRARY_CARD_NUMBER"
    password: "YOUR_PIN"
search_parameters:
  # Choose ONE of the following geography filter options:
  
  # Option 1: State/City/County/MSA filter
  state: "Georgia"              # Search by state only
  # state: "Atlanta, GA"        # Search by city and state
  # state: "Fulton County"      # Search by county
  # state: "Atlanta-Sandy Springs-Alpharetta"  # Search by Metropolitan Statistical Area
  
  # Option 2: ZIP code filter
  # zip_codes: "30339"          # Search by a single ZIP code
  # zip_codes: "30339, 30080"   # Search by multiple ZIP codes
  
  include_unverified: true
  include_closed: false
pages_per_batch: 10
pages_to_download: "all"
state_file: "reference_usa_state.json"
```

## Geographic Filtering

The scraper supports two types of geographic filtering:

### 1. State/City/County/MSA Filtering
Using the `state` parameter:
- **State only**: `state: "California"`
- **City and State**: `state: "Miami, FL"`
- **County**: `state: "Orange County"`
- **Metropolitan Statistical Area (MSA)**: `state: "Dallas-Fort Worth-Arlington"`

### 2. ZIP Code Filtering
Using the `zip_codes` parameter:
- **Single ZIP code**: `zip_codes: "30339"`
- **Multiple ZIP codes**: `zip_codes: "30339, 30080, 30060"`

You must choose one type of filtering - either state-based OR ZIP code-based. If both are specified, the ZIP code filter will be used.

For more detailed instructions, see the `Instructions/GEOGRAPHY_FILTERS.md` file.

## Troubleshooting

### Web Interface Connection Problems
- Make sure the server is running (check command line window)
- Try restarting the server
- Check if port 5000 is already in use by another application
- Try using the proxy server option

### Authentication Issues
- Verify your library credentials are correct
- Some libraries have specific authentication methods - you may need to manually assist with authentication the first time
- The scraper can handle multi-tab authentication flows but may need your assistance

### Browser Automation Problems
- Ensure Chrome is installed and up-to-date
- The scraper uses Selenium to automate Chrome - make sure you haven't disabled automation features
- If Chrome updates break functionality, try updating the scraper dependencies with `python install.py`

## Advanced Configuration

### Multi-tab Authentication
The scraper now supports authentication flows that open in new tabs.

## License

This tool is provided for educational purposes only. Please use responsibly and in accordance with Data Axle's terms of service.
