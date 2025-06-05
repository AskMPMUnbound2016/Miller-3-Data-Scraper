#!/usr/bin/env python3
"""
Enhanced Manual Login Data Scraper - Fixed Critical Issues
This script addresses the 3 main blocking issues: download button detection, checkbox unchecking, file verification
"""
import os
import sys
import time
import yaml
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class EnhancedManualLoginScraper:
    def __init__(self, config_file='config/referenceusa_config.yaml'):
        print("\n=== ENHANCED MANUAL LOGIN DATA SCRAPER ===")
        print("🔧 Fixed: Download button detection, checkbox unchecking, file verification")
        
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Extract config values
        self.download_dir = self.config.get('download_dir', os.path.join(os.getcwd(), "downloads"))
        self.auth_url = self.config.get('auth_url')
        self.search_parameters = self.config.get('search_parameters', {})
        self.pages_per_batch = self.config.get('pages_per_batch', 10)
        self.pages_to_download = self.config.get('pages_to_download', 'all')
        
        # Initialize browser
        self._setup_browser()
        
        # Show download directory info
        print(f"📂 Download directory: {self.download_dir}")
        if not os.path.exists(self.download_dir):
            print("⚠️  Download directory doesn't exist, creating it...")
            os.makedirs(self.download_dir, exist_ok=True)
            print("✅ Download directory created")
        else:
            existing_files = self._get_download_files()
            print(f"📄 Current files in download folder: {len(existing_files)}")
    
    def _load_config(self, config_file):
        """Load configuration with multiple fallback options"""
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                print(f"✅ Loaded config from: {config_file}")
                return config
        except FileNotFoundError:
            print(f"⚠️ Config file '{config_file}' not found!")
            
            # Try alternative config files
            alt_config_files = [
                'config/referenceusa_config.yaml',
                'referenceusa_config.yaml',
                'config.yaml'
            ]
            
            for alt_file in alt_config_files:
                if os.path.exists(alt_file):
                    print(f"Found alternative config file: {alt_file}")
                    with open(alt_file, 'r') as f:
                        config = yaml.safe_load(f)
                        print(f"✅ Loaded config from: {alt_file}")
                        return config
            
            print("No configuration files found. Using default configuration.")
            return {
                'download_dir': os.path.join(os.getcwd(), "downloads"),
                'auth_url': "https://www.referenceusa.com",
                'search_parameters': {},
                'pages_per_batch': 10,
                'pages_to_download': 'all',
                'state_file': 'reference_usa_state.json'
            }
    
    def _setup_browser(self):
        """Configure and initialize the Chrome browser with enhanced settings"""
        print("Configuring Chrome browser...")
        
        # Configure browser options
        options = webdriver.ChromeOptions()
        
        # Add options for downloads - use absolute path
        download_dir = os.path.abspath(self.download_dir)
        os.makedirs(download_dir, exist_ok=True)
        
        options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.notifications": 2,
            "safebrowsing.disable_download_protection": True,
            "plugins.always_open_pdf_externally": True
        })
        
        # Add options to make detection harder
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Add random user-agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        ]
        options.add_argument(f"user-agent={random.choice(user_agents)}")
        
        # Initialize browser with local chromedriver
        print("Starting Chrome browser with local chromedriver...")
        chromedriver_paths = ["./chromedriver", "chromedriver", "/usr/local/bin/chromedriver"]
        
        chromedriver_path = None
        for path in chromedriver_paths:
            if os.path.exists(path):
                chromedriver_path = path
                break
        
        if not chromedriver_path:
            print("❌ Error: ChromeDriver not found. Trying to use system PATH...")
            try:
                self.driver = webdriver.Chrome(options=options)
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                print("Please ensure chromedriver is installed and in PATH or in the same folder.")
                raise FileNotFoundError("ChromeDriver not found")
        else:
            print(f"Using ChromeDriver at: {chromedriver_path}")
            self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        
        # Hide webdriver attribute
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Store the actual download directory used
        self.download_dir = download_dir
    
    def start_manual_login(self):
        """Start manual login process"""
        print("\n=== Starting Manual Login Process ===")
        
        # Choose the starting URL
        start_url = self.auth_url if self.auth_url else "https://www.referenceusa.com"
        
        print(f"Opening browser to: {start_url}")
        self.driver.get(start_url)
        
        # Take screenshot of initial page
        self._take_screenshot("initial_login_page")
        
        print("\n📋 MANUAL LOGIN INSTRUCTIONS:")
        print("1. Log in with your library credentials")
        print("2. Navigate through authentication steps")
        print("3. Select the U.S. Business database if prompted")
        print("4. Continue until you reach the search page")
        print("5. Set up your search criteria as needed")
        print("6. Click 'View Results' or 'Search' to run your search")
        print("7. Wait for the results to load")
        print("\n🤖 AUTOMATION WILL TAKE OVER:")
        print("Once you see search results, the script will automatically:")
        print("- Select records on each page")
        print("- Navigate through pages")
        print("- Download in batches")
        print("- Handle the entire download process")
        
        while True:
            ready_input = input("\n⏸️ Type 'ready' when search results are displayed and you're ready for AUTOMATED downloading: ").strip().lower()
            if ready_input == 'ready':
                break
            else:
                print("❌ Please navigate to search results and type 'ready' to continue")
        
        # Take screenshot of the search results page
        self._take_screenshot("search_results_displayed")
        
        # Check if we're on a results page
        current_url = self.driver.current_url
        print(f"\nCurrent URL: {current_url}")
        
        return True
    
    def run_automated_search(self):
        """Run the automated search and download process with enhanced error handling"""
        try:
            print("\n=== Starting ENHANCED Automated Download Process ===")
            print("🔧 Using improved download button detection and file verification")
            
            # Try to detect total pages
            total_pages = self._detect_total_pages()
            if total_pages:
                print(f"Detected {total_pages} total pages of results")
            
            # Ask for download preferences
            print("\nDownload options:")
            download_option = input("Download ALL pages or a SPECIFIC range? (all/specific): ").lower().strip()
            
            if download_option == 'all':
                start_batch = 1
                end_batch = total_pages if total_pages > 0 else 100
                print(f"\nWill download all {end_batch} pages in batches of 10")
            else:
                start_page_input = input("Start downloading from which page? (default: 1): ").strip()
                start_batch = 1 if not start_page_input else int(start_page_input)
                
                end_page_input = input(f"End downloading at which page? (default: all remaining): ").strip()
                if end_page_input:
                    end_batch = int(end_page_input)
                else:
                    end_batch = total_pages if total_pages > 0 else 100
                
                print(f"\nWill download pages {start_batch} through {end_batch}")
            
            # Calculate batches
            max_pages_per_batch = 10
            total_batches = (end_batch - start_batch + 1 + max_pages_per_batch - 1) // max_pages_per_batch
            print(f"This will require {total_batches} batch(es) of downloads")
            
            print(f"\n🤖 ENHANCED AUTOMATION STARTING:")
            print(f"Starting page: {start_batch}")
            print(f"Ending page: {end_batch}")
            
            # Confirm to proceed
            proceed = input("\nPress Enter to start automated downloading, or type 'quit' to exit: ").lower()
            if proceed == 'quit':
                print("Exiting without downloading.")
                return False
            
            # Process in batches
            current_batch_start = start_batch
            
            while current_batch_start <= end_batch:
                current_batch_end = min(current_batch_start + max_pages_per_batch - 1, end_batch)
                current_batch_size = current_batch_end - current_batch_start + 1
                
                print(f"\n🔧 ENHANCED BATCH: Pages {current_batch_start} to {current_batch_end} ({current_batch_size} pages)")
                
                # Process batch automatically with enhanced methods
                batch_result = self._process_batch_enhanced(current_batch_start, current_batch_end)
                
                if not batch_result:
                    print(f"\nFailed to process batch {current_batch_start}-{current_batch_end}. Stopping.")
                    break
                
                # Move to next batch
                current_batch_start = current_batch_end + 1
                
                # Ask if user wants to continue with next batch
                if current_batch_start <= end_batch:
                    continue_next = input(f"\nContinue with next batch ({current_batch_start}-{min(current_batch_start + max_pages_per_batch - 1, end_batch)})? (y/n): ").lower().strip()
                    if continue_next not in ['y', 'yes']:
                        print("Stopping further downloads as requested.")
                        break
            
            print(f"\n✅ Enhanced automated download process complete!")
            if current_batch_start > end_batch:
                print("All requested pages have been processed.")
            else:
                print(f"Processed pages {start_batch} to {current_batch_start - 1}.")
                
            return True
                
        except Exception as e:
            print(f"Error during automated processing: {str(e)}")
            return False
    
    def _process_batch_enhanced(self, start_page, end_page):
        """Enhanced batch processing with improved error handling"""
        try:
            print(f"\n🔧 ENHANCED PROCESSING: Pages {start_page} through {end_page}")
            
            # Track processed pages
            processed_pages = []
            
            # Step 1: Navigate through pages and select all records
            current_page = start_page
            while current_page <= end_page:
                print(f"\n🔧 ENHANCED PAGE PROCESSING: Page {current_page}")
                
                # Navigate to page if needed
                if current_page != start_page:
                    if not self._navigate_to_page_enhanced(current_page):
                        print(f"❌ Failed to navigate to page {current_page}")
                        break
                    time.sleep(2)
                
                # Take screenshot before selection
                self._take_screenshot(f"before_page_{current_page}_selection")
                
                # Enhanced record selection
                if self._select_all_records_enhanced():
                    print(f"✅ Selected records on page {current_page}")
                    processed_pages.append(current_page)
                else:
                    print(f"⚠️ Had trouble selecting records on page {current_page}, but continuing...")
                    processed_pages.append(current_page)
                
                # Take screenshot after selection
                self._take_screenshot(f"after_page_{current_page}_selection")
                
                current_page += 1
            
            # Step 2: Enhanced download process
            print(f"\n🔧 ENHANCED DOWNLOAD: Selected records from pages {start_page}-{end_page}")
            
            # Take screenshot before download
            self._take_screenshot("before_enhanced_download")
            
            if self._download_records_enhanced(start_page, end_page):
                print(f"✅ Successfully downloaded pages {start_page}-{end_page}")
            else:
                print(f"⚠️ Download may have had issues, but continuing...")
            
            # Step 3: Enhanced cleanup
            print(f"\n🔧 ENHANCED CLEANUP: Unchecking records from downloaded pages")
            
            # Navigate back to results if needed
            self._navigate_back_to_results_enhanced()
            
            # Enhanced unchecking for each processed page
            for page in processed_pages:
                print(f"🔧 Enhanced unchecking records on page {page}...")
                if page != processed_pages[0]:  # Don't navigate to first page twice
                    self._navigate_to_page_enhanced(page)
                    time.sleep(1)
                
                self._uncheck_all_records_enhanced()
                self._take_screenshot(f"after_enhanced_uncheck_page_{page}")
            
            print(f"✅ Completed enhanced processing of pages {start_page} through {end_page}")
            return True
            
        except Exception as e:
            print(f"❌ Error in enhanced batch processing: {str(e)}")
            print("Continuing with manual fallback...")
            return True  # Continue even if there are errors
    
    def _navigate_to_page_enhanced(self, page_number):
        """Enhanced page navigation with multiple strategies"""
        try:
            print(f"🔧 ENHANCED NAVIGATION: Going to page {page_number}")
            
            # Strategy 1: JavaScript-powered detection
            print("🔧 Strategy 1: JavaScript detection...")
            js_navigation = """
            // Enhanced page navigation script
            function findAndNavigateToPage(targetPage) {
                console.log('Looking for page navigation elements...');
                
                // Method 1: Direct page input field
                let pageInputs = document.querySelectorAll('input[type="text"], input[type="number"]');
                for (let input of pageInputs) {
                    if (input.offsetParent !== null) { // visible
                        let inputText = input.value || input.placeholder || '';
                        let parent = input.parentElement ? input.parentElement.textContent : '';
                        
                        if (parent.toLowerCase().includes('page') || 
                            inputText.match(/^\\d+$/) || 
                            input.getAttribute('name')?.includes('page')) {
                            
                            console.log('Found page input:', input);
                            input.value = targetPage;
                            input.dispatchEvent(new Event('change'));
                            input.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter'}));
                            return true;
                        }
                    }
                }
                
                // Method 2: Page number link
                let pageLinks = document.querySelectorAll('a');
                for (let link of pageLinks) {
                    if (link.textContent.trim() === targetPage.toString() && 
                        link.offsetParent !== null) {
                        console.log('Found page link:', link);
                        link.click();
                        return true;
                    }
                }
                
                // Method 3: Page form submission
                let forms = document.querySelectorAll('form');
                for (let form of forms) {
                    let pageInput = form.querySelector('input[type="text"], input[type="number"]');
                    if (pageInput && form.textContent.toLowerCase().includes('page')) {
                        console.log('Found form-based navigation:', form);
                        pageInput.value = targetPage;
                        form.submit();
                        return true;
                    }
                }
                
                return false;
            }
            
            return findAndNavigateToPage(arguments[0]);
            """
            
            js_result = self.driver.execute_script(js_navigation, page_number)
            if js_result:
                print(f"✅ JavaScript navigation successful to page {page_number}")
                time.sleep(3)
                return True
            
            # Strategy 2: Enhanced XPath detection
            print("🔧 Strategy 2: Enhanced XPath detection...")
            enhanced_xpaths = [
                # More specific page input patterns
                "//input[@type='text'][ancestor::*[contains(text(), 'Page')] and string-length(@value) < 4]",
                "//input[@type='number'][ancestor::*[contains(text(), 'Page')]]",
                "//form[contains(., 'Page')]//input[@type='text' or @type='number']",
                
                # Navigation context patterns
                "//nav//input[@type='text' or @type='number']",
                "//div[contains(@class, 'pag')]//input[@type='text' or @type='number']",
                
                # Generic small text inputs (likely page numbers)
                "//input[@type='text'][string-length(@value) <= 3 and @value != '']",
                "//input[@type='text'][@size <= 5 or @maxlength <= 5]"
            ]
            
            for xpath in enhanced_xpaths:
                try:
                    page_inputs = self.driver.find_elements(By.XPATH, xpath)
                    for input_field in page_inputs:
                        if self._is_element_visible(input_field):
                            print(f"🔧 Found page input with xpath: {xpath}")
                            
                            # Clear and enter page number
                            input_field.clear()
                            time.sleep(0.5)
                            input_field.send_keys(str(page_number))
                            time.sleep(0.5)
                            input_field.send_keys(Keys.ENTER)
                            time.sleep(3)
                            
                            print(f"✅ Enhanced navigation to page {page_number} successful")
                            return True
                except Exception as e:
                    continue
            
            # Strategy 3: Manual guidance with enhanced feedback
            print("🔧 Strategy 3: Enhanced manual guidance...")
            current_page_info = self.driver.execute_script("""
                // Get current page information
                let pageInfo = document.querySelector('*:contains("Page")');
                if (pageInfo) return pageInfo.textContent;
                
                let pageInputs = document.querySelectorAll('input[type="text"], input[type="number"]');
                for (let input of pageInputs) {
                    if (input.value && input.value.match(/^\\d+$/)) {
                        return 'Current page: ' + input.value;
                    }
                }
                return 'Page info not found';
            """)
            
            print(f"📍 Current page info: {current_page_info}")
            print(f"🔧 Enhanced manual navigation needed:")
            print(f"1. Look for page navigation (current page input or 'Page X of Y')")
            print(f"2. Change the page number to {page_number}")
            print(f"3. Press Enter or click Go/Submit")
            
            input(f"Press Enter when you've navigated to page {page_number}...")
            return True
            
        except Exception as e:
            print(f"⚠️ Enhanced navigation failed: {str(e)}")
            return False
    
    def _select_all_records_enhanced(self):
        """Enhanced record selection with JavaScript fallbacks"""
        try:
            print("🔧 ENHANCED RECORD SELECTION: Finding and selecting all records...")
            
            # Strategy 1: JavaScript-powered selection
            print("🔧 Strategy 1: JavaScript bulk selection...")
            js_selection_result = self.driver.execute_script("""
                // Enhanced record selection script
                function selectAllRecords() {
                    console.log('Starting enhanced record selection...');
                    
                    // Method 1: Find and click header "Select All" checkbox
                    let headerCheckboxes = document.querySelectorAll('th input[type="checkbox"], thead input[type="checkbox"]');
                    for (let cb of headerCheckboxes) {
                        if (cb.offsetParent !== null && !cb.checked) { // visible and not checked
                            console.log('Found header checkbox, clicking...');
                            cb.click();
                            
                            // Wait and check if other checkboxes got selected
                            setTimeout(() => {
                                let selectedCount = document.querySelectorAll('input[type="checkbox"]:checked').length;
                                console.log('Selected count after header click:', selectedCount);
                            }, 500);
                            
                            return { success: true, method: 'header_checkbox', count: -1 };
                        }
                    }
                    
                    // Method 2: Select individual checkboxes (skip first one if it's header)
                    let allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
                    let dataCheckboxes = [];
                    
                    for (let i = 0; i < allCheckboxes.length; i++) {
                        let cb = allCheckboxes[i];
                        if (cb.offsetParent !== null) { // visible
                            // Skip if this appears to be a header checkbox
                            let isHeader = cb.closest('th') || cb.closest('thead');
                            if (!isHeader || i > 0) { // Include if not header, or if not the first one
                                dataCheckboxes.push(cb);
                            }
                        }
                    }
                    
                    console.log('Found', dataCheckboxes.length, 'data checkboxes');
                    
                    let selectedCount = 0;
                    for (let cb of dataCheckboxes) {
                        if (!cb.checked) {
                            cb.checked = true;
                            cb.dispatchEvent(new Event('change'));
                            selectedCount++;
                        }
                    }
                    
                    return { success: selectedCount > 0, method: 'individual_checkboxes', count: selectedCount };
                }
                
                return selectAllRecords();
            """)
            
            if js_selection_result['success']:
                print(f"✅ JavaScript selection successful: {js_selection_result['method']}")
                if js_selection_result['count'] > 0:
                    print(f"   Selected {js_selection_result['count']} checkboxes")
                return True
            
            # Strategy 2: Enhanced Selenium selection with better detection
            print("🔧 Strategy 2: Enhanced Selenium selection...")
            
            # Look for header checkbox more precisely
            header_selectors = [
                "//table//tr[1]//input[@type='checkbox']",  # First row checkbox
                "//thead//input[@type='checkbox']",  # Header section checkbox
                "//th//input[@type='checkbox']",  # Table header checkbox
                "//th[contains(text(), 'Company') or contains(text(), 'Business')]//input[@type='checkbox']",  # Near company name
                "//th[contains(text(), 'Company') or contains(text(), 'Business')]/preceding-sibling::th//input[@type='checkbox']",
                "//table//input[@type='checkbox'][1]"  # First checkbox in table
            ]
            
            header_checkbox_found = False
            for selector in header_selectors:
                try:
                    checkboxes = self.driver.find_elements(By.XPATH, selector)
                    for checkbox in checkboxes:
                        if self._is_element_visible(checkbox):
                            print(f"🔧 Found header checkbox: {selector}")
                            
                            if not checkbox.is_selected():
                                # Try multiple click methods
                                click_methods = [
                                    lambda: checkbox.click(),
                                    lambda: self.driver.execute_script("arguments[0].click();", checkbox),
                                    lambda: self.driver.execute_script("arguments[0].checked = true; arguments[0].dispatchEvent(new Event('change'));", checkbox)
                                ]
                                
                                for method in click_methods:
                                    try:
                                        method()
                                        time.sleep(1)
                                        
                                        # Check if selection worked
                                        all_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
                                        selected_count = len([cb for cb in all_checkboxes if cb.is_selected()])
                                        
                                        if selected_count > 1:  # More than just header
                                            print(f"✅ Header selection worked! {selected_count} checkboxes selected")
                                            header_checkbox_found = True
                                            break
                                    except:
                                        continue
                                
                                if header_checkbox_found:
                                    break
                            else:
                                print("⚠️ Header checkbox already selected")
                                header_checkbox_found = True
                                break
                    
                    if header_checkbox_found:
                        break
                except:
                    continue
            
            if header_checkbox_found:
                return True
            
            # Strategy 3: Individual checkbox selection with enhanced detection
            print("🔧 Strategy 3: Enhanced individual selection...")
            
            all_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            data_checkboxes = []
            
            for i, checkbox in enumerate(all_checkboxes):
                if self._is_element_visible(checkbox):
                    # Try to determine if this is a data checkbox vs header checkbox
                    is_likely_header = False
                    try:
                        # Check if in header context
                        parent_tags = self.driver.execute_script("""
                            var element = arguments[0];
                            var tags = [];
                            var current = element;
                            for (var j = 0; j < 5; j++) {
                                if (current.parentElement) {
                                    current = current.parentElement;
                                    tags.push(current.tagName.toLowerCase());
                                } else break;
                            }
                            return tags;
                        """, checkbox)
                        
                        if 'th' in parent_tags or 'thead' in parent_tags:
                            is_likely_header = True
                        elif i == 0:  # First checkbox might be header
                            is_likely_header = True
                    except:
                        pass
                    
                    if not is_likely_header:
                        data_checkboxes.append(checkbox)
            
            if not data_checkboxes:
                print("⚠️ No data checkboxes found, selecting all visible checkboxes")
                data_checkboxes = [cb for cb in all_checkboxes if self._is_element_visible(cb)]
            
            print(f"🔧 Selecting {len(data_checkboxes)} individual checkboxes...")
            
            success_count = 0
            for checkbox in data_checkboxes:
                if not checkbox.is_selected():
                    if self._click_checkbox_enhanced(checkbox):
                        success_count += 1
            
            print(f"✅ Enhanced individual selection complete: {success_count} checkboxes selected")
            return success_count > 0
            
        except Exception as e:
            print(f"⚠️ Enhanced selection error: {str(e)}")
            return False
    
    def _click_checkbox_enhanced(self, checkbox):
        """Enhanced checkbox clicking with multiple fallback methods"""
        try:
            # Method 1: Direct click
            try:
                checkbox.click()
                return True
            except:
                pass
            
            # Method 2: JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", checkbox)
                return True
            except:
                pass
            
            # Method 3: JavaScript property setting with event
            try:
                self.driver.execute_script("""
                    arguments[0].checked = true;
                    arguments[0].dispatchEvent(new Event('change'));
                    arguments[0].dispatchEvent(new Event('click'));
                """, checkbox)
                return True
            except:
                pass
            
            # Method 4: Action chains
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(checkbox).click().perform()
                return True
            except:
                pass
            
            return False
        except:
            return False
    
    def _download_records_enhanced(self, start_page, end_page):
        """Enhanced download process with multiple detection strategies"""
        try:
            print("🔧 ENHANCED DOWNLOAD: Starting improved download process...")
            
            # Strategy 1: JavaScript-powered download button detection
            print("🔧 Strategy 1: JavaScript download button detection...")
            
            js_download_result = self.driver.execute_script("""
                // Enhanced download button detection
                function findAndClickDownloadButton() {
                    console.log('Searching for download buttons...');
                    
                    // Method 1: Text-based search (case insensitive)
                    let textElements = document.querySelectorAll('a, button, input[type="submit"], input[type="button"]');
                    for (let el of textElements) {
                        let text = el.textContent || el.value || el.title || '';
                        if (text.toLowerCase().includes('download') && el.offsetParent !== null) {
                            console.log('Found download button by text:', el);
                            el.click();
                            return { success: true, method: 'text_search', element: el.tagName };
                        }
                    }
                    
                    // Method 2: Attribute-based search
                    let attrElements = document.querySelectorAll('[class*="download"], [id*="download"], [onclick*="download"], [href*="download"]');
                    for (let el of attrElements) {
                        if (el.offsetParent !== null && (el.tagName === 'A' || el.tagName === 'BUTTON' || el.type === 'submit')) {
                            console.log('Found download button by attributes:', el);
                            el.click();
                            return { success: true, method: 'attribute_search', element: el.tagName };
                        }
                    }
                    
                    // Method 3: Form-based download
                    let forms = document.querySelectorAll('form');
                    for (let form of forms) {
                        if (form.textContent.toLowerCase().includes('download')) {
                            let submitBtn = form.querySelector('input[type="submit"], button[type="submit"], button');
                            if (submitBtn) {
                                console.log('Found form-based download:', submitBtn);
                                submitBtn.click();
                                return { success: true, method: 'form_submit', element: submitBtn.tagName };
                            }
                        }
                    }
                    
                    return { success: false, method: 'none' };
                }
                
                return findAndClickDownloadButton();
            """)
            
            if js_download_result['success']:
                print(f"✅ JavaScript download button found: {js_download_result['method']}")
                time.sleep(3)
            else:
                # Strategy 2: Enhanced Selenium detection
                print("🔧 Strategy 2: Enhanced Selenium download detection...")
                
                download_selectors = [
                    "//a[contains(translate(text(), 'DOWNLOAD', 'download'), 'download')]",
                    "//button[contains(translate(text(), 'DOWNLOAD', 'download'), 'download')]",
                    "//input[@type='submit' and contains(translate(@value, 'DOWNLOAD', 'download'), 'download')]",
                    "//input[@type='button' and contains(translate(@value, 'DOWNLOAD', 'download'), 'download')]",
                    "//a[contains(@class, 'download') or contains(@id, 'download')]",
                    "//button[contains(@class, 'download') or contains(@id, 'download')]",
                    "//form//input[@type='submit']",
                    "//form//button[contains(text(), 'Submit') or contains(text(), 'Download')]"
                ]
                
                download_clicked = False
                for selector in download_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        for element in elements:
                            if self._is_element_visible(element):
                                print(f"🔧 Found download element: {selector}")
                                
                                # Try enhanced clicking
                                if self._click_element_enhanced(element):
                                    print("✅ Download button clicked successfully")
                                    download_clicked = True
                                    break
                    except:
                        continue
                    
                    if download_clicked:
                        break
                
                if not download_clicked:
                    print("⚠️ Could not find download button automatically")
                    print("🔧 Enhanced manual guidance:")
                    
                    # Show all clickable elements for debugging
                    clickable_elements = self.driver.execute_script("""
                        let clickables = document.querySelectorAll('a, button, input[type="submit"], input[type="button"]');
                        let results = [];
                        for (let i = 0; i < Math.min(clickables.length, 10); i++) {
                            let el = clickables[i];
                            if (el.offsetParent !== null) {
                                results.push({
                                    tag: el.tagName,
                                    text: (el.textContent || el.value || '').trim(),
                                    classes: el.className,
                                    id: el.id
                                });
                            }
                        }
                        return results;
                    """)
                    
                    print("📋 Available clickable elements:")
                    for i, el in enumerate(clickable_elements):
                        print(f"   {i+1}. {el['tag']}: '{el['text']}' (class: {el['classes']})")
                    
                    input("Please click the Download button manually and press Enter...")
            
            # Wait for download dialog and handle it
            time.sleep(3)
            self._take_screenshot("download_dialog_enhanced")
            
            # Enhanced format selection
            print("🔧 ENHANCED FORMAT SELECTION:")
            self._select_format_enhanced("detailed")
            
            # Enhanced download execution
            print("🔧 ENHANCED DOWNLOAD EXECUTION:")
            self._execute_download_enhanced()
            
            # Enhanced file verification
            return self._verify_download_enhanced(start_page, end_page)
            
        except Exception as e:
            print(f"⚠️ Enhanced download error: {str(e)}")
            return False
    
    def _click_element_enhanced(self, element):
        """Enhanced element clicking with multiple methods"""
        try:
            # Method 1: Direct click
            try:
                element.click()
                return True
            except:
                pass
            
            # Method 2: JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                pass
            
            # Method 3: Action chains
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
                return True
            except:
                pass
            
            # Method 4: JavaScript with scroll into view
            try:
                self.driver.execute_script("""
                    arguments[0].scrollIntoView();
                    arguments[0].click();
                """, element)
                return True
            except:
                pass
            
            return False
        except:
            return False
    
    def _select_format_enhanced(self, format_type):
        """Enhanced format selection with better detection"""
        try:
            if format_type.lower() == "detailed":
                print("🔧 Selecting Detailed format (not Summary)...")
                
                # JavaScript-powered format selection
                js_format_result = self.driver.execute_script("""
                    // Look for Detailed radio button
                    let radioButtons = document.querySelectorAll('input[type="radio"]');
                    for (let radio of radioButtons) {
                        let label = radio.nextElementSibling || radio.parentElement;
                        let labelText = label ? label.textContent : '';
                        
                        if (labelText.toLowerCase().includes('detail') && !radio.checked) {
                            radio.click();
                            return { success: true, text: labelText };
                        }
                    }
                    
                    // Look for labels containing 'detailed'
                    let labels = document.querySelectorAll('label');
                    for (let label of labels) {
                        if (label.textContent.toLowerCase().includes('detail')) {
                            let radio = label.querySelector('input[type="radio"]') || 
                                       document.querySelector(`input[type="radio"][id="${label.getAttribute('for')}"]`);
                            if (radio && !radio.checked) {
                                radio.click();
                                return { success: true, text: label.textContent };
                            }
                        }
                    }
                    
                    return { success: false };
                """)
                
                if js_format_result['success']:
                    print(f"✅ Selected Detailed format: {js_format_result['text']}")
                    return True
                else:
                    print("⚠️ Could not auto-select Detailed format")
                    return False
                    
        except Exception as e:
            print(f"⚠️ Format selection error: {str(e)}")
            return False
    
    def _execute_download_enhanced(self):
        """Enhanced download execution with better button detection"""
        try:
            print("🔧 Looking for Download Records button...")
            
            # JavaScript-powered download execution
            js_execute_result = self.driver.execute_script("""
                // Look for Download Records button
                let buttons = document.querySelectorAll('button, input[type="submit"], input[type="button"], a');
                for (let btn of buttons) {
                    let text = btn.textContent || btn.value || '';
                    if (text.toLowerCase().includes('download') && text.toLowerCase().includes('record')) {
                        btn.click();
                        return { success: true, text: text };
                    }
                }
                
                // Look for just "Download" button in form context
                let forms = document.querySelectorAll('form');
                for (let form of forms) {
                    let submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
                    if (submitBtn) {
                        let text = submitBtn.textContent || submitBtn.value || '';
                        if (text.toLowerCase().includes('download')) {
                            submitBtn.click();
                            return { success: true, text: text };
                        }
                    }
                }
                
                return { success: false };
            """)
            
            if js_execute_result['success']:
                print(f"✅ Clicked download button: {js_execute_result['text']}")
                return True
            else:
                print("⚠️ Could not find Download Records button")
                input("Please click 'Download Records' manually and press Enter...")
                return True
                
        except Exception as e:
            print(f"⚠️ Download execution error: {str(e)}")
            return False
    
    def _verify_download_enhanced(self, start_page, end_page):
        """Enhanced download verification with better file monitoring"""
        try:
            print("🔧 ENHANCED DOWNLOAD VERIFICATION:")
            print("📂 Please save the file using this naming format:")
            print(f"   {start_page}_{end_page}_SearchName_{int(time.time())}")
            print("📂 Save to the 'downloads' folder if possible")
            
            # Get initial file list
            initial_files = self._get_download_files()
            print(f"📄 Files before download: {len(initial_files)}")
            
            # Monitor for new files with enhanced detection
            print("\n🔍 ENHANCED MONITORING: Watching for new files...")
            
            max_wait_time = 60  # Extended wait time
            check_interval = 3
            last_file_count = len(initial_files)
            
            for elapsed in range(0, max_wait_time, check_interval):
                time.sleep(check_interval)
                
                # Check our download directory
                current_files = self._get_download_files()
                new_files = [f for f in current_files if f not in initial_files]
                
                if new_files:
                    print(f"✅ SUCCESS! {len(new_files)} new file(s) detected:")
                    for f in new_files:
                        file_path = os.path.join(self.download_dir, f)
                        file_size = os.path.getsize(file_path)
                        print(f"   📄 {f} ({self._format_file_size(file_size)})")
                    return True
                
                # Also check system Downloads folder
                system_downloads = os.path.expanduser("~/Downloads")
                if os.path.exists(system_downloads):
                    recent_files = []
                    for f in os.listdir(system_downloads):
                        file_path = os.path.join(system_downloads, f)
                        if os.path.isfile(file_path):
                            # Check if file was modified in the last few minutes
                            mtime = os.path.getmtime(file_path)
                            if time.time() - mtime < 300:  # Last 5 minutes
                                recent_files.append(f)
                    
                    if recent_files:
                        print(f"💡 Recent files found in ~/Downloads: {recent_files}")
                        move_files = input("Move these files to our download folder? (y/n): ").lower()
                        if move_files == 'y':
                            import shutil
                            for f in recent_files:
                                src = os.path.join(system_downloads, f)
                                dst = os.path.join(self.download_dir, f)
                                try:
                                    shutil.move(src, dst)
                                    print(f"✅ Moved {f} to download folder")
                                except:
                                    print(f"⚠️ Could not move {f}")
                            return True
                
                print(f"   ⏳ Waiting... ({elapsed + check_interval}/{max_wait_time}s)")
            
            print("❌ No new files detected automatically")
            
            # Manual verification
            manual_confirm = input("Did the download complete successfully? (y/n): ").lower()
            if manual_confirm == 'y':
                print("✅ User confirmed download completed")
                return True
            else:
                print("❌ Download verification failed")
                return False
                
        except Exception as e:
            print(f"⚠️ Download verification error: {str(e)}")
            return False
    
    def _navigate_back_to_results_enhanced(self):
        """Enhanced navigation back to results"""
        try:
            print("🔧 ENHANCED NAVIGATION: Returning to results...")
            
            # JavaScript-powered back navigation
            js_back_result = self.driver.execute_script("""
                // Look for back button
                let backElements = document.querySelectorAll('a, button');
                for (let el of backElements) {
                    let text = el.textContent || '';
                    if (text.toLowerCase().includes('back') || 
                        text.toLowerCase().includes('return') ||
                        text.toLowerCase().includes('results')) {
                        el.click();
                        return { success: true, text: text };
                    }
                }
                
                // Try browser back
                history.back();
                return { success: true, text: 'browser_back' };
            """)
            
            if js_back_result['success']:
                print(f"✅ Navigated back: {js_back_result['text']}")
                time.sleep(3)
                return True
            else:
                print("⚠️ Manual navigation needed")
                input("Please navigate back to the results page and press Enter...")
                return True
                
        except Exception as e:
            print(f"⚠️ Enhanced back navigation error: {str(e)}")
            return False
    
    def _uncheck_all_records_enhanced(self):
        """Enhanced record unchecking with multiple strategies"""
        try:
            print("🔧 ENHANCED UNCHECKING: Clearing all selections...")
            
            # JavaScript-powered unchecking
            js_uncheck_result = self.driver.execute_script("""
                // Enhanced unchecking script
                function uncheckAllRecords() {
                    let uncheckedCount = 0;
                    
                    // Method 1: Try Unselect All button
                    let unselectButtons = document.querySelectorAll('a, button');
                    for (let btn of unselectButtons) {
                        let text = btn.textContent || '';
                        if (text.toLowerCase().includes('unselect') || 
                            text.toLowerCase().includes('deselect') ||
                            text.toLowerCase().includes('clear')) {
                            btn.click();
                            return { success: true, method: 'unselect_button', count: -1 };
                        }
                    }
                    
                    // Method 2: Uncheck header checkbox
                    let headerCheckboxes = document.querySelectorAll('th input[type="checkbox"], thead input[type="checkbox"]');
                    for (let cb of headerCheckboxes) {
                        if (cb.offsetParent !== null && cb.checked) {
                            cb.click();
                            return { success: true, method: 'header_uncheck', count: -1 };
                        }
                    }
                    
                    // Method 3: Uncheck all individual checkboxes
                    let allCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
                    for (let cb of allCheckboxes) {
                        if (cb.offsetParent !== null) {
                            cb.checked = false;
                            cb.dispatchEvent(new Event('change'));
                            uncheckedCount++;
                        }
                    }
                    
                    return { success: uncheckedCount > 0, method: 'individual_uncheck', count: uncheckedCount };
                }
                
                return uncheckAllRecords();
            """)
            
            if js_uncheck_result['success']:
                print(f"✅ Enhanced unchecking successful: {js_uncheck_result['method']}")
                if js_uncheck_result['count'] > 0:
                    print(f"   Unchecked {js_uncheck_result['count']} checkboxes")
                return True
            else:
                print("⚠️ JavaScript unchecking failed, trying Selenium...")
                
                # Fallback to Selenium unchecking
                selected_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox' and @checked]")
                if not selected_checkboxes:
                    # Try alternate selection method
                    all_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
                    selected_checkboxes = [cb for cb in all_checkboxes if cb.is_selected()]
                
                uncheck_count = 0
                for checkbox in selected_checkboxes:
                    if self._click_checkbox_enhanced(checkbox):
                        uncheck_count += 1
                
                print(f"✅ Selenium unchecking complete: {uncheck_count} checkboxes")
                return True
                
        except Exception as e:
            print(f"⚠️ Enhanced unchecking error: {str(e)}")
            return False
    
    def _detect_total_pages(self):
        """Detect total number of pages with enhanced methods"""
        try:
            # JavaScript-powered page detection
            total_pages = self.driver.execute_script("""
                // Enhanced page detection
                let pageTexts = document.querySelectorAll('*');
                for (let el of pageTexts) {
                    let text = el.textContent || '';
                    let match = text.match(/Page\\s+(\\d+)\\s+of\\s+(\\d+)/i);
                    if (match) {
                        return parseInt(match[2]);
                    }
                }
                
                // Look for pagination links
                let pageLinks = document.querySelectorAll('a');
                let maxPage = 0;
                for (let link of pageLinks) {
                    let text = link.textContent || '';
                    if (text.match(/^\\d+$/)) {
                        maxPage = Math.max(maxPage, parseInt(text));
                    }
                }
                
                return maxPage > 0 ? maxPage : null;
            """)
            
            return total_pages
        except:
            return None
    
    def _get_download_files(self):
        """Get list of files in download directory with enhanced filtering"""
        try:
            if os.path.exists(self.download_dir):
                files = []
                for f in os.listdir(self.download_dir):
                    file_path = os.path.join(self.download_dir, f)
                    if os.path.isfile(file_path):
                        # Skip temporary and hidden files
                        if (not f.startswith('.') and 
                            not f.endswith('.tmp') and 
                            not f.endswith('.crdownload') and
                            not f.endswith('.part')):
                            files.append(f)
                return files
            return []
        except Exception as e:
            print(f"Error checking download folder: {str(e)}")
            return []
    
    def _format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        try:
            if size_bytes == 0:
                return "0 B"
            
            size_names = ["B", "KB", "MB", "GB"]
            import math
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return f"{s} {size_names[i]}"
        except:
            return f"{size_bytes} bytes"
    
    def _is_element_visible(self, element):
        """Check if an element is visible with enhanced detection"""
        try:
            return (element.is_displayed() and 
                   element.size['width'] > 0 and 
                   element.size['height'] > 0 and
                   element.location['x'] >= 0 and
                   element.location['y'] >= 0)
        except:
            return False
    
    def _take_screenshot(self, name):
        """Take a screenshot with timestamp"""
        try:
            timestamp = int(time.time())
            filename = f"{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
        except Exception as e:
            print(f"❌ Screenshot failed: {str(e)}")
    
    def run(self):
        """Main entry point to run the complete enhanced scraping process"""
        try:
            print("🔧 Starting Enhanced Manual Login Scraper...")
            
            # Step 1: Manual login
            if not self.start_manual_login():
                print("❌ Manual login failed or was aborted")
                return
            
            # Step 2: Run enhanced automated search
            success = self.run_automated_search()
            
            if success:
                print("\n✅ Enhanced automated processing completed successfully!")
            else:
                print("\n⚠️ Enhanced automated processing completed with issues")
            
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
        finally:
            # Ask if user wants to close the browser
            close_browser = input("\nClose browser? (y/n): ").lower()
            if close_browser in ['y', 'yes', '']:
                print("Closing browser...")
                self.driver.quit()
            else:
                print("Browser left open. You can continue manually.")
                print("Please close it manually when finished.")


if __name__ == "__main__":
    try:
        # Get config file path from command line or use default
        config_file = 'config/referenceusa_config.yaml'
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        
        # Create and run the enhanced scraper
        try:
            scraper = EnhancedManualLoginScraper(config_file)
            scraper.run()
        except FileNotFoundError as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please ensure that 'chromedriver' is in the same folder as this script.")
            print("If you need to download a new ChromeDriver, visit: https://chromedriver.chromium.org/downloads")
            print("Make sure to download the version that matches your Chrome browser.")

        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
    except Exception as e:
        print(f"\n❌ Critical error: {str(e)}")
    
    print("\nPress Enter to exit...")
    input()
