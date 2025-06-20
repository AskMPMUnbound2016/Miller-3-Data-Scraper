#!/usr/bin/env python3
"""
MILLER 3 DATA SCRAPER - MAIN LAUNCHER
====================================
Two Simple Options:
1. Pagination (Automated) - Manual login + Automated pagination and selection
2. No Pagination (Manual) - Manual login + Manual pagination and selection
"""

import os
import sys

def show_simple_menu():
    """Show the simplified two-option menu"""
    print("🎯" + "="*50 + "🎯")
    print("      MILLER 3 DATA SCRAPER")
    print("🎯" + "="*50 + "🎯")
    print()
    print("📋 AVAILABLE OPTIONS:")
    print()
    print("1. 🤖 PAGINATION")
    print("   • Manual login once")
    print("   • Automated page navigation")
    print("   • Automated record selection and downloading")
    print("   • Automated unchecking of prior batch records")
    print()
    print("2. 📋 NO PAGINATION") 
    print("   • Manual login once")
    print("   • Manual page navigation (you go to each page)")
    print("   • Automated record selection and downloading")
    print("   • Automated unchecking of prior batch records")
    print()
    print("3. 🔗 MERGE CSV FILES")
    print("   • Combine multiple downloaded CSV files")
    print("   • Remove duplicates automatically")
    print("   • Choose specific files or merge all")
    print("   • Limit by record count or date range")
    print()
    print("4. ❌ Exit")
    print()

def main():
    """Main entry point with simplified menu"""
    try:
        show_simple_menu()
        
        while True:
            choice = input("🔢 Choose option (1, 2, 3, or 4): ").strip()
            
            if choice == '1':
                print("\n🤖 Starting PAGINATION mode...")
                print("=" * 40)
                
                # Check if enhanced scraper exists
                if os.path.exists('run_enhanced_scraper.py'):
                    print("🚀 Launching automated pagination scraper...")
                    import subprocess
                    subprocess.run([sys.executable, 'run_enhanced_scraper.py'])
                elif os.path.exists('semi_automated_scraper.py'):
                    print("🚀 Launching automated scraper...")
                    import subprocess
                    subprocess.run([sys.executable, 'semi_automated_scraper.py'])
                else:
                    print("❌ Pagination scraper not found!")
                break
                
            elif choice == '2':
                print("\n📋 Starting NO PAGINATION mode...")
                print("=" * 40)
                
                # Check if manual scraper exists
                if os.path.exists('run_manual_simple.py'):
                    print("🚀 Launching manual scraper...")
                    import subprocess
                    subprocess.run([sys.executable, 'run_manual_simple.py'])
                elif os.path.exists('manual_process_simple.py'):
                    print("🚀 Launching manual scraper...")
                    import subprocess
                    subprocess.run([sys.executable, 'manual_process_simple.py'])
                else:
                    print("❌ Manual scraper not found!")
                break
                
            elif choice == '3':
                print("\n🔗 Starting CSV MERGER...")
                print("=" * 40)
                
                # Check if CSV merger exists
                if os.path.exists('csv_merger.py'):
                    print("🚀 Launching CSV merger...")
                    import subprocess
                    subprocess.run([sys.executable, 'csv_merger.py'])
                else:
                    print("❌ CSV merger not found!")
                break
                
            elif choice == '4':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Please choose 1, 2, 3, or 4")
                continue
        
    except KeyboardInterrupt:
        print("\n\n🛑 Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n⏸️ Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()
