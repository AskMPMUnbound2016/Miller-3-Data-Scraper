#!/usr/bin/env python3
"""
Miller 3 Data Scraper - Quick ChromeDriver Path Fix
Finds chromedriver and updates all scripts to use the correct path
"""

import os
import shutil
import glob

def find_and_fix_chromedriver():
    """Find chromedriver and fix the path in all scripts"""
    print("🔍 SEARCHING FOR CHROMEDRIVER...")
    print("=" * 40)
    
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Search for chromedriver files
    possible_paths = [
        "./chromedriver",
        "./chromedriver.exe", 
        "/usr/local/bin/chromedriver",
        "/usr/bin/chromedriver",
        os.path.expanduser("~/chromedriver"),
        os.path.join(current_dir, "chromedriver"),
        os.path.join(current_dir, "chromedriver.exe")
    ]
    
    # Also search in current directory with glob
    chromedriver_files = glob.glob("*chromedriver*")
    if chromedriver_files:
        possible_paths.extend([os.path.join(current_dir, f) for f in chromedriver_files])
    
    found_chromedriver = None
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Found: {path}")
            
            # Test if it's executable
            if os.access(path, os.X_OK):
                print(f"✅ Executable: {path}")
                found_chromedriver = path
                break
            else:
                print(f"⚠️ Not executable: {path}")
                # Try to make it executable
                try:
                    os.chmod(path, 0o755)
                    if os.access(path, os.X_OK):
                        print(f"✅ Made executable: {path}")
                        found_chromedriver = path
                        break
                except:
                    print(f"❌ Could not make executable: {path}")
    
    if not found_chromedriver:
        print("❌ No working chromedriver found!")
        print("\n💡 SOLUTIONS:")
        print("1. Download ChromeDriver from: https://chromedriver.chromium.org/downloads")
        print("2. Or install with: brew install chromedriver")
        print("3. Make sure it matches your Chrome version")
        return None
    
    print(f"\n✅ Using chromedriver: {found_chromedriver}")
    
    # Update scripts to use the correct path
    scripts_to_update = [
        "automation_diagnostic_test.py",
        "enhanced_automation_fix.py",
        "manual_login_scraper.py"
    ]
    
    for script in scripts_to_update:
        if os.path.exists(script):
            try:
                with open(script, 'r') as f:
                    content = f.read()
                
                # Replace the chromedriver path references
                old_patterns = [
                    'chromedriver_path = "chromedriver"',
                    "chromedriver_path = 'chromedriver'",
                    'chromedriver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")'
                ]
                
                new_path = f'chromedriver_path = "{found_chromedriver}"'
                
                updated = False
                for pattern in old_patterns:
                    if pattern in content:
                        content = content.replace(pattern, new_path)
                        updated = True
                
                if updated:
                    with open(script, 'w') as f:
                        f.write(content)
                    print(f"✅ Updated {script}")
                else:
                    print(f"⚠️ No chromedriver path found to update in {script}")
                    
            except Exception as e:
                print(f"❌ Error updating {script}: {e}")
    
    return found_chromedriver

if __name__ == "__main__":
    print("🚀 MILLER 3 DATA SCRAPER - CHROMEDRIVER PATH FIX")
    print("=" * 55)
    
    chromedriver_path = find_and_fix_chromedriver()
    
    if chromedriver_path:
        print(f"\n🎉 SUCCESS!")
        print(f"ChromeDriver ready at: {chromedriver_path}")
        print("\nYou can now run:")
        print("  python3 automation_launcher.py")
        print("  python3 automation_diagnostic_test.py")
        
        # Test the fix by importing and checking
        try:
            print("\n🧪 Testing the fix...")
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            
            service = Service(chromedriver_path)
            print("✅ ChromeDriver service created successfully!")
            
        except Exception as e:
            print(f"⚠️ Import test failed: {e}")
            print("But the path fix should still work.")
    
    else:
        print(f"\n❌ FAILED!")
        print("You need to install ChromeDriver first.")
        print("\nQuick install on Mac:")
        print("  brew install chromedriver")
        print("\nThen run this fix script again.")
    
    print("\nPress Enter to exit...")
    input()
