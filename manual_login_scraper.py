#!/usr/bin/env python3
"""
Manual Login Data Scraper - With Automated Record Selection
This script handles manual login but then AUTOMATES the record selection and downloading.
"""
import os
import sys
import time
import yaml
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class ManualLoginScraper:
    def __init__(self, config_file='config/referenceusa_config.yaml'):
        print("\n=== Manual Login Data Scraper - Automated Record Selection ===")
        
        # Load configuration
        try:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_file}' not found!")
            print("Looking for alternative config files...")
            
            # Try to find an alternative config file
            alt_config_files = [
                'config/referenceusa_config.yaml',
                'referenceusa_config.yaml',
                'config.yaml'
            ]
            
            for alt_file in alt_config_files:
                if os.path.exists(alt_file):
                    print(f"Found alternative config file: {alt_file}")
                    with open(alt_file, 'r') as f:
                        self.config = yaml.safe_load(f)
                    break
            else:
                print("No configuration files found. Using default configuration.")
                self.config = {
                    'download_dir': os.path.join(os.getcwd(), "downloads"),
                    'auth_url': "https://www.referenceusa.com",
                    'search_parameters': {},
                    'pages_per_batch': 10,
                    'pages_to_download': 'all',
                    'state_file': 'reference_usa_state.json'
                }
        
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
    
    def _setup_browser(self):
        """Configure and initialize the Chrome browser"""
        print("Configuring Chrome browser...")
        
        # Configure browser options
        options = webdriver.ChromeOptions()
        
        # Add options for downloads
        os.makedirs(self.download_dir, exist_ok=True)
        options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.notifications": 2
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
        chromedriver_path = "./chromedriver"
        if not os.path.exists(chromedriver_path):
            print(f"Warning: ChromeDriver not found at {chromedriver_path}")
            print("Searching for ChromeDriver in current directory...")
            if os.path.exists("chromedriver"):
                chromedriver_path = "./chromedriver"
            else:
                print("❌ Error: ChromeDriver not found. Please ensure chromedriver is in the same folder.")
                raise FileNotFoundError("ChromeDriver not found")
        
        print(f"Using ChromeDriver at: {chromedriver_path}")
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        
        # Hide webdriver attribute
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
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
            ready_input = input("\n⏸️ Type 'Ready' when search results are displayed and you're ready for AUTOMATED downloading: ").strip().lower()
            if ready_input == 'ready':
                break
            else:
                print("❌ Please navigate to search results and type 'Ready' to continue")
        
        # Take screenshot of the search results page
        self._take_screenshot("search_results_displayed")
        
        # Check if we're on a results page
        current_url = self.driver.current_url
        print(f"\nCurrent URL: {current_url}")
        
        return True
    
    def initialize_managers(self):
        """Initialize components - keeping for compatibility"""
        print("\n=== Ready for Automated Processing ===")
    
    def run_automated_search(self):
        """Run the automated search and download process"""
        try:
            print("\n=== Starting AUTOMATED Download Process ===")
            print("The automation will now handle record selection and downloading.")
            
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
            
            print(f"\n🤖 AUTOMATION STARTING:")
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
                
                print(f"\n🤖 AUTOMATED BATCH: Pages {current_batch_start} to {current_batch_end} ({current_batch_size} pages)")
                
                # Process batch automatically
                batch_result = self._process_batch_automated(current_batch_start, current_batch_end)
                
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
            
            print(f"\n✅ Automated download process complete!")
            if current_batch_start > end_batch:
                print("All requested pages have been processed.")
            else:
                print(f"Processed pages {start_batch} to {current_batch_start - 1}.")
                
            return True
                
        except Exception as e:
            print(f"Error during automated processing: {str(e)}")
            return False
    
    def _process_batch_automated(self, start_page, end_page):
        """Automatically process a batch of pages"""
        try:
            print(f"\n🤖 AUTOMATING: Processing pages {start_page} through {end_page}")
            
            # Track processed pages
            processed_pages = []
            
            # Step 1: Navigate through pages and select all records
            current_page = start_page
            while current_page <= end_page:
                print(f"\n🤖 AUTO-PROCESSING Page {current_page}")
                
                # Navigate to page if needed
                if current_page != start_page:
                    if not self._navigate_to_page_auto(current_page):
                        print(f"❌ Failed to navigate to page {current_page}")
                        break
                    time.sleep(2)
                
                # Take screenshot before selection
                self._take_screenshot(f"before_page_{current_page}_selection")
                
                # Automatically select all records on this page
                if self._select_all_records_auto():
                    print(f"✅ Selected records on page {current_page}")
                    processed_pages.append(current_page)
                else:
                    print(f"⚠️ Had trouble selecting records on page {current_page}, but continuing...")
                    processed_pages.append(current_page)
                
                # Take screenshot after selection
                self._take_screenshot(f"after_page_{current_page}_selection")
                
                current_page += 1
            
            # Step 2: Download the selected records
            print(f"\n🤖 AUTO-DOWNLOADING: Selected records from pages {start_page}-{end_page}")
            
            # Take screenshot before download
            self._take_screenshot("before_automated_download")
            
            if self._download_records_auto(start_page, end_page):
                print(f"✅ Successfully downloaded pages {start_page}-{end_page}")
            else:
                print(f"⚠️ Download may have had issues, but continuing...")
            
            # Step 3: Navigate back and uncheck records
            print(f"\n🤖 AUTO-CLEANUP: Unchecking records from downloaded pages")
            
            # Navigate back to results if needed
            self._navigate_back_to_results()
            
            # Uncheck records from each processed page
            for page in processed_pages:
                print(f"🤖 Unchecking records on page {page}...")
                if page != processed_pages[0]:  # Don't navigate to first page twice
                    self._navigate_to_page_auto(page)
                    time.sleep(1)
                
                self._uncheck_all_records_auto()
                self._take_screenshot(f"after_uncheck_page_{page}")
            
            print(f"✅ Completed automated processing of pages {start_page} through {end_page}")
            return True
            
        except Exception as e:
            print(f"❌ Error in automated batch processing: {str(e)}")
            print("Continuing with manual fallback...")
            return True  # Continue even if there are errors
    
    def _navigate_to_page_auto(self, page_number):
        """Automatically navigate to a specific page"""
        try:
            print(f"🤖 AUTO-NAVIGATE: Going to page {page_number}")
            
            # Debug: Show all input fields on the page
            print("🤖 DEBUG: Scanning for all input fields...")
            all_inputs = self.driver.find_elements(By.XPATH, "//input")
            for i, inp in enumerate(all_inputs):
                if self._is_element_visible(inp):
                    inp_type = inp.get_attribute('type') or 'text'
                    inp_id = inp.get_attribute('id') or 'no-id'
                    inp_name = inp.get_attribute('name') or 'no-name'
                    inp_class = inp.get_attribute('class') or 'no-class'
                    inp_placeholder = inp.get_attribute('placeholder') or 'no-placeholder'
                    print(f"   Input {i}: type={inp_type}, id={inp_id}, name={inp_name}, class={inp_class}, placeholder={inp_placeholder}")
            
            # Method 1: Look for page input field with multiple strategies
            page_input_xpaths = [
                "//input[@type='text'][ancestor::*[contains(text(), 'Page')]]",
                "//input[@type='text'][following-sibling::*[contains(text(), 'of')] or preceding-sibling::*[contains(text(), 'of')]]",
                "//span[contains(text(), 'Page')]/following::input[@type='text'][1]",
                "//span[contains(text(), 'Page')]/preceding::input[@type='text'][1]", 
                "//div[contains(text(), 'Page')]/descendant::input[@type='text']",
                "//input[@type='text'][contains(@name, 'page')]",
                "//input[@type='text'][contains(@id, 'page')]",
                "//input[@type='text' and (@size<10 or @maxlength<10)]",
                "//input[@type='text'][contains(@class, 'page')]",
                "//input[@type='number']",
                "//input[contains(@placeholder, 'page')]",
                "//input[@type='text'][ancestor::*[contains(@class, 'pag')]]",
                "//input[@type='text'][ancestor::*[contains(@id, 'pag')]]",
                "//input[@type='text'][ancestor::nav]",
                "//nav//input[@type='text']"
            ]
            
            for xpath in page_input_xpaths:
                try:
                    page_inputs = self.driver.find_elements(By.XPATH, xpath)
                    for input_field in page_inputs:
                        if self._is_element_visible(input_field):
                            print(f"🤖 Found page input field: {xpath}")
                            
                            # Clear and enter page number
                            input_field.clear()
                            time.sleep(0.5)
                            input_field.send_keys(str(page_number))
                            time.sleep(0.5)
                            input_field.send_keys(Keys.ENTER)
                            time.sleep(3)  # Wait longer for page to load
                            
                            print(f"✅ Navigated to page {page_number} via input field")
                            return True
                except Exception as e:
                    continue
            
            # Method 2: Try clicking page number link
            page_links = self.driver.find_elements(By.XPATH, f"//a[text()='{page_number}' or @aria-label='Page {page_number}']")
            for link in page_links:
                if self._is_element_visible(link):
                    link.click()
                    time.sleep(3)
                    print(f"✅ Navigated to page {page_number} via link")
                    return True
            
            # If standard methods fail, try a more general approach
            print("🤖 Trying general pagination detection...")
            
            # Look for any text containing "Page X of Y" pattern
            page_pattern_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Page') and contains(text(), 'of')]")
            
            for element in page_pattern_elements:
                print(f"🤖 Found pagination text: {element.text}")
                
                # Look for input fields near this element
                nearby_inputs = []
                
                # Check parent and siblings
                try:
                    parent = element.find_element(By.XPATH, "./parent::*")
                    nearby_inputs.extend(parent.find_elements(By.XPATH, ".//input[@type='text' or @type='number']"))
                except:
                    pass
                
                # Check the element itself
                try:
                    nearby_inputs.extend(element.find_elements(By.XPATH, ".//input[@type='text' or @type='number']"))
                except:
                    pass
                
                # Try each nearby input
                for inp in nearby_inputs:
                    if self._is_element_visible(inp):
                        try:
                            print(f"🤖 Trying input near pagination text...")
                            inp.clear()
                            time.sleep(0.5)
                            inp.send_keys(str(page_number))
                            time.sleep(0.5)
                            inp.send_keys(Keys.ENTER)
                            time.sleep(3)
                            print(f"✅ Successfully navigated to page {page_number} via nearby input")
                            return True
                        except Exception as e:
                            print(f"❌ Failed with nearby input: {str(e)}")
                            continue
            
            # Method 3: Use Next/Previous buttons as fallback
            print("🤖 Trying Next/Previous button navigation...")
            if self._navigate_using_next_prev(page_number):
                return True
            
            # Method 4: Manual fallback with guidance
            print(f"⚠️ Could not automatically navigate to page {page_number}")
            print(f"Looking at your interface, I can see 'Page 2 of 61' - please help:")
            print(f"1. Click on the number '2' (or the input field showing the current page)")
            print(f"2. Clear it and type '{page_number}'")
            print(f"3. Press Enter")
            input(f"Press Enter here when you've navigated to page {page_number}...")
            return True
            
        except Exception as e:
            print(f"⚠️ Auto-navigation failed: {str(e)}")
            return False
    
    def _navigate_using_next_prev(self, target_page):
        """Navigate using Next/Previous buttons"""
        try:
            # Try to determine current page
            current_page = 1
            page_indicators = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'current')] | //input[@type='text' and @value]")
            
            for indicator in page_indicators:
                try:
                    if indicator.tag_name == 'input':
                        value = indicator.get_attribute('value')
                        if value and value.isdigit():
                            current_page = int(value)
                            break
                    else:
                        text = indicator.text.strip()
                        if text and text.isdigit():
                            current_page = int(text)
                            break
                except:
                    pass
            
            print(f"🤖 Current page appears to be {current_page}, need page {target_page}")
            
            # Navigate using Next/Previous
            if current_page < target_page:
                clicks_needed = target_page - current_page
                for i in range(clicks_needed):
                    next_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')] | //button[contains(@class, 'next')]")
                    for button in next_buttons:
                        if self._is_element_visible(button):
                            button.click()
                            time.sleep(1)
                            break
            elif current_page > target_page:
                clicks_needed = current_page - target_page
                for i in range(clicks_needed):
                    prev_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Prev')] | //button[contains(@class, 'prev')]")
                    for button in prev_buttons:
                        if self._is_element_visible(button):
                            button.click()
                            time.sleep(1)
                            break
            
            return True
            
        except Exception as e:
            print(f"⚠️ Next/Prev navigation failed: {str(e)}")
            return False
    
    def _select_all_records_auto(self):
        """Automatically select all records on current page - OPTIMIZED"""
        try:
            print("🤖 AUTO-SELECT: Finding and selecting all records...")
            
            # First, try to find a "Select All" checkbox in the table header
            print("🤖 Looking for Select All checkbox...")
            
            # Look for header checkbox (most efficient) - specifically the one next to "Company Name"
            header_checkbox_xpaths = [
                "//th[contains(text(), 'Company Name')]//input[@type='checkbox']",
                "//th//span[contains(text(), 'Company Name')]//input[@type='checkbox']",
                "//th[contains(text(), 'Company Name')]/preceding-sibling::th//input[@type='checkbox']",
                "//th[contains(text(), 'Company Name')]/following-sibling::th//input[@type='checkbox']",
                "//th//input[@type='checkbox'][1]",
                "//thead//input[@type='checkbox']",
                "//table//tr[1]//input[@type='checkbox']",
                "//input[@type='checkbox'][1]"
            ]
            
            for xpath in header_checkbox_xpaths:
                try:
                    checkboxes = self.driver.find_elements(By.XPATH, xpath)
                    for checkbox in checkboxes:
                        if self._is_element_visible(checkbox):
                            print(f"🤖 Trying header checkbox: {xpath}")
                            
                            # Try to click it
                            if not checkbox.is_selected():
                                self._click_checkbox_fast(checkbox)
                                time.sleep(1)  # Give it time to propagate
                                
                                # Check if other checkboxes got selected
                                all_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
                                selected_count = len([cb for cb in all_checkboxes if cb.is_selected()])
                                
                                if selected_count > 1:  # More than just the header
                                    print(f"✅ Select All worked! {selected_count} checkboxes selected")
                                    return True
                except Exception as e:
                    continue
            
            # If Select All didn't work, select individual checkboxes efficiently
            print("🤖 Select All not found, selecting individual checkboxes...")
            
            # Get all visible checkboxes, but exclude the first one (likely header)
            all_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            data_checkboxes = []
            
            for i, checkbox in enumerate(all_checkboxes):
                if self._is_element_visible(checkbox):
                    # Skip the first checkbox if it seems to be a header
                    if i == 0:
                        # Check if this is in a header context
                        try:
                            parent_tag = checkbox.find_element(By.XPATH, "./ancestor::th | ./ancestor::thead")
                            continue  # Skip header checkboxes
                        except:
                            pass  # Not in header, include it
                    
                    data_checkboxes.append(checkbox)
            
            if not data_checkboxes:
                print("⚠️ No data checkboxes found")
                return False
            
            print(f"🤖 Selecting {len(data_checkboxes)} individual checkboxes...")
            
            # Select checkboxes in batches for better performance
            success_count = 0
            batch_size = 5
            
            for i in range(0, len(data_checkboxes), batch_size):
                batch = data_checkboxes[i:i + batch_size]
                
                for checkbox in batch:
                    if not checkbox.is_selected():
                        if self._click_checkbox_fast(checkbox):
                            success_count += 1
                
                # Brief pause between batches
                if i + batch_size < len(data_checkboxes):
                    time.sleep(0.2)
                
                # Show progress
                processed = min(i + batch_size, len(data_checkboxes))
                print(f"🤖 Progress: {success_count} of {processed} checkboxes selected")
            
            print(f"✅ Individual selection complete: {success_count} checkboxes selected")
            return success_count > 0
            
        except Exception as e:
            print(f"⚠️ Auto-selection error: {str(e)}")
            return False
    
    def _click_checkbox_fast(self, checkbox):
        """Fast checkbox clicking with fewer attempts"""
        try:
            # Method 1: Direct click (fastest)
            try:
                checkbox.click()
                return True
            except:
                pass
            
            # Method 2: JavaScript click (reliable backup)
            try:
                self.driver.execute_script("arguments[0].click();", checkbox)
                return True
            except:
                pass
            
            # Method 3: Set property directly (last resort)
            try:
                self.driver.execute_script("arguments[0].checked = true; arguments[0].dispatchEvent(new Event('change'));", checkbox)
                return True
            except:
                pass
            
            return False
        except:
            return False
    
    def _download_records_auto(self, start_page, end_page):
        """Automatically download the selected records"""
        try:
            print("🤖 AUTO-DOWNLOAD: Starting download process...")
            
            # Step 1: Find and click Download button
            download_buttons = [
                "//a[text()='Download']",
                "//button[text()='Download']",
                "//a[contains(@class, 'download')]",
                "//button[contains(@class, 'download')]",
                "//input[@value='Download']"
            ]
            
            download_clicked = False
            for xpath in download_buttons:
                elements = self.driver.find_elements(By.XPATH, xpath)
                for element in elements:
                    if self._is_element_visible(element):
                        try:
                            element.click()
                            print("✅ Clicked Download button")
                            download_clicked = True
                            break
                        except:
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                                print("✅ Clicked Download button via JavaScript")
                                download_clicked = True
                                break
                            except:
                                continue
                if download_clicked:
                    break
            
            if not download_clicked:
                print("⚠️ Could not find Download button automatically")
                input("Please click the Download button manually and press Enter...")
            
            # Wait for download dialog
            time.sleep(3)
            self._take_screenshot("download_dialog_auto")
            
            # Step 2: CSV format is already selected by default (Comma Delimited)
            print("🤖 AUTO-SELECT: CSV format (Comma Delimited) is already selected")
            
            # Step 3: Select Detailed data level (NOT Summary)
            print("🤖 AUTO-SELECT: Choosing Detailed data level (not Summary)...")
            detail_selected = self._select_format_auto("detailed")
            
            if not detail_selected:
                print("⚠️ Could not select Detailed automatically")
                print("Please select 'Detailed' (not Summary) manually")
                input("Press Enter when you've selected Detailed...")
            
            # Step 4: Click the "DOWNLOAD RECORDS" button
            print("🤖 AUTO-DOWNLOAD: Clicking Download Records...")
            download_records_buttons = [
                "//button[contains(text(), 'DOWNLOAD RECORDS')]",
                "//button[contains(text(), 'Download Records')]",
                "//input[@value='Download Records']",
                "//a[contains(text(), 'Download Records')]"
            ]
            
            records_clicked = False
            for xpath in download_records_buttons:
                elements = self.driver.find_elements(By.XPATH, xpath)
                for element in elements:
                    if self._is_element_visible(element):
                        try:
                            element.click()
                            print("✅ Clicked Download Records button")
                            records_clicked = True
                            break
                        except:
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                                print("✅ Clicked Download Records via JavaScript")
                                records_clicked = True
                                break
                            except:
                                continue
                if records_clicked:
                    break
            
            if not records_clicked:
                print("⚠️ Could not find Download Records button")
                input("Please click 'Download Records' manually and press Enter...")
            
            # Wait for download to complete and provide file saving instructions
            print("🤖 Download initiated! Please save the file:")
            print("1. ✅ Save file in 'Output' folder")
            print("2. ✅ Use naming format: Start#_End#_SearchName_Timestamp")
            print(f"   Example: {start_page}_{end_page}_Alabama_Businesses_{int(time.time())}")
            
            # Check downloads folder for new files
            print("\n🔍 Monitoring download folder for new files...")
            initial_files = self._get_download_files()
            print(f"📂 Files in download folder before: {len(initial_files)}")
            
            input("Press Enter when you've saved the file...")
            
            # Verify download completed
            print("\n🔍 Checking if download completed...")
            final_files = self._get_download_files()
            new_files = [f for f in final_files if f not in initial_files]
            
            if new_files:
                print(f"✅ SUCCESS! {len(new_files)} new file(s) downloaded:")
                for file in new_files:
                    file_size = os.path.getsize(os.path.join(self.download_dir, file))
                    print(f"   📄 {file} ({self._format_file_size(file_size)})")
                return True
            else:
                print("⚠️  No new files detected in download folder")
                print("   This might mean:")
                print("   - File was saved to a different location")
                print("   - Download is still in progress")
                print("   - Download failed")
                
                manual_confirm = input("Did the download complete successfully? (y/n): ").lower()
                if manual_confirm in ['y', 'yes']:
                    print("✅ User confirmed download completed")
                    return True
                else:
                    print("❌ Download appears to have failed")
                    return False
            
            return True
            
        except Exception as e:
            print(f"⚠️ Auto-download error: {str(e)}")
            return False
    
    def _select_format_auto(self, format_type):
        """Automatically select format (csv or detailed)"""
        try:
            if format_type.lower() == "csv":
                # CSV is already selected by default (Comma Delimited)
                print("✅ CSV format already selected (Comma Delimited)")
                return True
            else:  # detailed
                # Look for Detailed radio button
                detailed_selectors = [
                    "//input[@type='radio'][following-sibling::text()[contains(., 'Detailed')]]",
                    "//input[@type='radio'][following-sibling::*[contains(text(), 'Detailed')]]",
                    "//label[contains(text(), 'Detailed')]/input[@type='radio']",
                    "//label[contains(text(), 'Detailed')]",
                    "//input[@type='radio'][@value='detailed']"
                ]
                
                for xpath in detailed_selectors:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    for element in elements:
                        if self._is_element_visible(element):
                            try:
                                # If it's a label, look for the radio button inside or nearby
                                if element.tag_name.lower() == 'label':
                                    # Try to find radio button inside the label
                                    radio_inputs = element.find_elements(By.XPATH, ".//input[@type='radio']")
                                    if radio_inputs:
                                        radio_inputs[0].click()
                                    else:
                                        # Click the label itself
                                        element.click()
                                else:
                                    element.click()
                                
                                print(f"✅ Selected {format_type} format")
                                return True
                            except:
                                try:
                                    self.driver.execute_script("arguments[0].click();", element)
                                    print(f"✅ Selected {format_type} format via JavaScript")
                                    return True
                                except:
                                    continue
                
                print(f"⚠️ Could not auto-select {format_type} format")
                return False
                
        except Exception as e:
            print(f"⚠️ Format selection error: {str(e)}")
            return False
    
    def _navigate_back_to_results(self):
        """Navigate back to results page after download"""
        try:
            print("🤖 AUTO-NAVIGATE: Returning to results...")
            
            # Look for Back button on download page
            back_buttons = [
                "//a[contains(text(), 'Back')]",
                "//button[contains(text(), 'Back')]",
                "//a[contains(text(), 'Results')]", 
                "//a[contains(text(), 'Return')]",
                "//button[contains(@class, 'back')]"
            ]
            
            for xpath in back_buttons:
                elements = self.driver.find_elements(By.XPATH, xpath)
                for element in elements:
                    if self._is_element_visible(element):
                        try:
                            element.click()
                            time.sleep(3)  # Wait for page to load
                            print("✅ Clicked Back button to return to results")
                            return True
                        except:
                            continue
            
            # If no Back button found, ask for manual help
            print("⚠️ Could not find Back button automatically")
            print("Please click the 'Back' button on the download page to return to results")
            input("Press Enter when you've returned to the results page...")
            return True
            
        except Exception as e:
            print(f"⚠️ Navigation back error: {str(e)}")
            return False
    
    def _uncheck_all_records_auto(self):
        """Automatically uncheck all records on current page"""
        try:
            print("🤖 AUTO-UNCHECK: Unchecking all records...")
            
            # Look for Unselect All button first
            unselect_buttons = [
                "//a[contains(text(), 'Unselect All')]",
                "//button[contains(text(), 'Unselect All')]",
                "//a[contains(text(), 'Deselect All')]"
            ]
            
            for xpath in unselect_buttons:
                elements = self.driver.find_elements(By.XPATH, xpath)
                for element in elements:
                    if self._is_element_visible(element):
                        try:
                            element.click()
                            time.sleep(1)
                            print("✅ Clicked Unselect All")
                            return True
                        except:
                            continue
            
            # If no Unselect All, uncheck individual checkboxes
            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            selected_checkboxes = [cb for cb in checkboxes if cb.is_selected()]
            
            if selected_checkboxes:
                print(f"🤖 Unchecking {len(selected_checkboxes)} individual checkboxes...")
                for checkbox in selected_checkboxes:
                    try:
                        checkbox.click()
                    except:
                        try:
                            self.driver.execute_script("arguments[0].click();", checkbox)
                        except:
                            pass
                
                print("✅ Unchecked individual checkboxes")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Auto-uncheck error: {str(e)}")
            return False
    
    def _detect_total_pages(self):
        """Try to detect the total number of pages"""
        try:
            # Look for pagination info
            page_info_elements = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'Page') and contains(text(), 'of')]")
            if page_info_elements:
                page_info = page_info_elements[0].text
                if "of" in page_info:
                    total_pages = int(page_info.split("of")[1].strip())
                    return total_pages
        except:
            pass
        
        return None
    
    def _get_download_files(self):
        """Get list of files in download directory"""
        try:
            if os.path.exists(self.download_dir):
                files = []
                for f in os.listdir(self.download_dir):
                    if os.path.isfile(os.path.join(self.download_dir, f)):
                        # Skip temporary files
                        if not f.startswith('.') and not f.endswith('.tmp') and not f.endswith('.crdownload'):
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
        """Check if an element is visible"""
        try:
            return element.is_displayed() and element.size['width'] > 0 and element.size['height'] > 0
        except:
            return False
    
    def run(self):
        """Main entry point to run the complete scraping process"""
        try:
            # Step 1: Manual login
            if not self.start_manual_login():
                print("❌ Manual login failed or was aborted")
                return
            
            # Step 2: Initialize managers
            self.initialize_managers()
            
            # Step 3: Run automated search
            success = self.run_automated_search()
            
            if success:
                print("\n✅ Automated processing completed successfully!")
            else:
                print("\n⚠️ Automated processing completed with issues")
            
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
    
    def _take_screenshot(self, name):
        """Take a screenshot with timestamp"""
        try:
            timestamp = int(time.time())
            filename = f"{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
        except Exception as e:
            print(f"❌ Screenshot failed: {str(e)}")


if __name__ == "__main__":
    try:
        # Get config file path from command line or use default
        config_file = 'config/referenceusa_config.yaml'
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        
        # Create and run the scraper
        try:
            scraper = ManualLoginScraper(config_file)
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
