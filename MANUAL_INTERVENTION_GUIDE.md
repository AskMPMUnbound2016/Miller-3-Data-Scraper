# Miller 3 Data Scraper - Complete Manual Guide

## 📖 Table of Contents
1. [Overview](#overview)
2. [When Manual Intervention is Required](#when-manual-intervention-is-required)
3. [Manual Step-by-Step Procedures](#manual-step-by-step-procedures)
4. [Download Path Management](#download-path-management)
5. [Common Manual Scenarios](#common-manual-scenarios)
6. [Troubleshooting Manual Steps](#troubleshooting-manual-steps)
7. [Logging and Tracking](#logging-and-tracking)

---

## Overview

The Miller 3 Data Scraper is designed to automate the data collection process from ReferenceUSA. However, there are specific situations where **manual intervention** is required. This manual defines exactly what constitutes "manual intervention," when it occurs, and step-by-step instructions for completing manual tasks.

### 🎯 Goals of Manual Intervention
- **Maintain scraping progress** when automation fails
- **Provide user control** over download locations
- **Ensure data quality** through user verification
- **Handle edge cases** that automation cannot resolve

---

## When Manual Intervention is Required

### 🔴 **Critical Manual Intervention Points**

#### 1. **Login Process**
**Trigger:** Authentication systems require human verification
- Library card authentication
- CAPTCHA challenges
- Multi-factor authentication
- Session timeouts

#### 2. **Page Navigation Issues**
**Trigger:** Page structure changes or navigation failures
- Pagination controls not found
- Page input fields missing
- Navigation buttons unresponsive
- Unexpected page layouts

#### 3. **Record Selection Problems**
**Trigger:** Checkbox selection automation fails
- Select-all checkbox not found
- Individual checkboxes not responding
- Selection count indicators missing
- Page selection conflicts

#### 4. **Download Button Detection Failures**
**Trigger:** Button detection automation cannot locate download controls
- Download button not found in toolbar
- Download Records button not found on download page
- Button text/structure changes
- Page timeout during download initiation

#### 5. **File Download Issues**
**Trigger:** Download process requires user confirmation or path selection
- Browser download prompts
- File save location conflicts
- Download progress confirmation
- File naming conflicts

---

## Manual Step-by-Step Procedures

### 🔧 **Manual Procedure 1: Login Authentication**

#### When This Occurs:
- Script displays: `"Please complete the login process manually"`
- Browser opens to authentication page
- Automated login fails

#### Manual Steps:
1. **Complete Library Authentication:**
   ```
   → Enter library card number
   → Enter PIN/password
   → Solve any CAPTCHA if present
   → Click "Login" or "Submit"
   ```

2. **Navigate to ReferenceUSA:**
   ```
   → Look for "ReferenceUSA" or "Business Database" link
   → Click to access the database
   → Wait for ReferenceUSA interface to load
   ```

3. **Confirm Access:**
   ```
   → Verify you can see ReferenceUSA search interface
   → Press Enter in terminal when ready
   ```

#### Success Indicator:
- ReferenceUSA search page is visible
- Script continues with: `"✅ Authentication successful"`

---

### 🔧 **Manual Procedure 2: Page Navigation**

#### When This Occurs:
- Script displays: `"Please navigate to page X manually"`
- Current page number doesn't match target
- Navigation controls not responding

#### Manual Steps:
1. **Locate Page Navigation:**
   ```
   → Find pagination controls (usually at top or bottom of results)
   → Look for page input field or page number links
   ```

2. **Navigate to Target Page:**
   ```
   → Method 1: Enter page number in input field and press Enter
   → Method 2: Click on page number link
   → Method 3: Use Previous/Next buttons repeatedly
   ```

3. **Verify Page Number:**
   ```
   → Confirm current page matches target page
   → Press Enter in terminal when on correct page
   ```

#### Success Indicator:
- Correct page number displayed
- Script continues with: `"✅ Navigated to page X"`

---

### 🔧 **Manual Procedure 3: Record Selection**

#### When This Occurs:
- Script displays: `"Please select all records manually"`
- Checkbox selection automation fails
- Need to select specific page ranges

#### Manual Steps:
1. **Clear Existing Selections:**
   ```
   → Look for checked/selected records (highlighted rows)
   → Uncheck any previously selected items
   → Ensure no records are selected before starting
   ```

2. **Select Target Records:**
   ```
   → Method 1: Click "Select All" checkbox in table header
   → Method 2: Check individual record checkboxes
   → Method 3: Use Ctrl+Click for multiple selections
   ```

3. **Verify Selection Count:**
   ```
   → Look for selection indicator (e.g., "25 records selected")
   → Ensure correct number of records are selected
   → Press Enter in terminal when selection complete
   ```

#### Success Indicator:
- Visible selection count matches expected range
- Script continues with: `"✅ Records selected"`

---

### 🔧 **Manual Procedure 4: Download Button Clicking**

#### When This Occurs:
- Script displays: `"🔧 Manual Intervention Required - Download button not found"`
- Download automation fails
- Button detection strategies exhausted

#### Manual Steps:
1. **Download Path Configuration:**
   ```
   🔧 Manual Intervention Required - Download button not found
   ============================================================
   
   📁 Download Path Options During Manual Process
   ==================================================
   Current download directory: /Users/admin/Desktop/Miller 3 Data Scaper/downloads
   
   Would you like to:
   1. Continue with current download directory
   2. Change download directory for remaining batches
   3. Use browser's default Downloads folder
   4. Specify one-time download location for this batch
   
   Choose option (1-4): [Select your choice]
   ```

2. **If Changing Download Directory:**
   ```
   → Option 2: Enter new permanent download path
   → Option 3: Automatically uses ~/Downloads
   → Option 4: Enter temporary path for current batch only
   ```

3. **Locate and Click Download Button:**
   ```
   → Look for "Download" button in top toolbar/menu
   → Click the Download button
   → Wait for download options page to load
   ```

4. **Configure Download Options:**
   ```
   → Select "Comma Delimited (CSV)" format
   → Select "Detailed" data level (NOT Summary)
   → Verify other settings as needed
   ```

5. **Complete Download:**
   ```
   → Click "DOWNLOAD RECORDS" button
   → Save file to specified location with exact filename provided
   → Wait for download to complete
   ```

#### File Naming Instructions:
```
📁 Save Location Instructions:
   Directory: /Users/admin/Documents/MyData
   Filename: Alabama_1to10_280125_1530.csv
   Full Path: /Users/admin/Documents/MyData/Alabama_1to10_280125_1530.csv

📆 Important: Please save the file to this exact location!
```

#### Success Indicator:
- File downloaded to specified location
- Script continues with: `"✅ Download completed"`

---

### 🔧 **Manual Procedure 5: Download Confirmation**

#### When This Occurs:
- Script asks: `"Did the file download complete successfully? (y/n)"`
- After manual download process
- File verification needed

#### Manual Steps:
1. **Verify File Download:**
   ```
   → Check specified download directory
   → Confirm file exists with correct name
   → Verify file size (should be > 0 bytes)
   → Check file can be opened (optional)
   ```

2. **Respond to Script:**
   ```
   → Type "y" or "yes" if download successful
   → Type "n" or "no" if download failed
   → Press Enter to confirm response
   ```

#### Success Indicator:
- File exists in correct location
- Script continues to next batch

---

## Download Path Management

### 📁 **Download Path Decision Matrix**

| Scenario | Recommended Choice | Notes |
|----------|-------------------|--------|
| **First time user** | Option 2: Change directory | Set permanent location |
| **Temporary project** | Option 4: One-time location | Don't affect future runs |
| **Default is fine** | Option 1: Continue current | No changes needed |
| **Quick download** | Option 3: Browser default | Use ~/Downloads |

### 🎯 **Download Path Options Explained**

#### **Option 1: Continue with current directory**
- **Use when:** Current location is acceptable
- **Effect:** No changes, continue as before
- **Best for:** Ongoing projects, established workflows

#### **Option 2: Change directory for remaining batches**
- **Use when:** Want to change location permanently
- **Effect:** Updates download location for all future batches
- **Best for:** New project setup, reorganizing files

#### **Option 3: Use browser's default Downloads folder**
- **Use when:** Want standard download location
- **Effect:** Uses ~/Downloads folder
- **Best for:** Quick downloads, temporary data collection

#### **Option 4: Specify one-time download location**
- **Use when:** Special case for current batch only
- **Effect:** Temporary location, reverts after this batch
- **Best for:** Testing, backup locations, special projects

### 📂 **Recommended Download Directory Structure**
```
/Users/[username]/Documents/Miller3Data/
├── Alabama/
├── Georgia/
├── Texas/
└── [State]/
    ├── Batch_001_001to010_280125_1530.csv
    ├── Batch_002_011to020_280125_1545.csv
    └── ...
```

---

## Common Manual Scenarios

### 🔍 **Scenario 1: Complete Manual Session**
**Situation:** All automation fails, everything manual

**Manual Process:**
1. Complete login authentication manually
2. Navigate to search page manually
3. Set search criteria manually
4. Navigate through result pages manually
5. Select records manually for each page
6. Download files manually for each batch
7. Verify downloads manually

**Time Estimate:** 2-3 hours for 10 batches

---

### 🔍 **Scenario 2: Partial Automation with Manual Downloads**
**Situation:** Navigation works, but download buttons fail

**Manual Process:**
1. ✅ Automated: Login, navigation, selection
2. 🔧 Manual: Click download buttons, save files
3. ✅ Automated: Page navigation between batches
4. 🔧 Manual: Download verification

**Time Estimate:** 30-45 minutes for 10 batches

---

### 🔍 **Scenario 3: Manual Path Changes Mid-Session**
**Situation:** Need to change download location during scraping

**Manual Process:**
1. Wait for next manual intervention prompt
2. Choose Option 2: Change directory for remaining batches
3. Enter new download path
4. Continue with new location for all future batches

**Time Estimate:** 2-3 minutes per change

---

### 🔍 **Scenario 4: Browser Session Timeout**
**Situation:** Session expires during long scraping process

**Manual Process:**
1. Re-authenticate when prompted
2. Return to results page manually
3. Resume from last completed batch
4. Verify session state before continuing

**Time Estimate:** 5-10 minutes to recover

---

## Troubleshooting Manual Steps

### 🚨 **Common Manual Step Issues**

#### **Issue: Cannot find Download button**
**Symptoms:**
- No "Download" button visible in toolbar
- Page layout differs from expected

**Solutions:**
1. **Look for alternative button text:**
   - "Export"
   - "Save"
   - "Download Results"
   - "Get Data"

2. **Check different page areas:**
   - Top toolbar/menu
   - Right sidebar
   - Bottom of page
   - Context menu (right-click)

3. **Refresh page and retry:**
   ```
   → Press F5 or Cmd+R to refresh
   → Wait for page to fully load
   → Look for download options again
   ```

#### **Issue: File downloads to wrong location**
**Symptoms:**
- File appears in Downloads folder instead of specified location
- Cannot find downloaded file

**Solutions:**
1. **Check browser download settings:**
   ```
   → Open browser settings/preferences
   → Find "Downloads" section
   → Verify download location
   → Change if necessary
   ```

2. **Use "Save As" instead of direct download:**
   ```
   → Right-click download link
   → Choose "Save As" or "Save Link As"
   → Navigate to correct folder
   → Enter exact filename provided
   ```

3. **Move file after download:**
   ```
   → Find file in actual download location
   → Move to specified directory
   → Rename to exact filename if needed
   ```

#### **Issue: Download fails or times out**
**Symptoms:**
- Download starts but never completes
- Browser shows download error
- File is 0 bytes or corrupted

**Solutions:**
1. **Retry with smaller batch:**
   ```
   → Select fewer records (reduce pages)
   → Try downloading smaller subset
   → Combine files later if needed
   ```

2. **Check network connection:**
   ```
   → Verify internet connectivity
   → Try other websites to confirm
   → Wait and retry if network slow
   ```

3. **Clear browser cache:**
   ```
   → Clear browser cache and cookies
   → Restart browser
   → Re-authenticate and retry
   ```

#### **Issue: Selected records lost between pages**
**Symptoms:**
- Records appear unselected after page navigation
- Selection count resets to zero

**Solutions:**
1. **Use batch download approach:**
   ```
   → Select records on current page only
   → Download immediately
   → Move to next page and repeat
   ```

2. **Check for "Select All Pages" option:**
   ```
   → Look for "Select all X records" link
   → Click to select across all pages
   → Proceed with download
   ```

---

## Logging and Tracking

### 📝 **Manual Intervention Logging**

All manual interventions are automatically logged:

#### **Session Log Entry:**
```
2025-01-28 15:30:45 - WARNING - 🔧 MANUAL INTERVENTION REQUIRED
2025-01-28 15:30:45 - WARNING -    Reason: Download Records button not found
2025-01-28 15:30:50 - INFO - 📁 Download directory changed to: /Users/admin/Documents/MyData
2025-01-28 15:31:20 - INFO - ✅ Manual download completed for batch 3
```

#### **Debug Log Entry:**
```
2025-01-28 15:30:45 - DEBUG - find_download_records_button:285 - ❌ Strategy 1 failed
2025-01-28 15:30:45 - DEBUG - find_download_records_button:290 - ❌ Strategy 2 failed
2025-01-28 15:30:45 - DEBUG - find_download_records_button:295 - ❌ All strategies failed
2025-01-28 15:30:45 - INFO - handle_manual_download_intervention:125 - Manual intervention triggered
```

### 📊 **Tracking Manual vs Automated Steps**

The system tracks:
- **Total batches processed**
- **Automated successful batches**
- **Manual intervention instances**
- **Download path changes**
- **Time spent on manual steps**

### 📈 **Session Summary Example:**
```
🏁 MILLER 3 DATA SCRAPER SESSION ENDED
🕐 End Time: 2025-01-28 16:45:30
⏱️  Total Duration: 1:14:45
📊 SESSION STATISTICS:
   Successful Batches: 8
   Failed Batches: 0
   Manual Interventions: 3
   Download Path Changes: 1
   Total Files Downloaded: 8
   Download Directory: /Users/admin/Documents/MyData
```

---

## 🎯 Quick Reference Checklist

### ✅ **Before Starting Manual Steps:**
- [ ] Read the manual intervention message carefully
- [ ] Note the specific issue (button not found, navigation failed, etc.)
- [ ] Have target download directory ready
- [ ] Understand the expected file naming format

### ✅ **During Manual Steps:**
- [ ] Follow the step-by-step procedure for your specific issue
- [ ] Use exact file names and locations provided
- [ ] Verify each step before proceeding
- [ ] Take screenshots if helpful for reference

### ✅ **After Manual Steps:**
- [ ] Confirm file downloaded successfully
- [ ] Verify file location and name are correct
- [ ] Respond to script prompts accurately
- [ ] Check logs for proper recording

### ✅ **Best Practices:**
- [ ] Keep browser window visible during automation
- [ ] Don't navigate away from results pages manually
- [ ] Let automation complete before manual intervention
- [ ] Save files exactly as instructed
- [ ] Report recurring issues for future automation improvements

---

*This manual serves as the definitive guide for all manual intervention procedures in the Miller 3 Data Scraper. Keep this reference handy during scraping sessions.*
