import re
import sys
import requests
import json
import os
import io
from selectolax.parser import HTMLParser
from googletrans import Translator
from pathlib import Path

baseURL = "https://e-f-frontier.net/"


def getImagefromBase(path, gameName,gamePageHref):
	if ".." in path:
		Path(gameName + "/" + path[3:path.rindex("/")]).mkdir(parents=True, exist_ok=True)
		req = requests.get("https://e-f-frontier.net/" + path[3:],headers={"Referer": "https://e-f-frontier.net/","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
		open(gameName + "/" + path[3:], 'wb').write(req.content)
	else: 
		Path(gameName + "/" + path[0:path.rindex("/")]).mkdir(parents=True, exist_ok=True)	
		req = requests.get(baseURL + "/" + path,headers={"Referer": baseURL +"/"+gamePageHref,"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
		open(gameName + "/" + path, 'wb').write(req.content)

def get011Data(gameName,gamePageHref):
	paths = ["data/main.swf",
			"data/vo_so.swf",
			"data/s_6.swf",
			"data/s_7.swf",
			"data/s_8.swf",
			"data/s_9.swf",
			"data/s_10.swf",
			"data/s_11.swf",
			]
	Path(gameName + "/data").mkdir(parents=True, exist_ok=True)
	for path in paths:
		req = requests.get("https://e-f-frontier.net/" + gamePageHref[0: gamePageHref.rindex("/") +1] +path,headers={"Referer": "https://e-f-frontier.net/fla/fla011/011.swf","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
		open(gameName + "/" + path, 'wb').write(req.content)
	
def getGameInfo():
	gameList = []
	gamesPage = requests.get(baseURL + "/flash/flash_top.html", headers={"Referer":baseURL});
	gamesTree = HTMLParser(gamesPage.content)
	translator = Translator()
	for elem in gamesTree.css("div.bottom_right > .div1 > div > a.btn"):
		if not "http" in elem.attrs["href"]:
			gameMap = {
				"gamePageHref" : "",
				"gameBanner" : "",
				"gameTitle" : "",
				"gameSubject_jp" : "",
				"gameSubject_en" : "",
			}
			current = HTMLParser(elem.html)
			gameMap["gamePageHref"] = elem.attrs["href"][3:]
			gameMap["gameBanner"] = current.css_first("a > img").attrs["src"][3:]
			gamePage = requests.get(baseURL + "/" + gameMap["gamePageHref"], headers={"Referer":baseURL + "/flash/flash_top.html"});
			gameTree = HTMLParser(gamePage.content)
			titleString = gameTree.css_first("div.product_main_box_l > h1.mid").text().replace("＃","#")
			titlePattern = re.compile(r'([#\w ]*[0-9])(.*)',re.IGNORECASE)
			match = re.findall(titlePattern,titleString)[0]
			if match:
				gameMap["gameTitle"] = match[0]
				gameMap["gameSubject_jp"] = match[1]
				gameMap["gameSubject_en"] = translator.translate(match[1],src="ja", dest="en").text.replace('"', '「', 1).replace('"', '」', 1).replace("Lori","Loli")
			gameList.append(gameMap.copy())
	return gameList


def getGameData(gameMap):
	gameName = gameMap["gamePageHref"][gameMap["gamePageHref"].rindex("/") + 1:gameMap["gamePageHref"].rindex(".")]
	if os.path.isdir(gameName):
		gamePage = requests.get(baseURL + "/" + gameMap["gamePageHref"], headers={"Referer":baseURL + "/flash/flash_top.html"});
		gameTree = HTMLParser(gamePage.content)
		swfJSReq = requests.get(baseURL + gameTree.css_first("div.product_main_box_c > script").attrs["src"][3:],headers={"Referer":baseURL + "/flash/flash_top.html","content-type":"application/javascript"})
		swfPath = ""
		for line in io.StringIO(swfJSReq.text).readlines():
			if "document.writeln(" in line:
				swfPattern = re.compile(r'(src="(.*?)" *?width="(.*?)" *?height="(.*?)")',re.IGNORECASE)
				swfPath = re.findall(swfPattern,line)[0][1]
				print("found swf src: " + swfPath)
				width = re.findall(swfPattern,line)[0][2]
				height = re.findall(swfPattern,line)[0][3]
		if not swfPath == "":
			getImagefromBase(swfPath[3:],gameName,gameMap["gamePageHref"])
		getImagefromBase(gameMap["gameBanner"],gameName,gameMap["gamePageHref"])
		if "011" in gameMap["gameTitle"]:
			get011Data(gameName,gameMap["gamePageHref"])
		html = '''
		<!DOCTYPE html>
		<html>
			<head>
				<script src="../inject.js"></script>
				<link rel="stylesheet" href="../style.css"/>
			</head>
			<body>
				<div class="flashContainer">
					<embed class="flash" src="'''+ swfPath[3:]+ '''" width="'''+width+'''" height="'''+height+'''" type="application/x-shockwave-flash">
				</div>
			</body>

		'''		
		open(gameName + "/" + gameName+".html", 'w').write(html)	
	open(gameName + "/" + "info.json", 'w').write(json.dumps(gameMap, indent=4))



gameInfo = getGameInfo()
print("Found " + str(len(gameInfo)) + " games")

for info in gameInfo:
	getGameData(info)

