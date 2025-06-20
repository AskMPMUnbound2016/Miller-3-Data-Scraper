#!/usr/bin/env python3
"""
SIMPLE MANUAL LAUNCHER - Miller 3 Data Scraper
==============================================
Simplified manual-only process with user control
"""

import os
import subprocess
import sys

def main():
    print("🔧 MILLER 3 DATA SCRAPER - NO PAGINATION MODE")
    print("=" * 50)
    print()
    print("📋 NO PAGINATION FEATURES:")
    print("   ✅ Manual login once")
    print("   👤 YOU: Navigate to each page manually")
    print("   🤖 AUTO: Select records on each page")
    print("   🤖 AUTO: Download and save files")
    print("   🤖 AUTO: Uncheck prior batch records")
    print("   ✅ Step-by-step guidance for navigation")
    print("   ✅ Select page ranges (up to 10 pages per batch)")
    print("   ✅ Session state saved (resume if interrupted)")
    print()
    
    # Check if files exist
    manual_script = "manual_process_simple.py"
    if not os.path.exists(manual_script):
        print(f"❌ Error: {manual_script} not found!")
        print("Make sure you're in the correct directory.")
        input("Press Enter to exit...")
        return
    
    chromedriver = "./chromedriver"
    if not os.path.exists(chromedriver):
        print(f"❌ Error: chromedriver not found!")
        print("Please ensure chromedriver is in the same folder.")
        input("Press Enter to exit...")
        return
    
    print("✅ All required files found")
    print()
    
    # Ask user to confirm
    start = input("🚀 Start NO PAGINATION scraper? (y/n): ").lower().strip()
    if start not in ['y', 'yes']:
        print("❌ Cancelled")
        return
    
    print("\n🚀 Starting NO PAGINATION scraper...")
    print("=" * 50)
    
    try:
        # Run the manual process script
        subprocess.run([sys.executable, manual_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running scraper: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n📋 NO PAGINATION process complete")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
