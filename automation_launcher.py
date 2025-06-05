#!/usr/bin/env python3
"""
Miller 3 Data Scraper - Automation Diagnostic & Fix Launcher
Easy-to-use interface for running diagnostics and applying fixes
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
    print("🔬 MILLER 3 DATA SCRAPER - AUTOMATION DIAGNOSTIC & FIX LAUNCHER")
    print("=" * 70)
    print()
    print("This tool helps you diagnose and fix automation issues that require")
    print("manual interventions in your data scraper.")
    print()
    
    while True:
        print("📋 AVAILABLE OPTIONS:")
        print()
        print("1. 🔍 Run Automation Diagnostic Test")
        print("   - Identifies why automation is failing")
        print("   - Tests all automation components")
        print("   - Generates detailed report with screenshots")
        print("   - Provides specific recommendations")
        print()
        print("2. 🔧 Test Enhanced Automation Fix")
        print("   - Tests improved page navigation")
        print("   - Tests enhanced record selection")
        print("   - Tests advanced download button detection")
        print("   - Shows success rates for each component")
        print()
        print("3. 🚀 Run Enhanced Manual Scraper")
        print("   - Most reliable option with minimal manual steps")
        print("   - Manual authentication + automated processing")
        print("   - Enhanced error recovery and guidance")
        print("   - Recommended for production use")
        print()
        print("4. 📖 View Analysis & Solutions Documentation")
        print("   - Read detailed analysis of automation issues")
        print("   - See technical solutions implemented")
        print("   - Understand expected improvements")
        print()
        print("5. ❌ Exit")
        print()
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == "1":
            print("\n🔍 RUNNING AUTOMATION DIAGNOSTIC TEST...")
            print("=" * 50)
            print("This will test all automation components and identify issues.")
            print("You'll need to manually navigate to the search results page.")
            print()
            input("Press Enter to start the diagnostic test...")
            
            success = run_script("automation_diagnostic_test.py")
            if success:
                print("\n✅ Diagnostic test completed!")
                print("Check the generated diagnostic_report_*.json file for details.")
            else:
                print("\n❌ Diagnostic test encountered errors.")
            
        elif choice == "2":
            print("\n🔧 RUNNING ENHANCED AUTOMATION FIX TEST...")
            print("=" * 50)
            print("This will test the improved automation strategies.")
            print("You'll need to manually navigate to the search results page.")
            print()
            input("Press Enter to start the enhanced automation test...")
            
            success = run_script("enhanced_automation_fix.py")
            if success:
                print("\n✅ Enhanced automation test completed!")
            else:
                print("\n❌ Enhanced automation test encountered errors.")
            
        elif choice == "3":
            print("\n🚀 RUNNING ENHANCED MANUAL SCRAPER...")
            print("=" * 50)
            print("This is the most reliable option for production use.")
            print("It combines manual authentication with automated processing.")
            print()
            input("Press Enter to start the enhanced manual scraper...")
            
            success = run_script("manual_login_scraper.py")
            if success:
                print("\n✅ Enhanced manual scraper completed!")
            else:
                print("\n❌ Enhanced manual scraper encountered errors.")
            
        elif choice == "4":
            print("\n📖 VIEWING ANALYSIS & SOLUTIONS DOCUMENTATION...")
            print("=" * 50)
            
            try:
                with open("AUTOMATION_ANALYSIS_SOLUTIONS.md", "r") as f:
                    content = f.read()
                    print(content)
            except FileNotFoundError:
                print("❌ Documentation file not found.")
            except Exception as e:
                print(f"❌ Error reading documentation: {str(e)}")
            
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice. Please select 1-5.")
        
        if choice in ["1", "2", "3", "4"]:
            print("\n" + "=" * 70)
            input("Press Enter to return to main menu...")
            clear_screen()
            print("🔬 MILLER 3 DATA SCRAPER - AUTOMATION DIAGNOSTIC & FIX LAUNCHER")
            print("=" * 70)
            print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Launcher interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Launcher error: {str(e)}")
