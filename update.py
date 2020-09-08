from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlretrieve
import re
import requests
import platform
import os

elv = "\/downloads\/elvui-.*zip"
base = "https://www.tukui.org"

plt = platform.system()
if plt == "Windows":
	myLocal = os.getenv('LOCALAPPDATA')
	outf = myLocal + "\Temp\elvui.zip"
else:
	outf = r"/Users/elvui.zip"

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

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
	download(myLink, outf)
else:
	print("Download link was not found!")
	print("Could not update ElvUI")

