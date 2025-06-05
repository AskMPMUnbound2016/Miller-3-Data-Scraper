import time
import random
from selenium.webdriver.common.by import By
from improved_auth_handler import ImprovedAuthHandler


class ImprovedLoginManager:
    def __init__(self, browser_manager, auth_url, credentials):
        self.browser = browser_manager
        self.auth_url = auth_url
        self.credentials = credentials
        self.auth_handler = ImprovedAuthHandler(browser_manager)
    
    def login(self):
        """Enhanced login process with improved tab handling and authentication detection"""
        try:
            print("🚀 Starting enhanced login process...")
            
            # Store the original window handle
            original_handle = self.browser.get_current_window_handle()
            
            # Navigate to authentication page
            print(f"🌐 Navigating to authentication page: {self.auth_url}")
            self.browser.navigate(self.auth_url)
            
            # Handle any security challenges
            self.browser.handle_security_challenge()
            
            # Take screenshot of initial login page
            try:
                screenshot_path = "login_initial_page.png"
                self.browser.driver.save_screenshot(screenshot_path)
                print(f"📸 Saved screenshot: {screenshot_path}")
            except Exception as e:
                print(f"⚠️ Failed to save screenshot: {str(e)}")
            
            # Check if authentication happens in a new tab
            initial_handles = set(self.browser.get_window_handles())
            
            # Try automatic login if credentials are available
            auto_login_success = self._attempt_automatic_login()
            
            if auto_login_success:
                print("✅ Automatic login attempted")
            else:
                print("⚠️ Automatic login not possible - manual login required")
                self._prompt_manual_login()
            
            # Wait for potential new tabs to open
            time.sleep(3)
            
            # Check for new tabs after login
            current_handles = set(self.browser.get_window_handles())
            new_handles = current_handles - initial_handles
            
            if new_handles:
                print(f"🔄 Detected {len(new_handles)} new tab(s) after login")
                # Switch to the newest tab
                newest_handle = list(new_handles)[-1]
                self.browser.switch_to_window(newest_handle)
                print(f"🎯 Switched to newest tab")
            
            # Use improved authentication handler
            auth_success = self.auth_handler.handle_authentication_flow()
            
            if auth_success:
                print("✅ Login and navigation completed successfully!")
                
                # Final verification
                current_url = self.browser.driver.current_url.lower()
                reference_indicators = ["referenceusa.com", "proxy.openathens.net", "usbusiness", "data-axle"]
                
                if any(indicator in current_url for indicator in reference_indicators):
                    print(f"🎯 Successfully on target site: {current_url}")
                    
                    # Save final screenshot
                    try:
                        screenshot_path = "login_success_final.png"
                        self.browser.driver.save_screenshot(screenshot_path)
                        print(f"📸 Final screenshot saved: {screenshot_path}")
                    except Exception as e:
                        print(f"⚠️ Failed to save final screenshot: {str(e)}")
                    
                    return True
                else:
                    print(f"⚠️ Warning: Current URL doesn't match expected pattern: {current_url}")
                    return self._handle_unexpected_location()
            else:
                print("❌ Authentication flow failed")
                return self._handle_authentication_failure()
                
        except Exception as e:
            print(f"❌ Login process failed with error: {str(e)}")
            return self._handle_login_exception(e)
    
    def _attempt_automatic_login(self):
        """Try to automatically fill in login credentials"""
        try:
            print("🔍 Looking for login form...")
            
            # Get all input fields on the page
            input_fields = self.browser.find_elements(By.TAG_NAME, "input")
            username_field = None
            password_field = None
            
            # Identify username and password fields
            for field in input_fields:
                field_type = field.get_attribute("type") or ""
                field_id = (field.get_attribute("id") or "").lower()
                field_name = (field.get_attribute("name") or "").lower()
                field_placeholder = (field.get_attribute("placeholder") or "").lower()
                
                # Username field patterns
                username_patterns = ["user", "login", "barcode", "card", "email", "name", "id"]
                if (field_type.lower() in ["text", "email"] and 
                    any(pattern in field_id or pattern in field_name or pattern in field_placeholder 
                        for pattern in username_patterns)):
                    username_field = field
                    print(f"✅ Found username field: {field_id or field_name or 'no-id'}")
                
                # Password field
                if field_type.lower() == "password":
                    password_field = field
                    print(f"✅ Found password field: {field_id or field_name or 'no-id'}")
            
            # If we found login fields, use them
            if username_field and password_field:
                # Use first credential set from config
                credential_key = list(self.credentials.keys())[0]
                credentials = self.credentials[credential_key]
                
                print(f"🔑 Using credentials for: {credential_key}")
                
                # Clear and enter credentials with realistic typing delays
                username_field.clear()
                self._type_realistically(username_field, credentials["username"])
                time.sleep(random.uniform(0.5, 1.5))
                
                password_field.clear()
                self._type_realistically(password_field, credentials["password"])
                time.sleep(random.uniform(0.5, 1.5))
                
                # Find and click submit button
                submit_buttons = self.browser.find_elements(By.XPATH, 
                    "//button[@type='submit'] | //input[@type='submit'] | " +
                    "//button[contains(text(), 'Login') or contains(text(), 'Sign') or contains(text(), 'Submit')] | " +
                    "//input[@value and (contains(@value, 'Login') or contains(@value, 'Sign') or contains(@value, 'Submit'))]") 
                
                if submit_buttons:
                    # Before clicking, store current window handles
                    before_handles = set(self.browser.get_window_handles())
                    
                    print("🖱️ Clicking submit button...")
                    submit_buttons[0].click()
                    time.sleep(random.uniform(3, 6))
                    
                    # Check if a new tab was opened
                    after_handles = set(self.browser.get_window_handles())
                    new_handles = after_handles - before_handles
                    
                    if new_handles:
                        print(f"🔄 New tab detected after submit. Switching to it...")
                        new_handle = list(new_handles)[0]
                        self.browser.switch_to_window(new_handle)
                    
                    return True
                else:
                    print("⚠️ No submit button found after filling credentials")
                    return False
            else:
                print(f"⚠️ Login form not found automatically")
                print(f"  Username field found: {'Yes' if username_field else 'No'}")
                print(f"  Password field found: {'Yes' if password_field else 'No'}")
                return False
                
        except Exception as e:
            print(f"❌ Automatic login failed: {str(e)}")
            return False
    
    def _type_realistically(self, element, text):
        """Type text with realistic human-like delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))  # Random delay between keystrokes
    
    def _prompt_manual_login(self):
        """Prompt user to login manually"""
        print("\\n👤 Manual login required")
        print("📋 Instructions:")
        print("1. Complete the login process in the browser window")
        print("2. Enter your library card number and PIN")
        print("3. Click Login/Submit")
        print("4. Complete any additional authentication steps")
        print("5. The script will automatically detect when authentication is complete")
        print("\\n⏸️  You don't need to press Enter - the script will detect completion automatically")
    
    def _handle_unexpected_location(self):
        """Handle cases where we end up somewhere unexpected"""
        current_url = self.browser.driver.current_url
        page_title = self.browser.driver.title
        
        print(f"\\n🤔 Unexpected location detected:")
        print(f"  URL: {current_url}")
        print(f"  Title: {page_title}")
        
        # Check if we can still proceed
        if "error" in current_url.lower() or "error" in page_title.lower():
            print("❌ Error page detected - login likely failed")
            return False
        
        # Ask user if they want to continue
        print("\\n❓ The URL doesn't match expected patterns, but we might still be able to continue.")
        print("   Check the browser window to see if you're on a library or database page.")
        
        choice = input("\\n   Continue anyway? (y/n): ").lower().strip()
        if choice in ['y', 'yes', '']:
            print("✅ Continuing with current page...")
            return True
        else:
            print("❌ Aborting login process")
            return False
    
    def _handle_authentication_failure(self):
        """Handle authentication failure"""
        print("\\n❌ Authentication process failed")
        print("📋 Troubleshooting options:")
        print("1. Check your internet connection")
        print("2. Verify your library credentials in the config file")
        print("3. Try logging in manually through the library website")
        print("4. Contact your library for technical support")
        
        choice = input("\\n❓ Would you like to try manual navigation? (y/n): ").lower().strip()
        if choice in ['y', 'yes', '']:
            print("\\n👤 Please navigate to the ReferenceUSA search page manually")
            print("📋 Steps:")
            print("1. Go to your library's website")
            print("2. Find and access ReferenceUSA/Data-Axle database")
            print("3. Navigate to the U.S. Business database search")
            print("4. Look for 'Custom Search' or 'Advanced Search'")
            
            input("\\n⏸️  Press Enter when you've reached the search page...")
            
            # Try to verify we're on a search page
            if self.auth_handler._verify_search_page():
                print("✅ Search page detected - continuing with scraper")
                return True
            else:
                print("⚠️ Search page not clearly detected, but continuing anyway")
                return True
        else:
            return False
    
    def _handle_login_exception(self, exception):
        """Handle exceptions during login"""
        print(f"\\n💥 Unexpected error during login: {str(exception)}")
        print("📋 This might be due to:")
        print("1. Network connectivity issues")
        print("2. Changes in the library website")
        print("3. Browser/driver compatibility issues")
        print("4. Temporary website maintenance")
        
        # Take screenshot for debugging
        try:
            screenshot_path = f"login_error_{int(time.time())}.png"
            self.browser.driver.save_screenshot(screenshot_path)
            print(f"📸 Error screenshot saved: {screenshot_path}")
        except:
            pass
        
        choice = input("\\n❓ Would you like to try continuing anyway? (y/n): ").lower().strip()
        if choice in ['y', 'yes', '']:
            print("⚠️ Continuing despite error - manual intervention may be required")
            return True
        else:
            print("❌ Stopping due to login error")
            return False
