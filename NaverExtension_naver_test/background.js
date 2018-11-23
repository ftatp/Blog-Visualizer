console.log("Background!!")
window.alert("!!!!")	

var category = 0;
var url;
whale.tabs.onUpdated.addListener(function(tabid, changeinfo, tab) {
	if (tab.url != url) {
		url = tab.url;
		window.alert(url);

		if(url.match("blog.")){
			ajax_post();
		}
	}
});

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
		console.log("Connected .....");
		port.onMessage.addListener(function(msg) {
			console.log("message recieved" + msg);
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

}


