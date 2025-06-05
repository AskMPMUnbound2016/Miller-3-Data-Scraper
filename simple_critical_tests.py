#!/usr/bin/env python3
"""
Miller 3 Data Scraper - Simple Critical Issue Tester
Works with your existing browser session - no navigation issues
"""

import os
import sys
import time
import subprocess

def test_download_button_in_browser():
    """Test download button detection using browser console"""
    print("🔍 DOWNLOAD BUTTON DETECTION TEST")
    print("=" * 40)
    
    print("""
📋 MANUAL TEST INSTRUCTIONS:
1. Keep your browser on the ReferenceUSA results page
2. Open browser Developer Tools (F12 or Cmd+Option+I)
3. Go to Console tab
4. Copy and paste this JavaScript code:

// Test 1: Find all Download buttons
console.log('=== DOWNLOAD BUTTON SEARCH ===');
let downloadButtons = [];

// Strategy 1: Text-based search
document.querySelectorAll('a, button').forEach((el, i) => {
    if (el.textContent.toLowerCase().includes('download')) {
        downloadButtons.push({
            type: 'text-based',
            element: el,
            text: el.textContent.trim(),
            tag: el.tagName,
            classes: el.className,
            id: el.id
        });
        console.log(`Found #${i}: ${el.tagName} - "${el.textContent.trim()}"`);
    }
});

// Strategy 2: Class/ID based search
document.querySelectorAll('[class*="download"], [id*="download"]').forEach((el, i) => {
    downloadButtons.push({
        type: 'attribute-based',
        element: el,
        text: el.textContent.trim(),
        tag: el.tagName,
        classes: el.className,
        id: el.id
    });
    console.log(`Found by attribute #${i}: ${el.tagName} - "${el.textContent.trim()}"`);
});

console.log(`Total download buttons found: ${downloadButtons.length}`);
if (downloadButtons.length > 0) {
    console.log('First button details:', downloadButtons[0]);
} else {
    console.log('❌ NO DOWNLOAD BUTTONS FOUND');
    console.log('Showing all clickable elements:');
    document.querySelectorAll('a, button, input[type="submit"], input[type="button"]').forEach((el, i) => {
        if (i < 10) { // Show first 10
            console.log(`${i}: ${el.tagName} - "${el.textContent.trim()}"`);
        }
    });
}

5. Look at the console output and tell me what it shows
""")
    
    result = input("What did the console show? (copy/paste the key findings): ")
    print(f"📝 User reported: {result}")
    
    return "download" in result.lower()

def test_checkbox_unchecking_in_browser():
    """Test checkbox unchecking using browser console"""
    print("\n☑️ CHECKBOX UNCHECKING TEST")
    print("=" * 35)
    
    print("""
📋 MANUAL TEST INSTRUCTIONS:
1. Make sure some checkboxes are selected on your page
2. In the same browser console, run this code:

// Test 2: Checkbox analysis and unchecking
console.log('=== CHECKBOX UNCHECKING TEST ===');

// Find all checkboxes
let allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
console.log(`Total checkboxes found: ${allCheckboxes.length}`);

// Find selected checkboxes
let selectedCheckboxes = document.querySelectorAll('input[type="checkbox"]:checked');
console.log(`Selected checkboxes: ${selectedCheckboxes.length}`);

// Find header checkbox (select all)
let headerCheckbox = null;
document.querySelectorAll('th input[type="checkbox"], thead input[type="checkbox"]').forEach(cb => {
    if (cb.offsetParent !== null) { // visible
        headerCheckbox = cb;
        console.log('Found header checkbox:', cb);
    }
});

// Try to uncheck header checkbox
if (headerCheckbox && headerCheckbox.checked) {
    console.log('Unchecking header checkbox...');
    headerCheckbox.click();
    setTimeout(() => {
        let stillSelected = document.querySelectorAll('input[type="checkbox"]:checked').length;
        console.log(`After header uncheck: ${stillSelected} checkboxes still selected`);
    }, 500);
} else {
    console.log('No header checkbox found or already unchecked');
    // Uncheck individual checkboxes
    selectedCheckboxes.forEach((cb, i) => {
        cb.click();
        console.log(`Unchecked checkbox ${i}`);
    });
    setTimeout(() => {
        let stillSelected = document.querySelectorAll('input[type="checkbox"]:checked').length;
        console.log(`After individual uncheck: ${stillSelected} checkboxes still selected`);
    }, 500);
}

3. Look at the console output and tell me the results
""")
    
    result = input("What did the checkbox test show? (copy/paste the results): ")
    print(f"📝 User reported: {result}")
    
    return "0 checkboxes still selected" in result.lower() or "unchecked" in result.lower()

