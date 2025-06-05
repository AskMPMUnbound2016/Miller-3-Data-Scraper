#!/usr/bin/env python3
"""
Miller 3 Data Scraper - Simple Launcher
Essential tools only: Manual scraper and diagnostic
"""

import os
import sys
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_script(script_name):
    """Run a Python script and handle errors"""
    try:
        result = subprocess.run([sys.executable, script_name], cwd=os.getcwd())
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {script_name}: {str(e)}")
        return False

def main():
    clear_screen()
    print("🚀 MILLER 3 DATA SCRAPER - SIMPLE LAUNCHER")
    print("=" * 50)
    print()
    print("Essential tools for data scraping with minimal manual intervention")
    print()
    
    while True:
        print("📋 AVAILABLE OPTIONS:")
        print()
        print("1. 🚀 Run Manual Login Scraper (Recommended)")
        print("   - Manual authentication + automated processing")
        print("   - Most reliable option with minimal manual steps")
        print("   - Enhanced error recovery and guidance")
        print()
        print("2. 🔍 Run Diagnostic Test")
        print("   - Identifies automation issues")
        print("   - Tests all components")
        print("   - Generates detailed report")
        print()
        print("3. 🔧 Fix ChromeDriver Issues")
        print("   - Fixes path and permission problems")
        print("   - Required if you get ChromeDriver errors")
        print()
        print("4. ❌ Exit")
        print()
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == "1":
            print("\n🚀 RUNNING MANUAL LOGIN SCRAPER...")
            print("=" * 40)
            print("This is the most reliable scraper option.")
            print("You'll do manual authentication, then automation takes over.")
            print()
            input("Press Enter to start the manual login scraper...")
            
            success = run_script("manual_login_scraper.py")
            if success:
                print("\n✅ Manual login scraper completed!")
            else:
                print("\n❌ Manual login scraper encountered errors.")
            
        elif choice == "2":
            print("\n🔍 RUNNING DIAGNOSTIC TEST...")
            print("=" * 40)
            print("This will test all automation components.")
            print("You'll need to manually navigate to search results.")
            print()
            input("Press Enter to start the diagnostic test...")
            
            success = run_script("automation_diagnostic_test.py")
            if success:
                print("\n✅ Diagnostic test completed!")
                print("Check the generated diagnostic_report_*.json file for details.")
            else:
                print("\n❌ Diagnostic test encountered errors.")
            
        elif choice == "3":
            print("\n🔧 FIXING CHROMEDRIVER ISSUES...")
            print("=" * 40)
            print("This will fix ChromeDriver path and permission issues.")
            print()
            input("Press Enter to run the ChromeDriver fix...")
            
            success = run_script("fix_chromedriver_path.py")
            if success:
                print("\n✅ ChromeDriver fix completed!")
            else:
                print("\n❌ ChromeDriver fix encountered errors.")
            
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice. Please select 1-4.")
        
        if choice in ["1", "2", "3"]:
            print("\n" + "=" * 50)
            input("Press Enter to return to main menu...")
            clear_screen()
            print("🚀 MILLER 3 DATA SCRAPER - SIMPLE LAUNCHER")
            print("=" * 50)
            print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Launcher interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Launcher error: {str(e)}")
