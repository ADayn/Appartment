"use strict";

console.log("loaded2");

function onLoad2() {
	console.log("It loaded!2");
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

function test() {
	console.log("tested");
}
