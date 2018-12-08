whale.extension.onMessage.addListener(function(message, messageSender, sendResponse) {
    // message is the message you sent, probably an object
    // messageSender is an object that contains info about the context that sent the message
    // sendResponse is a function to run when you have a response
	if (message['msg'] == 'loading bar off'){
		$('#loading').hide();
		data = message['data'];
		console.log(data);
		change_context(data);
	}
	if (message['msg'] == 'loading bar on'){
		$('#loading').show();
	};
	if (message['msg'] == 'sidebar on'){
		whale.sidebarAction.show();
	};
});


function change_context(data){
	predict_class = data["post"].Predict["predict_classes"];
	if(predict_class == 0){
		credibility_text = "0";
	}
	else if(predict_class == 1){
		credibility_text = "1";
	}
	//...................
	//------------------------------------------------------

	predict_prob = data["post"].Predict["prob"];

	//------------------------------------------------------
	credibility_sent = "<p>????</p>";
	
	//------------------------------------------------------
	predict_cluster = data["post"].Predict["predict_cluster_class"];

 	if(predict_cluster == 5){
 		details = "<p>1. 경험적 글이 많음(1인칭, 2인칭 대명사를 제일 많이 사용함).</p><p>2. 블로그 내부 글들의 구조가 자유롭고 다양함(규칙적인 방식으로 글을 쓰지 않음)</p>";
 	}
 	else if(data["post"].Predict["predict_cluster_class"] == 6){
 		details = "<p>1. 정렬 기능을 제일 많이 사용함.</p><p>2. 주관성이 낮고 냉정함 (감정표현을 제일 쓰지 않음).</p><p>3. 이미지를 제일 많이 사용한 집단.</p>";
 	}
 	else if(data["post"].Predict["predict_cluster_class"] == 2){//2
 		details = "<p>1. 긍정 부정의 단어 표현이 가장 많이 사용됨.</p><p>2. 블로그 내부 글들의 구조가 자유롭고 다양함(규칙적인 방식으로 글을 쓰지 않음).</p><p>3. 이미지가 다른 집단과 비교하여 비교적 많이 사용됨.</p>";
 	}
 	else if(data["post"].Predict["predict_cluster_class"] == 7){//
 		details = "<p>1. 감정 단어 점수값이 높으며 스티커를 많이 사용함.</p><p>2. 해당분야에 비해서 글과 이미지 수가 많음.</p>";
 	}
 	else if(data["post"].Predict["predict_cluster_class"] == 0){
 		details = "<p>1. 물음표가 가장 많이 사용되었으며 긍정 단어의 비율이 높음.</p><p>2. 글의 길이가 가장 길고 태그를 제일 많이 사용함.</p><p>3. 띄어쓰기 오류가 많이 발견됨.</p>";
 	}
 	else if(data["post"].Predict["predict_cluster_class"] == 1){
 		details = '<p>1. 중앙정렬이 비교적 많음</p><p>2. 블로그 내부 글들의 구조가 "사진-글-사진-글-사진" 혹은 "글-사진-글-사진-글" 순으로 일관되어있음</p>';
 	}

	$('#credibility-text').html(credibility_text);
	$('#credibility-num').html("<p>신뢰성 확률: " + (100*predict_prob).toFixed(2).toString() + "%</p>");
	$('#credibility-sent').html(credibility_sent);
 	$('#details').html(details);

}


