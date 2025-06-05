#!/usr/bin/env python3
"""
Miller 3 Data Scraper - Critical Issue Fixes
Addresses the 3 major blocking issues: download button, checkbox unchecking, file verification
"""

import os
import sys
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class CriticalIssueFixer:
    def __init__(self):
        print("🔧 MILLER 3 DATA SCRAPER - CRITICAL ISSUE FIXES")
        print("=" * 55)
        print("🎯 Fixing: Download button detection, checkbox unchecking, file verification")
        
        # Load configuration first
        self.config = self._load_config()
        self.auth_url = self.config.get('auth_url')
        
        print(f"📍 Using predefined URL: {self.auth_url}")
        
        # Initialize browser for testing
        self._setup_browser()
    
    def _load_config(self, config_file='config/referenceusa_config.yaml'):
        """Load configuration file"""
        try:
            import yaml
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                print(f"✅ Loaded config from: {config_file}")
                return config
        except FileNotFoundError:
            print(f"⚠️ Config file {config_file} not found")
            # Try alternative locations
            alt_configs = ['referenceusa_config.yaml', 'config.yaml']
            for alt_config in alt_configs:
                try:
                    with open(alt_config, 'r') as f:
                        config = yaml.safe_load(f)
                        print(f"✅ Loaded config from: {alt_config}")
                        return config
                except:
                    continue
            
            print("❌ No config file found, using defaults")
            return {
                'auth_url': 'https://www.referenceusa.com',
                'download_dir': './downloads'
            }
    
    def _setup_browser(self):
        """Setup browser for testing"""
        options = webdriver.ChromeOptions()
        
        # Download configuration - use config download_dir
        download_dir = self.config.get('download_dir', './downloads')
        download_dir = os.path.abspath(download_dir)  # Convert to absolute path
        os.makedirs(download_dir, exist_ok=True)
        
        options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        
        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Find chromedriver
        chromedriver_path = "./chromedriver"
        if not os.path.exists(chromedriver_path):
            chromedriver_path = "chromedriver"
        
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.download_dir = download_dir
    
    def test_download_button_detection(self):
        """Test advanced download button detection strategies"""
        print("\n🔍 TESTING DOWNLOAD BUTTON DETECTION")
        print("=" * 45)
        
        input("Navigate to the results page (if needed) and press Enter...")
        
        # Take screenshot for debugging
        self.driver.save_screenshot("download_button_debug.png")
        
        # Advanced detection strategies
        detection_strategies = [
            # Strategy 1: Standard text-based detection
            {
                'name': 'Standard Download Text',
                'xpath': "//a[contains(text(), 'Download')] | //button[contains(text(), 'Download')]"
            },
            
            # Strategy 2: Toolbar-specific detection
            {
                'name': 'Toolbar Download Button',
                'xpath': "//div[contains(@class, 'toolbar') or contains(@class, 'nav') or contains(@class, 'menu')]//a[contains(text(), 'Download')] | //div[contains(@class, 'toolbar') or contains(@class, 'nav') or contains(@class, 'menu')]//button[contains(text(), 'Download')]"
            },
            
            # Strategy 3: Icon-based detection
            {
                'name': 'Download Icon',
                'xpath': "//a[contains(@class, 'download') or contains(@title, 'download')] | //button[contains(@class, 'download') or contains(@title, 'download')]"
            },
            
            # Strategy 4: Form submission buttons
            {
                'name': 'Form Download Buttons',
                'xpath': "//form//input[@type='submit' and contains(@value, 'Download')] | //form//button[contains(text(), 'Download')]"
            },
            
            # Strategy 5: Case-insensitive broad search
            {
                'name': 'Case Insensitive Download',
                'xpath': "//*[contains(translate(text(), 'DOWNLOAD', 'download'), 'download') and (name()='a' or name()='button' or name()='input')]"
            },
            
            # Strategy 6: ReferenceUSA-specific patterns
            {
                'name': 'ReferenceUSA Specific',
                'xpath': "//a[contains(@href, 'download') or contains(@onclick, 'download')] | //button[contains(@onclick, 'download')]"
            },
            
            # Strategy 7: Any clickable element with download-related attributes
            {
                'name': 'Download Attributes',
                'xpath': "//*[contains(@id, 'download') or contains(@name, 'download') or contains(@class, 'download')][@href or @onclick or name()='button']"
            },
            
            # Strategy 8: Look for specific button structure
            {
                'name': 'Button Structure',
                'xpath': "//button[contains(@class, 'btn') and contains(text(), 'Download')] | //a[contains(@class, 'btn') and contains(text(), 'Download')]"
            }
        ]
        
        found_buttons = []
        
        for strategy in detection_strategies:
            try:
                elements = self.driver.find_elements(By.XPATH, strategy['xpath'])
                visible_elements = [e for e in elements if e.is_displayed()]
                
                print(f"\n🔍 {strategy['name']}: {len(visible_elements)} found")
                
                for element in visible_elements:
                    try:
                        text = element.text or element.get_attribute('value') or element.get_attribute('title') or 'no-text'
                        href = element.get_attribute('href') or 'no-href'
                        onclick = element.get_attribute('onclick') or 'no-onclick'
                        class_attr = element.get_attribute('class') or 'no-class'
                        
                        button_info = {
                            'strategy': strategy['name'],
                            'element': element,
                            'text': text.strip(),
                            'tag': element.tag_name,
                            'href': href,
                            'onclick': onclick,
                            'class': class_attr
                        }
                        
                        found_buttons.append(button_info)
                        print(f"   ✅ {element.tag_name}: '{text.strip()}' | class: {class_attr}")
                        
                    except Exception as e:
                        print(f"   ❌ Error getting element info: {e}")
                        
            except Exception as e:
                print(f"   ❌ Strategy failed: {e}")
        
        if found_buttons:
            print(f"\n🎯 FOUND {len(found_buttons)} POTENTIAL DOWNLOAD BUTTONS!")
            
            # Test clicking the most promising button
            print("\n🧪 Testing button clicks...")
            for i, btn in enumerate(found_buttons[:3]):  # Test first 3
                try:
                    print(f"\nTesting button {i+1}: {btn['text']} ({btn['strategy']})")
                    
                    # Test if clickable
                    element = btn['element']
                    if element.is_enabled():
                        print(f"   ✅ Button is enabled")
                        
                        # Ask user if they want to test click
                        test_click = input(f"   Test click this button? (y/n): ").lower()
                        if test_click == 'y':
                            try:
                                element.click()
                                print("   ✅ Click successful!")
                                time.sleep(2)
                                
                                # Check if we navigated somewhere
                                new_url = self.driver.current_url
                                print(f"   📍 New URL: {new_url}")
                                
                                return True
                            except Exception as e:
                                print(f"   ❌ Click failed: {e}")
                    else:
                        print(f"   ❌ Button is disabled")
                        
                except Exception as e:
                    print(f"   ❌ Error testing button: {e}")
        else:
            print("\n❌ NO DOWNLOAD BUTTONS FOUND WITH ANY STRATEGY!")
            
            # Debug: Show all clickable elements
            print("\n🔍 DEBUG: All clickable elements on page:")
            all_clickable = self.driver.find_elements(By.XPATH, "//a | //button | //input[@type='submit'] | //input[@type='button']")
            
            for i, element in enumerate(all_clickable[:15]):  # Show first 15
                try:
                    if element.is_displayed():
                        text = element.text or element.get_attribute('value') or 'no-text'
                        print(f"   {i+1}. {element.tag_name}: '{text.strip()}'")
                except:
                    pass
        
        return False
    
    def test_checkbox_unchecking(self):
        """Test advanced checkbox unchecking strategies"""
        print("\n☑️ TESTING CHECKBOX UNCHECKING")
        print("=" * 35)
        
        input("Make sure some checkboxes are selected and press Enter...")
        
        # Take screenshot before unchecking
        self.driver.save_screenshot("before_uncheck.png")
        
        # Strategy 1: Find and uncheck the "select all" checkbox in header
        print("\n🔍 Strategy 1: Unchecking select-all checkbox...")
        
        select_all_selectors = [
            "//th//input[@type='checkbox']",
            "//thead//input[@type='checkbox']", 
            "//th[contains(text(), 'Company Name')]//input[@type='checkbox']",
            "//th[contains(text(), 'Company Name')]/preceding-sibling::th//input[@type='checkbox']",
            "//table//tr[1]//input[@type='checkbox']",
            "//input[@type='checkbox'][1]"
        ]
        
        select_all_found = False
        for selector in select_all_selectors:
            try:
                checkboxes = self.driver.find_elements(By.XPATH, selector)
                for checkbox in checkboxes:
                    if checkbox.is_displayed():
                        print(f"   ✅ Found select-all checkbox: {selector}")
                        
                        if checkbox.is_selected():
                            try:
                                checkbox.click()
                                print("   ✅ Clicked select-all checkbox")
                                time.sleep(1)
                                select_all_found = True
                                break
                            except Exception as e:
                                print(f"   ❌ Click failed: {e}")
                                # Try JavaScript click
                                try:
                                    self.driver.execute_script("arguments[0].click();", checkbox)
                                    print("   ✅ JavaScript click successful")
                                    select_all_found = True
                                    break
                                except:
                                    print("   ❌ JavaScript click also failed")
                        else:
                            print("   ⚠️ Select-all checkbox is already unchecked")
                            select_all_found = True
                            break
                
                if select_all_found:
                    break
                    
            except Exception as e:
                print(f"   ❌ Selector failed: {e}")
        
        if not select_all_found:
            print("   ❌ No select-all checkbox found")
            
            # Strategy 2: Uncheck individual checkboxes
            print("\n🔍 Strategy 2: Unchecking individual checkboxes...")
            
            all_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            selected_checkboxes = [cb for cb in all_checkboxes if cb.is_displayed() and cb.is_selected()]
            
            print(f"   Found {len(selected_checkboxes)} selected checkboxes")
            
            unchecked_count = 0
            for checkbox in selected_checkboxes:
                try:
                    checkbox.click()
                    unchecked_count += 1
                    time.sleep(0.1)  # Brief pause
                except:
                    try:
                        self.driver.execute_script("arguments[0].click();", checkbox)
                        unchecked_count += 1
                    except:
                        pass
            
            print(f"   ✅ Unchecked {unchecked_count} individual checkboxes")
        
        # Take screenshot after unchecking
        self.driver.save_screenshot("after_uncheck.png")
        
        # Verify unchecking worked
        time.sleep(1)
        remaining_selected = self.driver.find_elements(By.XPATH, "//input[@type='checkbox' and @checked]")
        if not remaining_selected:
            # Try JavaScript check
            remaining_count = self.driver.execute_script("""
                return Array.from(document.querySelectorAll('input[type="checkbox"]'))
                       .filter(cb => cb.checked).length;
            """)
        else:
            remaining_count = len(remaining_selected)
        
        print(f"\n📊 Verification: {remaining_count} checkboxes still selected")
        
        if remaining_count == 0:
            print("✅ SUCCESS: All checkboxes unchecked!")
            return True
        else:
            print(f"⚠️ WARNING: {remaining_count} checkboxes still selected")
            return False
    
    def test_file_download_verification(self):
        """Test file download verification"""
        print("\n📥 TESTING FILE DOWNLOAD VERIFICATION")
        print("=" * 40)
        
        # Get initial file list
        initial_files = self._get_download_files()
        print(f"📂 Files in download folder before: {len(initial_files)}")
        
        if initial_files:
            print("   Existing files:")
            for f in initial_files[-5:]:  # Show last 5
                print(f"     📄 {f}")
        
        input("Trigger a download and press Enter when it should be complete...")
        
        # Wait and check for new files
        print("🔍 Monitoring download folder for new files...")
        
        max_wait = 30  # Wait up to 30 seconds
        check_interval = 2
        
        for i in range(0, max_wait, check_interval):
            time.sleep(check_interval)
            current_files = self._get_download_files()
            new_files = [f for f in current_files if f not in initial_files]
            
            if new_files:
                print(f"✅ SUCCESS! {len(new_files)} new file(s) detected:")
                for f in new_files:
                    file_path = os.path.join(self.download_dir, f)
                    file_size = os.path.getsize(file_path)
                    print(f"   📄 {f} ({self._format_file_size(file_size)})")
                return True
            
            print(f"   ⏳ Waiting... ({i+check_interval}/{max_wait}s)")
        
        print("❌ FAILED: No new files detected after 30 seconds")
        
        # Enhanced debugging
        print("\n🔍 DEBUG: Download folder analysis...")
        print(f"   📂 Download directory: {self.download_dir}")
        print(f"   📂 Directory exists: {os.path.exists(self.download_dir)}")
        
        if os.path.exists(self.download_dir):
            all_files = os.listdir(self.download_dir)
            print(f"   📄 Total files in directory: {len(all_files)}")
            
            # Check for partial downloads
            partial_files = [f for f in all_files if f.endswith('.crdownload') or f.endswith('.tmp')]
            if partial_files:
                print(f"   ⏳ Partial downloads found: {partial_files}")
        
        # Check browser downloads page
        try:
            self.driver.get("chrome://downloads/")
            time.sleep(2)
            print("   🌐 Opened browser downloads page for manual inspection")
        except:
            pass
        
        return False
    
    def _get_download_files(self):
        """Get list of actual files in download directory"""
        try:
            if os.path.exists(self.download_dir):
                all_items = os.listdir(self.download_dir)
                files = []
                for item in all_items:
                    item_path = os.path.join(self.download_dir, item)
                    if os.path.isfile(item_path):
                        # Skip temporary and hidden files
                        if not item.startswith('.') and not item.endswith('.tmp') and not item.endswith('.crdownload'):
                            files.append(item)
                return files
            return []
        except Exception as e:
            print(f"❌ Error checking download folder: {e}")
            return []
    
    def _format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    def run_all_tests(self):
        """Run all critical issue tests"""
        print("\n🚀 RUNNING ALL CRITICAL ISSUE TESTS")
        print("=" * 45)
        
        # Navigate to the predefined URL first
        print(f"📍 Navigating to predefined URL: {self.auth_url}")
        try:
            self.driver.get(self.auth_url)
            time.sleep(3)
            print("✅ Successfully navigated to configured URL")
            
            # Take screenshot of the page we landed on
            self.driver.save_screenshot("config_url_page.png")
            print("📸 Screenshot saved: config_url_page.png")
            
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            print("Please navigate manually to your ReferenceUSA results page")
        
        print("\n📋 MANUAL STEP:")
        print("If you're not on the search results page:")
        print("1. Complete authentication if needed")
        print("2. Navigate to search results with pagination")
        print("3. Make sure you can see the data table with checkboxes")
        
        input("\nPress Enter when you're on the search results page...")
        
        results = {}
        
        # Test 1: Download button detection
        print("\n1️⃣ DOWNLOAD BUTTON DETECTION TEST")
        results['download_button'] = self.test_download_button_detection()
        
        # Test 2: Checkbox unchecking
        print("\n2️⃣ CHECKBOX UNCHECKING TEST")
        results['checkbox_unchecking'] = self.test_checkbox_unchecking()
        
        # Test 3: File download verification
        print("\n3️⃣ FILE DOWNLOAD VERIFICATION TEST")
        results['file_verification'] = self.test_file_download_verification()
        
        # Summary
        print("\n📊 TEST RESULTS SUMMARY")
        print("=" * 30)
        
        passed_tests = sum(1 for result in results.values() if result)
        total_tests = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name.replace('_', ' ').title()}")
        
        print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL CRITICAL ISSUES RESOLVED!")
        else:
            print("⚠️ Some issues need manual fixes or code updates")
        
        return results

if __name__ == "__main__":
    try:
        print("🔧 Starting critical issue testing...")
        
        fixer = CriticalIssueFixer()
        
        print("\n📋 This will test the 3 critical blocking issues:")
        print("1. Download button detection")
        print("2. Checkbox unchecking") 
        print("3. File download verification")
        print()
        
        input("Press Enter to start testing...")
        
        results = fixer.run_all_tests()
        
        print("\n💡 Next steps based on results:")
        if not results.get('download_button'):
            print("🔧 Download Button: Needs manual identification or code updates")
        if not results.get('checkbox_unchecking'):
            print("🔧 Checkbox Unchecking: Needs improved selection clearing")
        if not results.get('file_verification'):
            print("🔧 File Verification: Check download settings and folder permissions")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing error: {str(e)}")
    
    print("\nPress Enter to exit...")
    input()
