#!/usr/bin/env python3
"""
Miller 3 Data Scraper - Main Menu
Easy launcher with clear status indicators and process alerts
"""

import os
import sys
import subprocess
import time

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    """Show main header"""
    print("🔬 MILLER 3 DATA SCRAPER - MAIN MENU")
    print("=" * 50)
    print("🎯 Goal: Reduce manual interventions in your automation")
    print("📊 Status: Ready for operation")
    print()

def show_process_alert(script_name, description):
    """Show process starting alert"""
    clear_screen()
    print("\n" + "🔴" * 20 + " PROCESS STARTING " + "🔴" * 20)
    print(f"🚨 ALERT: {script_name.upper()} IS NOW RUNNING")
    print("🔄 STATUS: ACTIVE - Please wait...")
    print(f"💻 {description}")
    print("⚠️  DO NOT close this terminal window")
    print("🔴" * 58)
    print()
    
    # Countdown
    for i in range(3, 0, -1):
        print(f"🔄 Starting in {i} seconds...")
        time.sleep(1)
    
    print("🚀 STARTING NOW!")
    print()

def run_script(script_name, description, show_alert=True):
    """Run a Python script with proper alerts"""
    if show_alert:
        show_process_alert(script_name, description)
    
    try:
        print(f"🔄 STATUS: Running {script_name}...")
        result = subprocess.run([sys.executable, script_name], cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"\n✅ {script_name} completed successfully!")
        else:
            print(f"\n⚠️ {script_name} finished with warnings or errors")
        
        return result.returncode == 0
    except Exception as e:
        print(f"\n❌ Error running {script_name}: {str(e)}")
        return False

def show_menu():
    """Display the main menu options"""
    print("📋 AVAILABLE OPTIONS:")
    print()
    print("1. 🔍 Run Enhanced Diagnostic Test")
    print("   • Tests all automation components")
    print("   • Clear process alerts and status updates")
    print("   • Identifies specific blocking issues")
    print("   • Generates detailed report with solutions")
    print()
    print("2. 🚀 Run Manual Login Scraper (Recommended)")
    print("   • Most reliable option for production use")
    print("   • Manual authentication + automated processing")
    print("   • Minimal manual interventions required")
    print("   • Enhanced error recovery and guidance")
    print()
    print("3. 🔧 Fix ChromeDriver Issues")
    print("   • Fixes path and permission problems")
    print("   • Required if you get ChromeDriver errors")
    print("   • Auto-detects and resolves common issues")
    print()
    print("4. 📊 View Previous Diagnostic Reports")
    print("   • Shows results from previous diagnostic runs")
    print("   • Displays automation success rates")
    print("   • Reviews identified issues and solutions")
    print()
    print("5. 🧹 Clean Up Old Files")
    print("   • Removes unnecessary automation files")
    print("   • Keeps only essential scripts")
    print("   • Organizes download folder")
    print()
    print("6. ❌ Exit")
    print()

def view_diagnostic_reports():
    """View previous diagnostic reports"""
    print("\n📊 PREVIOUS DIAGNOSTIC REPORTS")
    print("=" * 40)
    
    # Look for diagnostic report files
    import glob
    reports = glob.glob("diagnostic_report_*.json")
    
    if not reports:
        print("❌ No diagnostic reports found")
        print("💡 Run the diagnostic test first to generate a report")
        return
    
    # Sort by timestamp (newest first)
    reports.sort(reverse=True)
    
    print(f"✅ Found {len(reports)} diagnostic report(s):")
    print()
    
    for i, report in enumerate(reports[:5], 1):  # Show last 5 reports
        try:
            import json
            with open(report, 'r') as f:
                data = json.load(f)
            
            timestamp = data.get('timestamp', 0)
            if timestamp:
                import datetime
                date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            else:
                date_str = "Unknown date"
            
            # Count successful tests
            test_results = data.get('test_results', {})
            successful_tests = sum(1 for k, v in test_results.items() if v is True and k != 'manual_interventions')
            total_tests = len([k for k in test_results.keys() if k != 'manual_interventions'])
            manual_interventions = len(test_results.get('manual_interventions', []))
            
            print(f"{i}. {report}")
            print(f"   📅 Date: {date_str}")
            print(f"   ✅ Tests Passed: {successful_tests}/{total_tests}")
            print(f"   🔧 Manual Interventions: {manual_interventions}")
            print()
            
        except Exception as e:
            print(f"{i}. {report} (Error reading: {e})")
    
    if len(reports) > 5:
        print(f"... and {len(reports) - 5} more reports")

def cleanup_old_files():
    """Clean up old files"""
    print("\n🧹 CLEANING UP OLD FILES")
    print("=" * 30)
    
    # Files to potentially remove
    cleanup_candidates = [
        "diagnostic_*.png",
        "manual_login_start_*.png", 
        "search_results_ready_*.png",
        "*.tmp",
        "*.log"
    ]
    
    import glob
    files_to_remove = []
    
    for pattern in cleanup_candidates:
        files_to_remove.extend(glob.glob(pattern))
    
    if not files_to_remove:
        print("✅ No old files found to clean up")
        return
    
    print(f"Found {len(files_to_remove)} file(s) to clean up:")
    for f in files_to_remove[:10]:  # Show first 10
        print(f"   🗑️ {f}")
    
    if len(files_to_remove) > 10:
        print(f"   ... and {len(files_to_remove) - 10} more files")
    
    confirm = input("\nProceed with cleanup? (y/N): ").lower().strip()
    
    if confirm in ['y', 'yes']:
        removed_count = 0
        for f in files_to_remove:
            try:
                os.remove(f)
                removed_count += 1
            except Exception as e:
                print(f"⚠️ Could not remove {f}: {e}")
        
        print(f"✅ Cleaned up {removed_count} files")
    else:
        print("❌ Cleanup cancelled")

def main():
    """Main menu loop"""
    while True:
        clear_screen()
        show_header()
        show_menu()
        
        try:
            choice = input("Choose an option (1-6): ").strip()
            
            if choice == "1":
                success = run_script(
                    "run_diagnostic_with_alerts.py",
                    "Running comprehensive automation diagnostic with enhanced feedback"
                )
                if success:
                    print("\n💡 Check the generated diagnostic_report_*.json file for detailed results")
            
            elif choice == "2":
                success = run_script(
                    "manual_login_scraper.py", 
                    "Running manual login scraper with automated processing"
                )
                if success:
                    print("\n💡 Check the downloads folder for your data files")
            
            elif choice == "3":
                success = run_script(
                    "fix_chromedriver_path.py",
                    "Fixing ChromeDriver path and permission issues",
                    show_alert=False
                )
                
            elif choice == "4":
                view_diagnostic_reports()
                
            elif choice == "5":
                cleanup_old_files()
                
            elif choice == "6":
                print("\n👋 Goodbye!")
                print("🔄 STATUS: Exiting Main Menu")
                break
                
            else:
                print("\n❌ Invalid choice. Please select 1-6.")
            
            if choice in ["1", "2", "3", "4", "5"]:
                print("\n" + "=" * 50)
                input("Press Enter to return to main menu...")
        
        except KeyboardInterrupt:
            print("\n\n🛑 Main menu interrupted (Ctrl+C)")
            print("👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Menu error: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        print("🚀 MILLER 3 DATA SCRAPER - INITIALIZING...")
        time.sleep(1)
        
        main()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Startup interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Startup error: {str(e)}")
        print("💡 Make sure you're running this from the Miller 3 Data Scaper folder")
        input("Press Enter to exit...")
