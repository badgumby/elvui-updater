#######################################
##  BAD Gumby's ElvUI Update Script  ##
#######################################

# Imports and their uses
from tkinter import Tk # Used for addons folder selection file dialog box
from tkinter.filedialog import askdirectory # Used for addons folder selection file dialog box
import requests # Used to get webpage HTML
from bs4 import BeautifulSoup # Used to parse HTML
import re # Used for regex
import tempfile # Used to determine the OS defined temp directory
import os # Used for OS path joining and testing
import zipfile # Used to uncompress zip file

# Reads the config.txt file next to the script to get the 'Addons' directory
cfg = open('config.txt','r')
cfgtxt = cfg.readline()
cfg.close()
if cfgtxt == "directory=" or cfgtxt == "":
	print("WoW Addon directory not selected.")
	newpath = askdirectory(title='Select the "Addons" directory',initialdir = '/',mustexist = 'TRUE')
	if newpath == "":
		print("No directory selected. Exiting...")
		exit()
	else:
		cfg = open('config.txt','w+')
		cfg.write("directory=" + newpath)
		wow_addons = newpath
		cfg.close()
else:
	wow_addons = cfgtxt.replace("directory=","")

# Regex pattern used to get version from the ElvUI.toc file
pattern = re.compile("## Version: \d+\.\d+")

# Get currently installed version
elvFile = wow_addons + "\ElvUI\ElvUI.toc"
if os.path.exists(elvFile):
	elvOpen = open(elvFile, 'r')
	elvRead = elvOpen.read()
	elvOpen.close()
	matches = re.findall(pattern, elvRead)
	myVer = matches[0].replace("## Version: ", "")
else:
	myVer = "Not installed"

print("Currently installed version of ElvUI: " + myVer)

myTemp = tempfile.gettempdir()

elv = "\/downloads\/elvui-.*zip"
ver = "\d+\.\d+"
base = "https://www.tukui.org"
outf = os.path.join(myTemp, "elvui.zip")

# Download file function
def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

# Unzip file function
def unzipme(myFile, myPath):
	with zipfile.ZipFile(myFile, 'r') as zip_ref:
		zip_ref.extractall(myPath)

elvPage = requests.get("https://www.tukui.org/download.php?ui=elvui")

soup = BeautifulSoup(elvPage.text, "lxml")

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

myLink = "Not Found"
for jibb in links:
	if re.search(elv, str(jibb)):
		myLink = base + str(jibb)
		
i = 0
if myLink != "Not Found":
	print("File found at: " + myLink)
	webVer = re.findall(ver, str(myLink))
	if webVer[0] == myVer:
		print("ElvUI is already the newest version: " + myVer)
		print("Skipping download and install. Please check back later for a newer version.")
		i = 1
	if i == 0:
		print("ElvUI is not the newest version available.")
		print("Downloading to: " + outf + "...")
		download(myLink, outf)
		unzipme(outf, wow_addons)
		print("ElvUI has been updated to version " + str(webVer[0]) + ".")
else:
	print("Download link was not found!")
	print("Could not update ElvUI")
