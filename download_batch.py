
def _process_batch_2025(self, start_page, end_page, download_xpaths=None, format_xpaths=None):
    """Process a batch of pages with the 2025 Data Axle interface"""
    try:
        print(f"\nProcessing pages {start_page} through {end_page}")
        
        # Track which pages we've processed in this batch
        processed_pages = []
        
        # Process each page in the batch, selecting all records on each page
        current_page = start_page
        while current_page <= end_page:
            print(f"\n=== Processing Page {current_page} ===")
            
            # If we're not on the first page of the batch, navigate to this page
            if current_page != start_page or len(processed_pages) > 0:
                self._navigate_to_page(current_page)
                time.sleep(2)  # Wait for page to load
            
            # Take screenshot of the current page
            self._take_screenshot(f"page_{current_page}_before_selection")
            
            # Select all records on this page
            self._handle_record_selection_2025()
            
            # Mark this page as processed
            processed_pages.append(current_page)
            print(f"Selected records on page {current_page}")
            
            # Take screenshot after selection
            self._take_screenshot(f"page_{current_page}_after_selection")
            
            # Move to next page in the batch
            current_page += 1
            
            # If we have more pages to process in this batch, navigate to the next page
            if current_page <= end_page:
                print(f"Moving to page {current_page}...")
            else:
                print(f"Completed selecting records for all pages in batch ({start_page}-{end_page})")
        
        # Now that we've selected records from all pages in the batch, download them
        print("\n=== Downloading Selected Records ===")
        
        # Take a screenshot before starting download
        self._take_screenshot("before_download_process")
        
        # 1. Click Download button from the main results page
        print("Looking for Download button...")
        download_clicked = False
        
        # First look for the Download button in the navigation menu
        nav_download_xpaths = [
            "//a[text()='Download']",
            "//button[text()='Download']",
            "//a[@id='download-button']",
            "//a[contains(@class, 'download')]",
            "//button[contains(@class, 'download')]"
        ]
        
        for xpath in nav_download_xpaths:
            elements = self.driver.find_elements(By.XPATH, xpath)
            if elements:
                for element in elements:
                    if self._is_element_visible(element):
                        try:
                            print(f"Clicking Download button: {element.text}")
                            element.click()
                            download_clicked = True
                            break
                        except:
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                                download_clicked = True
                                break
                            except:
                                continue
                
                if download_clicked:
                    break
        
        # If still not clicked, try the other download xpaths
        if not download_clicked and download_xpaths:
            for xpath in download_xpaths:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements:
                    for element in elements:
                        if self._is_element_visible(element):
                            try:
                                print(f"Clicking download button: {element.text}")
                                element.click()
                                download_clicked = True
                                break
                            except:
                                try:
                                    self.driver.execute_script("arguments[0].click();", element)
                                    download_clicked = True
                                    break
                                except:
                                    continue
                    
                    if download_clicked:
                        break
        
        # If automated methods failed, ask for manual help
        if not download_clicked:
            print("Could not find or click download button automatically.")
            print("Please click the Download button manually.")
            input("Press Enter after clicking the Download button...")
            download_clicked = True  # Assume user did it successfully
        
        # Wait for download dialog to appear
        time.sleep(3)
        
        # Take screenshot of download dialog
        self._take_screenshot("download_dialog")
        
        # 2. Select file format (CSV by default)
        print("Selecting CSV format...")
        format_selected = False
        
        # Try to find the format radio buttons
        csv_format_xpaths = [
            "//input[@type='radio'][@value='csv' or @id='csv']",
            "//label[contains(text(), 'Comma') or contains(text(), 'CSV')]/input[@type='radio']",
            "//label[contains(text(), 'Comma') or contains(text(), 'CSV')]",
            "//input[@type='radio'][contains(@id, 'comma') or contains(@name, 'comma')]"
        ]
        
        for xpath in csv_format_xpaths:
            elements = self.driver.find_elements(By.XPATH, xpath)
            if elements:
                for element in elements:
                    try:
                        if element.is_displayed():
                            try:
                                element.click()
                                print("Selected CSV format")
                                format_selected = True
                                break
                            except:
                                try:
                                    self.driver.execute_script("arguments[0].click();", element)
                                    print("Selected CSV format via JavaScript")
                                    format_selected = True
                                    break
                                except:
                                    continue
                    except:
                        continue
                
                if format_selected:
                    break
        
        # If standard methods failed, try to find labels that wrap radio buttons
        if not format_selected:
            label_xpaths = [
                "//label[contains(text(), 'Comma') or contains(text(), 'CSV')]",
                "//span[contains(text(), 'Comma') or contains(text(), 'CSV')]"
            ]
            
            for xpath in label_xpaths:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements:
                    for element in elements:
                        if self._is_element_visible(element):
                            try:
                                element.click()
                                print("Selected CSV format via label")
                                format_selected = True
                                break
                            except:
                                try:
                                    self.driver.execute_script("arguments[0].click();", element)
                                    print("Selected CSV format via JavaScript on label")
                                    format_selected = True
                                    break
                                except:
                                    continue
                    
                    if format_selected:
                        break
        
        # If still not selected, ask for manual help
        if not format_selected:
            print("Could not select CSV format automatically. Please select CSV format manually.")
            input("Press Enter when you've selected CSV format...")
        
        # Wait a moment for any UI updates
        time.sleep(1)
        
        # 3. Select detail level (Detailed by default)
        print("Selecting Detailed data level...")
        detail_selected = False
        
        # Try to find the Detailed radio button
        detailed_xpaths = [
            "//input[@type='radio'][@value='detailed' or @id='detailed']",
            "//label[contains(text(), 'Detailed')]/input[@type='radio']",
            "//label[contains(text(), 'Detailed')]",
            "//input[@type='radio'][contains(@id, 'detailed') or contains(@name, 'detailed')]"
        ]
        
        for xpath in detailed_xpaths:
            elements = self.driver.find_elements(By.XPATH, xpath)
            if elements:
                for element in elements:
                    try:
                        if element.is_displayed():
                            try:
                                element.click()
                                print("Selected Detailed data level")
                                detail_selected = True
                                break
                            except:
                                try:
                                    self.driver.execute_script("arguments[0].click();", element)
                                    print("Selected Detailed data level via JavaScript")
                                    detail_selected = True
                                    break
                                except:
                                    continue
                    except:
                        continue
                
                if detail_selected:
                    break
        
        # If standard methods failed, try to find labels
        if not detail_selected:
            label_xpaths = [
                "//label[contains(text(), 'Detailed')]",
                "//span[contains(text(), 'Detailed')]"
            ]
            
            for xpath in label_xpaths:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements:
                    for element in elements:
                        if self._is_element_visible(element):
                            try:
                                element.click()
                                print("Selected Detailed data level via label")
                                detail_selected = True
                                break
                            except:
                                try:
                                    self.driver.execute_script("arguments[0].click();", element)
                                    print("Selected Detailed data level via JavaScript on label")
                                    detail_selected = True
                                    break
                                except:
                                    continue
                    
                    if detail_selected:
                        break
        
        # If still not selected, ask for manual help
        if not detail_selected:
            print("Could not select Detailed data level automatically. Please select Detailed data level manually.")
            input("Press Enter when you've selected Detailed data level...")
        
        # Take screenshot after format and detail selection
        self._take_screenshot("after_format_detail_selection")
        
        # 4. Click the "Download Records" button
        print("Looking for 'Download Records' button...")
        download_records_clicked = False
        
        download_records_xpaths = [
            "//button[contains(text(), 'DOWNLOAD RECORDS')]",
            "//button[contains(text(), 'Download Records')]",
            "//input[@type='button'][contains(@value, 'Download')]",
            "//a[contains(text(), 'DOWNLOAD RECORDS')]",
            "//a[contains(text(), 'Download Records')]",
            "//button[contains(@class, 'download')]",
            "//input[contains(@class, 'download')]"
        ]
        
        for xpath in download_records_xpaths:
            elements = self.driver.find_elements(By.XPATH, xpath)
            if elements:
                for element in elements:
                    if self._is_element_visible(element):
                        try:
                            print(f"Clicking Download Records button: {element.text}")
                            element.click()
                            download_records_clicked = True
                            break
                        except:
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                                print("Clicked Download Records button via JavaScript")
                                download_records_clicked = True
                                break
                            except:
                                continue
                
                if download_records_clicked:
                    break
        
        # If standard buttons fail, try looking for any buttons on the page
        if not download_records_clicked:
            buttons = self.driver.find_elements(By.XPATH, "//button | //input[@type='button'] | //input[@type='submit']")
            for button in buttons:
                if self._is_element_visible(button):
                    try:
                        button_text = button.text.lower() if hasattr(button, 'text') else ''
                        button_value = button.get_attribute('value') or ''
                        
                        if 'download' in button_text or 'download' in button_value:
                            print(f"Trying button: {button_text or button_value}")
                            button.click()
                            download_records_clicked = True
                            break
                    except:
                        try:
                            self.driver.execute_script("arguments[0].click();", button)
                            download_records_clicked = True
                            break
                        except:
                            continue
        
        # If still not clicked, ask for manual help
        if not download_records_clicked:
            print("Could not find or click Download Records button automatically.")
            print("Please click the Download Records button manually.")
            input("Press Enter after clicking the Download Records button...")
        
        # Wait for download to complete
        input("Press Enter when the download is complete...")
        print(f"Downloaded data for pages {start_page} through {end_page}")
        
        # 5. Navigate back to results if there are more pages to process
        if end_page < int(self.pages_to_download):
            print("\nNavigating back to results page...")
            
            # Look for Back or Revise Search buttons
            back_xpaths = [
                "//a[contains(text(), 'Back')]",
                "//button[contains(text(), 'Back')]",
                "//a[contains(text(), 'Revise Search')]",
                "//button[contains(text(), 'Revise Search')]",
                "//a[contains(@class, 'back')]",
                "//button[contains(@class, 'back')]"
            ]
            
            back_clicked = False
            for xpath in back_xpaths:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements:
                    for element in elements:
                        if self._is_element_visible(element):
                            try:
                                print(f"Clicking back button: {element.text}")
                                element.click()
                                back_clicked = True
                                break
                            except:
                                try:
                                    self.driver.execute_script("arguments[0].click();", element)
                                    back_clicked = True
                                    break
                                except:
                                    continue
                    
                    if back_clicked:
                        break
            
            # If no back button found, try browser back button
            if not back_clicked:
                try:
                    print("Using browser back button")
                    self.driver.back()
                    back_clicked = True
                except:
                    print("Could not navigate back automatically")
            
            # If still not navigated back, ask for manual help
            if not back_clicked:
                print("Could not navigate back automatically. Please navigate back to the results page manually.")
                input("Press Enter when you've returned to the results page...")
            
            # Wait for page to load
            time.sleep(3)
            
            # 6. Uncheck all records from the downloaded batch
            print("\n=== Unchecking all records from the downloaded batch ===")
            
            # For each page we processed, go back and uncheck all records
            for page in processed_pages:
                print(f"\nNavigating back to page {page} to uncheck records...")
                self._navigate_to_page(page)
                time.sleep(2)  # Wait for page to load
                
                # Uncheck all records on this page
                self._uncheck_all_records()
                
                # Take screenshot after unchecking
                self._take_screenshot(f"page_{page}_after_unchecking")
        
        print(f"\nSuccessfully processed and downloaded pages {start_page} through {end_page}")
        return True
        
    except Exception as e:
        print(f"Error processing batch: {str(e)}")
        print("Please try downloading manually.")
        input("Press Enter to continue...")
        return False