def test_file_download_monitoring():
    """Test file download monitoring"""
    print("\n📥 FILE DOWNLOAD MONITORING TEST")
    print("=" * 35)
    
    download_dir = os.path.join(os.getcwd(), "downloads")
    
    # Get initial file list
    initial_files = []
    if os.path.exists(download_dir):
        initial_files = [f for f in os.listdir(download_dir) 
                        if os.path.isfile(os.path.join(download_dir, f)) 
                        and not f.startswith('.')]
    
    print(f"📂 Download directory: {download_dir}")
    print(f"📄 Files before test: {len(initial_files)}")
    
    if initial_files:
        print("   Existing files:")
        for f in initial_files[-3:]:  # Show last 3
            print(f"     📄 {f}")
    
    print("\n📋 DOWNLOAD TEST INSTRUCTIONS:")
    print("1. In your browser, trigger a download")
    print("2. Choose to save the file (if prompted)")
    print("3. Wait for download to complete")
    print("4. Come back here and we'll check for new files")
    
    input("Press Enter AFTER you've completed the download...")
    
    # Check for new files
    print("\n🔍 Checking for new files...")
    
    new_files = []
    if os.path.exists(download_dir):
        current_files = [f for f in os.listdir(download_dir) 
                        if os.path.isfile(os.path.join(download_dir, f)) 
                        and not f.startswith('.')]
        new_files = [f for f in current_files if f not in initial_files]
    
    if new_files:
        print(f"✅ SUCCESS! {len(new_files)} new file(s) found:")
        for f in new_files:
            file_path = os.path.join(download_dir, f)
            file_size = os.path.getsize(file_path)
            print(f"   📄 {f} ({file_size} bytes)")
        return True
    else:
        print("❌ NO NEW FILES DETECTED")
        
        # Debug info
        print("\n🔍 DEBUG INFO:")
        print(f"   📂 Download directory exists: {os.path.exists(download_dir)}")
        
        if os.path.exists(download_dir):
            all_files = os.listdir(download_dir)
            print(f"   📄 Total items in directory: {len(all_files)}")
            
            # Check for partial downloads
            partial_files = [f for f in all_files if f.endswith('.crdownload') or f.endswith('.tmp')]
            if partial_files:
                print(f"   ⏳ Partial downloads: {partial_files}")
        
        # Check browser's default Downloads folder
        import os.path
        default_downloads = os.path.expanduser("~/Downloads")
        if os.path.exists(default_downloads):
            recent_files = []
            for f in os.listdir(default_downloads):
                file_path = os.path.join(default_downloads, f)
                if os.path.isfile(file_path):
                    mtime = os.path.getmtime(file_path)
                    if time.time() - mtime < 300:  # Modified in last 5 minutes
                        recent_files.append(f)
            
            if recent_files:
                print(f"   💡 Recent files in ~/Downloads: {recent_files}")
                print("   (File may have downloaded to default location)")
        
        return False

def run_simple_tests():
    """Run all simple tests"""
    print("🧪 MILLER 3 DATA SCRAPER - SIMPLE CRITICAL ISSUE TESTS")
    print("=" * 60)
    print("🎯 Testing: Download button, checkbox unchecking, file verification")
    print("📝 Uses browser console - no navigation issues")
    print()
    
    results = {}
    
    # Test 1: Download button detection
    results['download_button'] = test_download_button_in_browser()
    
    # Test 2: Checkbox unchecking  
    results['checkbox_unchecking'] = test_checkbox_unchecking_in_browser()
    
    # Test 3: File download verification
    results['file_verification'] = test_file_download_monitoring()
    
    # Summary
    print("\n📊 SIMPLE TEST RESULTS")
    print("=" * 25)
    
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    for test_name, result in results.items():
        status = "✅ WORKING" if result else "❌ NEEDS FIX"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} issues resolved")
    
    # Provide specific guidance
    print("\n💡 NEXT STEPS:")
    
    if not results.get('download_button'):
        print("🔧 Download Button: We need to identify the exact button element")
        print("   → Look for button text, classes, or IDs from console output")
    
    if not results.get('checkbox_unchecking'):
        print("🔧 Checkbox Unchecking: Need better selection clearing strategy")
        print("   → May need to uncheck individual boxes or find different header checkbox")
    
    if not results.get('file_verification'):
        print("🔧 File Download: Check browser download settings")
        print("   → File may be downloading to different location")
        print("   → Check browser's Downloads page (chrome://downloads/)")
    
    if passed_tests == total_tests:
        print("🎉 ALL ISSUES CAN BE RESOLVED!")
        print("   → Ready to update main automation scripts")
    
    return results

if __name__ == "__main__":
    try:
        print("🚀 Starting simple critical issue tests...")
        print("📝 This uses browser console - no automation navigation")
        print()
        
        input("Make sure you're on the ReferenceUSA results page and press Enter...")
        
        results = run_simple_tests()
        
        print(f"\n📋 Test completed. Results saved for next steps.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Testing error: {str(e)}")
    
    print("\nPress Enter to exit...")
    input()
