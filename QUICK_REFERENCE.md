# MILLER 3 DATA SCRAPER - QUICK REFERENCE
============================================

## 🔗 CORRECT URL
http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Quick/497be73bf9a94fe3aebb7eb4857b584f

## 📋 WORKFLOW STEPS

### 1. AUTHENTICATION
- Script opens the OpenAthens proxy URL
- Complete OpenAthens authentication if prompted
- You should see "ReferenceUSA U.S. Business Quick Search" page

### 2. SEARCH SETUP
- Fill in your search criteria:
  - Location (state, city, zip code)
  - Industry/SIC codes
  - Company size
  - Other filters as needed
- Click "Search" or "View Results" button
- Wait for search results to load

### 3. RESULTS PAGE
- You should see a list of business records
- Look for pagination controls (Page 1 of X)
- Note the total number of pages
- This is where you'll tell the script you're ready

### 4. SCRAPER OPERATION
- Manual Version: You navigate, script guides you
- Automated Version: Script handles navigation and selection

## 🚀 QUICK START COMMANDS

### Manual Version (Manual Pagination):
```bash
cd "/Users/admin/Desktop/Build/Coded/Miller 3 Data Scaper"
python3 run_manual_simple.py
```

### Automated Version (Automated Pagination):
```bash
cd "/Users/admin/Desktop/Build/Coded/Miller 3 Data Scaper"
python3 run_enhanced_scraper.py
```

### Test Both Versions:
```bash
python3 test_scrapers.py
```

## 📁 FILE LOCATIONS
- Downloads: `downloads/` folder
- Session state: `manual_scraper_state.json`
- Configuration: `config/referenceusa_config.yaml`
- Logs: `logs/` folder

## ⚠️ IMPORTANT NOTES
- Always start from the Quick Search page
- Make sure you can see business records before continuing
- The script works with the pagination controls
- Sessions are automatically saved and can be resumed
- Both versions handle batches of up to 10 pages

## 🔧 CONFIGURATION
The correct URL is now configured in:
- Default URL in all Python files
- Configuration file: `config/referenceusa_config.yaml`
- Can be overridden if needed

## 📞 TROUBLESHOOTING
- If authentication fails: Check OpenAthens credentials
- If wrong page loads: Verify the URL is correct
- If no records show: Check search criteria
- If pagination missing: Make sure search returned results
