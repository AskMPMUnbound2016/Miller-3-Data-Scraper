#!/usr/bin/env python3
"""
SEMI-AUTOMATED DATA SCRAPER - Miller 3 Data Scraper
===================================================
Manual login + Automated checkbox selection, pagination, and downloading
Enhanced with batch methods from enhanced_batch_methods
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

# Enhanced batch methods removed - using built-in functionality

class SemiAutomatedScraper:
    def __init__(self, config_file='config/referenceusa_config.yaml'):
        print("\n=== SEMI-AUTOMATED DATA SCRAPER ===")
        print("Manual login + Automated selection and downloading")
        
        # Load configuration
        self.config = self._load_config(config_file)
        self.download_dir = self.config.get('download_dir', os.path.join(os.getcwd(), "downloads"))
        self.state_file = "manual_scraper_state.json"
        self.session_state = self._load_session_state()
        
        # Initialize browser
        self._setup_browser()
        
        # Initialize WebDriverWait
        self.wait = WebDriverWait(self.driver, 10)
        
        # Using built-in automation methods
        
        print(f"📂 Download directory: {self.download_dir}")
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
                    'downloads_completed': [],
                    'current_batch': 1
                }
        except Exception as e:
            print(f"⚠️ Error loading session state: {e}")
            return {
                'search_name': '',
                'total_pages': 0,
                'completed_batches': [],
                'last_completed_page': 0,
                'downloads_completed': [],
                'current_batch': 1
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
        """Setup Chrome browser with download preferences and Cloudflare resistance"""
        print("🛡️ Setting up Cloudflare-resistant browser...")
        
        options = webdriver.ChromeOptions()
        
        # Fix for data:, URL issue - set proper startup behavior
        options.add_argument("--homepage=about:blank")
        options.add_argument("--disable-default-apps")
        
        # Create download directory if it doesn't exist
        os.makedirs(self.download_dir, exist_ok=True)
        
        # ENHANCED ANTI-DETECTION FOR CLOUDFLARE
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Configure download settings
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False
        }
        options.add_experimental_option("prefs", prefs)
        
        # Initialize browser
        chromedriver_path = "./chromedriver"
        if not os.path.exists(chromedriver_path):
            print(f"❌ ChromeDriver not found at {chromedriver_path}")
            print("Please ensure chromedriver is in the same folder.")
            sys.exit(1)
        
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        
        # Immediately navigate to blank page to prevent data:, URL issue
        self.driver.get("about:blank")
        
        # ADVANCED JAVASCRIPT ANTI-DETECTION
        print("🔧 Applying JavaScript anti-detection...")
        
        # Hide webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Override automation detection
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)
        
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)
        
        self.driver.execute_script("""
            Object.defineProperty(navigator, 'platform', {
                get: () => 'MacIntel'
            });
        """)
        
        print("✅ Cloudflare-resistant browser configured")
    
    def wait_for_cloudflare_and_load(self, timeout=20):
        """Wait for Cloudflare check and page load"""
        try:
            # Check for Cloudflare challenge
            cf_indicators = ["checking your browser", "just a moment", "ddos protection", "cloudflare"]
            start_time = time.time()
            
            while time.time() - start_time < 10:  # Check for 10 seconds
                page_source = self.driver.page_source.lower()
                cf_detected = any(indicator in page_source for indicator in cf_indicators)
                
                if cf_detected:
                    print("🛡️ Cloudflare challenge detected, waiting...")
                    time.sleep(5)
                else:
                    break
            
            # Wait for document ready
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Additional wait for dynamic content
            time.sleep(random.uniform(2, 4))
            return True
        except:
            return False
    
    def start_manual_login(self):
        """Handle manual login process"""
        print("\n" + "="*60)
        print("STEP 1: MANUAL LOGIN")
        print("="*60)
        
        # Get starting URL
        start_url = self.config.get('auth_url', 'http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Quick/497be73bf9a94fe3aebb7eb4857b584f')
        
        print(f"🌐 Opening: {start_url}")
        self.driver.get(start_url)
        
        print("\n📋 MANUAL LOGIN INSTRUCTIONS:")
        print("1. ✅ Complete OpenAthens authentication if prompted")
        print("2. ✅ You should see the ReferenceUSA U.S. Business Quick Search page")
        print("3. ✅ Set up your search criteria (location, industry, etc.)")
        print("4. ✅ Click 'Search' or 'View Results' button")
        print("5. ✅ Wait for search results to load completely")
        print("6. ✅ You should see a list of business records with pagination")
        
        input("\n⏸️ Press Enter when you can see the search results page...")
        
        # Get search details
        search_name = input("📝 Enter a name for this search (e.g., 'Alabama_Businesses'): ").strip()
        if not search_name:
            search_name = f"Search_{int(time.time())}"
        
        self.session_state['search_name'] = search_name
        print(f"✅ Search named: {search_name}")
        
        return True
    
    def detect_total_pages(self):
        """Try to automatically detect total pages"""
        print("\n🔍 Attempting to detect total pages...")
        
        try:
            # Look for pagination indicators
            page_indicators = [
                "//span[contains(text(), 'Page') and contains(text(), 'of')]",
                "//div[contains(text(), 'Page') and contains(text(), 'of')]",
                "//span[contains(text(), 'Results') and contains(text(), 'of')]",
                "//div[contains(text(), 'Results') and contains(text(), 'of')]"
            ]
            
            for selector in page_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        text = element.text
                        print(f"📊 Found pagination text: {text}")
                        
                        # Try to extract total pages
                        if "of" in text.lower():
                            parts = text.lower().split("of")
                            if len(parts) > 1:
                                # Look for number after "of"
                                import re
                                numbers = re.findall(r'\d+', parts[1])
                                if numbers:
                                    total_pages = int(numbers[0])
                                    print(f"✅ Auto-detected total pages: {total_pages}")
                                    return total_pages
                except:
                    continue
            
            print("⚠️ Could not auto-detect total pages")
            return None
            
        except Exception as e:
            print(f"⚠️ Error detecting pages: {e}")
            return None
    
    def get_total_pages(self):
        """Get total number of pages"""
        print("\n" + "="*60)
        print("STEP 2: DETERMINE TOTAL PAGES")
        print("="*60)
        
        # Try auto-detection first
        auto_detected = self.detect_total_pages()
        
        if auto_detected:
            confirm = input(f"\n📊 Auto-detected {auto_detected} pages. Is this correct? (y/n): ").lower().strip()
            if confirm in ['y', 'yes']:
                self.session_state['total_pages'] = auto_detected
                print(f"✅ Total pages set to: {auto_detected}")
                return True
        
        # Manual input
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
    
    def navigate_to_page(self, page_num):
        """ENHANCED navigation for ReferenceUSA pagination layout"""
        print(f"🔄 Navigating to page {page_num} (ReferenceUSA)...")
        
        # Human-like delay
        time.sleep(random.uniform(2, 4))
        
        try:
            # Wait for page stability
            self.wait_for_cloudflare_and_load()
            
            # STRATEGY 1: ReferenceUSA specific page input + arrow
            print("🎯 Strategy 1: ReferenceUSA page input + navigation...")
            
            # Find page input (showing current page)
            page_input_selectors = [
                "//input[@type='text' and @value and string-length(@value) <= 3]",
                "//input[@type='text'][ancestor::*[contains(text(), 'Page')]]",
                "//input[@type='text']"
            ]
            
            page_input = None
            current_page = None
            
            for selector in page_input_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            value = element.get_attribute('value') or ''
                            if value.isdigit() and int(value) <= 100:
                                page_input = element
                                current_page = int(value)
                                print(f"📍 Found page input: current {current_page}, target {page_num}")
                                break
                    if page_input:
                        break
                except:
                    continue
            
            if not page_input:
                print("⚠️ No page input found")
                return self._try_step_navigation_referenceusa(page_num)
            
            if current_page == page_num:
                print(f"✅ Already on page {page_num}")
                return True
            
            # APPROACH A: For single step forward (most common)
            if page_num == current_page + 1:
                print("🎯 Single step forward - looking for next arrow...")
                
                next_selectors = [
                    # Right arrow images
                    "//img[contains(@src, 'arrow') and contains(@src, 'right')]",
                    "//input[@type='image' and contains(@src, 'arrow') and contains(@src, 'right')]",
                    "//img[contains(@src, 'next')]",
                    
                    # Next buttons near pagination
                    "//a[contains(@title, 'Next') or text()='>' or text()='→']",
                    "//button[contains(@title, 'Next') or text()='>' or text()='→']",
                    
                    # Look for clickable elements near page input
                    "//a[@href and string-length(text()) <= 3]",
                    "//span[@onclick and string-length(text()) <= 3]",
                    
                    # Images that might be navigation arrows
                    "//img[@onclick or @src][contains(@src, 'arrow') or contains(@alt, 'next')]"
                ]
                
                for selector in next_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        for element in elements:
                            if element.is_displayed():
                                print(f"🎯 Found next element: {element.tag_name}")
                                ActionChains(self.driver).move_to_element(element).pause(0.3).click().perform()
                                time.sleep(4)
                                self.wait_for_cloudflare_and_load()
                                print("✅ Clicked next navigation")
                                return True
                    except Exception as e:
                        continue
            
            # APPROACH B: Direct page input + enter
            print(f"⌨️ Trying direct page input for page {page_num}...")
            try:
                # Focus and clear input
                page_input.click()
                time.sleep(0.5)
                page_input.clear()
                time.sleep(0.3)
                page_input.send_keys(str(page_num))
                time.sleep(0.5)
                
                # Try Enter key
                page_input.send_keys(Keys.ENTER)
                time.sleep(4)
                self.wait_for_cloudflare_and_load()
                print("✅ Used Enter key navigation")
                return True
                
            except Exception as e:
                print(f"⚠️ Direct input failed: {e}")
            
            # APPROACH C: JavaScript navigation
            print("🔧 Trying JavaScript navigation...")
            js_result = self.driver.execute_script(f"""
                var pageInputs = document.querySelectorAll('input[type="text"]');
                for(var i = 0; i < pageInputs.length; i++) {{
                    var input = pageInputs[i];
                    if(input.value && input.value.length <= 3 && !isNaN(input.value)) {{
                        input.value = '{page_num}';
                        input.dispatchEvent(new Event('change'));
                        
                        // Try Enter key
                        var enterEvent = new KeyboardEvent('keydown', {{key: 'Enter', bubbles: true}});
                        input.dispatchEvent(enterEvent);
                        
                        return true;
                    }}
                }}
                return false;
            """)
            
            if js_result:
                time.sleep(4)
                self.wait_for_cloudflare_and_load()
                print("✅ JavaScript navigation succeeded")
                return True
            
            print("❌ All navigation methods failed")
            return self._manual_navigation_fallback(page_num)
            
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return self._manual_navigation_fallback(page_num)
    
    def _try_step_navigation_referenceusa(self, target_page):
        """Step navigation specifically for ReferenceUSA"""
        print(f"🔄 Step navigation to page {target_page}...")
        
        current_page = 1  # Assume starting at page 1
        max_steps = abs(target_page - current_page) + 2
        
        for step in range(max_steps):
            if current_page >= target_page:
                break
            
            # Look for next arrow
            next_selectors = [
                "//img[contains(@src, 'arrow') and contains(@src, 'right')]",
                "//a[text()='>' or text()='→' or contains(@title, 'Next')]",
                "//button[text()='>' or text()='→' or contains(@title, 'Next')]",
                "//input[@type='image' and contains(@src, 'right')]"
            ]
            
            clicked = False
            for selector in next_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            ActionChains(self.driver).move_to_element(element).pause(0.3).click().perform()
                            current_page += 1
                            clicked = True
                            print(f"➡️ Step {step + 1}: moved to page {current_page}")
                            break
                    if clicked:
                        break
                except:
                    continue
            
            if not clicked:
                print("❌ Next button not found for step navigation")
                return False
            
            time.sleep(random.uniform(2, 4))
            self.wait_for_cloudflare_and_load()
        
        return current_page >= target_page
    
    def _manual_navigation_fallback(self, page_num):
        """Manual navigation fallback with ReferenceUSA specific guidance"""
        print(f"\n🔧 MANUAL NAVIGATION REQUIRED - REFERENCEUSA")
        print(f"=" * 50)
        print(f"Target page: {page_num}")
        
        print(f"\n📋 REFERENCEUSA NAVIGATION STEPS:")
        print(f"1. 🔍 Look for the page input field (currently shows page number)")
        print(f"2. 🖱️ Click in the page input field")
        print(f"3. ⌨️ Clear it and type: {page_num}")
        print(f"4. 🖱️ Look for a right arrow (→) button next to the input")
        print(f"5. 🖱️ Click the right arrow OR press Enter")
        print(f"6. ⏳ Wait for the page to load")
        
        print(f"\n💡 REFERENCEUSA TIPS:")
        print(f"   • The arrow might be a small image button")
        print(f"   • Look for → or ▶ symbols")
        print(f"   • The navigation is usually right next to the page input")
        print(f"   • Try pressing Enter if no arrow is visible")
        
        input(f"\n⏸️ Press Enter after navigating to page {page_num}...")
        
        # Wait for page load
        self.wait_for_cloudflare_and_load()
        return True
    
    def _detect_current_page(self):
        """Better current page detection"""
        try:
            # Method 1: Page input field value
            input_elements = self.driver.find_elements(By.XPATH, 
                "//input[@type='text' and @value and string-length(@value) <= 3]"
            )
            for element in input_elements:
                if element.is_displayed():
                    value = element.get_attribute('value')
                    if value and value.isdigit():
                        return int(value)
            
            # Method 2: Active page indicator
            active_selectors = [
                "//span[contains(@class, 'current') and text()]",
                "//a[contains(@class, 'current') and text()]",
                "//span[contains(@class, 'active') and text()]",
                "//strong[text() and string-length(text()) <= 3]"
            ]
            
            for selector in active_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    text = element.text.strip()
                    if text.isdigit():
                        return int(text)
            
            # Method 3: Parse "Page X of Y" text
            page_text_elements = self.driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'Page') and contains(text(), 'of')]"
            )
            for element in page_text_elements:
                text = element.text
                import re
                match = re.search(r'Page\s+(\d+)\s+of', text, re.IGNORECASE)
                if match:
                    return int(match.group(1))
            
            # Default to page 1 if cannot detect
            return 1
            
        except:
            return 1
    
    def select_all_records_on_page(self):
        """Automatically select all records on current page with Cloudflare resistance"""
        print("☑️ Selecting all records (Cloudflare-resistant)...")
        
        # Wait for page stability and Cloudflare
        self.wait_for_cloudflare_and_load()
        
        # Add human-like delay
        time.sleep(random.uniform(1, 3))
        
        try:
            # Enhanced checkbox detection with multiple strategies
            checkbox_selectors = [
                "//input[@type='checkbox']",  # Any checkbox
                "//table//input[@type='checkbox']",  # Table checkboxes  
                "//form//input[@type='checkbox']",  # Form checkboxes
                "//tr//input[@type='checkbox']",  # Row checkboxes
                "//th//input[@type='checkbox']",  # Header checkboxes
                "//thead//input[@type='checkbox']",  # Table header checkboxes
                "//tbody//input[@type='checkbox']",  # Table body checkboxes
                "//div[@class='data-table']//input[@type='checkbox']",  # Data table checkboxes
                "//div[contains(@class, 'table')]//input[@type='checkbox']",  # Generic table class
                "//div[contains(@id, 'results')]//input[@type='checkbox']"  # Results area
            ]
            
            total_checkboxes = 0
            all_checkboxes = []
            
            print("🔍 Searching for checkboxes with enhanced detection...")
            
            for i, selector in enumerate(checkbox_selectors, 1):
                try:
                    # Use explicit wait for each selector
                    checkboxes = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_all_elements_located((By.XPATH, selector))
                    )
                    
                    # Filter for visible checkboxes
                    visible_checkboxes = [cb for cb in checkboxes if cb.is_displayed()]
                    
                    if visible_checkboxes:
                        print(f"   ✅ Selector {i}: Found {len(visible_checkboxes)} visible checkboxes")
                        all_checkboxes.extend(visible_checkboxes)
                        total_checkboxes += len(visible_checkboxes)
                    else:
                        print(f"   ⚠️ Selector {i}: No visible checkboxes")
                        
                except TimeoutException:
                    print(f"   ⚠️ Selector {i}: Timeout")
                    continue
                except Exception as e:
                    print(f"   ⚠️ Selector {i}: Error - {e}")
                    continue
            
            print(f"📊 Found {total_checkboxes} total visible checkboxes")
            
            if total_checkboxes == 0:
                print("❌ No checkboxes found - Cloudflare may be blocking elements")
                print("🛡️ Try refreshing the page or waiting longer for elements to load")
                return False
            
            # Remove duplicates while preserving order
            unique_checkboxes = []
            seen = set()
            for cb in all_checkboxes:
                cb_id = id(cb)
                if cb_id not in seen:
                    unique_checkboxes.append(cb)
                    seen.add(cb_id)
            
            print(f"📊 After deduplication: {len(unique_checkboxes)} unique checkboxes")
            
            # Strategy 1: Try header/select-all checkbox first (usually first few)
            print("🎯 Trying header/select-all checkboxes...")
            for i, checkbox in enumerate(unique_checkboxes[:5]):
                try:
                    if not checkbox.is_selected():
                        print(f"   Trying checkbox {i+1}...")
                        
                        # Human-like interaction
                        ActionChains(self.driver).move_to_element(checkbox).pause(random.uniform(0.2, 0.5)).click().perform()
                        time.sleep(random.uniform(1, 2))
                        
                        print(f"✅ Successfully clicked header checkbox {i+1}")
                        return True
                except Exception as e:
                    print(f"   ⚠️ Header checkbox {i+1} failed: {e}")
                    continue
            
            # Strategy 2: Try individual checkboxes
            print("📋 Trying individual checkboxes...")
            selected_count = 0
            max_individual = min(25, len(unique_checkboxes))  # Limit to 25 individual selections
            
            for i, checkbox in enumerate(unique_checkboxes[:max_individual]):
                try:
                    if not checkbox.is_selected():
                        ActionChains(self.driver).move_to_element(checkbox).pause(random.uniform(0.1, 0.2)).click().perform()
                        selected_count += 1
                        time.sleep(random.uniform(0.1, 0.3))
                        
                        if selected_count >= 10:  # Don't select too many individually
                            break
                except Exception as e:
                    continue
            
            if selected_count > 0:
                print(f"✅ Selected {selected_count} individual records")
                return True
            else:
                print("❌ Could not select any records")
                return False
                
        except Exception as e:
            print(f"❌ Error selecting records: {e}")
            return False
    
    def uncheck_all_records_on_page(self):
        """Automatically uncheck all records on current page"""
        print("☐ Unchecking all records on current page...")
        
        try:
            # Method 1: Header checkbox (unselect all)
            header_checkbox_selectors = [
                "//th//input[@type='checkbox']",
                "//thead//input[@type='checkbox']",
                "//table//tr[1]//input[@type='checkbox']"
            ]
            
            for selector in header_checkbox_selectors:
                try:
                    checkboxes = self.driver.find_elements(By.XPATH, selector)
                    for checkbox in checkboxes:
                        if checkbox.is_displayed() and checkbox.is_selected():
                            checkbox.click()
                            time.sleep(random.uniform(0.5, 1))
                            print("✅ Clicked header checkbox (unselect all)")
                            return True
                except:
                    continue
            
            # Method 2: Individual checkboxes
            record_checkboxes = self.driver.find_elements(By.XPATH, "//tr//input[@type='checkbox']")
            
            unchecked_count = 0
            for checkbox in record_checkboxes:
                try:
                    if checkbox.is_displayed() and checkbox.is_selected():
                        checkbox.click()
                        unchecked_count += 1
                        time.sleep(random.uniform(0.1, 0.3))
                except:
                    continue
            
            if unchecked_count > 0:
                print(f"✅ Unchecked {unchecked_count} records")
                return True
            else:
                print("✅ No records were selected")
                return True
                
        except Exception as e:
            print(f"⚠️ Error unchecking records: {e}")
            return False
    
    def find_and_click_download_button(self):
        """Find and click the main Download button"""
        print("🔍 Looking for Download button...")
        
        download_selectors = [
            "//button[text()='Download']",
            "//a[text()='Download']",
            "//button[contains(text(), 'Download')]",
            "//a[contains(text(), 'Download')]",
            "//input[@type='submit' and @value='Download']",
            "//button[contains(@class, 'download')]",
            "//a[contains(@class, 'download')]"
        ]
        
        for selector in download_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        print(f"🎯 Found Download button: {element.text}")
                        element.click()
                        time.sleep(random.uniform(2, 4))
                        print("✅ Clicked Download button")
                        return True
            except Exception as e:
                print(f"⚠️ Error clicking download button: {e}")
                continue
        
        print("❌ Download button not found")
        return False
    
    def configure_download_options(self):
        """Configure download options (CSV, Detailed)"""
        print("⚙️ Configuring download options...")
        
        try:
            # Select CSV format
            csv_selectors = [
                "//input[@type='radio' and following-sibling::*[contains(text(), 'Comma')]]",
                "//input[@type='radio' and following-sibling::*[contains(text(), 'CSV')]]",
                "//label[contains(text(), 'Comma')]//input[@type='radio']"
            ]
            
            csv_selected = False
            for selector in csv_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and not element.is_selected():
                            element.click()
                            time.sleep(1)
                            print("✅ Selected CSV format")
                            csv_selected = True
                            break
                    if csv_selected:
                        break
                except:
                    continue
            
            if not csv_selected:
                print("⚠️ CSV format may already be selected")
            
            # Select Detailed level
            detailed_selectors = [
                "//input[@type='radio' and following-sibling::*[contains(text(), 'Detailed')]]",
                "//label[contains(text(), 'Detailed')]//input[@type='radio']"
            ]
            
            detailed_selected = False
            for selector in detailed_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed() and not element.is_selected():
                            element.click()
                            time.sleep(1)
                            print("✅ Selected Detailed level")
                            detailed_selected = True
                            break
                    if detailed_selected:
                        break
                except:
                    continue
            
            if not detailed_selected:
                print("⚠️ Detailed level selection may have failed")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Error configuring download options: {e}")
            return False
    
    def click_download_records_button(self):
        """Find and click the Download Records button"""
        print("🔍 Looking for Download Records button...")
        
        download_records_selectors = [
            "//button[contains(text(), 'DOWNLOAD RECORDS')]",
            "//button[contains(text(), 'Download Records')]",
            "//input[@type='submit' and contains(@value, 'DOWNLOAD RECORDS')]",
            "//input[@type='submit' and contains(@value, 'Download Records')]",
            "//a[contains(text(), 'DOWNLOAD RECORDS')]",
            "//button[@type='submit']",
            "//input[@type='submit']"
        ]
        
        for selector in download_records_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        print(f"🎯 Found Download Records button: {element.text or element.get_attribute('value')}")
                        element.click()
                        time.sleep(random.uniform(3, 6))
                        print("✅ Clicked Download Records button")
                        return True
            except Exception as e:
                print(f"⚠️ Error clicking download records button: {e}")
                continue
        
        print("❌ Download Records button not found")
        return False
    
    def wait_for_download_completion(self, expected_filename=""):
        """Wait for download to complete"""
        print("⏳ Waiting for download to complete...")
        
        # Get initial file list
        initial_files = []
        if os.path.exists(self.download_dir):
            initial_files = os.listdir(self.download_dir)
        
        # Wait for new file to appear
        max_wait = 30  # seconds
        wait_time = 0
        
        while wait_time < max_wait:
            time.sleep(2)
            wait_time += 2
            
            if os.path.exists(self.download_dir):
                current_files = os.listdir(self.download_dir)
                new_files = [f for f in current_files if f not in initial_files and not f.endswith('.crdownload')]
                
                if new_files:
                    print(f"✅ Download completed: {new_files[0]}")
                    return new_files[0]
        
        print("⚠️ Download timeout - file may still be downloading")
        return None
    
    def navigate_back_to_results(self):
        """Navigate back to search results"""
        print("🔙 Navigating back to results...")
        
        try:
            # Method 1: Back button
            back_buttons = self.driver.find_elements(By.XPATH, 
                "//a[contains(text(), 'Back')] | //button[contains(text(), 'Back')]")
            
            if back_buttons:
                back_buttons[0].click()
                time.sleep(random.uniform(2, 4))
                print("✅ Clicked Back button")
                return True
            
            # Method 2: Browser back
            self.driver.back()
            time.sleep(random.uniform(2, 4))
            print("✅ Used browser back")
            return True
            
        except Exception as e:
            print(f"⚠️ Error navigating back: {e}")
            return False
    
    # ENHANCED METHODS
    def run_method1_manual_batch_enhanced(self):
        """Enhanced Method 1: Manual navigation + auto-continue"""
        print("❌ Enhanced methods have been consolidated into the main automation")
        print("💡 Use the standard Method 1 or Method 2 instead")
        return False
    
    def run_method2_full_automation_enhanced(self):
        """Enhanced Method 2: Full automation + auto-continue"""
        print("❌ Enhanced methods have been consolidated into the main automation")
        print("💡 Use the standard Method 1 or Method 2 instead")
        return False
    
    def show_enhanced_menu(self):
        """Show enhanced menu with new methods"""
        print("\n🎯 ENHANCED SCRAPER METHODS")
        print("=" * 50)
        print("1. 🎯 Method 1 Enhanced: Manual Navigation + Auto-Continue")
        print("2. 🤖 Method 2 Enhanced: Full Automation + Auto-Continue")
        print("3. 📊 Original Automated Process")
        print("4. 📋 View Session Status")
        print("5. 🧹 Clear Session State")
        print("6. ❌ Exit")
        
        while True:
            try:
                choice = input("\n🔢 Choose method (1-6): ").strip()
                
                if choice == '1':
                    return self.run_method1_manual_batch_enhanced()
                elif choice == '2':
                    return self.run_method2_full_automation_enhanced()
                elif choice == '3':
                    return self.run_automated_download_process()
                elif choice == '4':
                    self.show_session_status()
                    continue
                elif choice == '5':
                    self.clear_session_state()
                    continue
                elif choice == '6':
                    print("👋 Exiting...")
                    return False
                else:
                    print("❌ Please choose 1-6")
                    continue
                    
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                return False
    
    def show_session_status(self):
        """Show current session status"""
        print("\n📊 SESSION STATUS")
        print("=" * 30)
        print(f"Search name: {self.session_state.get('search_name', 'None')}")
        print(f"Total pages: {self.session_state.get('total_pages', 0)}")
        print(f"Last completed page: {self.session_state.get('last_completed_page', 0)}")
        print(f"Completed batches: {len(self.session_state.get('completed_batches', []))}")
        print(f"Downloaded files: {len(self.session_state.get('downloads_completed', []))}")
        
        if self.session_state.get('completed_batches'):
            print("\n📄 Recent batches:")
            for batch in self.session_state['completed_batches'][-3:]:
                method = batch.get('method', 'unknown')
                timestamp = batch.get('timestamp', 'unknown')
                batch_num = batch.get('batch_num', 'unknown')
                print(f"   • Batch {batch_num} ({method}) - {timestamp}")
        
        if self.session_state.get('downloads_completed'):
            print(f"\n📁 Downloaded files ({len(self.session_state['downloads_completed'])}):")
            for file in self.session_state['downloads_completed'][-5:]:
                print(f"   • {file}")
    
    def clear_session_state(self):
        """Clear session state"""
        confirm = input("\n⚠️ Clear all session data? This cannot be undone. (y/n): ").lower().strip()
        if confirm in ['y', 'yes']:
            self.session_state = {
                'search_name': '',
                'total_pages': 0,
                'completed_batches': [],
                'last_completed_page': 0,
                'downloads_completed': [],
                'current_batch': 1
            }
            self._save_session_state()
            print("✅ Session state cleared")
        else:
            print("❌ Session state unchanged")
    
    def run_automated_download_process(self):
        """Run the original automated download process"""
        try:
            # Get download range
            start_page, end_page = self.get_download_range()
            
            # Calculate batches (max 10 pages per batch)
            total_pages_to_download = end_page - start_page + 1
            batch_size = 10
            total_batches = (total_pages_to_download + batch_size - 1) // batch_size
            
            print(f"\n📊 AUTOMATED DOWNLOAD PLAN:")
            print(f"   Pages to download: {start_page} to {end_page} ({total_pages_to_download} pages)")
            print(f"   Batch size: {batch_size} pages maximum")
            print(f"   Total batches: {total_batches}")
            print(f"   Download directory: {self.download_dir}")
            
            proceed = input(f"\n🤖 Start automated downloading? (y/n): ").lower().strip()
            if proceed not in ['y', 'yes']:
                print("❌ Download cancelled")
                return False
            
            # Process each batch automatically
            current_page = start_page
            batch_num = self.session_state.get('current_batch', 1)
            
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
                
                # Process the batch automatically
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
                
                # Brief pause between batches
                if current_page <= end_page:
                    print(f"\n⏳ Brief pause before next batch...")
                    time.sleep(random.uniform(3, 5))
            
            # Final summary
            completed_batches = len(self.session_state['completed_batches'])
            print(f"\n🏁 AUTOMATED DOWNLOAD PROCESS COMPLETE!")
            print(f"✅ Completed batches: {completed_batches}")
            print(f"📁 Downloaded files: {len(self.session_state['downloads_completed'])}")
            print(f"📂 Download directory: {self.download_dir}")
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
    
    def process_batch(self, batch_start, batch_end, batch_num, total_batches):
        """FULL AUTOMATION - Handles 500K+ records with UI state management"""
        print(f"\n🤖 FULL AUTO BATCH {batch_num}/{total_batches}: PAGES {batch_start}-{batch_end}")
        print(f"🎯 Optimized for 500K+ records")
        print("=" * 60)
        
        try:
            selected_pages = []
            
            # PHASE 1: Process each page (uncheck → navigate → select)
            for page in range(batch_start, batch_end + 1):
                print(f"\n📍 Processing page {page}...")
                
                # Step 1: Ensure navigation is available (uncheck if needed)
                if page > batch_start:  # Don't uncheck on first page
                    print("🧠 Ensuring navigation is available...")
                    self.restore_navigation_if_hidden()
                
                # Step 2: Navigate to page
                if self.navigate_to_page_with_state_management(page):
                    print(f"✅ Navigated to page {page}")
                    
                    # Step 3: Select records immediately
                    if self.select_all_records_on_page():
                        print(f"✅ Selected records on page {page}")
                        selected_pages.append(page)
                    else:
                        print(f"❌ Selection failed on page {page}")
                    
                    time.sleep(random.uniform(1, 2))
                else:
                    print(f"❌ Navigation to page {page} failed")
            
            if not selected_pages:
                print("❌ No pages were successfully processed")
                return False
            
            print(f"\n📊 Successfully processed {len(selected_pages)} pages: {selected_pages}")
            
            # PHASE 2: Download all selected records
            print(f"\n📥 Downloading records from {len(selected_pages)} pages...")
            
            if not self.find_and_click_download_button():
                print("❌ Download button not found")
                return False
            
            self.configure_download_options()
            
            if not self.click_download_records_button():
                print("❌ Download Records button failed")
                return False
            
            # Wait for download
            search_name = self.session_state['search_name']
            timestamp = time.strftime('%m%d%y_%H%M')
            expected_filename = f"{search_name}_batch{batch_num}_{timestamp}.csv"
            
            downloaded_file = self.wait_for_download_completion(expected_filename)
            
            # PHASE 3: Clean up and prepare for next batch
            self.navigate_back_to_results()
            self.bulk_uncheck_all_records()
            
            # Update session
            self.session_state['completed_batches'].append({
                'batch_num': batch_num,
                'start_page': batch_start,
                'end_page': batch_end,
                'pages_processed': selected_pages,
                'filename': downloaded_file or expected_filename,
                'timestamp': timestamp
            })
            self.session_state['last_completed_page'] = batch_end
            self.session_state['current_batch'] = batch_num + 1
            if downloaded_file:
                self.session_state['downloads_completed'].append(downloaded_file)
            
            self._save_session_state()
            
            print(f"\n✅ Batch {batch_num} complete: {len(selected_pages)} pages → {downloaded_file}")
            return True
            
        except Exception as e:
            print(f"❌ Batch {batch_num} error: {e}")
            return False
    
    def restore_navigation_if_hidden(self):
        """Restore navigation by unchecking boxes if needed"""
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
                print("🔧 Navigation hidden - restoring...")
                self.bulk_uncheck_all_records()
                time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Error checking navigation state: {e}")
    
    def navigate_to_page_with_state_management(self, page_num):
        """Navigate with awareness of UI state changes"""
        try:
            # Check current page
            current_page = self._detect_current_page_simple()
            if current_page == page_num:
                return True
            
            # Find page input
            page_inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
            
            for input_elem in page_inputs:
                if input_elem.is_displayed() and input_elem.is_enabled():
                    value = input_elem.get_attribute('value') or ''
                    if value.isdigit() and int(value) <= 100:
                        print(f"📍 Page input: {value} → {page_num}")
                        
                        # Navigate
                        input_elem.click()
                        time.sleep(0.3)
                        input_elem.clear()
                        time.sleep(0.2)
                        input_elem.send_keys(str(page_num))
                        time.sleep(0.3)
                        input_elem.send_keys(Keys.ENTER)
                        time.sleep(3)
                        
                        return True
            
            return False
            
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False
    
    def bulk_uncheck_all_records(self):
        """Bulk uncheck all selected records"""
        try:
            # Method 1: Look for bulk uncheck buttons
            uncheck_selectors = [
                "//button[contains(text(), 'Unselect')]",
                "//a[contains(text(), 'Unselect')]",
                "//button[contains(text(), 'Clear')]",
                "//a[contains(text(), 'Clear')]",
                "//button[contains(text(), 'None')]"
            ]
            
            for selector in uncheck_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        print(f"🎯 Found uncheck button: {element.text}")
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
                print(f"✅ JavaScript unchecked {js_result} checkboxes")
                time.sleep(2)
                return True
            
            # Method 3: Header checkbox toggle
            header_checkboxes = self.driver.find_elements(By.XPATH, 
                "//th//input[@type='checkbox'] | //thead//input[@type='checkbox']")
            
            for checkbox in header_checkboxes:
                if checkbox.is_displayed() and checkbox.is_selected():
                    checkbox.click()
                    time.sleep(1)
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Bulk uncheck error: {e}")
            return False
    
    def _detect_current_page_simple(self):
        """Simple current page detection"""
        try:
            inputs = self.driver.find_elements(By.XPATH, "//input[@type='text']")
            for inp in inputs:
                if inp.is_displayed():
                    value = inp.get_attribute('value') or ''
                    if value.isdigit() and int(value) <= 100:
                        return int(value)
            return 1
        except:
            return 1
    
    def run(self):
        """Main entry point with enhanced menu"""
        try:
            print("🚀 Starting Enhanced Semi-Automated Data Scraper")
            
            # Step 1: Manual login
            if not self.start_manual_login():
                print("❌ Login process failed or cancelled")
                return
            
            # Step 2: Get total pages
            if not self.get_total_pages():
                print("❌ Could not determine total pages")
                return
            
            # Step 3: Show enhanced menu
            self.show_enhanced_menu()
            
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


if __name__ == "__main__":
    try:
        scraper = SemiAutomatedScraper()
        
        # Check if there's a previous session
        if scraper.session_state.get('search_name'):
            print("🔄 Previous session detected!")
            print(f"   Search: {scraper.session_state.get('search_name')}")
            print(f"   Total pages: {scraper.session_state.get('total_pages')}")
            print(f"   Last completed: {scraper.session_state.get('last_completed_page')}")
            print(f"   Completed batches: {len(scraper.session_state.get('completed_batches', []))}")
            
            resume = input("\n🔄 Resume previous session? (y/n): ").lower().strip()
            if resume in ['y', 'yes']:
                print("✅ Resuming previous session...")
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
                
                scraper.show_enhanced_menu()
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
