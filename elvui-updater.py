from bs4 import BeautifulSoup
import re
import requests
import tempfile
import os
import zipfile

# You will need to set this to the WoW addons directory
wow_addons = r"F:\Games\Blizzard Games\World of Warcraft\_retail_\Interface\AddOns"

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

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
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
