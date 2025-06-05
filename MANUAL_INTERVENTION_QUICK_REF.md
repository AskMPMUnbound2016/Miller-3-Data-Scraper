# 🔧 Manual Intervention Quick Reference Card

## 🚨 WHEN MANUAL INTERVENTION IS REQUIRED

### 🔑 **LOGIN ISSUES**
```
Message: "Please complete the login process manually"
Action: Enter library card + PIN → Find ReferenceUSA link → Click → Press Enter
```

### 🧭 **NAVIGATION ISSUES**
```
Message: "Please navigate to page X manually"
Action: Find page controls → Enter page number OR click page link → Press Enter
```

### ☑️ **SELECTION ISSUES**
```
Message: "Please select all records manually"
Action: Uncheck existing → Click "Select All" OR check individual boxes → Press Enter
```

### 📥 **DOWNLOAD BUTTON ISSUES**
```
Message: "Manual Intervention Required - Download button not found"
Action: Choose download path option → Click "Download" button → Press Enter
```

### 💾 **DOWNLOAD RECORDS ISSUES**
```
Message: "Manual Intervention Required - Download Records button not found"
Action: Choose download path → Click "DOWNLOAD RECORDS" → Save to exact location → Press Enter
```

---

## 📁 DOWNLOAD PATH OPTIONS

| Option | When to Use | Effect |
|--------|-------------|--------|
| **1** | Happy with current location | No change |
| **2** | Want new permanent location | Changes all future batches |
| **3** | Use standard Downloads folder | Uses ~/Downloads |
| **4** | Special location for this batch only | Temporary change |

---

## 🎯 MANUAL DOWNLOAD PROCESS

### Step 1: Path Selection
```
Choose option (1-4): [Your choice]
If option 2 or 4: Enter directory path
```

### Step 2: Download Configuration
```
→ Select "Comma Delimited (CSV)" format
→ Select "Detailed" data level (NOT Summary)
```

### Step 3: File Saving
```
📁 Save Location Instructions:
   Directory: /path/to/directory
   Filename: State_001to010_280125_1530.csv
   Full Path: /full/path/to/file.csv

📆 Save to EXACT location shown!
```

### Step 4: Confirmation
```
Did the file download complete successfully? (y/n)
→ Check file exists in correct location
→ Type "y" if successful, "n" if failed
```

---

## 🔍 TROUBLESHOOTING QUICK FIXES

### ❌ **Can't Find Download Button**
```
Look for: "Export", "Save", "Download Results", "Get Data"
Check: Top toolbar, right sidebar, bottom of page
Try: F5 to refresh page
```

### ❌ **File Downloads to Wrong Location**
```
Fix 1: Right-click → "Save As" → Navigate to correct folder
Fix 2: Move file from Downloads to specified location
Fix 3: Check browser download settings
```

### ❌ **Selection Lost Between Pages**
```
Fix 1: Download current page immediately
Fix 2: Look for "Select all X records" option
Fix 3: Use smaller batch sizes
```

### ❌ **Download Fails/Times Out**
```
Fix 1: Select fewer records (smaller batch)
Fix 2: Check internet connection
Fix 3: Clear browser cache and retry
```

---

## ⏱️ TIME ESTIMATES

| Scenario | Time Estimate |
|----------|---------------|
| **Complete manual session** | 2-3 hours (10 batches) |
| **Manual downloads only** | 30-45 minutes (10 batches) |
| **Path change mid-session** | 2-3 minutes |
| **Session recovery** | 5-10 minutes |

---

## 📋 QUICK CHECKLIST

### ✅ Before Manual Steps:
- [ ] Read error message carefully
- [ ] Note specific issue type
- [ ] Have download directory ready

### ✅ During Manual Steps:
- [ ] Follow exact procedure for issue type
- [ ] Use provided file names/locations
- [ ] Verify each step before continuing

### ✅ After Manual Steps:
- [ ] Confirm file downloaded successfully
- [ ] Check file location and name
- [ ] Respond to script prompts accurately

---

## 🆘 EMERGENCY COMMANDS

```bash
# View this quick reference
cat MANUAL_INTERVENTION_QUICK_REF.md

# View full manual
cat MANUAL_INTERVENTION_GUIDE.md

# Check recent logs
ls -la logs/session_logs/

# Find downloaded files
find . -name "*.csv" -mtime -1

# Stop scraper gracefully
Ctrl+C (then let it clean up)
```

---

**🔖 Keep this card open during scraping sessions for quick reference!**
