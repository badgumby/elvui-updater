from bs4 import BeautifulSoup
import re
import requests
import tempfile
import os
import zipfile

# You will need to set this to the WoW addons directory
wow_addons = r"F:\Games\Blizzard Games\World of Warcraft\_retail_\Interface\AddOns"

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
	myVer = re.findall(ver, str(myLink))
	num = "## Version: " + myVer[0]
	with open(wow_addons + "\ElvUI\ElvUI.toc") as search:
		for line in search:
			line = line.rstrip()
			if num == line:
				print("ElvUI is already the newest version: " + myVer[0])
				i = 1
	if i == 0:
		print("ElvUI is not the newest version available.")
		print("Downloading to: " + outf + "...")
		download(myLink, outf)
		unzipme(outf, wow_addons)
		print("ElvUI has been updated to version " + str(myVer[0]) + ".")
else:
	print("Download link was not found!")
	print("Could not update ElvUI")

