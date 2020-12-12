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
import time # Used to sleep
from tqdm import tqdm # Used for download progress bar
import json # Used for config file

# Set colors for windows
os.system("color")

# Colors for highlighting text (not all are used)
class bcolors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Select a directory
def selectDir():
	global wow_addons
	newpath = askdirectory(title='Select the "Addons" directory',initialdir = '/', mustexist = 'TRUE')
	if newpath == "":
		print(f"{bcolors.BOLD}{bcolors.RED}No directory selected. Exiting...{bcolors.ENDC}")
		exit()
	else:
		with open('config.json','w+') as f:
			wow_addons = newpath
			jsonDir = {'directory': newpath}
			json.dump(jsonDir, f)

# Reads the config.txt file next to the script to get the 'Addons' directory
if os.path.exists('config.json'):
	with open('config.json','r') as f:
		cfg = f.read()
		if cfg == "":
			selectDir()
		else:
			cfgJson = json.loads(cfg)
			if "directory" not in cfgJson or cfgJson["directory"] == "":
				print(f"{bcolors.BOLD}{bcolors.BLUE}WoW Addon directory not selected.{bcolors.ENDC}")
				selectDir()
			else:
				wow_addons = cfgJson["directory"]
else:
	print(f"{bcolors.BOLD}{bcolors.RED}Updater config file not found.{bcolors.ENDC}")
	selectDir()

# Regex pattern used to get version from the ElvUI.toc file
pattern = re.compile("## Version: \d+\.\d+")

# Get currently installed version
elvFile = os.path.join(wow_addons,'ElvUI','ElvUI.toc')

# Check to see if ElvUI is already installed in the WoW Addons directory
if os.path.exists(elvFile):
	elvOpen = open(elvFile, 'r')
	elvRead = elvOpen.read()
	elvOpen.close()
	matches = re.findall(pattern, elvRead)
	myVer = matches[0].replace("## Version: ", "")
else:
	myVer = "Not installed"

# Print out to user the installed version info
print(f"Currently installed version of ElvUI: {bcolors.BOLD}{bcolors.BLUE}" + myVer + f"{bcolors.ENDC}")

# Set temp directory for downloading the new version (if needed)
myTemp = tempfile.gettempdir()
outf = os.path.join(myTemp, "elvui.zip")

# Regex for ElvUI file link search
elv = '\/downloads\/elvui-.*zip'
# Regex for ElvUI file version search
ver = '\d+\.\d+'
# ElvUI Official website
base = 'https://www.tukui.org'


# Download file function
def download(url, file_name):
	resp = requests.get(url, stream=True)
	total = int(resp.headers.get('content-length', 0))
	print(f'{bcolors.BOLD}{bcolors.CYAN}')
	with open(file_name, 'wb') as file, tqdm(
		desc=file_name,
		total=total,
		unit='iB',
		unit_scale=True,
		unit_divisor=1024,
    ) as bar:
		for data in resp.iter_content(chunk_size=1024):
			size = file.write(data)
			bar.update(size)
	print(f'{bcolors.ENDC}')

# Unzip file function
def unzipme(myFile, myPath):
	with zipfile.ZipFile(myFile, 'r') as zip_ref:
		zip_ref.extractall(myPath)

elvPage = requests.get("https://www.tukui.org/download.php?ui=elvui")

soup = BeautifulSoup(elvPage.text, "lxml")

# Find all links on the Tukui website
links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

# Set default value for 'myLink' variable
myLink = "Not Found"

# Loop thru links, search link strings via regex to get version, then compare to installed version on this machine
for jibb in links:
	if re.search(elv, str(jibb)):
		myLink = base + str(jibb)

# Set default value for true/false flage		
i = 0

# If a link is found, compare 
if myLink != "Not Found":
	print("File found at: " + myLink)
	webVer = re.findall(ver, str(myLink))
	if webVer[0] == myVer:
		print(f"ElvUI is already the newest version: {bcolors.BOLD}{bcolors.GREEN}" + myVer + f"{bcolors.ENDC}")
		print("Skipping download and install. Please check back later for a newer version.")
		i = 1
	if i == 0:
		print(f"{bcolors.BOLD}{bcolors.YELLOW}ElvUI is not the newest version available.{bcolors.ENDC}")
		print("Downloading to: " + outf + "...")
		download(myLink, outf)
		print("Extracting to " + wow_addons)
		unzipme(outf, wow_addons)
		print(f"ElvUI has been updated to version {bcolors.BOLD}{bcolors.GREEN}" + str(webVer[0]) + f"{bcolors.ENDC}.")
else:
	# Couldn't find the download link on the Tukui website
	print(f"{bcolors.BOLD}{bcolors.RED}Download link was not found!{bcolors.ENDC}")
	print(f"{bcolors.BOLD}{bcolors.RED}Could not update ElvUI{bcolors.ENDC}")

# Sleep for 5 seconds so user can read output
time.sleep(5)
