#!/usr/bin/env python3
"""
CSV MERGER LAUNCHER - Miller 3 Data Scraper
===========================================
Quick launcher for the CSV file merger
"""

import os
import subprocess
import sys

def main():
    print("🔗 CSV FILE MERGER - MILLER 3 DATA SCRAPER")
    print("=" * 50)
    print()
    print("🔗 CSV MERGER FEATURES:")
    print("   ✅ Combine multiple downloaded CSV files")
    print("   ✅ Remove duplicate records automatically")
    print("   ✅ Choose specific files or merge all")
    print("   ✅ Limit by record count or date range")
    print("   ✅ Add source file tracking")
    print("   ✅ Smart filename suggestions")
    print()
    
    # Check if files exist
    merger_script = "csv_merger.py"
    if not os.path.exists(merger_script):
        print(f"❌ Error: {merger_script} not found!")
        print("Make sure you're in the correct directory.")
        input("Press Enter to exit...")
        return
    
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        print(f"❌ Error: {downloads_dir} directory not found!")
        print("No CSV files to merge.")
        input("Press Enter to exit...")
        return
    
    print("✅ All required files found")
    print()
    
    # Ask user to confirm
    start = input("🚀 Start CSV merger? (y/n): ").lower().strip()
    if start not in ['y', 'yes']:
        print("❌ Cancelled")
        return
    
    print("\n🚀 Starting CSV merger...")
    print("=" * 50)
    
    try:
        # Run the CSV merger script
        subprocess.run([sys.executable, merger_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running merger: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n📋 CSV merger complete")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
