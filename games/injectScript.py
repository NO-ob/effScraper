import re
import sys
import requests
import json
import os
from selectolax.parser import HTMLParser

for dir in os.listdir("./"):
	if not "." in dir:
		if os.path.isfile(dir+"/"+dir+".html"):
			htmlFile = open(dir+"/"+dir+".html","r")
			lines = htmlFile.readlines()
			os.remove(dir+"/"+dir+".html") 
			newhtmlFile = open(dir+"/"+dir+".html","w")
			for line in lines:
				newhtmlFile.write(line)
				if "</style>" in line:
					newhtmlFile.write('<script src="../inject.js"></script>\n')
			print(dir+"/"+dir+".html")		