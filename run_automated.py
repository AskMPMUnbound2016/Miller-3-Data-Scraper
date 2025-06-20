#!/usr/bin/env python3
"""
AUTOMATED LAUNCHER - Miller 3 Data Scraper
==========================================
Manual login + Automated checkbox selection, pagination, and downloading
"""

import os
import subprocess
import sys

def main():
    print("🤖 MILLER 3 DATA SCRAPER - PAGINATION MODE")
    print("=" * 50)
    print()
    print("🎯 PAGINATION FEATURES:")
    print("   ✅ Manual login once")
    print("   🤖 AUTO: Navigate to each page automatically")
    print("   🤖 AUTO: Select records on each page")
    print("   🤖 AUTO: Download and save files")
    print("   🤖 AUTO: Uncheck prior batch records")
    print("   🤖 AUTO: Process batches (1-10 pages each)")
    print("   🤖 AUTO: Repeat until all pages complete")
    print("   💾 AUTO: Save session state (resume if interrupted)")
    print()
    
    # Check if files exist
    automated_script = "semi_automated_scraper.py"
    if not os.path.exists(automated_script):
        print(f"❌ Error: {automated_script} not found!")
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
    
    print("📋 PROCESS OVERVIEW:")
    print("   1. 👤 You log in manually to the website")
    print("   2. 👤 You navigate to search results")
    print("   3. 🤖 Script detects total pages automatically")
    print("   4. 👤 You choose page range to download")
    print("   5. 🤖 Script processes batches automatically:")
    print("      • Automatically navigates to pages 1-10")
    print("      • Automatically selects records on each page")
    print("      • Automatically downloads the batch")
    print("      • Automatically unchecks all boxes")
    print("      • Moves to pages 11-20")
    print("      • Repeats until done")
    print()
    
    # Ask user to confirm
    start = input("🚀 Start PAGINATION scraper? (y/n): ").lower().strip()
    if start not in ['y', 'yes']:
        print("❌ Cancelled")
        return
    
    print("\n🚀 Starting PAGINATION scraper...")
    print("=" * 50)
    
    try:
        # Run the automated script
        subprocess.run([sys.executable, automated_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running scraper: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n📋 PAGINATION process complete")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
