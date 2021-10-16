import re
import sys
import requests
import json
import os
from selectolax.parser import HTMLParser
from googletrans import Translator
from pathlib import Path

baseURL = "https://e-f-frontier.net/"


def getGameInfo():
	gameList = []
	gamesPage = requests.get("https://e-f-frontier.net/flash/flash_top.html");
	gamesTree = HTMLParser(gamesPage.content)
	translator = Translator()
	for elem in gamesTree.css("div.fla_capbox_l"):
		gameMap = {
			"gamePageHref" : "",
			"gameBanner" : "",
			"gameTitle" : "",
			"gameSubject_jp" : "",
			"gameSubject_en" : "",
			"gameDescription_jp" : "",
			"gameDescription_en" : "",
			"gameHref" : "",
			"gameImage" : "",
		}
		current = HTMLParser(elem.html)

		gameMap["gamePageHref"] = current.css_first("a").attrs["href"][3:]
		gameMap["gameBanner"] = current.css_first("a > img").attrs["src"][3:]
		gameMap["gameTitle"] = current.css_first("h1").text()
		gameMap["gameSubject_jp"] = current.css_first("h4").text()
		gameMap["gameSubject_en"] = translator.translate(gameMap["gameSubject_jp"],src="ja", dest="en").text
		gameMap["gameDescription_jp"] = current.css_first("p").text().replace("\t","")
		gameMap["gameDescription_en"] = translator.translate(gameMap["gameDescription_jp"],src="ja", dest="en").text
		gamePage = requests.get(baseURL + gameMap["gamePageHref"]);
		gameTree = HTMLParser(gamePage.content)
		gameMap["gameHref"] = gameTree.css_first("div.product_main_box_c > a").attrs["href"][3:]
		gameMap["gameImage"] = gameTree.css_first("div.product_main_box_c > a > img").attrs["src"][3:]
		gameList.append(gameMap.copy())
	return gameList


def writeGameData(gameName, gameBaseURL,gamePageURL,jsUrl):

	'''baseURL = "https://e-f-frontier.net/fla/fla21_a/"
	pageURL = "https://e-f-frontier.net/fla/fla21_a/21a.html"
	
	
	with open('21a.js') as jsfile:
	    lines = jsfile.readlines()
	'''
	
	
	dataURLPattern = re.compile(r'(?<=src:")([a0-z9._\/\?]*)(?=")',re.IGNORECASE)
	gameScript = requests.get(gameBaseURL +"/"+jsUrl,headers={"Referer": gamePageURL,"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0","content-type": "application/javascript"})
	readingData=False
	open(gameName + "/"+ jsUrl.split("?")[0], 'wb').write(gameScript.content)
	with open(gameName + "/"+ jsUrl.split("?")[0], "r") as jsFile:	
		for line in jsFile:
			if not readingData: 
				if "manifest: [" in line:
					readingData = True
					print("found manifest");
			elif "]," in line: 
					readingData = False
					print("found end of manifest");
			elif readingData and "src" in line:
					for match in re.findall(dataURLPattern,line):
						print("Getting: " + match)
						req = requests.get(gameBaseURL+"/"+match,headers={"Referer": gamePageURL,"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
						if req.status_code == 200:
							Path(gameName + "/"+ match[0:match.rindex("/")]).mkdir(parents=True, exist_ok=True)
							open(gameName + "/"+ match.split("?")[0], 'wb').write(req.content)
				
def writePreloader(preloaderPath,gameBaseURL,gamePageURL,gameName):
	req = requests.get(gameBaseURL+"/"+preloaderPath,headers={"Referer": gamePageURL,"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
	open(gameName + "/"+ preloaderPath, 'wb').write(req.content)

def getImagefromBase(path, gameName):
	req = requests.get(baseURL + "/" + path)
	Path(gameName + "/img").mkdir(parents=True, exist_ok=True)
	open(gameName + "/" + path, 'wb').write(req.content)

def getGameData(gameInfo):
	gameName = gameInfo["gameHref"][gameInfo["gameHref"].rindex("/") + 1:gameInfo["gameHref"].rindex(".")]
	gameBaseURL = baseURL + gameInfo["gameHref"][0:gameInfo["gameHref"].rindex("/")]
	gamePageURL = baseURL + gameInfo["gameHref"]
	if not os.path.isdir(gameName):
		print(gamePageURL)
		gamePage = requests.get(gamePageURL,headers={"Referer": baseURL +"/"+gameInfo["gamePageHref"],"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"});
		gameTree = HTMLParser(gamePage.content)
		jsUrls = []
		for elem in gameTree.css("script"):
			if "src" in elem.attrs:
				if "create" in elem.attrs["src"]:
					req = requests.get("https://code.createjs.com/createjs-2015.11.26.min.js")
					Path(gameName + "/scripts/").mkdir(parents=True, exist_ok=True)
					open(gameName + "/scripts/create.js", 'wb').write(req.content)
					elem.attrs["src"] = "scripts/create.js"
					print("updated createjs")
				else:
					jsUrls.append(elem.attrs["src"])
				
		for elem in gameTree.css("link"):
			if "rel" in elem.attrs:
				if "http" not in elem.attrs["href"]:
					req = requests.get(gameBaseURL + elem.attrs["href"])
					Path(gameName + "/" + elem.attrs["href"][0:elem.attrs["href"].rindex("/")]).mkdir(parents=True, exist_ok=True)
					open(gameName + "/" + elem.attrs["href"].split("?")[0], 'wb').write(req.content)
					print("wrote " + gameName + "/" + elem.attrs["href"].split("?")[0])		
		for jsUrl in jsUrls:
			if gameName in jsUrl:
				writeGameData(gameName, gameBaseURL,gamePageURL,jsUrl)
		# banner and game image
		getImagefromBase(gameInfo["gameBanner"],gameName)
		getImagefromBase(gameInfo["gameImage"],gameName)
		open(gameName + "/" + gameName + ".html", 'w').write(gameTree.html)
		writePreloader(gameTree.css_first("#_preload_div_ > img").attrs["src"],gameBaseURL,gamePageURL,gameName)
		open(gameName + "/" + "info.json", 'w').write(json.dumps(gameInfo, indent=4))



gameInfo = getGameInfo()
print("Found " + str(len(gameInfo)) + " games")

for info in gameInfo:
	getGameData(info)

