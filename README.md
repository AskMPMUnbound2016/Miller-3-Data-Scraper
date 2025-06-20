# Miller 3 Data Scraper

A powerful, automated web scraper designed for extracting business data from ReferenceUSA through library authentication systems. This tool provides both manual and automated options for data collection with built-in CSV merging capabilities.

## 🚀 Quick Start

### 1. Run the Main Launcher
```bash
python start_scraper.py
```

Choose from three options:
- **🤖 PAGINATION** - Full automation mode
- **📋 NO PAGINATION** - Semi-automated mode  
- **🔗 MERGE CSV FILES** - Combine downloaded files

### 2. System Requirements
- Python 3.7+
- Chrome browser installed
- ChromeDriver (included)
- Library access to ReferenceUSA

## 📋 Features

### 🤖 Automation Modes

**PAGINATION MODE (Full Automation)**
- ✅ Manual login once
- 🤖 **Automated page navigation** - automatically goes through pages 1-10, 11-20, etc.
- 🤖 **Automated record selection** - selects all records on each page
- 🤖 **Automated downloading** - handles CSV format and detailed settings
- 🤖 **Automated cleanup** - unchecks prior batch records
- 🤖 **Process batches** - continues until all pages complete
- 💾 **Session saving** - resume if interrupted

**NO PAGINATION MODE (Semi-Automated)**
- ✅ Manual login once
- 👤 **Manual page navigation** - you navigate to each page manually
- 🤖 **Automated record selection** - automatically selects records
- 🤖 **Automated downloading** - handles CSV format and detailed settings
- 🤖 **Automated cleanup** - unchecks prior batch records
- 💾 **Session saving** - resume if interrupted

### 🔗 CSV Merger
- **Combine multiple files** - merge all downloaded CSV files
- **Remove duplicates** - automatically detect and remove duplicate records
- **Flexible selection** - choose specific files, date ranges, or record limits
- **Source tracking** - adds source file column for traceability
- **Smart naming** - automatic filename suggestions

## 🎯 Step-by-Step Usage

### Option 1: PAGINATION MODE (Recommended for Large Jobs)

1. **Start the scraper:**
   ```bash
   python start_scraper.py
   ```
   Choose option **1** (🤖 PAGINATION)

2. **Manual Setup (You do this once):**
   - Browser opens to login page automatically
   - Complete library authentication (OpenAthens, etc.)
   - Navigate to ReferenceUSA U.S. Business database
   - Set up your search criteria (location, industry, etc.)
   - Click 'Search' and wait for results to load
   - Press Enter when you see the search results page

3. **Automation Takes Over:**
   - Script automatically detects total pages
   - Processes pages in batches of 10
   - Downloads CSV files with proper naming
   - Continues until all pages are complete
   - Shows progress and saves session state

### Option 2: NO PAGINATION MODE (Manual Navigation)

1. **Start the scraper:**
   ```bash
   python start_scraper.py
   ```
   Choose option **2** (📋 NO PAGINATION)

2. **Manual Setup (You do this once):**
   - Same login process as above
   - Navigate to search results page

3. **Semi-Automation:**
   - You manually navigate to each page
   - Script automatically selects all records
   - Script automatically downloads and saves files
   - Script automatically unchecks prior batch records
   - Repeat for each page range you want

### Option 3: CSV MERGER

1. **Start the merger:**
   ```bash
   python start_scraper.py
   ```
   Choose option **3** (🔗 MERGE CSV FILES)

2. **Merge Options:**
   - **Merge all files** - combine everything
   - **Select specific files** - choose by number (e.g., 1,3,5-8)
   - **Limit by record count** - merge up to X records
   - **Date range** - merge files from specific dates

## 📁 File Structure

```
Miller 3 Data Scraper/
├── start_scraper.py           # Main launcher (START HERE)
├── manual_process_simple.py   # Semi-automated scraper
├── semi_automated_scraper.py  # Full pagination scraper
├── full_automation_scraper.py # Alternative full automation
├── csv_merger.py             # CSV file merger
├── config/
│   └── referenceusa_config.yaml # Configuration settings
├── downloads/                # Your downloaded CSV files
├── logs/                     # Session logs
└── chromedriver             # Chrome automation driver
```

