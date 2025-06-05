import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class LoginManager:
    def __init__(self, browser_manager, auth_url, credentials):
        self.browser = browser_manager
        self.auth_url = auth_url
        self.credentials = credentials
        
        # Import the enhanced auth handler
        try:
            from enhanced_auth_handler import EnhancedAuthHandler
            self.enhanced_auth = EnhancedAuthHandler(browser_manager)
        except ImportError:
            print("⚠️ Enhanced auth handler not found, using fallback methods")
            self.enhanced_auth = None
    
    def login(self):
        """
        Enhanced login process that handles modern authentication flows
        """
        try:
            print("🔐 Starting enhanced login process...")
            
            # Store the original window handle
            original_handle = self.browser.get_current_window_handle()
            initial_handles = set(self.browser.get_window_handles())
            
            print(f"📱 Starting with {len(initial_handles)} tab(s)")
            
            # Step 1: Navigate to authentication page
            print("Step 1: Navigating to authentication page...")
            self.browser.navigate(self.auth_url)
            time.sleep(3)
            
            # Take screenshot of initial page
            self._take_screenshot("initial_auth_page")
            
            # Handle any immediate security challenges
            self.browser.handle_security_challenge()
            
            # Step 2: Attempt automatic login if form is detected
            print("Step 2: Looking for login form...")
            login_attempted = self._attempt_automatic_login()
            
            if not login_attempted:
                print("🔧 No login form found automatically")
                print("Please complete authentication manually in the browser")
                print("This may include:")
                print("  - Library card login")
                print("  - Multi-factor authentication")
                print("  - Terms acceptance")
                print("  - Database selection")
                
                input("⏸️ Press Enter when you've completed the initial login steps...")
            
            # Step 3: Use enhanced authentication handler for the complex flow
            print("Step 3: Starting enhanced authentication flow...")
            
            if self.enhanced_auth:
                # Use the enhanced handler for the complex authentication flow
                auth_success = self.enhanced_auth.handle_complete_auth_flow()
                
                if auth_success:
                    print("✅ Enhanced authentication flow completed successfully!")
                    return True
                else:
                    print("⚠️ Enhanced authentication flow had issues, but continuing...")
            
            # Step 4: Fallback verification
            print("Step 4: Performing final verification...")
            return self._verify_final_authentication()
            
        except Exception as e:
            print(f"❌ Login process encountered an error: {str(e)}")
            print("🔧 Attempting manual recovery...")
            return self._handle_login_error(e)
    
    def _attempt_automatic_login(self):
        """
        Attempt to automatically fill and submit login form if found
        """
        try:
            # Look for login form elements
            input_fields = self.browser.find_elements(By.TAG_NAME, "input")
            
            if not input_fields:
                print("No input fields found on page")
                return False
            
            username_field = None
            password_field = None
            
            # Identify username and password fields
            for field in input_fields:
                field_type = field.get_attribute("type") or ""
                field_id = (field.get_attribute("id") or "").lower()
                field_name = (field.get_attribute("name") or "").lower()
                field_placeholder = (field.get_attribute("placeholder") or "").lower()
                
                # Enhanced field detection
                username_indicators = ["user", "login", "barcode", "card", "email", "name", "id"]
                password_indicators = ["password", "pin", "pass"]
                
                if field_type.lower() in ["text", "email", "tel"] or not field_type:
                    if any(indicator in field_id or indicator in field_name or indicator in field_placeholder 
                           for indicator in username_indicators):
                        username_field = field
                        print(f"Found username field: {field_id or field_name or 'unnamed'}")
                
                if field_type.lower() == "password":
                    password_field = field
                    print(f"Found password field: {field_id or field_name or 'unnamed'}")
            
            # If we found both fields, use them
            if username_field and password_field:
                return self._fill_and_submit_login(username_field, password_field)
            
            # If only username field found, might be a multi-step process
            elif username_field:
                print("Found username field but no password field - might be multi-step login")
                return self._handle_multi_step_login(username_field)
            
            print("No recognizable login fields found")
            return False
            
        except Exception as e:
            print(f"Error in automatic login attempt: {str(e)}")
            return False
    
    def _fill_and_submit_login(self, username_field, password_field):
        """
        Fill and submit login form with credentials
        """
        try:
            # Get credentials from config
            if not self.credentials:
                print("No credentials provided in config")
                return False
            
            # Use first credential set from config
            credential_key = list(self.credentials.keys())[0]
            credentials = self.credentials[credential_key]
            
            print(f"Using credentials for: {credential_key}")
            
            # Fill username field
            username_field.clear()
            username_field.send_keys(credentials["username"])
            time.sleep(random.uniform(0.5, 1.5))
            
            # Fill password field
            password_field.clear()
            password_field.send_keys(credentials["password"])
            time.sleep(random.uniform(0.5, 1.5))
            
            # Store handles before submission to detect new tabs
            before_handles = set(self.browser.get_window_handles())
            
            # Try to submit the form
            submit_success = self._submit_login_form(username_field, password_field)
            
            if submit_success:
                print("✅ Login form submitted successfully")
                time.sleep(5)  # Wait for processing
                
                # Check for new tabs
                after_handles = set(self.browser.get_window_handles())
                new_handles = after_handles - before_handles
                
                if new_handles:
                    print(f"🆕 {len(new_handles)} new tab(s) opened after login")
                    # Note: Enhanced auth handler will manage tab switching
                
                return True
            else:
                print("❌ Failed to submit login form")
                return False
                
        except Exception as e:
            print(f"Error filling login form: {str(e)}")
            return False
    
    def _handle_multi_step_login(self, username_field):
        """
        Handle multi-step login process (username first, then password)
        """
        try:
            if not self.credentials:
                return False
            
            credential_key = list(self.credentials.keys())[0]
            credentials = self.credentials[credential_key]
            
            print("Handling multi-step login - entering username first")
            
            # Fill username
            username_field.clear()
            username_field.send_keys(credentials["username"])
            time.sleep(1)
            
            # Try to submit or continue
            username_field.send_keys(Keys.ENTER)
            time.sleep(3)
            
            # Look for password field on new page
            password_fields = self.browser.find_elements(By.XPATH, "//input[@type='password']")
            
            if password_fields:
                print("Found password field on next step")
                password_fields[0].clear()
                password_fields[0].send_keys(credentials["password"])
                time.sleep(1)
                
                # Submit password
                password_fields[0].send_keys(Keys.ENTER)
                time.sleep(3)
                
                return True
            else:
                print("No password field found after username submission")
                return False
                
        except Exception as e:
            print(f"Error in multi-step login: {str(e)}")
            return False
    
    def _submit_login_form(self, username_field, password_field):
        """
        Submit login form using various methods
        """
        # Method 1: Look for submit button
        submit_buttons = self.browser.find_elements(By.XPATH, 
            "//button[@type='submit'] | //input[@type='submit'] | " +
            "//button[contains(text(), 'Login') or contains(text(), 'Sign') or contains(text(), 'Submit')] | " +
            "//input[contains(@value, 'Login') or contains(@value, 'Sign') or contains(@value, 'Submit')]")
        
        if submit_buttons:
            print("Clicking submit button...")
            submit_buttons[0].click()
            return True
        
        # Method 2: Press Enter on password field
        print("No submit button found, pressing Enter on password field...")
        password_field.send_keys(Keys.ENTER)
        return True
    
    def _verify_final_authentication(self):
        """
        Verify that authentication was successful
        """
        try:
            # Check current state
            current_url = self.browser.driver.current_url.lower()
            page_title = self.browser.driver.title.lower()
            
            print(f"Final verification:")
            print(f"  URL: {current_url}")
            print(f"  Title: {page_title}")
            
            # Reference indicators
            reference_indicators = ["referenceusa.com", "usbusiness", "data-axle"]
            
            # Check URL
            if any(indicator in current_url for indicator in reference_indicators):
                print("✅ URL indicates successful authentication")
                self._take_screenshot("successful_authentication")
                return True
            
            # Check title
            title_indicators = ["u.s. businesses", "business", "database", "reference", "data-axle"]
            if any(indicator in page_title for indicator in title_indicators):
                print("✅ Page title indicates successful authentication")
                self._take_screenshot("successful_authentication")
                return True
            
            # Check all open tabs
            print("🔍 Checking all open tabs for authentication success...")
            all_handles = self.browser.get_window_handles()
            
            for i, handle in enumerate(all_handles):
                try:
                    self.browser.switch_to_window(handle)
                    tab_url = self.browser.driver.current_url.lower()
                    tab_title = self.browser.driver.title.lower()
                    
                    print(f"  Tab {i+1}: {tab_title[:40]}...")
                    
                    if (any(indicator in tab_url for indicator in reference_indicators) or
                        any(indicator in tab_title for indicator in title_indicators)):
                        print(f"✅ Found authentication success in tab {i+1}")
                        self._take_screenshot(f"successful_auth_tab_{i+1}")
                        return True
                        
                except Exception as e:
                    print(f"  Error checking tab {i+1}: {str(e)}")
                    continue
            
            # If no clear indicators, ask user
            print("⚠️ Cannot automatically verify authentication success")
            print("Current page may require manual verification")
            
            self._take_screenshot("verification_unclear")
            
            choice = input("Does the current page show successful authentication? (y/n): ").lower().strip()
            return choice in ['y', 'yes', '']
            
        except Exception as e:
            print(f"Error in final verification: {str(e)}")
            return True  # Continue anyway
    
    def _handle_login_error(self, error):
        """
        Handle errors during login process
        """
        print(f"🔧 Handling login error: {str(error)}")
        
        # Take screenshot for debugging
        self._take_screenshot("login_error")
        
        # Check if we might actually be authenticated despite the error
        current_url = self.browser.driver.current_url.lower()
        reference_indicators = ["referenceusa.com", "proxy.openathens.net", "usbusiness", "data-axle"]
        
        if any(indicator in current_url for indicator in reference_indicators):
            print("✅ Despite error, appears to be on ReferenceUSA - continuing")
            return True
        
        # Offer manual recovery
        print("\n🔧 Manual recovery options:")
        print("1. Complete authentication manually in the browser")
        print("2. Check for popup blockers or security restrictions")
        print("3. Verify library credentials are correct")
        print("4. Try refreshing the page")
        
        input("Press Enter when you've resolved the authentication issue...")
        
        # Re-verify after manual intervention
        return self._verify_final_authentication()
    
    def _take_screenshot(self, name):
        """
        Take a screenshot with timestamp for debugging
        """
        try:
            timestamp = int(time.time())
            filename = f"{name}_{timestamp}.png"
            self.browser.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
        except Exception as e:
            print(f"❌ Screenshot failed: {str(e)}")
    
    def get_authentication_status(self):
        """
        Get detailed authentication status for debugging
        """
        try:
            status = {
                'current_url': self.browser.driver.current_url,
                'page_title': self.browser.driver.title,
                'tab_count': len(self.browser.get_window_handles()),
                'timestamp': time.time()
            }
            
            # Add enhanced status if available
            if self.enhanced_auth:
                status['enhanced_status'] = self.enhanced_auth.get_current_status()
            
            return status
            
        except Exception as e:
            return {'error': str(e)}
    
    def debug_current_state(self):
        """
        Print debug information about current state
        """
        print("\n🔍 DEBUG: Current Authentication State")
        print("=" * 50)
        
        try:
            status = self.get_authentication_status()
            
            print(f"URL: {status.get('current_url', 'Unknown')}")
            print(f"Title: {status.get('page_title', 'Unknown')}")
            print(f"Tab Count: {status.get('tab_count', 'Unknown')}")
            
            if 'enhanced_status' in status:
                enhanced = status['enhanced_status']
                print(f"Enhanced Auth Score: {enhanced.get('auth_score', 'N/A')}")
                print(f"Is Database Selection: {enhanced.get('is_database_selection', 'N/A')}")
                print(f"Is Search Page: {enhanced.get('is_search_page', 'N/A')}")
            
            # Check for login form elements
            input_fields = self.browser.find_elements(By.TAG_NAME, "input")
            print(f"Input Fields Found: {len(input_fields)}")
            
            if input_fields:
                print("Input Field Types:")
                for i, field in enumerate(input_fields[:5]):  # Show first 5
                    field_type = field.get_attribute("type") or "text"
                    field_id = field.get_attribute("id") or "no-id"
                    print(f"  {i+1}. Type: {field_type}, ID: {field_id}")
            
        except Exception as e:
            print(f"Error getting debug info: {str(e)}")
        
        print("=" * 50)
