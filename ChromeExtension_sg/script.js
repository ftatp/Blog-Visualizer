var loginPayload = {
	"d": "dfsjrskrtdsktd"

};

var callback = function (response) {
	console.log(response);
};

var handle_error = function (obj, error_text_status){
	console.log(error_text_status + " " + obj);
};

/*
$.ajax({
	url: 'https://127.0.0.1:8000/analysis',
	type: 'POST',
	success: callback,
	data: JSON.stringify(loginPayload),
	contentType: 'application/json',
	error: handle_error
});
*/
function Success(data, textStatus, jqXHR){
	//$('#loading').attr('style', 'visibility:hidden');
	$('#resultDiv').html(data);
}

$(function(){
	$('#clickme').on("click", function(){
		//var tr = $(this);
		//var td = tr.children();
		var tmp = "HI"; //+ td.eq(1).text().split(" ")[0]
		//$(this).siblings().css("background-color", "white");
		//$(this).css("background-color", "#D3FFFE");
		loginPayload.username = document.getElementById('name').value;
		loginPayload.password = document.getElementById('details').value;
		console.log(loginPayload);


		$.ajax({
			type: "POST",
			url: "http://127.0.0.1:8000/analysis/",
			data: {
				'search_list': tmp + loginPayload.username,
				'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
			},
			
		success: Success,
		dataType: 'html'
		});
//
//		var xhr = new XMLHttpRequest();
//		xhr.onreadystatechange = handleStateChange; // Implemented elsewhere.
//		xhr.open("GET", chrome.extension.getURL('http://127.0.0.1:8000'), true);
//		xhr.send();
	});

//	$("#prescription_text_1").text("총 {{ prescriptions_cnt }}개 데이터 검색됨");
});



