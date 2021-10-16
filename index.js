const { app, BrowserWindow } = require('electron')
const fs = require('fs')


function generateHTML(){
	let gameDir = "./games/swf"
	let containerDivs = "";
	let navDiv = '<div class="navBar"><img class="navLogo" src="logo.png"/>'+
	'<ul id="contentToggles">' + 
	'<li><input id="toggle-swf" type="checkbox" checked="true"><label for="toggle-swf">Flash</label></li>'+
	'<li><input id="toggle-free" type="checkbox" checked="true"><label for="toggle-free">Free</label></li>'+
	'<li><input id="toggle-paywall" type="checkbox" checked="true"><label for="toggle-paywall">Paywalled</label></li>'+
	'</ul>' +
	'</img><ul class="navLinks swf">';
	let files = fs.readdirSync(gameDir)
	let containerEnd = "";
	let navEnd = "";
	files.forEach(game => {
		let stat = fs.lstatSync(gameDir+"/"+game);
		if (stat.isDirectory()){
			let infoFile = fs.readFileSync(gameDir+"/"+game+"/info.json");
			let gameData = JSON.parse(infoFile);
			let container = "";
			let nav = "";
			container = '<div class="swfInfoContainer  swf" id="'+game+'"">'+
  						'<a class="swfLink" href="games/swf/'+game+"/"+game+'.html">' +
  						'<div class="metaData">' + 
	  						'<h2 class="gameSubject eng">' + gameData.gameSubject_en +  '</h1>' +
	  						'<h2 class="gameSubject jap">' + gameData.gameSubject_jp +  '</h1>' +
  						'</div>' + 
  						'<div class="gameImages">' +
  							'<img class="gameBanner" src="games/swf/'+game+"/"+gameData.gameBanner+'"/>' + 
		  				'</div>'+
		  				'</a>' +
					'</div>';
			nav = '<li><a href="#'+game+'">'+gameData.gameTitle+'</a></li>';
			containerDivs += container;
			navDiv += nav;		
		}
	});
	let swfContainer = '<div class="containers swf">' + containerDivs + containerEnd + '</div>';
	navDiv += navEnd + '</ul><ul class="navLinks free">'
	containerDivs = "";
  	navEnd = "";
  	containerEnd = "";
	gameDir = "./games/free";
	files = fs.readdirSync(gameDir);
	files.forEach(game => {
		console.log(game);
		let stat = fs.lstatSync(gameDir+"/"+game);
		
		if (stat.isDirectory()){
			let infoFile = fs.readFileSync(gameDir+"/"+game+"/info.json");
			let gameData = JSON.parse(infoFile);
			let container = "";
			let nav = "";
			console.log(gameData.gameTitle);
			if (!gameData.gameImage.includes("mov")){
				container = '<div class="gameInfoContainer  free" id="'+game+'"">'+
						'<div class="metaData">' + 
  						'<h2 class="gameSubject eng">' + gameData.gameSubject_en.replace('"','「').replace('"','」') +  '</h1>' +
  						'<p class="gameDescription eng">' + gameData.gameDescription_en + "</p>" +
  						'<h2 class="gameSubject jap">' + gameData.gameSubject_jp +  '</h1>' +
  						'<p class="gameDescription jap">' + gameData.gameDescription_jp + "</p>" +
						'</div>' + 
  						'<div class="gameImages">' +
  							'<img class="gameBanner" src="games/free/'+game+"/"+gameData.gameBanner+'"/>' + 
	  						'<a href="games/free/' + game + '/' +game + '.html">' +
		  							'<img src="games/free/'+game+"/"+gameData.gameImage+'"/>' + 
		  					'</a>' +
	  					'</div>'+
					'</div>';
			} 
			else {
				container = '<div class="gameInfoContainer  free" id="'+game+'"">'+
  						'<div class="metaData">' + 
	  						'<h2 class="gameSubject eng">' + gameData.gameSubject_en.replace('"','「').replace('"','」') +  '</h1>' +
	  						'<p class="gameDescription eng">' + gameData.gameDescription_en + "</p>" +
	  						'<h2 class="gameSubject jap">' + gameData.gameSubject_jp +  '</h1>' +
	  						'<p class="gameDescription jap">' + gameData.gameDescription_jp + "</p>" +
  						'</div>' + 
  						'<div class="gameImages">' +
  							'<img class="gameBanner" src="games/free/'+game+"/"+gameData.gameBanner+'"/>' + 
  							'<video controls>' + 
  								'<source src="games/free/'+game+"/"+gameData.gameImage+'" type="video/mp4"/>' +
  							'</video>' 
		  				'</div>'+
					'</div>';
			}
			nav = '<li><a href="#'+game+'">'+gameData.gameTitle+'</a></li>';
			if (game == "12" || game == "Md-a1"){
				containerEnd += container;
				navEnd += nav;
			} else {
				containerDivs += container;
				navDiv += nav;
			}
		}

	});
  	let freeContainer = '<div class="containers free">' + containerDivs + containerEnd + '</div>';
  	navDiv += navEnd + '</ul><ul class="navLinks paywall">'
  	containerDivs = "";
  	navEnd = "";
  	containerEnd = "";
	gameDir = "./games/paywall";
	files = fs.readdirSync(gameDir);
	console.log(files.length);
	files.forEach(game => {
		let stat = fs.lstatSync(gameDir+"/"+game);
		if (stat.isDirectory()){
			let infoFile = fs.readFileSync(gameDir+"/"+game+"/info.json");
			let gameData = JSON.parse(infoFile);
			let container = "";
			let nav = "";
			console.log(gameData.gameTitle);
			if (!gameData.gameImage.includes("mov")){
				container = '<div class="gameInfoContainer  paywall" id="'+game+'"">'+
						'<div class="metaData">' + 
  						'<h2 class="gameSubject eng">' + gameData.gameSubject_en.replace('"','「').replace('"','」') +  '</h1>' +
  						'<p class="gameDescription eng">' + gameData.gameDescription_en + "</p>" +
  						'<h2 class="gameSubject jap">' + gameData.gameSubject_jp +  '</h1>' +
  						'<p class="gameDescription jap">' + gameData.gameDescription_jp + "</p>" +
						'</div>' + 
  						'<div class="gameImages">' +
  							'<img class="gameBanner" src="games/paywall/'+game+"/"+gameData.gameBanner+'"/>' + 
	  						'<a href="games/paywall/' + game + '/' +game + '.html">' +
		  							'<img src="games/paywall/'+game+"/"+gameData.gameImage+'"/>' + 
		  					'</a>' +
	  					'</div>'+
					'</div>';
				
			} 
			else {
				container = '<div class="gameInfoContainer  paywall" id="'+game+'"">'+
  						'<div class="metaData">' + 
	  						'<h2 class="gameSubject eng">' + gameData.gameSubject_en.replace('"','「').replace('"','」') +  '</h1>' +
	  						'<p class="gameDescription eng">' + gameData.gameDescription_en + "</p>" +
	  						'<h2 class="gameSubject jap">' + gameData.gameSubject_jp +  '</h1>' +
	  						'<p class="gameDescription jap">' + gameData.gameDescription_jp + "</p>" +
  						'</div>' + 
  						'<div class="gameImages">' +
  							'<img class="gameBanner" src="games/paywall/'+game+"/"+gameData.gameBanner+'"/>' + 
  							'<video controls>' + 
  								'<source src="games/paywall/'+game+"/"+gameData.gameImage+'" type="video/mp4"/>' +
  							'</video>' 
		  				'</div>'+
					'</div>';
			}
			nav = '<li><a href="#'+game+'">'+gameData.gameTitle+'</a></li>';
			if (game == "12" || game == "Md-a1"){
				containerEnd += container;
				navEnd += nav;
			} else {
				containerDivs += container;
				navDiv += nav;
			}
				
		}
	});
  	paywallContainer = '<div class="containers paywall">' + containerDivs + containerEnd + '</div>';
  	navDiv += navEnd
  	navDiv += '</ul></div>';
  	writeHTML(navDiv + '<div class="main">' + swfContainer + freeContainer + paywallContainer + '</div>');
	
}
function writeHTML(bodyElems){
	let pageTop = '<!doctype html>' + '<html> <head><title>e.f.frontier Minigame Collection</title><link rel="stylesheet" href="index.css"><script src="hideElems.js"></script></head><body>';
	let pageBottom = '</body> </html>';
	try {
  		fs.writeFileSync('./index.html', pageTop + bodyElems + pageBottom);
	} catch (err) {
  		console.error(err);
	}

}
function createWindow () {  
	const win = new BrowserWindow({
		width:800,
		height:600,
		minWidth:500,
		minheight:600,
		webPreferences: {
			plugins: true
    	},
  	});
  	win.loadFile('index.html');
  	//win.webContents.openDevTools()
  	win.removeMenu();
}

	generateHTML();
	/*let pluginName;
	  switch (process.platform) {
	    case 'win32':
	      pluginName = 'plugins/pepflashplayer.dll'
	      break
	    case 'darwin':
	      pluginName = 'plugins/Player.plugin'
	      break
	    case 'linux':
	      pluginName = 'plugins/libpepflashplayer.so'
	      break
	  }
	app.commandLine.appendSwitch('ppapi-flash-path', path.join(__dirname, pluginName))*/
	app.whenReady().then(() => {  createWindow()});