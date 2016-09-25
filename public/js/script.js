"use strict";

console.log("loaded");

function onLoad() {
	console.log("It loaded!");
	document.body.innerHTML += this.responseText;
}

function click() {
	console.log("clicked");
	var testReq = new XMLHttpRequest();
	testReq.addEventListener("load", onLoad);
	var url = "test.txt",
		url2 = "test2/test2.txt";
	testReq.open("GET", url2);
	testReq.send();
}