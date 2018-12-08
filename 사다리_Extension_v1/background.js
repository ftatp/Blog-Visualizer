
var category = 0;
var url="";

whale.sidebarAction.show();
whale.sidebarAction.hide();

whale.tabs.onUpdated.addListener(function(tabid, changeinfo, tab) {
	if (tab.url != url) {
		url = tab.url;
		if(url.match("blog.naver.com") || url.match("blog.me")) {
			whale.runtime.sendMessage({msg: 'loading bar on'});
			ajax_post();
		};
	};
});

function ajax_post(){
	$.ajax({
		type: "POST",
		url: "http://127.0.0.1:8000/analysis/",
		//url: "http://54.180.25.83:8000/analysis/",
		data: {
			'url': url,
			'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
		},
		success: Success,
		dataType: 'json'
	});

};

function Success(data, textStatus, jqXHR){
	d3_data = data;
	var s = document.createElement('script');
	s.src = whale.extension.getURL('test.js');
	(document.body).appendChild(s);
	whale.runtime.sendMessage({msg: 'loading bar off', data: data});
};


