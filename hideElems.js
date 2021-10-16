window.onload = function() {
	document.querySelectorAll("#contentToggles > li > input").forEach(elem => {
		elem.addEventListener('change', function() {
			checkBoxToggle(this);
		});
	});
}

function checkBoxToggle(checkbox){
	if (checkbox.checked) {
		    document.querySelectorAll("."+checkbox.id.split("-")[1]).forEach(elem => {
		    	if (checkbox.id.split("-")[1] == "free" && document.querySelector("div.containers.paywall").style.display != "none" && window.innerWidth > 1620){
		    		document.querySelector("div.containers.paywall").style.marginLeft = "0px";
		    	}
		    	if (checkbox.id.split("-")[1] == "paywall" && document.querySelector("div.containers.free").style.display != "none" && window.innerWidth > 1620){
		    		document.querySelector("div.containers.paywall").style.marginLeft = "0px";
		    	}
		    	elem.style.display = "";
		    });
	} else {
		    document.querySelectorAll("."+checkbox.id.split("-")[1]).forEach(elem => {
		    	if (checkbox.id.split("-")[1] == "free" && document.querySelector(".free").style.display == "none" && window.innerWidth > 1620){
		    		document.querySelector("div.containers.paywall").style.marginLeft = "200px";
		    	}
		    	elem.style.display = "none";
		    });
	}
}

