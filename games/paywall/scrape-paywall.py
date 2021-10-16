import re
import sys
import requests
import json
import os
from selectolax.parser import HTMLParser
from googletrans import Translator
from pathlib import Path

baseURL = ""


def getGameInfo():
	gameList = []
	gamesPage = requests.get(baseURL + "annex_main.html",headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"});
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

		gameMap["gamePageHref"] = current.css_first("a").attrs["href"]
		gameMap["gameBanner"] = current.css_first("a > img").attrs["src"]
		gameMap["gameTitle"] = current.css_first("h1").text()
		gameMap["gameSubject_jp"] = current.css_first("h4").text()
		gameMap["gameSubject_en"] = translator.translate(gameMap["gameSubject_jp"],src="ja", dest="en").text
		gameMap["gameDescription_jp"] = current.css_first("p").text().replace("\t","")
		gameMap["gameDescription_en"] = translator.translate(gameMap["gameDescription_jp"],src="ja", dest="en").text
		gamePage = requests.get(baseURL + gameMap["gamePageHref"],headers={"Referer": "https://e-f-frontier.net/j71gkxvo16_annex/annex_main.html","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"});
		print(baseURL + gameMap["gamePageHref"])
		gameTree = HTMLParser(gamePage.content)
		if gameTree.css_first("div.product_main_box_c"):
			#https://e-f-frontier.net/j71gkxvo16_annex/annex_md_a1.html need to get this
			if len(gameTree.css_first("div.product_main_box_c").select("a.btn").matches) > 1:
				print(gameTree.css_first("div.product_main_box_c").select("a.btn").matches[1].attrs["href"])
				gameMap["gameImage"] = gameTree.css_first("div.product_main_box_c > a > img").attrs["src"]
				gameMap["gameHref"] = gameTree.css_first("div.product_main_box_c").select("a.btn").matches[1].attrs["href"]
			elif gameTree.css_first("div.product_main_box_c > video"):
				gameMap["gameImage"] = gameTree.css_first("div.product_main_box_c > video > source").attrs["src"]
				gameMap["gameHref"] = ""
			elif gameTree.css_first("div.product_main_box_c > a"):
				gameMap["gameImage"] = gameTree.css_first("div.product_main_box_c > a > img").attrs["src"]
				gameMap["gameHref"] = gameTree.css_first("div.product_main_box_c > a").attrs["href"]
			gameList.append(gameMap.copy())
			print(gameMap)
	return gameList


def writeGameData(gameName, gameBaseURL,gamePageURL,jsUrl):

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
	Path(gameName + "/image").mkdir(parents=True, exist_ok=True)
	open(gameName + "/"+ preloaderPath.split("?")[0], 'wb').write(req.content)

def getImagefromBase(path, gameName,gamePageHref):
	if ".." in path:
		Path(gameName + "/" + path[3:].split("/")[0]).mkdir(parents=True, exist_ok=True)
		req = requests.get("https://e-f-frontier.net/" + path[3:],headers={"Referer": "https://e-f-frontier.net/","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
		open(gameName + "/" + path[3:], 'wb').write(req.content)
	else: 
		Path(gameName + "/" + path.split("/")[0]).mkdir(parents=True, exist_ok=True)	
		req = requests.get(baseURL + "/" + path,headers={"Referer": baseURL +"/"+gamePageHref,"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
		open(gameName + "/" + path, 'wb').write(req.content)

def getJSURLS(gameName, HTMLTree):
	jsUrls = []
	for elem in HTMLTree.css("script"):
		if "src" in elem.attrs:
			if "create" in elem.attrs["src"]:
				req = requests.get("https://code.createjs.com/createjs-2015.11.26.min.js")
				Path(gameName + "/scripts/").mkdir(parents=True, exist_ok=True)
				open(gameName + "/scripts/create.js", 'wb').write(req.content)
				elem.attrs["src"] = "scripts/create.js"
				print("updated createjs")
			else:
				jsUrls.append(elem.attrs["src"])
	return jsUrls

def getCSS(gameName, gameTree):
	for elem in gameTree.css("link"):
		if "rel" in elem.attrs:
			if "http" not in elem.attrs["href"]:
				req = requests.get(gameBaseURL + elem.attrs["href"])
				Path(gameName + "/" + elem.attrs["href"][0:elem.attrs["href"].rindex("/")]).mkdir(parents=True, exist_ok=True)
				open(gameName + "/" + elem.attrs["href"].split("?")[0], 'wb').write(req.content)
				print("wrote " + gameName + "/" + elem.attrs["href"].split("?")[0])		

def getGameData(gameInfo):
	if gameInfo["gameHref"] == "":
		gameName = gameInfo["gameTitle"].replace("#","")
	else: 
		gameName = gameInfo["gameHref"][gameInfo["gameHref"].rindex("/") + 1:gameInfo["gameHref"].rindex(".")]	
		
	if not os.path.isdir(gameName):
		if not gameInfo["gameHref"] == "":
			gameBaseURL = baseURL + gameInfo["gameHref"][0:gameInfo["gameHref"].rindex("/")]
			gamePageURL = baseURL + gameInfo["gameHref"]
			print(gamePageURL)
			gamePage = requests.get(gamePageURL,headers={"Referer": baseURL +"/"+gameInfo["gamePageHref"],"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"});
			gameTree = HTMLParser(gamePage.content)
			jsUrls = getJSURLS(gameName, gameTree)
			getCSS(gameName, gameTree)

			for jsUrl in jsUrls:
				if gameName in jsUrl:
					writeGameData(gameName, gameBaseURL,gamePageURL,jsUrl)
			open(gameName + "/" + gameName + ".html", 'w').write(gameTree.html)
			writePreloader(gameTree.css_first("#_preload_div_ > img").attrs["src"],gameBaseURL,gamePageURL,gameName)
		
		#banner and game image
		getImagefromBase(gameInfo["gameBanner"],gameName,gameInfo["gamePageHref"])
		getImagefromBase(gameInfo["gameImage"],gameName,gameInfo["gamePageHref"])
		if ".." in gameInfo["gameBanner"]:
			gameInfo["gameBanner"] = gameInfo["gameBanner"][3:]
		if ".." in gameInfo["gameImage"]:
			gameInfo["gameImage"] = gameInfo["gameImage"][3:]	
		open(gameName + "/" + "info.json", 'w').write(json.dumps(gameInfo, indent=4))



gameInfo = getGameInfo()
print("Found " + str(len(gameInfo)) + " games")

for info in gameInfo:
	getGameData(info)

