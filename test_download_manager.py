#!/usr/bin/env python3
"""
Test script for the enhanced Download Manager
This script tests the button detection logic and other improvements
"""

import sys
import os
import time
from unittest.mock import Mock, MagicMock

# Add the current directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_mock_browser():
    """Create a mock browser manager for testing"""
    mock_browser = Mock()
    mock_driver = Mock()
    
    # Mock the driver and its methods
    mock_browser.driver = mock_driver
    mock_browser.find_elements = Mock()
    
    return mock_browser

def create_mock_state():
    """Create a mock state manager for testing"""
    mock_state = Mock()
    mock_state.state = {
        "results_url": "https://example.com/results",
        "last_batch": 0,
        "total_batches": 10,
        "downloaded_files": []
    }
    mock_state.add_downloaded_file = Mock()
    mock_state.remove_batch_data = Mock()
    mock_state.update_last_batch = Mock()
    mock_state.add_completed_batch = Mock()
    
    return mock_state

def test_button_detection_strategies():
    """Test the button detection strategies"""
    print("🧪 Testing Button Detection Strategies...")
    
    try:
        # Import our download manager
        from download_manager import DownloadManager
        
        # Create mocks
        mock_browser = create_mock_browser()
        mock_state = create_mock_state()
        search_params = {
            'state': 'TestState',
            'pages_per_batch': 10
        }
        
        # Create download manager instance
        dm = DownloadManager(mock_browser, mock_state, search_params)
        
        print("✅ Successfully imported DownloadManager")
        print("✅ Successfully created DownloadManager instance")
        
        # Test 1: Mock finding a button with Strategy 1 (direct text)
        print("\n📋 Test 1: Direct text button detection")
        mock_button = Mock()
        mock_button.text = "DOWNLOAD RECORDS"
        mock_browser.find_elements.return_value = [mock_button]
        
        result = dm.find_download_records_button()
        assert result is not None, "Should find button with direct text"
        print("✅ Direct text detection works")
        
        # Test 2: Mock no buttons found
        print("\n📋 Test 2: No buttons found scenario")
        mock_browser.find_elements.return_value = []
        
        result = dm.find_download_records_button()
        assert result is None, "Should return None when no buttons found"
        print("✅ Gracefully handles no buttons found")
        
        # Test 3: Mock finding button with case-insensitive search
        print("\n📋 Test 3: Case-insensitive detection")
        mock_button2 = Mock()
        mock_button2.text = "download records"
        mock_button2.get_attribute = Mock(return_value="download records")
        
        # Mock the sequence: first calls return empty, case-insensitive call returns button
        mock_browser.find_elements.side_effect = [
            [],  # Strategy 1 - direct text (empty)
            [mock_button2],  # Strategy 2 - case insensitive (found)
        ]
        
        result = dm.find_download_records_button()
        assert result is not None, "Should find button with case-insensitive search"
        print("✅ Case-insensitive detection works")
        
        print("\n🎉 All button detection tests passed!")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure you're running this script from the Miller 3 Data Scaper directory")
        return False
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return False
    
    return True

