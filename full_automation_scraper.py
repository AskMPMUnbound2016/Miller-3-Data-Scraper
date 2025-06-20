#!/usr/bin/env python3
"""
MILLER 3 DATA SCRAPER - FULL AUTOMATION
======================================
User navigates to search results → Complete automation takes over
- Selection, page navigation, downloads
- Batches of 250 records or 10 pages
- No manual intervention required
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

class FullAutomationScraper:
    def __init__(self, config_file='config/referenceusa_config.yaml'):
        print("\n🤖 MILLER 3 DATA SCRAPER - FULL AUTOMATION")
        print("=" * 60)
        print("👤 YOU: Navigate to search results")
        print("🤖 AUTOMATION: Everything else (selection, navigation, downloads)")
        print()
        
        # Load configuration
        self.config = self._load_config(config_file)
        self.download_dir = self.config.get('download_dir', os.path.join(os.getcwd(), "downloads"))
        self.state_file = "automation_state.json"
        self.session_state = self._load_session_state()
        
        # Batch configuration
        self.BATCH_SIZE_PAGES = 10  # Pages per batch
        self.RECORDS_PER_PAGE = 25  # Estimated records per page
        self.TARGET_RECORDS_PER_BATCH = 250  # Target records per download
        
        # Initialize browser with anti-detection
        self._setup_browser()
        self.wait = WebDriverWait(self.driver, 15)
        
        print(f"📂 Download directory: {self.download_dir}")
        print(f"📊 Batch size: {self.BATCH_SIZE_PAGES} pages (~{self.TARGET_RECORDS_PER_BATCH} records)")
    
    def _load_config(self, config_file):
        """Load configuration file if it exists"""
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f)
            else:
                return {}
        except Exception as e:
            print(f"⚠️ Config error: {e}")
            return {}
    
    def _load_session_state(self):
        """Load previous session state if available"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    print(f"📋 Previous session found: {state.get('search_name', 'Unknown')}")
                    return state
            else:
                return {
                    'search_name': '',
                    'total_pages': 0,
                    'total_records': 0,
                    'completed_batches': [],
                    'last_completed_page': 0,
                    'downloads_completed': [],
                    'current_batch': 1,
                    'start_time': time.time()
                }
        except Exception as e:
            print(f"⚠️ Session state error: {e}")
            return {
                'search_name': '',
                'total_pages': 0,
                'total_records': 0,
                'completed_batches': [],
                'last_completed_page': 0,
                'downloads_completed': [],
                'current_batch': 1,
                'start_time': time.time()
            }
    
    def _save_session_state(self):
        """Save current session state"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.session_state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Save error: {e}")
    
    def _setup_browser(self):
        """Setup browser with advanced anti-detection"""
        print("🛡️ Setting up anti-detection browser...")
        
        options = webdriver.ChromeOptions()
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Fix for data:, URL issue - set proper startup behavior
        options.add_argument("--homepage=about:blank")
        options.add_argument("--disable-default-apps")
        
        # Advanced anti-detection
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Download preferences
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)
        
        # Initialize browser
        chromedriver_path = "./chromedriver"
        if not os.path.exists(chromedriver_path):
            print(f"❌ ChromeDriver not found at {chromedriver_path}")
            sys.exit(1)
        
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        
        # Immediately navigate to blank page to prevent data:, URL issue
        self.driver.get("about:blank")
        
        # JavaScript anti-detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});")
        self.driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'MacIntel'});")
        
        print("✅ Browser configured")
    
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
    
    def start_automation_from_search_results(self):
        """Start full automation from search results page"""
        print("\n🚀 STARTING FULL AUTOMATION")
        print("=" * 40)
        
        # Get starting URL from config - ensure it opens to login page directly
        start_url = self.config.get('auth_url', 'http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Quick/497be73bf9a94fe3aebb7eb4857b584f')
        print(f"🌐 Opening login URL: {start_url}")
        self.driver.get(start_url)
        
        print("👤 MANUAL STEP: Navigate to your search results page")
        print("📋 Instructions:")
        print("1. ✅ Complete library authentication")
        print("2. ✅ Navigate to U.S. Business database")
        print("3. ✅ Set up your search criteria")
        print("4. ✅ Click 'Search' or 'View Results'")
        print("5. ✅ Wait for results to load completely")
        print("6. ✅ Ensure you can see the data table with companies")
        
        input("\n⏸️ Press Enter when you're on the search results page and ready for automation...")
        
        # Get search details
        search_name = input("📝 Enter a name for this search (e.g., 'Alabama_Businesses_Dec2024'): ").strip()
        if not search_name:
            search_name = f"AutoSearch_{int(time.time())}"
        
        self.session_state['search_name'] = search_name
        self.session_state['start_time'] = time.time()
        
        print(f"\n✅ Search named: {search_name}")
        print("🤖 AUTOMATION STARTING...")
        
        return True
    
    def auto_detect_search_info(self):
        """Automatically detect total pages and records"""
        print("\n🔍 AUTO-DETECTING SEARCH INFORMATION...")
        
        self.wait_for_page_stability()
        
        # Detect total pages
        total_pages = self._detect_total_pages()
        total_records = self._detect_total_records()
        
        if total_pages:
            self.session_state['total_pages'] = total_pages
            print(f"📊 Auto-detected: {total_pages} pages")
        else:
            # Manual fallback
            total_pages = int(input("📊 Could not auto-detect. How many total pages? "))
            self.session_state['total_pages'] = total_pages
        
        if total_records:
            self.session_state['total_records'] = total_records
            print(f"📈 Auto-detected: {total_records:,} total records")
        else:
            estimated_records = total_pages * self.RECORDS_PER_PAGE
            self.session_state['total_records'] = estimated_records
            print(f"📈 Estimated: {estimated_records:,} total records")
        
        # Calculate batches
        total_batches = (total_pages + self.BATCH_SIZE_PAGES - 1) // self.BATCH_SIZE_PAGES
        
        print(f"\n📋 AUTOMATION PLAN:")
        print(f"   Total pages: {total_pages}")
        print(f"   Total records: {self.session_state['total_records']:,}")
        print(f"   Batch size: {self.BATCH_SIZE_PAGES} pages per batch")
        print(f"   Total batches: {total_batches}")
        print(f"   Download directory: {self.download_dir}")
        
        return True
    
    def _detect_total_pages(self):
        """Auto-detect total pages from pagination"""
        try:
            page_indicators = [
                "//span[contains(text(), 'Page') and contains(text(), 'of')]",
                "//div[contains(text(), 'Page') and contains(text(), 'of')]",
                "//*[contains(text(), 'of') and contains(text(), 'Page')]"
            ]
            
            for selector in page_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        text = element.text
                        if "of" in text.lower():
                            parts = text.lower().split("of")
                            if len(parts) > 1:
                                import re
                                numbers = re.findall(r'\\d+', parts[1])
                                if numbers:
                                    return int(numbers[0])
                except:
                    continue
            return None
        except:
            return None
    
    def _detect_total_records(self):
        """Auto-detect total records from results summary"""
        try:
            record_indicators = [
                "//*[contains(text(), 'Results') and contains(text(), ',')]",
                "//*[contains(text(), 'records') and contains(text(), ',')]",
                "//*[contains(text(), 'companies') and contains(text(), ',')]"
            ]
            
            for selector in record_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        text = element.text
                        import re
                        # Look for numbers with commas (like "1,534 Results")
                        numbers = re.findall(r'[\\d,]+', text)
                        for num in numbers:
                            if ',' in num:
                                return int(num.replace(',', ''))
                except:
                    continue
            return None
        except:
            return None
    
    def run_full_automation(self):
        """Run complete automation from current page"""
        print("\\n🤖 STARTING FULL AUTOMATION SEQUENCE")
        print("=" * 50)
        
        total_pages = self.session_state['total_pages']
        
        # Resume from last completed page if continuing session
        start_page = self.session_state.get('last_completed_page', 0) + 1
        if start_page > 1:
            print(f"🔄 Resuming from page {start_page}")
        
        # Calculate batches
        total_batches = (total_pages - start_page + 1 + self.BATCH_SIZE_PAGES - 1) // self.BATCH_SIZE_PAGES
        current_page = start_page
        batch_num = self.session_state.get('current_batch', 1)
        
        print(f"📊 Processing pages {start_page} to {total_pages} in {total_batches} batches")
        
        try:
            while current_page <= total_pages:
                batch_end = min(current_page + self.BATCH_SIZE_PAGES - 1, total_pages)
                
                print(f"\\n🎯 BATCH {batch_num}/{total_batches + batch_num - 1}: PAGES {current_page}-{batch_end}")
                print("=" * 50)
                
                # Process batch with full automation
                success = self.process_batch_full_auto(current_page, batch_end, batch_num)
                
                if success:
                    print(f"✅ Batch {batch_num} completed successfully")
                    current_page = batch_end + 1
                    batch_num += 1
                    
                    # Brief pause between batches
                    if current_page <= total_pages:
                        print("⏳ Brief pause before next batch...")
                        time.sleep(random.uniform(3, 6))
                else:
                    print(f"❌ Batch {batch_num} failed")
                    
                    retry = input("🔄 Retry this batch? (y/n): ").lower().strip()
                    if retry not in ['y', 'yes']:
                        print("🛑 Automation stopped by user")
                        break
            
            # Final summary
            self.print_completion_summary()
            
        except KeyboardInterrupt:
            print("\\n🛑 Automation interrupted by user")
            self._save_session_state()
        except Exception as e:
            print(f"\\n❌ Automation error: {e}")
            self._save_session_state()
    
    def process_batch_full_auto(self, batch_start, batch_end, batch_num):
        """Process a batch with full automation - no manual intervention"""
        try:
            selected_pages = []
            
            # PHASE 1: Navigate and select each page
            for page in range(batch_start, batch_end + 1):
                print(f"\\n📍 Page {page}: Navigate → Select")
                
                # Ensure navigation is available
                if page > batch_start:
                    self.ensure_navigation_available()
                
                # Navigate to page
                if self.auto_navigate_to_page(page):
                    # Select all records immediately
                    if self.auto_select_all_records():
                        selected_pages.append(page)
                        print(f"✅ Page {page}: Selected")
                    else:
                        print(f"⚠️ Page {page}: Selection failed")
                else:
                    print(f"❌ Page {page}: Navigation failed")
                
                time.sleep(random.uniform(1, 2))
            
            if not selected_pages:
                return False
            
            print(f"\\n📊 Batch summary: {len(selected_pages)}/{batch_end - batch_start + 1} pages selected")
            
            # PHASE 2: Download all selected records
            print("\\n📥 Downloading batch...")
            download_success = self.auto_download_records(batch_num)
            
            # PHASE 3: Clean up for next batch
            print("\\n🧹 Cleaning up...")
            self.auto_cleanup_after_download()
            
            # Update session state
            self.update_session_state(batch_num, batch_start, batch_end, selected_pages)
            
            return download_success
            
        except Exception as e:
            print(f"❌ Batch processing error: {e}")
            return False
    
    def ensure_navigation_available(self):
        """Ensure navigation elements are available (uncheck if needed)"""
        try:
            # Check if page input is visible
            page_inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
            navigation_visible = False
            
            for input_elem in page_inputs:
                if input_elem.is_displayed():
                    value = input_elem.get_attribute('value') or ''
                    if value.isdigit() and int(value) <= 100:
                        navigation_visible = True
                        break
            
            if not navigation_visible:
                print("🔧 Restoring navigation...")
                self.bulk_uncheck_all()
                time.sleep(2)
                self.wait_for_page_stability()
            
        except Exception as e:
            print(f"⚠️ Navigation check error: {e}")
    
    def auto_navigate_to_page(self, page_num):
        """Fully automated navigation to page"""
        try:
            current_page = self.detect_current_page()
            if current_page == page_num:
                return True
            
            # Find page input
            page_inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
            
            for input_elem in page_inputs:
                if input_elem.is_displayed() and input_elem.is_enabled():
                    value = input_elem.get_attribute('value') or ''
                    if value.isdigit() and int(value) <= 100:
                        # Navigate using input + Enter
                        input_elem.click()
                        time.sleep(0.2)
                        input_elem.clear()
                        time.sleep(0.1)
                        input_elem.send_keys(str(page_num))
                        time.sleep(0.2)
                        input_elem.send_keys(Keys.ENTER)
                        time.sleep(3)
                        
                        self.wait_for_page_stability()
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False
    
    def auto_select_all_records(self):
        """Fully automated record selection"""
        try:
            # Wait for page to load
            self.wait_for_page_stability()
            
            # Enhanced checkbox detection
            checkbox_selectors = [
                "//input[@type='checkbox']",
                "//table//input[@type='checkbox']",
                "//th//input[@type='checkbox']",
                "//thead//input[@type='checkbox']"
            ]
            
            # Find all checkboxes
            all_checkboxes = []
            for selector in checkbox_selectors:
                try:
                    checkboxes = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_all_elements_located((By.XPATH, selector))
                    )
                    visible_checkboxes = [cb for cb in checkboxes if cb.is_displayed()]
                    all_checkboxes.extend(visible_checkboxes)
                except:
                    continue
            
            if not all_checkboxes:
                return False
            
            # Remove duplicates
            unique_checkboxes = []
            seen = set()
            for cb in all_checkboxes:
                cb_id = id(cb)
                if cb_id not in seen:
                    unique_checkboxes.append(cb)
                    seen.add(cb_id)
            
            # Try header checkbox first (select all)
            for checkbox in unique_checkboxes[:3]:
                try:
                    if not checkbox.is_selected():
                        ActionChains(self.driver).move_to_element(checkbox).pause(0.2).click().perform()
                        time.sleep(1)
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Selection error: {e}")
            return False
    
    def auto_download_records(self, batch_num):
        """Fully automated download process"""
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
            filename = self.wait_for_download(batch_num)
            return filename is not None
            
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
            initial_files = os.listdir(self.download_dir) if os.path.exists(self.download_dir) else []
            
            max_wait = 60  # 60 seconds
            wait_time = 0
            
            while wait_time < max_wait:
                time.sleep(2)
                wait_time += 2
                
                if os.path.exists(self.download_dir):
                    current_files = os.listdir(self.download_dir)
                    new_files = [f for f in current_files if f not in initial_files and not f.endswith('.crdownload')]
                    
                    if new_files:
                        print(f"✅ Downloaded: {new_files[0]}")
                        return new_files[0]
            
            print("⚠️ Download timeout")
            return None
            
        except Exception as e:
            print(f"❌ Download wait error: {e}")
            return None
    
    def auto_cleanup_after_download(self):
        """Automatic cleanup after download"""
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
            self.bulk_uncheck_all()
            
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")
    
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
    
    def update_session_state(self, batch_num, batch_start, batch_end, selected_pages):
        """Update session state with batch results"""
        try:
            search_name = self.session_state['search_name']
            timestamp = time.strftime('%m%d%y_%H%M')
            
            self.session_state['completed_batches'].append({
                'batch_num': batch_num,
                'start_page': batch_start,
                'end_page': batch_end,
                'pages_processed': selected_pages,
                'timestamp': timestamp
            })
            
            self.session_state['last_completed_page'] = batch_end
            self.session_state['current_batch'] = batch_num + 1
            
            self._save_session_state()
            
        except Exception as e:
            print(f"⚠️ Session update error: {e}")
    
    def print_completion_summary(self):
        """Print automation completion summary"""
        completed_batches = len(self.session_state['completed_batches'])
        total_time = time.time() - self.session_state['start_time']
        
        print(f"\\n🏁 AUTOMATION COMPLETE!")
        print("=" * 40)
        print(f"✅ Search: {self.session_state['search_name']}")
        print(f"✅ Completed batches: {completed_batches}")
        print(f"✅ Last page processed: {self.session_state['last_completed_page']}")
        print(f"✅ Total time: {total_time/60:.1f} minutes")
        print(f"✅ Download directory: {self.download_dir}")
        
        # List downloaded files
        if os.path.exists(self.download_dir):
            files = [f for f in os.listdir(self.download_dir) if f.endswith('.csv')]
            print(f"✅ Downloaded files: {len(files)}")
            for file in files[-5:]:  # Show last 5 files
                print(f"   📄 {file}")
    
    def run(self):
        """Main automation entry point"""
        try:
            # Step 1: User navigates to search results
            if not self.start_automation_from_search_results():
                return
            
            # Step 2: Auto-detect search information
            if not self.auto_detect_search_info():
                return
            
            # Step 3: Confirm automation start
            print(f"\\n🤖 READY TO START FULL AUTOMATION")
            proceed = input("🚀 Start automated processing? (y/n): ").lower().strip()
            
            if proceed not in ['y', 'yes']:
                print("❌ Automation cancelled")
                return
            
            # Step 4: Run full automation
            self.run_full_automation()
            
        except Exception as e:
            print(f"\\n❌ Automation failed: {e}")
        finally:
            input("\\nPress Enter to close browser...")
            self.driver.quit()

if __name__ == "__main__":
    try:
        scraper = FullAutomationScraper()
        scraper.run()
    except KeyboardInterrupt:
        print("\\n🛑 Automation interrupted")
    except Exception as e:
        print(f"\\n❌ Critical error: {e}")
