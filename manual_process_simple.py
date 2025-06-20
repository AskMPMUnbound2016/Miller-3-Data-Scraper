#!/usr/bin/env python3
"""
MILLER 3 DATA SCRAPER - SEMI-AUTOMATED VERSION
==============================================
User handles login and navigation setup - Automation handles record processing
- USER: Initial login and search setup
- AUTOMATION: Record selection, downloading, file saving, and cleanup
- Automatic navigation between pages
- Automatic record selection on each page
- Automatic download with proper CSV format and detailed settings
- Automatic cleanup and unchecking of processed records
- Fallback to manual steps if automation fails
"""

import os
import sys
import time
import yaml
import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class ManualProcessScraper:
    def __init__(self, config_file='config/referenceusa_config.yaml'):
        print("\n=== MILLER 3 DATA SCRAPER - SEMI-AUTOMATED ===")
        print("🤖 AUTOMATION: Record selection, downloads, file saving, cleanup")
        print("👤 MANUAL: Login and initial search setup only")
        
        # Load configuration if available
        self.config = self._load_config(config_file)
        self.download_dir = self.config.get('download_dir', os.path.join(os.getcwd(), "downloads"))
        self.state_file = "manual_scraper_state.json"
        self.session_state = self._load_session_state()
        
        # Initialize browser
        self._setup_browser()
        self.wait = WebDriverWait(self.driver, 15)
        
        print(f"📂 Downloads will be saved by browser to your designated folder")
        print(f"📄 Session state saved to: {self.state_file}")
    
    def _load_config(self, config_file):
        """Load configuration file if it exists"""
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f)
            else:
                print("⚠️ No config file found, using defaults")
                return {}
        except Exception as e:
            print(f"⚠️ Error loading config: {e}")
            return {}
    
    def _load_session_state(self):
        """Load previous session state if available"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    print(f"📋 Loaded previous session: {state.get('search_name', 'Unknown')}")
                    return state
            else:
                return {
                    'search_name': '',
                    'total_pages': 0,
                    'completed_batches': [],
                    'last_completed_page': 0,
                    'downloads_completed': []
                }
        except Exception as e:
            print(f"⚠️ Error loading session state: {e}")
            return {
                'search_name': '',
                'total_pages': 0,
                'completed_batches': [],
                'last_completed_page': 0,
                'downloads_completed': []
            }
    
    def _save_session_state(self):
        """Save current session state"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.session_state, f, indent=2)
            print(f"💾 Session state saved")
        except Exception as e:
            print(f"⚠️ Error saving session state: {e}")
    
    def _setup_browser(self):
        """Setup Chrome browser"""
        print("🌐 Setting up browser...")
        
        options = webdriver.ChromeOptions()
        
        # Fix for data:, URL issue - set proper startup behavior
        options.add_argument("--homepage=about:blank")
        options.add_argument("--disable-default-apps")
        
        # Add options for downloads and ensure files go to correct directory
        os.makedirs(self.download_dir, exist_ok=True)
        options.add_experimental_option("prefs", {
            "download.default_directory": os.path.abspath(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "profile.default_content_setting_values.notifications": 2
        })
        
        # Initialize browser
        chromedriver_path = "./chromedriver"
        if not os.path.exists(chromedriver_path):
            print(f"❌ ChromeDriver not found at {chromedriver_path}")
            print("Please ensure chromedriver is in the same folder.")
            sys.exit(1)
        
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        
        # Immediately navigate to blank page to prevent data:, URL issue
        self.driver.get("about:blank")
        
        print("✅ Browser ready")
    
    def start_manual_login(self):
        """Start the manual login process"""
        print("\n" + "="*60)
        print("STEP 1: MANUAL LOGIN")
        print("="*60)
        
        # Get starting URL from config - ensure it opens to login page directly
        start_url = self.config.get('auth_url', 'http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Quick/497be73bf9a94fe3aebb7eb4857b584f')
        
        print(f"🌐 Opening login URL: {start_url}")
        self.driver.get(start_url)
        
        print("\n📋 MANUAL LOGIN INSTRUCTIONS:")
        print("1. ✅ Complete OpenAthens authentication if prompted")
        print("2. ✅ You should see the ReferenceUSA U.S. Business Quick Search page")
        print("3. ✅ Set up your search criteria (location, industry, etc.)")
        print("4. ✅ Click 'Search' or 'View Results' button")
        print("5. ✅ Wait for search results to load completely")
        print("6. ✅ You should see a list of business records with pagination")
        
        input("\n⏸️ Press Enter when you can see the search results page...")
        
        # Get search details from user
        search_name = input("📝 Enter a name for this search (e.g., 'Alabama_Businesses'): ").strip()
        if not search_name:
            search_name = f"Search_{int(time.time())}"
        
        self.session_state['search_name'] = search_name
        print(f"✅ Search named: {search_name}")
        
        return True
    
    def get_total_pages(self):
        """Get total number of pages from user"""
        print("\n" + "="*60)
        print("STEP 2: DETERMINE TOTAL PAGES")
        print("="*60)
        
        print("🔍 Look at your search results page")
        print("Look for pagination info like 'Page 1 of 45' or 'Results 1-25 of 1,125'")
        
        while True:
            try:
                total_input = input("\n📊 How many total pages of results do you have? ").strip()
                if total_input.lower() in ['q', 'quit', 'exit']:
                    return False
                
                total_pages = int(total_input)
                if total_pages <= 0:
                    print("❌ Please enter a positive number")
                    continue
                
                self.session_state['total_pages'] = total_pages
                print(f"✅ Total pages set to: {total_pages}")
                break
                
            except ValueError:
                print("❌ Please enter a valid number")
                continue
        
        return True
    
    def get_download_range(self):
        """Get the range of pages to download"""
        print("\n" + "="*60)
        print("STEP 3: SELECT DOWNLOAD RANGE")
        print("="*60)
        
        total_pages = self.session_state['total_pages']
        last_completed = self.session_state['last_completed_page']
        
        if last_completed > 0:
            print(f"📋 Previous session: Completed through page {last_completed}")
            print(f"📊 Total pages: {total_pages}")
            
            resume = input(f"\n🔄 Resume from page {last_completed + 1}? (y/n): ").lower().strip()
            if resume in ['y', 'yes']:
                start_page = last_completed + 1
                end_page = total_pages
                print(f"✅ Resuming from page {start_page} to {end_page}")
                return start_page, end_page
        
        print(f"📊 Total pages available: {total_pages}")
        
        download_all = input("\n📥 Download ALL pages? (y/n): ").lower().strip()
        if download_all in ['y', 'yes']:
            return 1, total_pages
        
        # Get custom range
        while True:
            try:
                start_input = input(f"\n📍 Start page (1-{total_pages}): ").strip()
                start_page = int(start_input)
                
                if start_page < 1 or start_page > total_pages:
                    print(f"❌ Start page must be between 1 and {total_pages}")
                    continue
                
                end_input = input(f"📍 End page ({start_page}-{total_pages}): ").strip()
                end_page = int(end_input)
                
                if end_page < start_page or end_page > total_pages:
                    print(f"❌ End page must be between {start_page} and {total_pages}")
                    continue
                
                print(f"✅ Will download pages {start_page} to {end_page} ({end_page - start_page + 1} total pages)")
                return start_page, end_page
                
            except ValueError:
                print("❌ Please enter valid numbers")
                continue
    
    def process_batch(self, batch_start, batch_end, batch_num, total_batches):
        """Process a single batch with automation for record selection, download, and cleanup"""
        print(f"\n" + "="*60)
        print(f"BATCH {batch_num} of {total_batches}: PAGES {batch_start} TO {batch_end}")
        print("="*60)
        
        pages_in_batch = batch_end - batch_start + 1
        print(f"📄 Processing {pages_in_batch} page(s): {batch_start} to {batch_end}")
        
        # Step 1: Navigate and auto-select pages
        print(f"\n🤖 STEP 1: AUTO-SELECT PAGES {batch_start} TO {batch_end}")
        print("=" * 40)
        
        selected_pages = []
        for page in range(batch_start, batch_end + 1):
            print(f"\n📍 PAGE {page}: Navigating and selecting...")
            
            # Navigate to page
            if self.auto_navigate_to_page(page):
                # Auto-select all records on this page
                if self.auto_select_all_records():
                    selected_pages.append(page)
                    print(f"✅ Page {page}: Records selected automatically")
                else:
                    print(f"⚠️ Page {page}: Auto-selection failed - manual selection required")
                    input(f"   ⏸️ Please manually select all records on page {page}, then press Enter...")
                    selected_pages.append(page)
            else:
                print(f"❌ Page {page}: Navigation failed - manual navigation required")
                input(f"   ⏸️ Please manually navigate to page {page} and select all records, then press Enter...")
                selected_pages.append(page)
            
            # Brief pause between pages
            time.sleep(random.uniform(1, 2))
        
        print(f"\n📊 Selected {len(selected_pages)} pages for download")
        
        # Step 2: Auto-download
        print(f"\n🤖 STEP 2: AUTO-DOWNLOAD BATCH {batch_num}")
        print("=" * 40)
        
        # Generate filename
        search_name = self.session_state['search_name']
        timestamp = time.strftime('%m%d%y_%H%M')
        suggested_filename = f"{search_name}_{batch_start}to{batch_end}_{timestamp}.csv"
        
        download_success = self.auto_download_records(batch_num, suggested_filename)
        
        if not download_success:
            print("⚠️ Auto-download failed - manual download required")
            print("📋 Manual download instructions:")
            print("1. ✅ Click the 'Download' button (usually in top toolbar)")
            print("2. ✅ On download page, select 'Comma Delimited (CSV)' format")
            print("3. ✅ Select 'Detailed' data level (NOT Summary)")
            print("4. ✅ Click 'DOWNLOAD RECORDS' button")
            print(f"5. ✅ Save file as: {suggested_filename}")
            
            download_success = input(f"\n⏸️ Press Enter after download completes (or 'r' to retry): ").strip().lower()
            if download_success == 'r':
                print("🔄 Retrying batch...")
                return self.process_batch(batch_start, batch_end, batch_num, total_batches)
        
        # Step 3: Auto-uncheck records
        print(f"\n🤖 STEP 3: AUTO-UNCHECK RECORDS")
        print("=" * 40)
        
        cleanup_success = self.auto_cleanup_after_download()
        
        if not cleanup_success:
            print("⚠️ Auto-cleanup failed - manual cleanup required")
            print("📋 Manual cleanup instructions:")
            for page in range(batch_start, batch_end + 1):
                print(f"   📍 Go to page {page} and uncheck all records")
            print("\n💡 TIP: Look for 'Unselect All' button or uncheck header checkbox")
            input("⏸️ Press Enter after unchecking all downloaded records...")
        
        # Update session state
        self.session_state['completed_batches'].append({
            'batch_num': batch_num,
            'start_page': batch_start, 
            'end_page': batch_end,
            'filename': suggested_filename,
            'timestamp': timestamp,
            'pages_selected': selected_pages
        })
        self.session_state['last_completed_page'] = batch_end
        self.session_state['downloads_completed'].append(suggested_filename)
        self._save_session_state()
        
        print(f"✅ Batch {batch_num} completed successfully!")
        return True
    
    def run_download_process(self):
        """Run the main download process"""
        try:
            # Get download range
            start_page, end_page = self.get_download_range()
            
            # Calculate batches (max 10 pages per batch)
            total_pages_to_download = end_page - start_page + 1
            batch_size = 10
            total_batches = (total_pages_to_download + batch_size - 1) // batch_size
            
            print(f"\n📊 DOWNLOAD PLAN:")
            print(f"   Pages to download: {start_page} to {end_page} ({total_pages_to_download} pages)")
            print(f"   Batch size: {batch_size} pages maximum")
            print(f"   Total batches: {total_batches}")
            
            proceed = input(f"\n🚀 Start downloading? (y/n): ").lower().strip()
            if proceed not in ['y', 'yes']:
                print("❌ Download cancelled")
                return False
            
            # Process each batch
            current_page = start_page
            batch_num = 1
            
            while current_page <= end_page:
                batch_end = min(current_page + batch_size - 1, end_page)
                
                # Check if user wants to continue
                if batch_num > 1:
                    continue_choice = input(f"\n🔄 Continue with batch {batch_num}? (y/n/q): ").lower().strip()
                    if continue_choice == 'q':
                        print("🛑 Process stopped by user")
                        break
                    elif continue_choice == 'n':
                        print("⏸️ Pausing process")
                        break
                
                # Process the batch
                success = self.process_batch(current_page, batch_end, batch_num, total_batches)
                
                if not success:
                    print(f"❌ Batch {batch_num} failed")
                    retry = input("🔄 Retry this batch? (y/n): ").lower().strip()
                    if retry not in ['y', 'yes']:
                        break
                    else:
                        continue  # Retry same batch
                
                # Move to next batch
                current_page = batch_end + 1
                batch_num += 1
                
                # Small break between batches
                if current_page <= end_page:
                    print(f"\n⏳ Brief pause before next batch...")
                    time.sleep(2)
            
            # Final summary
            completed_batches = len(self.session_state['completed_batches'])
            print(f"\n🏁 DOWNLOAD PROCESS COMPLETE!")
            print(f"✅ Completed batches: {completed_batches}")
            print(f"📁 Downloaded files: {len(self.session_state['downloads_completed'])}")
            print(f"📋 Last completed page: {self.session_state['last_completed_page']}")
            
            if self.session_state['downloads_completed']:
                print(f"\n📄 Downloaded files:")
                for filename in self.session_state['downloads_completed']:
                    print(f"   • {filename}")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n🛑 Process interrupted by user")
            self._save_session_state()
            return False
        except Exception as e:
            print(f"\n❌ Error in download process: {e}")
            self._save_session_state()
            return False
    
    def run(self):
        """Main entry point"""
        try:
            print("🚀 Starting Manual Process Data Scraper")
            
            # Step 1: Manual login
            if not self.start_manual_login():
                print("❌ Login process failed or cancelled")
                return
            
            # Step 2: Get total pages
            if not self.get_total_pages():
                print("❌ Could not determine total pages")
                return
            
            # Step 3: Run download process
            self.run_download_process()
            
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            # Ask if user wants to close browser
            close_browser = input("\n🌐 Close browser? (y/n): ").lower().strip()
            if close_browser in ['y', 'yes', '']:
                print("🌐 Closing browser...")
                self.driver.quit()
            else:
                print("🌐 Browser left open for manual use")
    
    def show_session_status(self):
        """Show current session status"""
        print(f"\n📋 SESSION STATUS:")
        print(f"   Search name: {self.session_state.get('search_name', 'Not set')}")
        print(f"   Total pages: {self.session_state.get('total_pages', 'Not set')}")
        print(f"   Last completed page: {self.session_state.get('last_completed_page', 0)}")
        print(f"   Completed batches: {len(self.session_state.get('completed_batches', []))}")
        print(f"   Downloads completed: {len(self.session_state.get('downloads_completed', []))}")

    def auto_navigate_to_page(self, page_num):
        """Automatically navigate to a specific page"""
        try:
            current_page = self.detect_current_page()
            if current_page == page_num:
                return True
            
            # Find page input field
            page_inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
            
            for input_elem in page_inputs:
                if input_elem.is_displayed() and input_elem.is_enabled():
                    value = input_elem.get_attribute('value') or ''
                    if value.isdigit() and int(value) <= 1000:
                        # Navigate using input + Enter
                        input_elem.click()
                        time.sleep(0.2)
                        input_elem.clear()
                        time.sleep(0.1)
                        input_elem.send_keys(str(page_num))
                        time.sleep(0.2)
                        input_elem.send_keys(Keys.ENTER)
                        time.sleep(3)
                        
                        # Wait for page to load
                        self.wait_for_page_stability()
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False

    def auto_select_all_records(self):
        """Automatically select all records on current page"""
        try:
            print("🔍 Searching for checkboxes to select...")
            
            # Wait for page to load
            self.wait_for_page_stability()
            
            # Multiple strategies to find and select checkboxes
            
            # Strategy 1: Look for "Select All" or header checkbox
            header_selectors = [
                "//th//input[@type='checkbox']",
                "//thead//input[@type='checkbox']",
                "//input[@type='checkbox' and contains(@id, 'select')]",
                "//input[@type='checkbox' and contains(@name, 'select')]",
                "//input[@type='checkbox' and contains(@class, 'select')]"
            ]
            
            for selector in header_selectors:
                try:
                    print(f"🔍 Trying header selector: {selector}")
                    checkboxes = self.driver.find_elements(By.XPATH, selector)
                    for checkbox in checkboxes:
                        if checkbox.is_displayed() and checkbox.is_enabled():
                            print(f"✅ Found header checkbox, clicking...")
                            # Scroll into view
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                            time.sleep(0.5)
                            # Click using JavaScript to avoid interception
                            self.driver.execute_script("arguments[0].click();", checkbox)
                            time.sleep(2)
                            print(f"✅ Header checkbox clicked successfully")
                            return True
                except Exception as e:
                    print(f"⚠️ Header selector failed: {e}")
                    continue
            
            # Strategy 2: Find all visible checkboxes and select them individually
            print("🔍 Trying individual checkbox selection...")
            checkbox_selectors = [
                "//input[@type='checkbox']",
                "//table//input[@type='checkbox']",
                "//tr//input[@type='checkbox']",
                "//td//input[@type='checkbox']"
            ]
            
            all_checkboxes = []
            for selector in checkbox_selectors:
                try:
                    checkboxes = self.driver.find_elements(By.XPATH, selector)
                    visible_checkboxes = [cb for cb in checkboxes if cb.is_displayed() and cb.is_enabled()]
                    all_checkboxes.extend(visible_checkboxes)
                except:
                    continue
            
            if not all_checkboxes:
                print("❌ No checkboxes found on page")
                return False
            
            # Remove duplicates
            unique_checkboxes = []
            seen = set()
            for cb in all_checkboxes:
                try:
                    cb_location = cb.location
                    cb_key = (cb_location['x'], cb_location['y'])
                    if cb_key not in seen:
                        unique_checkboxes.append(cb)
                        seen.add(cb_key)
                except:
                    continue
            
            print(f"📊 Found {len(unique_checkboxes)} unique checkboxes")
            
            # Select all unchecked checkboxes
            selected_count = 0
            for i, checkbox in enumerate(unique_checkboxes):
                try:
                    if not checkbox.is_selected():
                        # Scroll into view
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                        time.sleep(0.1)
                        # Click using JavaScript
                        self.driver.execute_script("arguments[0].click();", checkbox)
                        selected_count += 1
                        time.sleep(0.1)
                        
                        # Break after selecting many (likely all individual records)
                        if selected_count >= 25:  # Assume max 25 records per page
                            break
                except Exception as e:
                    print(f"⚠️ Failed to click checkbox {i}: {e}")
                    continue
            
            if selected_count > 0:
                print(f"✅ Selected {selected_count} checkboxes")
                time.sleep(1)
                return True
            else:
                print("❌ No checkboxes were selected")
                return False
            
        except Exception as e:
            print(f"❌ Selection error: {e}")
            return False

    def auto_download_records(self, batch_num, filename):
        """Automatically download selected records"""
        try:
            # Find and click Download button
            download_selectors = [
                "//button[contains(text(), 'Download')]",
                "//a[contains(text(), 'Download')]",
                "//input[@type='submit' and contains(@value, 'Download')]"
            ]
            
            for selector in download_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        time.sleep(3)
                        break
                else:
                    continue
                break
            else:
                return False
            
            # Configure download options
            self.auto_configure_download()
            
            # Click Download Records
            download_records_selectors = [
                "//button[contains(text(), 'DOWNLOAD RECORDS')]",
                "//input[@type='submit' and contains(@value, 'DOWNLOAD RECORDS')]",
                "//button[@type='submit']"
            ]
            
            for selector in download_records_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        time.sleep(3)
                        break
                else:
                    continue
                break
            
            # Wait for download
            downloaded_file = self.wait_for_download(batch_num)
            return downloaded_file is not None
            
        except Exception as e:
            print(f"❌ Download error: {e}")
            return False

    def auto_configure_download(self):
        """Automatically configure download options"""
        try:
            # Select CSV format
            csv_elements = self.driver.find_elements(By.XPATH, 
                "//input[@type='radio' and (following-sibling::*[contains(text(), 'Comma')] or following-sibling::*[contains(text(), 'CSV')])]")
            
            for element in csv_elements:
                if element.is_displayed() and not element.is_selected():
                    element.click()
                    time.sleep(0.5)
                    break
            
            # Select Detailed level
            detailed_elements = self.driver.find_elements(By.XPATH,
                "//input[@type='radio' and following-sibling::*[contains(text(), 'Detailed')]]")
            
            for element in detailed_elements:
                if element.is_displayed() and not element.is_selected():
                    element.click()
                    time.sleep(0.5)
                    break
            
        except Exception as e:
            print(f"⚠️ Configuration error: {e}")

    def wait_for_download(self, batch_num):
        """Wait for download to complete"""
        try:
            os.makedirs(self.download_dir, exist_ok=True)
            abs_download_dir = os.path.abspath(self.download_dir)
            print(f"📂 Monitoring download directory: {abs_download_dir}")
            
            initial_files = os.listdir(abs_download_dir) if os.path.exists(abs_download_dir) else []
            print(f"📋 Initial files in directory: {len(initial_files)}")
            
            max_wait = 60  # 60 seconds
            wait_time = 0
            
            while wait_time < max_wait:
                time.sleep(2)
                wait_time += 2
                
                if os.path.exists(abs_download_dir):
                    current_files = os.listdir(abs_download_dir)
                    
                    # Check for .crdownload files (Chrome partial downloads)
                    downloading_files = [f for f in current_files if f.endswith('.crdownload')]
                    if downloading_files:
                        print(f"⏳ Download in progress: {downloading_files[0]} ({wait_time}s)")
                    
                    # Check for completed new files
                    new_files = [f for f in current_files if f not in initial_files and not f.endswith('.crdownload')]
                    
                    if new_files:
                        print(f"✅ Downloaded: {new_files[0]}")
                        print(f"📁 File location: {os.path.join(abs_download_dir, new_files[0])}")
                        return new_files[0]
                
                # Show progress every 10 seconds
                if wait_time % 10 == 0:
                    print(f"⏳ Waiting for download... ({wait_time}/{max_wait}s)")
            
            print("⚠️ Download timeout - checking final state")
            if os.path.exists(abs_download_dir):
                final_files = os.listdir(abs_download_dir)
                print(f"📋 Final files in directory: {len(final_files)}")
                for f in final_files:
                    print(f"   📄 {f}")
            
            return None
            
        except Exception as e:
            print(f"❌ Download wait error: {e}")
            return None

    def auto_cleanup_after_download(self):
        """Automatically clean up after download"""
        try:
            # Navigate back to results
            back_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Back')] | //button[contains(text(), 'Back')]")
            if back_buttons:
                back_buttons[0].click()
                time.sleep(3)
            else:
                self.driver.back()
                time.sleep(3)
            
            self.wait_for_page_stability()
            
            # Bulk uncheck all records
            return self.bulk_uncheck_all()
            
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")
            return False

    def bulk_uncheck_all(self):
        """Bulk uncheck all selected records"""
        try:
            # Method 1: Look for unselect buttons
            uncheck_selectors = [
                "//button[contains(text(), 'Unselect')]",
                "//a[contains(text(), 'Unselect')]",
                "//button[contains(text(), 'Clear')]",
                "//a[contains(text(), 'Clear')]"
            ]
            
            for selector in uncheck_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        time.sleep(2)
                        return True
            
            # Method 2: JavaScript bulk uncheck
            js_result = self.driver.execute_script("""
                var checkboxes = document.querySelectorAll('input[type="checkbox"]');
                var unchecked = 0;
                for(var i = 0; i < checkboxes.length; i++) {
                    if(checkboxes[i].checked) {
                        checkboxes[i].checked = false;
                        checkboxes[i].dispatchEvent(new Event('change'));
                        unchecked++;
                    }
                }
                return unchecked;
            """)
            
            if js_result > 0:
                time.sleep(2)
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Bulk uncheck error: {e}")
            return False

    def detect_current_page(self):
        """Detect current page number"""
        try:
            inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
            for inp in inputs:
                if inp.is_displayed():
                    value = inp.get_attribute('value') or ''
                    if value.isdigit() and int(value) <= 1000:
                        return int(value)
            return 1
        except:
            return 1

    def wait_for_page_stability(self, timeout=10):
        """Wait for page to be stable and loaded"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(random.uniform(1, 2))
            return True
        except:
            return False


if __name__ == "__main__":
    try:
        scraper = ManualProcessScraper()
        
        # Check if there's a previous session
        if scraper.session_state.get('search_name'):
            print("🔄 Previous session detected!")
            scraper.show_session_status()
            
            resume = input("\n🔄 Resume previous session? (y/n): ").lower().strip()
            if resume in ['y', 'yes']:
                print("✅ Resuming previous session...")
                # Skip login, go straight to download process
                # Navigate to the proper starting URL instead of about:blank
                start_url = scraper.config.get('auth_url', 'http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Quick/497be73bf9a94fe3aebb7eb4857b584f')
                print(f"🌐 Opening: {start_url}")
                scraper.driver.get(start_url)
                print("\n📋 RESUMING SESSION:")
                print("1. ✅ Complete OpenAthens authentication if needed")
                print("2. ✅ Navigate to your search results page")
                print("3. ✅ Make sure you're on the correct search")
                print("4. ✅ Verify you can see business records and pagination")
                input("⏸️ Press Enter when you're back on the search results page...")
                
                scraper.run_download_process()
            else:
                print("🆕 Starting new session...")
                scraper.run()
        else:
            scraper.run()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
    
    print("\n⏸️ Press Enter to exit...")
    input()