def test_download_manager_initialization():
    """Test that the DownloadManager can be initialized properly"""
    print("\n🧪 Testing DownloadManager Initialization...")
    
    try:
        from download_manager import DownloadManager
        
        # Test with various configurations
        configs = [
            {'state': 'Alabama', 'pages_per_batch': 10},
            {'state': 'California', 'pages_per_batch': 5},
            {'state': 'Texas', 'pages_per_batch': 20},
        ]
        
        for config in configs:
            mock_browser = create_mock_browser()
            mock_state = create_mock_state()
            
            dm = DownloadManager(mock_browser, mock_state, config)
            
            assert dm.pages_per_batch == config['pages_per_batch']
            assert dm.search_parameters == config
            
            print(f"✅ Initialized with config: {config}")
        
        print("🎉 All initialization tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Testing File Structure...")
    
    required_files = [
        'download_manager.py',
        'reference_usa_scraper.py',
    ]
    
    optional_files = [
        'browser_manager.py',
        'state_manager.py',
        'login_manager.py',
        'search_manager.py',
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ Found required file: {file}")
        else:
            print(f"❌ Missing required file: {file}")
            return False
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ Found optional file: {file}")
        else:
            print(f"⚠️  Optional file not found: {file}")
    
    print("🎉 File structure check passed!")
    return True

def test_enhanced_methods():
    """Test that enhanced methods exist and are callable"""
    print("\n🧪 Testing Enhanced Methods...")
    
    try:
        from download_manager import DownloadManager
        
        mock_browser = create_mock_browser()
        mock_state = create_mock_state()
        search_params = {'state': 'TestState', 'pages_per_batch': 10}
        
        dm = DownloadManager(mock_browser, mock_state, search_params)
        
        # Check that our new method exists
        assert hasattr(dm, 'find_download_records_button'), "Missing find_download_records_button method"
        print("✅ find_download_records_button method exists")
        
        # Check that it's callable
        assert callable(dm.find_download_records_button), "find_download_records_button is not callable"
        print("✅ find_download_records_button is callable")
        
        # Check other required methods
        required_methods = [
            'navigate_to_page',
            'select_pages', 
            'download_selected_records',
            'download_batch'
        ]
        
        for method_name in required_methods:
            assert hasattr(dm, method_name), f"Missing {method_name} method"
            assert callable(getattr(dm, method_name)), f"{method_name} is not callable"
            print(f"✅ {method_name} method exists and is callable")
        
        print("🎉 All enhanced methods test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Methods Error: {e}")
        return False

def test_xpath_selectors():
    """Test that XPath selectors are valid"""
    print("\n🧪 Testing XPath Selectors...")
    
    # Common XPath patterns used in the button detection
    xpath_patterns = [
        "//button[contains(text(), 'DOWNLOAD RECORDS')]",
        "//button[contains(text(), 'Download Records')]",
        "//a[contains(text(), 'DOWNLOAD RECORDS')]",
        "//input[@type='submit' and contains(@value, 'DOWNLOAD RECORDS')]",
        "//button[contains(@class, 'download')]",
        "//div[contains(@class, 'download')]//button"
    ]
    
    try:
        # Try to validate XPath syntax (basic check)
        for xpath in xpath_patterns:
            # Basic validation - check for balanced brackets and quotes
            if xpath.count('[') != xpath.count(']'):
                raise ValueError(f"Unbalanced brackets in XPath: {xpath}")
            
            if xpath.count("'") % 2 != 0:
                raise ValueError(f"Unbalanced quotes in XPath: {xpath}")
            
            print(f"✅ Valid XPath: {xpath}")
        
        print("🎉 All XPath selectors are valid!")
        return True
        
    except Exception as e:
        print(f"❌ XPath Error: {e}")
        return False

def run_integration_test():
    """Run a mock integration test"""
    print("\n🧪 Running Integration Test...")
    
    try:
        from download_manager import DownloadManager
        
        # Create more realistic mocks
        mock_browser = create_mock_browser()
        mock_state = create_mock_state()
        
        # Mock a realistic browser interaction
        mock_button = Mock()
        mock_button.text = "DOWNLOAD RECORDS"
        mock_button.click = Mock()
        
        # Set up mock returns for different scenarios
        mock_browser.find_elements.side_effect = [
            [mock_button],  # First call finds the button
        ]
        
        mock_browser.driver.execute_script = Mock()
        mock_browser.driver.save_screenshot = Mock()
        
        search_params = {
            'state': 'TestState',
            'pages_per_batch': 10,
            'download_options': {}
        }
        
        dm = DownloadManager(mock_browser, mock_state, search_params)
        
        # Test the button finding
        result = dm.find_download_records_button()
        assert result is not None, "Should find button in integration test"
        assert result == mock_button, "Should return the correct button"
        
        print("✅ Integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integration Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Download Manager Test Suite")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Download Manager Initialization", test_download_manager_initialization),
        ("Enhanced Methods", test_enhanced_methods),
        ("XPath Selectors", test_xpath_selectors),
        ("Button Detection Strategies", test_button_detection_strategies),
        ("Integration Test", run_integration_test),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                failed += 1
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 TEST SUMMARY")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Your enhanced download manager is ready!")
        print("💡 You can now run your scraper and it should automatically handle downloads.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
        print("💡 Most likely issues:")
        print("   - Make sure you're in the Miller 3 Data Scaper directory")
        print("   - Check that download_manager.py was updated correctly")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
