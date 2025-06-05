#!/usr/bin/env python3
"""
Miller 3 Data Scraper - Enhanced Diagnostic with Better User Feedback
Shows clear status indicators and alerts when process is running
"""

import os
import sys
import time

def show_startup_alert():
    """Show clear startup alert"""
    print("\n" + "🔴" * 20 + " PROCESS STARTING " + "🔴" * 20)
    print("🚨 ALERT: DIAGNOSTIC TEST IS NOW RUNNING")
    print("🔄 STATUS: ACTIVE - Please wait...")
    print("💻 Opening browser and starting tests...")
    print("⏰ Expected duration: 5-10 minutes")
    print("⚠️  DO NOT close this terminal window")
    print("🔴" * 58)
    print()
    
    # Countdown to make it clear something is happening
    for i in range(3, 0, -1):
        print(f"🔄 Starting in {i} seconds...")
        time.sleep(1)
    
    print("🚀 STARTING NOW!")
    print()

def main():
    """Main function with enhanced user feedback"""
    print("🔬 MILLER 3 DATA SCRAPER - ENHANCED DIAGNOSTIC")
    print("=" * 55)
    
    # Show startup alert
    show_startup_alert()
    
    # Import and run the actual diagnostic
    try:
        # Change to the correct directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Import the diagnostic class
        from automation_diagnostic_test import AutomationDiagnosticTest
        
        print("🔄 STATUS: Initializing diagnostic system...")
        
        # Get config file
        config_file = 'config/referenceusa_config.yaml'
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        
        print("🔄 STATUS: Loading configuration...")
        print("🔄 STATUS: Setting up browser...")
        
        # Create and run diagnostic
        diagnostic = AutomationDiagnosticTest(config_file)
        
        print("\n🟢" + "=" * 50 + "🟢")
        print("🟢 DIAGNOSTIC SYSTEM READY - STARTING TESTS")
        print("🟢" + "=" * 50 + "🟢")
        
        diagnostic.run_comprehensive_diagnostic()
        
    except KeyboardInterrupt:
        print("\n\n🛑 PROCESS INTERRUPTED")
        print("🔄 STATUS: User pressed Ctrl+C")
        print("✅ Exiting safely...")
    except ImportError as e:
        print(f"\n❌ IMPORT ERROR: {e}")
        print("💡 Make sure automation_diagnostic_test.py is in the same folder")
    except Exception as e:
        print(f"\n❌ STARTUP ERROR: {e}")
        print("💡 Check that all required files are present")
    
    print("\n🏁 PROCESS COMPLETE")
    print("🔄 STATUS: Finished")

if __name__ == "__main__":
    main()
