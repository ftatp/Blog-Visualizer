whale.extension.onMessage.addListener(function(message, messageSender, sendResponse) {
    // message is the message you sent, probably an object
    // messageSender is an object that contains info about the context that sent the message
    // sendResponse is a function to run when you have a response
	if (message['msg'] == 'loading bar off'){
		console.log("mess: loading bar off");
		$('#loading').hide();
		data = message['data'];
		console.log(data);
		change_context(data);

		//Load sentiment word
		senti_words = data.post.words

		var sentiment_class = ['Positive', "Neutral", "Negative"];
		var sentiment_value = [senti_words.positive.length, senti_words.neutral.length, senti_words.negative.length];

		var temp_sentiment_data = change_data_type(sentiment_value, sentiment_class);
		console.log(temp_sentiment_data);
		draw_sentiment_pie(temp_sentiment_data);
		
		//Load piebarchart 
		var change_cluster6 = change_index(cluster6);
		var change_cluster7 = change_index(cluster7);
		var change_feature = change_index(features_name);


		var feature_set_names = ['글의 구조', '기타 정보', '글의 감정'];
		var feature_nums = [13, 13, 5];

	
		post = data.post
		var post_list = [
			post.Structure['img img img img img'],		
			post.Structure['img img img img text'],
			post.Structure['img img img text img'],
			post.Structure['img img text img img'],
			post.Structure['img img text img text'],
			post.Structure['img text img img img'],
			post.Structure['img text img img text'],
			post.Structure['img text img text img'],
			post.Structure['text img img img img'],
			post.Structure['text img img img text'],
			post.Structure['text img img text img'],
			post.Structure['text img text img img'],
			post.Structure['text img text img text'],

			post.Sentiment['pos_ratio'],
			post.Sentiment['neg_ratio'],
			post.Sentiment['subjectivity'],
			post.Sentiment['polarity'],
			post.Sentiment['senti_diffs_per_ref'],

			post.Other['Question_count'],
			post.Other['First_ratio'],
			post.Other['Second_ratio'],
			post.Other['Tag_count'],
			post.Other['Sticker_count'],
			post.Other['Text_len'],
			post.Other['Count_space_mistake'],
			post.Other['effort_ratio'],
			post.Other['effort_img_ratio'],
			post.Other['Left'],
			post.Other['Center'],
			post.Other['Right'],
			post.Other['Justify']
		];


		var left_mod_cluster0 = normalizeCluster(post_list);
		drawPie(feature_set_names, feature_nums, left_mod_cluster0);

		var cluster = data.post.Predict.predict_cluster_class;
		var cluster_list = "";
		if(cluster == 0)
			cluster_list = cluster0;
		else if(cluster == 1)
			cluster_list = cluster1;
		else if(cluster == 2)
			cluster_list = cluster2;
		else if(cluster == 5)
			cluster_list = cluster5;
		else if(cluster == 6)
			cluster_list = cluster6;
		else
			cluster_list = cluster7;
		
		var lefts = document.getElementsByClassName("total_left");

		//$(.total_left).find
		var right_mod_cluster1 = normalizeCluster(cluster_list);
		drawPie2(feature_set_names, feature_nums, right_mod_cluster1);

		//Load RadarChart

	}
	if (message['msg'] == 'loading bar on'){
		$('#loading').show();
	};
	if (message['msg'] == 'sidebar on'){
		whale.sidebarAction.show();
	};
});


function change_context(data){
	//predict_class = data["post"].Predict["predict_classes"];
	image_url = "";
	color_code = "";
	//내용 변경: 신뢰도 텍스트
	predict_prob = data["post"].Predict["prob"];
	if(predict_prob >= 0.7){
		credibility_text = "좋음";
		image_url = '/resource/project/good.png';
		color_code = "#4C994E";
	}
	else if(predict_prob >= 0.3 && predict_prob < 0.7){
		credibility_text = "주의";
		image_url = '/resource/project/soso.png';
		color_code = "#E77C19";
	}
	else{
		credibility_text = "경계";
		image_url = '/resource/project/alert.png';
		console.log(image_url);
		color_code = "#BF604A";
	}

	//------------------------------------------------------
	//내용 변경: 블로그 타입
	predict_type = data["post"].Predict["blog_type"];
	
	if(predict_type == 1){
		credibility_sent = "<p>제품을 업체로부터 제공받아 체험 후 작성한 글로 추정됩니다</p>";
	}
	else if(predict_type == 2){
		credibility_sent = "<p>업체로부터 사진과 글을 제공받아 작성한 글로 추정됩니다</p>";
	}
	else{
		credibility_sent = "<p>일반 블로거의 글로 추정됩니다</p>";
	}

	//------------------------------------------------------
	//내용 변경: 블로그 군집 특징
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

	//-------------------------------------------------------
  
	
	$('.floating-image').css('background-image', "url(" + image_url + ")");
	
	$('#credibility-text').html(credibility_text);
	$('#credibility-text').css('color', color_code);
	$('#credibility-num').html("<p>신뢰성 확률: " + (100*predict_prob).toFixed(2).toString() + "%</p>");
	$('#credibility-sent').html(credibility_sent);
 	$('#details').html(details);

}


