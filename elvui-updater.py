from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlretrieve
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

req = Request("https://www.tukui.org/download.php?ui=elvui")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

myLink = "Not Found"
for jibb in links:
	if re.search(elv, str(jibb)):
		myLink = base + str(jibb)
		

if myLink != "Not Found":
	print("File found at: " + myLink)
	print("Downloading to: " + outf + "...")
	myVer = re.findall(ver, str(myLink))
	download(myLink, outf)
	unzipme(outf, wow_addons)
	print("ElvUI has been updated to version " + str(myVer[0]) + ".")
else:
	print("Download link was not found!")
	print("Could not update ElvUI")