def _uncheck_all_records(self):
    """Uncheck all checkboxes on the current page"""
    print("Unchecking all records on the current page...")
    
    try:
        # Take screenshot before unchecking
        self._take_screenshot("before_unchecking")
        
        # First, try to find an "Unselect All" option if it exists
        unselect_all_xpaths = [
            "//a[contains(text(), 'Unselect All')]",
            "//button[contains(text(), 'Unselect All')]",
            "//a[contains(text(), 'Deselect All')]",
            "//button[contains(text(), 'Deselect All')]",
            "//span[contains(text(), 'Unselect All')]",
            "//span[contains(text(), 'Deselect All')]"
        ]
        
        unselect_all_clicked = False
        for xpath in unselect_all_xpaths:
            elements = self.driver.find_elements(By.XPATH, xpath)
            if elements:
                for element in elements:
                    if self._is_element_visible(element):
                        try:
                            print(f"Clicking {element.text} button")
                            element.click()
                            unselect_all_clicked = True
                            time.sleep(1)  # Wait for checkboxes to update
                            break
                        except:
                            try:
                                self.driver.execute_script("arguments[0].click();", element)
                                unselect_all_clicked = True
                                time.sleep(1)
                                break
                            except:
                                continue
                
                if unselect_all_clicked:
                    break
        
        # If we found and clicked an Unselect All option, verify it worked
        if unselect_all_clicked:
            # Check if any checkboxes are still selected
            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            selected_checkboxes = [cb for cb in checkboxes if cb.is_selected()]
            
            if not selected_checkboxes:
                print("Successfully unchecked all records using 'Unselect All' option")
                return True
            else:
                print(f"'Unselect All' option didn't work completely. {len(selected_checkboxes)} checkboxes still selected.")
                # Continue to individual checkbox unchecking
        
        # If no Unselect All option or it didn't work, try to find all checked checkboxes and uncheck them
        print("Looking for checked checkboxes...")
        
        # Find all selected checkboxes
        checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        selected_checkboxes = [cb for cb in checkboxes if cb.is_selected()]
        
        if selected_checkboxes:
            print(f"Found {len(selected_checkboxes)} selected checkboxes")
            
            # Uncheck each checkbox
            success_count = 0
            for i, checkbox in enumerate(selected_checkboxes):
                try:
                    if checkbox.is_selected():
                        try:
                            # Try direct click
                            checkbox.click()
                            if not checkbox.is_selected():
                                success_count += 1
                        except:
                            try:
                                # Try JavaScript click
                                self.driver.execute_script("arguments[0].click();", checkbox)
                                if not checkbox.is_selected():
                                    success_count += 1
                            except:
                                try:
                                    # Try setting checked property directly
                                    self.driver.execute_script("""
                                        arguments[0].checked = false;
                                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                                    """, checkbox)
                                    if not checkbox.is_selected():
                                        success_count += 1
                                except:
                                    pass
                except:
                    pass
                
                # Print progress periodically
                if (i + 1) % 5 == 0 or i == len(selected_checkboxes) - 1:
                    print(f"Unchecked {success_count} of {len(selected_checkboxes)} checkboxes...")
            
            if success_count > 0:
                print(f"Successfully unchecked {success_count} checkboxes")
                return True
            else:
                print("Failed to uncheck any checkboxes via direct methods")
        else:
            print("No selected checkboxes found")
        
        # If individual unchecking failed or no checkboxes found, try using JavaScript to uncheck all
        try:
            print("Attempting to uncheck all checkboxes via JavaScript...")
            
            uncheck_count = self.driver.execute_script("""
                var checkboxes = document.querySelectorAll('input[type="checkbox"]');
                var count = 0;
                
                checkboxes.forEach(function(checkbox) {
                    if (checkbox.checked) {
                        checkbox.checked = false;
                        checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                        count++;
                    }
                });
                
                return count;
            """)
            
            if uncheck_count > 0:
                print(f"Unchecked {uncheck_count} checkboxes via JavaScript")
                return True
            else:
                print("No checkboxes unchecked via JavaScript")
        except Exception as js_error:
            print(f"JavaScript unchecking failed: {str(js_error)}")
        
        # If all attempts fail, ask for manual help
        print("\nAutomated unchecking failed. Please uncheck all records manually.")
        input("Press Enter when you've unchecked all records...")
        return True
            
    except Exception as e:
        print(f"Error unchecking records: {str(e)}")
        print("Please uncheck records manually.")
        input("Press Enter when you've unchecked all records...")
        return True
