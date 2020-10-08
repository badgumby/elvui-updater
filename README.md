# ElvUI Updater Script
This script will fetch the latest ElvUI zip from the Tukui.org website, and extract it to your WoW directory. 
The WoW 'Addons' directory will be set on first run by a selection dialog box.

This script requires the following non-Standard Library Python components:

 - requests
 	- Used to get webpage HTML
 - tqdm
	- Used to display download progress
 - bs4 (BeautifulSoup)
	- Used to parse the HTML results
 - lxml
 	- Used by BeautifulSoup to parse the DOM
