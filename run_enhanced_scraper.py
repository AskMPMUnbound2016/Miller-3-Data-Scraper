#!/usr/bin/env python3
"""
ENHANCED MILLER 3 DATA SCRAPER - MAIN RUNNER
============================================
Enhanced with Auto-Continue Batch Flow

METHODS AVAILABLE:
1. Method 1 Enhanced: Manual Navigation + Auto-Continue
   - User manually logs in and does search
   - User manually goes to next page
   - Processes in batches of up to 10
   - Downloads file and saves file for each batch
   - Auto-unselects files from prior batch
   - Selects next batch automatically

2. Method 2 Enhanced: Full Automation + Auto-Continue
   - User manually logs in and does search
   - Automation selects records and goes to next page
   - Up to 10 pages per batch
   - Downloads files and saves files
   - Auto-unselects prior batch files
   - Selects next batch, saves, downloads, repeats until done

3. Original Automated Process (legacy)
"""

import sys
import os
from semi_automated_scraper import SemiAutomatedScraper

def show_welcome():
    """Show enhanced welcome screen"""
    print("🎯" + "="*70 + "🎯")
    print("           MILLER 3 DATA SCRAPER - PAGINATION MODE")
    print("              Enhanced Auto-Continue Batch Flow")
    print("🎯" + "="*70 + "🎯")
    print()
    print("🆕 NEW ENHANCED FEATURES:")
    print("   ✅ Auto-continue until all pages downloaded")
    print("   ✅ Auto-unselect records after each batch")
    print("   ✅ Smart batch management (1-10 pages)")
    print("   ✅ Enhanced error recovery")
    print("   ✅ Session state management")
    print("   ✅ Progress tracking")
    print()
    print("📋 AVAILABLE METHODS:")
    print("   1️⃣ Method 1 Enhanced: Manual Navigation + Auto-Continue")
    print("   2️⃣ Method 2 Enhanced: Full Automation + Auto-Continue")
    print("   3️⃣ Original Automated Process")
    print()

def main():
    """Main entry point"""
    try:
        show_welcome()
        
        # Initialize enhanced scraper
        print("🚀 Initializing Enhanced Scraper...")
        scraper = SemiAutomatedScraper()
        
        # Check for previous session
        if scraper.session_state.get('search_name'):
            print("\n🔄 PREVIOUS SESSION DETECTED!")
            print("=" * 40)
            print(f"📝 Search: {scraper.session_state.get('search_name')}")
            print(f"📊 Total pages: {scraper.session_state.get('total_pages', 0)}")
            print(f"📄 Last completed: {scraper.session_state.get('last_completed_page', 0)}")
            print(f"📁 Completed batches: {len(scraper.session_state.get('completed_batches', []))}")
            print(f"💾 Downloaded files: {len(scraper.session_state.get('downloads_completed', []))}")
            
            if scraper.session_state.get('downloads_completed'):
                print(f"\n📂 Recent downloads:")
                for file in scraper.session_state['downloads_completed'][-3:]:
                    print(f"   • {file}")
            
            print("\n🔄 RESUME OPTIONS:")
            print("   (r) Resume previous session")
            print("   (n) Start new session")
            print("   (s) Show session details")
            print("   (q) Quit")
            
            while True:
                choice = input("\nChoose option (r/n/s/q): ").lower().strip()
                
                if choice == 'r':
                    print("✅ Resuming previous session...")
                    # Navigate to the proper starting URL instead of about:blank
                    start_url = scraper.config.get('auth_url', 'http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Quick/497be73bf9a94fe3aebb7eb4857b584f')
                    print(f"🌐 Opening: {start_url}")
                    scraper.driver.get(start_url)
                    print("\n📋 RESUMING SESSION INSTRUCTIONS:")
                    print("1. ✅ Complete OpenAthens authentication if needed")
                    print("2. ✅ Navigate to your search results page")
                    print("3. ✅ Make sure you're on the correct search")
                    print("4. ✅ Ensure you're logged in")
                    print("5. ✅ Verify you can see business records and pagination")
                    input("⏸️ Press Enter when ready on the search results page...")
                    
                    # Go directly to enhanced menu
                    scraper.show_enhanced_menu()
                    break
                    
                elif choice == 'n':
                    print("🆕 Starting new session...")
                    scraper.clear_session_state()
                    scraper.run()
                    break
                    
                elif choice == 's':
                    scraper.show_session_status()
                    continue
                    
                elif choice == 'q':
                    print("👋 Goodbye!")
                    scraper.driver.quit()
                    return
                    
                else:
                    print("❌ Please choose r, n, s, or q")
                    continue
        else:
            print("🆕 No previous session found. Starting fresh...")
            scraper.run()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Process interrupted by user")
        print("💾 Session state has been saved automatically")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        print("💾 Attempting to save session state...")
        try:
            if 'scraper' in locals():
                scraper._save_session_state()
                print("✅ Session state saved")
        except:
            print("❌ Could not save session state")
    
    print("\n⏸️ Press Enter to exit...")
    input()

if __name__ == "__main__":
    main()
