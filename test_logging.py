#!/usr/bin/env python3
"""
Test script for the new logging system
"""

import os
import sys

def test_logging_system():
    """Test the new logging system"""
    print("🧪 Testing New Logging System...")
    
    try:
        # Import the logging manager
        from logging_manager import get_logger, ScraperLogger
        
        # Create a test logger
        logger = ScraperLogger("test_session")
        
        print("✅ Successfully created logger")
        
        # Test basic logging
        logger.log_batch_start(1, 1, 10)
        logger.log_download_start(1)
        logger.log_download_success(1, "test_file.csv")
        logger.log_batch_end(1, True, "test_file.csv")
        
        print("✅ Basic logging methods work")
        
        # Test session end
        stats = {
            "Batches Processed": 1,
            "Files Downloaded": 1,
            "Total Records": 100
        }
        logger.log_session_end(stats)
        
        print("✅ Session logging works")
        
        # Check if log directories were created
        expected_dirs = [
            "logs",
            "logs/screenshots", 
            "logs/session_logs",
            "logs/debug"
        ]
        
        for dir_path in expected_dirs:
            if os.path.exists(dir_path):
                print(f"✅ Directory created: {dir_path}")
            else:
                print(f"❌ Missing directory: {dir_path}")
                return False
        
        # Check if log files were created
        if os.path.exists("logs/session_logs") and os.listdir("logs/session_logs"):
            print("✅ Session log files created")
        else:
            print("❌ No session log files found")
        
        if os.path.exists("logs/debug") and os.listdir("logs/debug"):
            print("✅ Debug log files created")
        else:
            print("❌ No debug log files found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_download_manager_integration():
    """Test that download manager can use the new logging"""
    print("\n🧪 Testing Download Manager Integration...")
    
    try:
        from unittest.mock import Mock
        from download_manager import DownloadManager
        
        # Create mocks
        mock_browser = Mock()
        mock_browser.driver = Mock()
        mock_browser.find_elements = Mock(return_value=[])
        
        mock_state = Mock()
        mock_state.state = {"results_url": "test"}
        
        search_params = {'state': 'TestState', 'pages_per_batch': 10}
        
        # Create download manager with logging
        dm = DownloadManager(mock_browser, mock_state, search_params)
        
        print("✅ DownloadManager created with logging")
        
        # Test that logger is available
        assert hasattr(dm, 'logger'), "DownloadManager should have logger"
        assert dm.logger is not None, "Logger should not be None"
        
        print("✅ Logger properly integrated with DownloadManager")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run logging tests"""
    print("🚀 Testing New Logging System")
    print("=" * 50)
    
    tests = [
        ("Logging System Creation", test_logging_system),
        ("Download Manager Integration", test_download_manager_integration),
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
            print(f"❌ {test_name} FAILED: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 LOGGING TEST SUMMARY")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 LOGGING SYSTEM READY!")
        print("📁 Log files will be organized in:")
        print("   logs/session_logs/  - Main session logs")
        print("   logs/debug/         - Detailed debug logs") 
        print("   logs/screenshots/   - All screenshots")
        print("\n💡 Your scraper will now create organized logs!")
    else:
        print(f"\n⚠️  Some tests failed. Check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
