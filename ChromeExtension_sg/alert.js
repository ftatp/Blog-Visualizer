document.write("I'm here");

var hr = new XMLHttpRequest();
var url = "http://localhost:8000/";

var fn = document.getElementById("user").value;
var ln = document.getElementById("details").value;
var vars = "name=" + fn + "&details=" + ln;
hr.open("POST", url, true);

hr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")

hr.send(vars)

