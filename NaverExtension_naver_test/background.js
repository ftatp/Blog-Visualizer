
var category = 0;
var url;

//var port = whale.extension.connect({
//	name: "connection"		
//});
//whale.extension.onConnect.addListener(function(port){

//	window.alert(port);
whale.tabs.onUpdated.addListener(function(tabid, changeinfo, tab) {
	if (tab.url != url) {
		url = tab.url;

		// whale.tabs.executeScript(null,{
		//   code:"var s = document.createElement('div');var newContent = document.createTextNode('환영합니다!');s.appendChild(newContent);(document.body).appendChild(s);"
		// });

		if(url.match("blog.")){
			window.alert(url);
			//1. Change frontground to loading
//			whale.extension.onConnect.addListener(function(port) {
//				port.onMessage.addListener(function(msg) {
//					console.log("message received" + msg);
//					port.postMessage("Sended");
//				});
//			});

			//port.postMessage("Sended");
			//window.alert(url);

			
			
			//document.getElementById("whole").style.display = "none";
			//document.getElementById("loader").style.display = "block";

			//2. Send post to server
			ajax_post();

			//3. Make notification
			var s = document.createElement('script');
			var c = document.createElement('style');
			s.src = whale.extension.getURL('test.js');
			c.src = whale.extension.getURL('test.css');
			// s.onload = function(){
			//   this.remove();
			// };
			(document.body).appendChild(c);
			(document.body).appendChild(s);
		
		}
	}
});
//});

function ajax_post(){
	$.ajax({
		type: "POST",
		url: "http://127.0.0.1:8000/analysis/",
		data: {
			'category': category,
			'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
		},
		success: Success,
		dataType: 'json'
	});

}

function Success(data, textStatus, jqXHR){
	//$('#loading').attr('style', 'visibility:hidden');
	d3_data = data;
	console.log("HI");
	console.log(d3_data);

	whale.extension.onConnect.addListener(function(port) {
		port.onMessage.addListener(function(msg) {
			console.log("message received" + msg);
			port.postMessage(JSON.stringify(d3_data));
		});
	});

	notify = 'prob = data.post.Predict["prob"];if(prob >= 0.7){$.notify("신뢰도 높음", "success");}else if(prob >= 0.3 && prob < 0.7){$.notify("경고", "warn");}else{$.notify("위험", "error");}'


	whale.tabs.getSelected(null, function(tab){
		whale.tabs.executeScript(tab.id, {code: notify});
	});

	whale.tabs.query({active: true, currentWindow: true}, function(tabs) {
		var currTab = tabs[0];
		if (currTab) { // Sanity check
		     /* do stuff */

			prob = data.post.Predict["prob"];
			if(prob >= 0.7){
				$.notify("신뢰도 높음", "success");
			}
			else if(prob >= 0.3 && prob < 0.7){
				$.notify("경고", "warn");
			}
			else{
				$.notify("위험", "error");
			}


		}
	});

};
