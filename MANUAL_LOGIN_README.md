# Manual Login Scraper Instructions

This scraper addresses the issue where the automated login fails and the search page opens in a new tab. This version allows you to manually log in and navigate to the search page, then continues with automated searching.

## Important Note
This scraper uses the ChromeDriver that is already in the Miller 3 Data Scraper folder. It will not download or use any other browser.

## How to Use

### On Windows:
1. Double-click on `Run_Manual_Login.bat`
2. A Chrome browser window will open
3. Log in manually with your library credentials
4. Navigate through the authentication steps
5. When you reach the search page, return to the command window and press Enter
6. The scraper will continue with automated searching and downloading

### On Mac:
1. Double-click on `Run_Manual_Login.command` 
   * If you get a permission error, open Terminal and run:
   * `chmod +x /path/to/Miller\ 3\ Data\ Scaper/Run_Manual_Login.command`
2. A Chrome browser window will open
3. Log in manually with your library credentials
4. Navigate through the authentication steps
5. When you reach the search page, return to the Terminal window and press Enter
6. The scraper will continue with automated searching and downloading

## Target Search Page

The target search page URL is:
```
http://referenceusa.com.us1.proxy.openathens.net/UsBusiness/Search/Custom/c98223fd8fc64862ae6ff63d8ac03781
```

Make sure you have reached this page or a similar search page before continuing with the automated portion.

## Troubleshooting

If the scraper fails to recognize the search page:
1. Verify you're on a page with search form fields
2. Select "Continue anyway" when prompted
3. The scraper will attempt to apply search criteria and continue

If downloads aren't working:
1. Check the Chrome settings to ensure downloads are enabled
2. Verify the download directory exists and is writable

## Questions or Issues?

If you encounter any problems, please document them with screenshots and detailed error messages.
