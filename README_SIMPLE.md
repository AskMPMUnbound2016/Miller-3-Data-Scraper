# MILLER 3 DATA SCRAPER - SIMPLIFIED GUIDE
==========================================

## 🎯 THREE SIMPLE OPTIONS

### 1. 🤖 PAGINATION MODE
- Manual login once
- **Automated page navigation**
- **Automated record selection and downloading**
- **Automated unchecking of prior batch records**
- Best for large datasets - fully hands-off

### 2. 📋 NO PAGINATION MODE  
- Manual login once
- **Manual page navigation** (you go to each page)
- **Automated record selection and downloading**
- **Automated unchecking of prior batch records**
- Best when you want control over which pages to process

### 3. 🔗 MERGE CSV FILES
- **Combine multiple downloaded CSV files into one**
- **Remove duplicate records automatically**
- **Choose all files, specific files, or limit by record count**
- **Add source file tracking to merged data**
- Perfect for consolidating batch downloads

## 🚀 QUICK START

### Option 1: Use the Main Launcher
```bash
cd "/Users/admin/Desktop/Build/Coded/Miller 3 Data Scaper"
python3 start_scraper.py
```
Then choose option 1 (Pagination), 2 (No Pagination), or 3 (Merge CSV Files)

### Option 2: Run Directly

**Pagination Mode:**
```bash
python3 run_enhanced_scraper.py
```

**No Pagination Mode:**
```bash
python3 run_manual_simple.py
```

**CSV Merger:**
```bash
python3 run_csv_merger.py
```

## 📋 SCRAPER WORKFLOW

### BOTH SCRAPING MODES START THE SAME:
1. 🌐 Script opens: `http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Quick/497be73bf9a94fe3aebb7eb4857b584f`
2. 🔐 Complete OpenAthens authentication if prompted
3. 🔍 Set up your search criteria (location, industry, etc.)
4. 🎯 Click "Search" or "View Results"
5. ⏳ Wait for search results to load
6. ✅ Tell script you're ready to proceed

### THEN THEY DIFFER:

**🤖 PAGINATION MODE:**
- Script automatically navigates through pages
- Script automatically selects records on each page
- Script automatically downloads batches
- Script automatically unchecks prior batch records
- You just monitor progress

**📋 NO PAGINATION MODE:**
- You manually navigate to each page (script tells you which page)
- Script automatically selects records on that page
- Script automatically downloads batches
- Script automatically unchecks prior batch records
- You control the pace and page selection

## 🔗 CSV MERGER WORKFLOW:
1. 📊 Shows all CSV files in downloads folder with statistics
2. 🎯 Choose merge options:
   - **All files** - merge everything
   - **Specific files** - choose by file numbers (e.g., 1,3,5-8)
   - **Record limit** - merge until you reach X records
   - **Date range** - merge files from specific dates
3. 📝 Enter output filename (or use suggested name)
4. 🔗 Files are merged with duplicate removal
5. 📋 Source file tracking added to each record
6. ✅ Combined file saved to downloads folder

## 💾 CSV MERGER FEATURES:
- **Smart duplicate detection** - removes exact duplicate records
- **Source tracking** - adds source_file column to track which file each record came from
- **Record counting** - shows exactly how many records from each file
- **Flexible selection** - merge all, specific files, or limit by count/date
- **Error handling** - skips problematic files and continues
- **File size reporting** - shows total records and file size

## 📁 FILES ARE SAVED TO:
- `downloads/` folder in the scraper directory
- Session state saved automatically
- Can resume if interrupted

## 💡 WHICH MODE TO CHOOSE?

**Choose PAGINATION MODE if:**
- You have many pages to process (50+ pages)
- You want fully hands-off automation
- You want to process all pages in sequence

**Choose NO PAGINATION MODE if:**
- You want control over which specific pages to process
- You want to monitor each page individually
- You want to pause/resume at specific points
- You want to skip certain pages

**Choose CSV MERGER if:**
- You have multiple downloaded CSV files to combine
- You want to remove duplicate records
- You need one consolidated file for analysis
- You want to track which file each record came from

## 🔧 REQUIREMENTS
- Python 3.7+
- Chrome browser
- ChromeDriver (included)
- Required packages: `pip install -r requirements.txt`
  - pandas (for CSV merging)
  - selenium (for web scraping)
  - pyyaml (for configuration)

## 📞 TROUBLESHOOTING
- If authentication fails: Check OpenAthens credentials
- If wrong page loads: Verify the URL is correct
- If stuck: Press Ctrl+C to stop and restart
- Session data is saved automatically for resuming
- For CSV merger: Ensure CSV files are in downloads folder

## 🎯 TYPICAL WORKFLOW
1. **First**: Use Pagination or No Pagination mode to download data
2. **Then**: Use CSV Merger to combine all downloaded files
3. **Result**: One clean, consolidated CSV file with all your data
