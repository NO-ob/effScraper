
window.onload = function(){
  if (!document.getElementById("homeButton")) {
    let homeButton = document.createElement("Button");
  homeButton.innerHTML = "Home";
  homeButton.setAttribute("id", "homeButton");
  homeButton.style = "top:0;right:0;position:absolute;z-index: 9999;background-color: white; color: #2F9B8D;margin:1em;border-color:#2F9B8D";
  document.body.appendChild(homeButton);
  document.getElementById("homeButton").addEventListener('click', () => {
      document.location.href = document.URL.split("games")[0]+"index.html#" + document.URL.substring(document.URL.lastIndexOf("/") + 1,document.URL.lastIndexOf("."));
    }, false);
  }
  scaleFlash();
}
window.onresize = scaleFlash;

function scaleFlash(){
    let embed = document.querySelector("embed.flash");
    console.log(embed.width)
    embed.width =(window.innerHeight * (embed.width / embed.height)) * 0.95;
    embed.height = window.innerHeight * 0.95;
}