## ⚙️ Configuration

Edit `config/referenceusa_config.yaml` to customize:

```yaml
# Login URL (update if your library uses different proxy)
auth_url: "http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Quick/497be73bf9a94fe3aebb7eb4857b584f"

# Download settings
download_dir: "downloads"
batch_size: 10
max_retries: 3

# Browser settings
browser_timeout: 30
page_load_timeout: 20
```

## 🔄 Session Management

**Resume Interrupted Sessions:**
- Sessions are automatically saved
- If interrupted, restart and choose to resume
- Script remembers where you left off
- Continue from last completed page

**Session Files:**
- `manual_scraper_state.json` - tracks progress
- `logs/` - detailed session logs

## 📊 Output Files

**Naming Convention:**
```
SearchName_StartPage-to-EndPage_MMDDYY_HHMM.csv
Example: Alabama_Businesses_1to10_061825_1430.csv
```

**CSV Format:**
- Detailed business records
- All available ReferenceUSA fields
- Source file tracking (when merged)
- No duplicates (when using merger)

## 🛠️ Troubleshooting

### Common Issues

**"ChromeDriver not found"**
- Ensure `chromedriver` file is in the same folder
- Download latest ChromeDriver if needed

**"Authentication failed"**
- Verify library credentials
- Check if VPN is required
- Update auth_url in config file

**"No records selected"**
- Page may not have loaded completely
- Try manual selection mode
- Check for page navigation issues

**"Download failed"**
- Check download folder permissions
- Ensure sufficient disk space
- Verify browser download settings

### Recovery Options

**If script stops unexpectedly:**
1. Restart `python start_scraper.py`
2. Choose same mode you were using
3. Select "Resume previous session"
4. Continue from where you left off

**If downloads are incomplete:**
1. Use CSV Merger to combine partial files
2. Check `downloads/` folder for all files
3. Restart from last successful page

## 🎯 Tips for Best Results

### Before Starting
- **Stable internet connection**
- **Close unnecessary browser tabs**
- **Ensure library access is working**
- **Test with small page range first**

### During Operation
- **Don't close the browser manually**
- **Let automation complete each batch**
- **Monitor for any error messages**
- **Save work frequently (auto-saved)**

### Large Jobs
- **Use PAGINATION mode for 100+ pages**
- **Process in chunks if needed**
- **Use CSV Merger to combine results**
- **Take breaks between large batches**

## 📞 Support

### Before Reporting Issues
1. Check `logs/` folder for error details
2. Try with a small test (1-2 pages)
3. Verify library access works manually
4. Update ChromeDriver if needed

### Session Recovery
- All progress is automatically saved
- Restart anytime and resume
- Session files contain your progress
- No work is lost on interruption

## 🔐 Security & Compliance

- **Uses your existing library credentials**
- **No data stored outside your computer**
- **Respects website rate limits**
- **Downloads only what you have access to**
- **Session data stored locally only**

## 📈 Performance

**Typical Performance:**
- **10 pages**: 5-10 minutes
- **50 pages**: 25-50 minutes  
- **100+ pages**: 1-2 hours
- **Speed varies by:** page load times, record count, network speed

**Optimization:**
- Use ethernet instead of WiFi
- Close other applications
- Use PAGINATION mode for large jobs
- Process during off-peak hours

---

## 🚀 Getting Started Checklist

- [ ] Python 3.7+ installed
- [ ] Chrome browser installed
- [ ] Library access to ReferenceUSA verified
- [ ] Downloaded/extracted scraper files
- [ ] Run `python start_scraper.py`
- [ ] Choose your mode (PAGINATION recommended)
- [ ] Complete one-time login setup
- [ ] Let automation handle the rest!

**Need help?** Start with a small test of 1-5 pages to familiarize yourself with the process.