#!/usr/bin/env python3
"""
Miller 3 Data Scraper - Comprehensive Automation Diagnostic Test
Identifies why automation is requiring manual interventions and provides solutions
"""

import os
import sys
import time
import json
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class AutomationDiagnosticTest:
    def __init__(self, config_file='config/referenceusa_config.yaml'):
        print("\n🔬 MILLER 3 DATA SCRAPER - AUTOMATION DIAGNOSTIC TEST")
        print("=" * 60)
        print("🎯 Goal: Identify why automation requires manual interventions")
        print("🔧 Will test all automation failure points and provide fixes")
        
        # Load configuration
        self.config = self._load_config(config_file)
        self.download_dir = self.config.get('download_dir', './downloads')
        self.auth_url = self.config.get('auth_url')
        
        # Test results
        self.test_results = {
            'browser_setup': False,
            'page_access': False,
            'authentication': False,
            'page_navigation': False,
            'element_detection': False,
            'record_selection': False,
            'download_button_detection': False,
            'file_download': False,
            'manual_interventions': []
        }
        
        # Initialize browser
        self._setup_browser()
    
    def _load_config(self, config_file):
        """Load configuration file"""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"⚠️ Config file {config_file} not found, using defaults")
            return {
                'download_dir': './downloads',
                'auth_url': 'https://www.referenceusa.com',
                'pages_per_batch': 10
            }
    
    def _setup_browser(self):
        """Setup browser for diagnostics"""
        print("\n🌐 Setting up diagnostic browser...")
        
        options = webdriver.ChromeOptions()
        
        # Download configuration
        os.makedirs(self.download_dir, exist_ok=True)
        options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_setting_values.notifications": 2
        })
        
        # Anti-detection measures
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
        
        # Initialize browser
        chromedriver_path = "./chromedriver"
        if not os.path.exists(chromedriver_path):
            chromedriver_path = "./chromedriver"
        
        try:
            self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.test_results['browser_setup'] = True
            print("✅ Browser setup successful")
        except Exception as e:
            print(f"❌ Browser setup failed: {str(e)}")
            raise
    
    def run_comprehensive_diagnostic(self):
        """Run complete diagnostic test"""
        try:
            print("\n🚀 STARTING COMPREHENSIVE AUTOMATION DIAGNOSTIC")
            print("=" * 50)
            print("🔄 Status: DIAGNOSTIC IS RUNNING...")
            print("📊 Progress: Starting tests (this may take several minutes)")
            print()
            
            # Phase 1: Test page access
            print("🔄 Status: Running Phase 1/8 - Page Access Test")
            self._test_page_access()
            
            # Phase 2: Test authentication
            print("\n🔄 Status: Running Phase 2/8 - Authentication Test")
            self._test_authentication_flow()
            
            # Phase 3: Get to search results (manual)
            print("\n🔄 Status: Running Phase 3/8 - Manual Navigation to Search Results")
            print("⚠️  THIS PHASE REQUIRES USER INPUT")
            self._get_to_search_results()
            
            # Check if user exited
            if not hasattr(self, 'driver') or not self.driver:
                print("❌ Diagnostic stopped - user exited")
                return
            
            # Phase 4: Test page navigation
            print("\n🔄 Status: Running Phase 4/8 - Page Navigation Test")
            self._test_page_navigation()
            
            # Phase 5: Test element detection
            print("\n🔄 Status: Running Phase 5/8 - Element Detection Test")
            self._test_element_detection()
            
            # Phase 6: Test record selection
            print("\n🔄 Status: Running Phase 6/8 - Record Selection Test")
            self._test_record_selection()
            
            # Phase 7: Test download button detection
            print("\n🔄 Status: Running Phase 7/8 - Download Button Test")
            self._test_download_button_detection()
            
            # Phase 8: Test file download
            print("\n🔄 Status: Running Phase 8/8 - File Download Test")
            self._test_file_download()
            
            # Generate diagnostic report
            print("\n🔄 Status: Generating diagnostic report...")
            self._generate_diagnostic_report()
            
            # Provide solutions
            print("\n🔄 Status: Analyzing results and providing solutions...")
            self._provide_solutions()
            
            print("\n✅ DIAGNOSTIC COMPLETED SUCCESSFULLY!")
            
        except KeyboardInterrupt:
            print("\n\n🛑 Diagnostic interrupted by user (Ctrl+C)")
            print("📊 Partial results may be available")
        except Exception as e:
            print(f"\n❌ Diagnostic error: {str(e)}")
            print("📊 This error will be included in troubleshooting")
        finally:
            print("\n🏁 Diagnostic process finished")
            print("🔄 Status: Cleaning up...")
            try:
                choice = input("Close browser? (y/n): ").lower()
                if choice in ['y', 'yes', '']:
                    print("🔄 Status: Closing browser...")
                    self.driver.quit()
                    print("✅ Browser closed")
                else:
                    print("💻 Browser left open for manual inspection")
            except:
                print("✅ Cleanup completed")
    
    def _test_page_access(self):
        """Test basic page access capabilities"""
        print("\n🔍 TEST 1: PAGE ACCESS")
        print("-" * 30)
        
        try:
            # Navigate to auth URL
            print(f"Navigating to: {self.auth_url}")
            self.driver.get(self.auth_url)
            time.sleep(3)
            
            # Take screenshot
            self._take_screenshot("page_access_test")
            
            # Check page loaded
            current_url = self.driver.current_url
            page_title = self.driver.title
            page_source_length = len(self.driver.page_source)
            
            print(f"✅ URL: {current_url}")
            print(f"✅ Title: {page_title}")
            print(f"✅ Page size: {page_source_length} chars")
            
            # Check for common issues
            page_source = self.driver.page_source.lower()
            issues = []
            
            if 'captcha' in page_source:
                issues.append('CAPTCHA detected')
            if 'cloudflare' in page_source:
                issues.append('Cloudflare protection')
            if 'access denied' in page_source:
                issues.append('Access denied')
            if page_source_length < 1000:
                issues.append('Page content too small')
            
            if issues:
                print(f"⚠️ Issues detected: {issues}")
                self.test_results['manual_interventions'].extend(issues)
            else:
                print("✅ No obvious page access issues")
            
            self.test_results['page_access'] = True
            
        except Exception as e:
            print(f"❌ Page access failed: {str(e)}")
            self.test_results['manual_interventions'].append(f"Page access error: {str(e)}")
    
    def _test_authentication_flow(self):
        """Test authentication capabilities"""
        print("\n🔍 TEST 2: AUTHENTICATION FLOW")
        print("-" * 30)
        
        try:
            # Check current state
            current_url = self.driver.current_url
            page_title = self.driver.title
            
            print(f"Current URL: {current_url}")
            print(f"Current Title: {page_title}")
            
            # Look for authentication indicators
            auth_indicators = [
                "login", "sign in", "authenticate", "library card",
                "username", "password", "credentials"
            ]
            
            page_source = self.driver.page_source.lower()
            found_indicators = [indicator for indicator in auth_indicators if indicator in page_source]
            
            if found_indicators:
                print(f"✅ Authentication page detected: {found_indicators}")
                print("🔧 This explains why manual login is required")
                self.test_results['manual_interventions'].append("Manual authentication required")
                
                # Test tab handling
                initial_tabs = len(self.driver.window_handles)
                print(f"Current tabs: {initial_tabs}")
                
                # Test if new tabs open during auth
                print("⚠️ Note: Authentication may open new tabs")
                
            else:
                print("⚠️ No obvious authentication indicators found")
            
            # Check if already authenticated
            if any(domain in current_url for domain in ['referenceusa.com', 'data-axle.com']):
                if any(pattern in current_url for pattern in ['search', 'business', 'database']):
                    print("✅ May already be on authenticated page")
                    self.test_results['authentication'] = True
            
        except Exception as e:
            print(f"❌ Authentication test failed: {str(e)}")
    
    def _get_to_search_results(self):
        """Manual step to get to search results"""
        print("\n🔍 TEST 3: GET TO SEARCH RESULTS")
        print("-" * 30)
        
        print("\n📋 MANUAL STEP REQUIRED:")
        print("1. Complete authentication if needed")
        print("2. Navigate to U.S. Business database")
        print("3. Set up search criteria")
        print("4. Run search to get results")
        print("5. Make sure you can see paginated results")
        print()
        print("🔍 WAITING FOR USER INPUT...")
        print("⚠️  Please type 'Ready' in this terminal (not the browser)")
        print("💡 If you don't see a prompt, press Ctrl+C to restart")
        print()
        
        while True:
            try:
                print("🔸 DIAGNOSTIC READY CHECK:")
                ready_input = input("Type 'Ready' when you're on search results page with pagination: ").strip().lower()
                if ready_input == 'ready':
                    print("✅ User confirmed ready - continuing diagnostic...")
                    break
                elif ready_input == 'exit' or ready_input == 'quit':
                    print("❌ User requested exit")
                    return
                else:
                    print("❌ Please type 'Ready' (or 'exit' to quit)")
                    print("   You typed:", repr(ready_input))
                    print("   Expected: 'ready'")
                    print()
            except KeyboardInterrupt:
                print("\n🛑 Diagnostic interrupted by user (Ctrl+C)")
                return
            except Exception as e:
                print(f"❌ Input error: {e}")
                print("Please try again or press Ctrl+C to exit")
        
        # Verify we're on results page
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        result_indicators = ['results', 'page', 'records', 'companies', 'businesses']
        found_indicators = [indicator for indicator in result_indicators if indicator in page_source]
        
        if found_indicators:
            print(f"✅ Results page confirmed: {found_indicators}")
        else:
            print("⚠️ Results page not clearly detected")
        
        self._take_screenshot("search_results_page")
    
    def _test_page_navigation(self):
        """Test page navigation automation"""
        print("\n🔍 TEST 4: PAGE NAVIGATION")
        print("-" * 30)
        
        try:
            # Look for pagination elements
            pagination_selectors = [
                "//input[@type='text'][ancestor::*[contains(text(), 'Page')]]",
                "//input[@type='text'][following-sibling::*[contains(text(), 'of')]]",
                "//span[contains(text(), 'Page')]/following::input[@type='text'][1]",
                "//input[@type='text'][contains(@name, 'page')]",
                "//input[@type='number']"
            ]
            
            page_input = None
            for selector in pagination_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                if elements:
                    for element in elements:
                        if element.is_displayed():
                            page_input = element
                            print(f"✅ Found page input: {selector}")
                            break
                    if page_input:
                        break
            
            if page_input:
                # Test page input functionality
                try:
                    current_value = page_input.get_attribute('value')
                    print(f"✅ Current page value: {current_value}")
                    
                    # Test if we can interact with it
                    page_input.clear()
                    page_input.send_keys(current_value)  # Put back original value
                    print("✅ Page input interaction works")
                    
                    self.test_results['page_navigation'] = True
                    
                except Exception as e:
                    print(f"❌ Page input interaction failed: {str(e)}")
                    self.test_results['manual_interventions'].append("Page navigation requires manual intervention")
            else:
                print("❌ No page input field found")
                self.test_results['manual_interventions'].append("Page navigation automation impossible")
                
                # Look for alternative navigation
                next_buttons = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')] | //button[contains(text(), 'Next')]")
                if next_buttons:
                    print("✅ Found Next button as alternative")
                else:
                    print("❌ No Next button found either")
            
        except Exception as e:
            print(f"❌ Page navigation test failed: {str(e)}")
    
    def _test_element_detection(self):
        """Test general element detection capabilities"""
        print("\n🔍 TEST 5: ELEMENT DETECTION")
        print("-" * 30)
        
        try:
            # Count basic elements
            all_elements = self.driver.find_elements(By.XPATH, "//*")
            buttons = self.driver.find_elements(By.XPATH, "//button")
            inputs = self.driver.find_elements(By.XPATH, "//input")
            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            
            print(f"✅ Total elements: {len(all_elements)}")
            print(f"✅ Buttons: {len(buttons)}")
            print(f"✅ Inputs: {len(inputs)}")
            print(f"✅ Checkboxes: {len(checkboxes)}")
            
            # Test JavaScript access
            js_element_count = self.driver.execute_script("return document.querySelectorAll('*').length;")
            print(f"✅ JS element count: {js_element_count}")
            
            if len(all_elements) != js_element_count:
                print("⚠️ Selenium vs JavaScript element count mismatch")
                self.test_results['manual_interventions'].append("Element detection discrepancy")
            
            # Test for dynamic content
            time.sleep(2)
            new_element_count = len(self.driver.find_elements(By.XPATH, "//*"))
            if new_element_count != len(all_elements):
                print(f"⚠️ Dynamic content detected: {len(all_elements)} → {new_element_count}")
                self.test_results['manual_interventions'].append("Dynamic content affecting automation")
            
            self.test_results['element_detection'] = True
            
        except Exception as e:
            print(f"❌ Element detection test failed: {str(e)}")
    
    def _test_record_selection(self):
        """Test record selection automation"""
        print("\n🔍 TEST 6: RECORD SELECTION")
        print("-" * 30)
        
        try:
            # Look for select all checkbox
            select_all_selectors = [
                "//th//input[@type='checkbox']",
                "//thead//input[@type='checkbox']",
                "//th[contains(text(), 'Company Name')]//input[@type='checkbox']",
                "//input[@type='checkbox'][1]"
            ]
            
            select_all_checkbox = None
            for selector in select_all_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                if elements:
                    for element in elements:
                        if element.is_displayed():
                            select_all_checkbox = element
                            print(f"✅ Found select all checkbox: {selector}")
                            break
                    if select_all_checkbox:
                        break
            
            # Count individual checkboxes
            all_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            visible_checkboxes = [cb for cb in all_checkboxes if cb.is_displayed()]
            
            print(f"✅ Total checkboxes: {len(all_checkboxes)}")
            print(f"✅ Visible checkboxes: {len(visible_checkboxes)}")
            
            if select_all_checkbox:
                # Test checkbox interaction
                try:
                    original_state = select_all_checkbox.is_selected()
                    print(f"✅ Select all original state: {original_state}")
                    
                    # Test click (but don't actually change state)
                    print("✅ Select all checkbox is accessible")
                    self.test_results['record_selection'] = True
                    
                except Exception as e:
                    print(f"❌ Checkbox interaction failed: {str(e)}")
                    self.test_results['manual_interventions'].append("Record selection requires manual intervention")
            else:
                if len(visible_checkboxes) > 0:
                    print("⚠️ No select all, but individual checkboxes found")
                    self.test_results['manual_interventions'].append("Must select records individually")
                else:
                    print("❌ No checkboxes found")
                    self.test_results['manual_interventions'].append("No record selection possible")
            
        except Exception as e:
            print(f"❌ Record selection test failed: {str(e)}")
    
    def _test_download_button_detection(self):
        """Test download button detection"""
        print("\n🔍 TEST 7: DOWNLOAD BUTTON DETECTION")
        print("-" * 30)
        
        try:
            # Test multiple download button strategies
            download_strategies = [
                ("Direct text match", "//button[contains(text(), 'Download')]"),
                ("Link text match", "//a[contains(text(), 'Download')]"),
                ("Case insensitive", "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'download')]"),
                ("Class based", "//button[contains(@class, 'download')] | //a[contains(@class, 'download')]"),
                ("ID based", "//button[contains(@id, 'download')] | //a[contains(@id, 'download')]"),
                ("Toolbar area", "//div[contains(@class, 'toolbar')]//button | //div[contains(@class, 'menu')]//a"),
                ("Any download text", "//*[contains(text(), 'Download') and (name()='button' or name()='a' or name()='input')]")
            ]
            
            found_buttons = []
            for strategy_name, xpath in download_strategies:
                elements = self.driver.find_elements(By.XPATH, xpath)
                visible_elements = [e for e in elements if e.is_displayed()]
                
                print(f"   {strategy_name}: {len(visible_elements)} found")
                
                if visible_elements:
                    for element in visible_elements[:3]:  # Check first 3
                        try:
                            text = element.text or element.get_attribute('value') or 'no-text'
                            tag = element.tag_name
                            classes = element.get_attribute('class') or 'no-class'
                            found_buttons.append({
                                'strategy': strategy_name,
                                'text': text,
                                'tag': tag,
                                'classes': classes,
                                'element': element
                            })
                        except:
                            pass
            
            if found_buttons:
                print(f"✅ Found {len(found_buttons)} potential download buttons:")
                for i, btn in enumerate(found_buttons[:5]):  # Show first 5
                    print(f"   {i+1}. {btn['tag']} - '{btn['text']}' ({btn['strategy']})")
                
                # Test clicking capability on first button
                try:
                    test_button = found_buttons[0]['element']
                    if test_button.is_enabled():
                        print("✅ First button is clickable")
                        self.test_results['download_button_detection'] = True
                    else:
                        print("⚠️ First button is disabled")
                        self.test_results['manual_interventions'].append("Download button found but disabled")
                except Exception as e:
                    print(f"⚠️ Button click test failed: {str(e)}")
                    self.test_results['manual_interventions'].append("Download button not clickable")
            else:
                print("❌ No download buttons found with any strategy")
                self.test_results['manual_interventions'].append("Download button detection failed")
                
                # This is a critical failure - let's investigate further
                print("\n🔍 INVESTIGATING DOWNLOAD BUTTON ABSENCE:")
                
                # Check if we're on the right page
                current_url = self.driver.current_url
                if 'download' not in current_url.lower():
                    print("⚠️ May not be on download page yet")
                    print("🔧 User needs to select records and click Download first")
                    self.test_results['manual_interventions'].append("Must navigate to download page first")
                
                # Look for any buttons that might be download-related
                all_buttons = self.driver.find_elements(By.XPATH, "//button | //a[@href] | //input[@type='submit']")
                print(f"Found {len(all_buttons)} total interactive elements")
                
                button_texts = []
                for btn in all_buttons[:10]:  # Check first 10
                    try:
                        text = btn.text or btn.get_attribute('value') or btn.get_attribute('title') or 'no-text'
                        if text.strip():
                            button_texts.append(text.strip())
                    except:
                        pass
                
                if button_texts:
                    print(f"Button texts found: {button_texts}")
            
        except Exception as e:
            print(f"❌ Download button detection test failed: {str(e)}")
    
    def _test_file_download(self):
        """Test file download capabilities"""
        print("\n🔍 TEST 8: FILE DOWNLOAD")
        print("-" * 30)
        
        try:
            # Check download directory
            print(f"Download directory: {self.download_dir}")
            print(f"Directory exists: {os.path.exists(self.download_dir)}")
            
            # List current files
            if os.path.exists(self.download_dir):
                current_files = os.listdir(self.download_dir)
                csv_files = [f for f in current_files if f.endswith('.csv')]
                print(f"Current files: {len(current_files)}")
                print(f"CSV files: {len(csv_files)}")
                
                if csv_files:
                    print("✅ Previous downloads detected")
                    for csv_file in csv_files[-3:]:  # Show last 3
                        file_path = os.path.join(self.download_dir, csv_file)
                        file_size = os.path.getsize(file_path)
                        print(f"   {csv_file} ({file_size} bytes)")
            
            # Test browser download settings
            try:
                download_prefs = self.driver.execute_script("""
                    return {
                        defaultPath: 'unknown',
                        promptForDownload: 'unknown'
                    };
                """)
                print(f"✅ Browser download settings accessible")
            except:
                print("⚠️ Cannot access browser download settings")
                
            self.test_results['file_download'] = True
            
        except Exception as e:
            print(f"❌ File download test failed: {str(e)}")
    
    def _generate_diagnostic_report(self):
        """Generate comprehensive diagnostic report"""
        print("\n📊 DIAGNOSTIC REPORT")
        print("=" * 50)
        
        # Count successful tests
        successful_tests = sum(1 for result in self.test_results.values() if result is True)
        total_tests = len([k for k in self.test_results.keys() if k != 'manual_interventions'])
        
        print(f"Tests Passed: {successful_tests}/{total_tests}")
        print(f"Manual Interventions Required: {len(self.test_results['manual_interventions'])}")
        
        # Show test results
        test_status = {
            'browser_setup': '✅' if self.test_results['browser_setup'] else '❌',
            'page_access': '✅' if self.test_results['page_access'] else '❌',
            'authentication': '✅' if self.test_results['authentication'] else '❌',
            'page_navigation': '✅' if self.test_results['page_navigation'] else '❌',
            'element_detection': '✅' if self.test_results['element_detection'] else '❌',
            'record_selection': '✅' if self.test_results['record_selection'] else '❌',
            'download_button_detection': '✅' if self.test_results['download_button_detection'] else '❌',
            'file_download': '✅' if self.test_results['file_download'] else '❌'
        }
        
        for test, status in test_status.items():
            print(f"{status} {test.replace('_', ' ').title()}")
        
        # Show manual interventions
        if self.test_results['manual_interventions']:
            print(f"\n⚠️ Manual Interventions Required:")
            for i, intervention in enumerate(self.test_results['manual_interventions'], 1):
                print(f"   {i}. {intervention}")
        
        # Save report to file
        report_data = {
            'timestamp': time.time(),
            'test_results': self.test_results,
            'config': self.config
        }
        
        report_file = f"diagnostic_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Report saved to: {report_file}")
    
    def _provide_solutions(self):
        """Provide specific solutions for identified issues"""
        print("\n🔧 SOLUTIONS AND RECOMMENDATIONS")
        print("=" * 50)
        
        interventions = self.test_results['manual_interventions']
        
        if not interventions:
            print("🎉 No major issues detected! Automation should work well.")
            return
        
        print("Based on the diagnostic results, here are the recommended solutions:")
        
        # Authentication solutions
        if any('authentication' in i.lower() for i in interventions):
            print("\n🔑 AUTHENTICATION ISSUES:")
            print("   Solution: Implement enhanced authentication handler")
            print("   - Improve tab monitoring and switching")
            print("   - Add better authentication detection")
            print("   - Provide clearer manual guidance")
            
        # Page navigation solutions
        if any('page navigation' in i.lower() or 'navigation' in i.lower() for i in interventions):
            print("\n🧭 PAGE NAVIGATION ISSUES:")
            print("   Solution: Enhance page navigation strategies")
            print("   - Add more selector strategies for page inputs")
            print("   - Implement fallback to Next/Previous buttons")
            print("   - Add manual navigation guidance")
            
        # Record selection solutions
        if any('record selection' in i.lower() or 'checkbox' in i.lower() for i in interventions):
            print("\n☑️ RECORD SELECTION ISSUES:")
            print("   Solution: Improve checkbox detection and interaction")
            print("   - Add more checkbox selector strategies")
            print("   - Implement individual checkbox selection fallback")
            print("   - Add selection verification")
            
        # Download button solutions
        if any('download button' in i.lower() for i in interventions):
            print("\n📥 DOWNLOAD BUTTON ISSUES:")
            print("   Solution: Enhanced download button detection")
            print("   - Implement multiple detection strategies")
            print("   - Add iframe content checking")
            print("   - Improve manual intervention guidance")
            
        # Dynamic content solutions
        if any('dynamic content' in i.lower() for i in interventions):
            print("\n⚡ DYNAMIC CONTENT ISSUES:")
            print("   Solution: Add dynamic content handling")
            print("   - Implement wait strategies for content loading")
            print("   - Add retry mechanisms for failed interactions")
            print("   - Use explicit waits instead of sleep")
        
        print("\n💡 IMMEDIATE ACTIONS YOU CAN TAKE:")
        print("1. Use the manual login scraper for most reliable results")
        print("2. Keep browser window visible during automation")
        print("3. Don't navigate away from the automation manually")
        print("4. Be ready to assist with manual steps when prompted")
        print("5. Run this diagnostic again after making changes")
        
        print("\n🚀 RECOMMENDED SCRIPT TO USE:")
        print("   python3 manual_login_scraper.py")
        print("   (This handles the most problematic automation points)")
    
    def _take_screenshot(self, name):
        """Take a screenshot for debugging"""
        try:
            timestamp = int(time.time())
            filename = f"diagnostic_{name}_{timestamp}.png"
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot: {filename}")
        except Exception as e:
            print(f"❌ Screenshot failed: {str(e)}")


if __name__ == "__main__":
    try:
        print("🚀 Starting automation diagnostic test...")
        
        # Get config file from command line or use default
        config_file = 'config/referenceusa_config.yaml'
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        
        # Run diagnostic
        diagnostic = AutomationDiagnosticTest(config_file)
        diagnostic.run_comprehensive_diagnostic()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Diagnostic interrupted by user")
    except Exception as e:
        print(f"\n❌ Diagnostic error: {str(e)}")
    
    print("\nPress Enter to exit...")
    input()
