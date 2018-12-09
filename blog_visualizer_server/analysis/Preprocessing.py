from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
from pykospacing import spacing
import pandas as pd
from konlpy.tag import Kkma
import numpy as np
import pickle
from keras.models import load_model
import jpype
import tensorflow as tf
from sklearn import linear_model
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# prob = 1
# predict_classes = 1
kkma = Kkma()
sentiment = pd.read_csv('static/polarity.csv')
word_list = sentiment['ngram'].tolist()
label = sentiment['max.value'].tolist()
pos_word = ['행복/NNG;하/XSV;어요/EFN;./SF','행복/NNG;하/XSV;네요/EFN;./SF','감사/NNG;하/XSV;네요/EFN','좋/VA;아요/EFN','최고/NNG;에/JKM;요/JX','추천/NNG;하/XSV;ㅂ니다/EFN;!/SF','추천/NNG;하/XSV;ㅂ니다/EFN','대박/NNG;이/VCP;에요/EFN','대박/NNG;이/VCP;에요/EFN;!/SF','최고/NNG;의/JKG','자/VA;ㄹ/ETD','되/VV;ㄹ/ETD;거/NNB;에/JKM;요/JX;!/SF','희망차/VA;ㄴ/ETD','낫/VA;은/ETD','훨씬/MAG','낫/VA;다/EFN','상쾌/XR;하/XSA;ㄴ/ETD','행복/NNG;하/XSV;ㄴ/ETD','사랑/NNG;에/JKM','기쁘/VA;어요/EFN','도전/NNG','긍정적/NNG;이/VCP;ㄴ/ETD','응원/NNG;하/XSV;ㄴ다/EFN','설레/VV;ㄴ다/EFN','설레/VV;다/EFN','예쁘/VA;다/EFN']
neg_word = ['무섭/VA;어요/EFN','무섭/VA;게/ECD','화가/NNG;나/VV;었/EPT;어요/EFN','분/NNB;이/VCP','겁쟁이/NNG;에/JKM;요/JX','겁/NNG;에/JKM','질리/VV;어서/ECD','구리/NNG;이/VCP;다/EFN','별로/MAG;네/MDN;요/NNG','별/NNG;로/XSN;에/JKM;요/JX','않/VXV;을/ETD','배리/VV;고/ECE','속/VV;았/EPT;네요/EFN','속/VV;았/EPT;어요/EFN','우울/NNG;하/XSV;ㄴ/ETD','힘들/VA;어요/EFN','어렵/VA;어요/EFN','부정적/NNG;이/VCP;ㄴ/ETD','게으르/VA;다/EFN','아프/VA;다/EFN','화나/VV;ㄴ다/EFN','불행/NNG;하/XSA;다/EFN','가난/NNG;하다/NNP']
pos_label = ['POS' for i in range(len(pos_word)) ]
neg_label = ['NEG' for i in range(len(pos_word)) ]
word_list = word_list + pos_word
word_list = word_list + neg_label
label = label + pos_label
label = label + neg_label


Category_average_img_count = {'IT·컴퓨터': 10.128282828282828,
	'건강·의학': 8.582714382174206,
	'공연·전시': 12.55934065934066,
	'교육·학문': 10.158496732026144,
	'국내여행': 26.041441441441442,
	'드라마·방송': 11.486739469578783,
	'등산·낚시·레저': 23.269372693726936,
	'만화·애니': 17.366032210834554,
	'맛집': 18.8370720188902,
	'사진': 13.06946876824285,
	'스포츠': 8.87403314917127,
	'시사·인문·경제': 5.872727272727273,
	'어학·외국어': 11.586510263929618,
	'와인·술': 7.527027027027027,
	'육아·결혼': 15.317307692307692,
	'자동차': 17.298047276464544,
	'차·커피·디저트': 14.595382746051033,
	'패션·뷰티': 14.654545454545454
}

Category_average_text_len = {'IT·컴퓨터': 1245.679798090909,
	'건강·의학': 1300.688048757597,
	'공연·전시': 1468.787912648351,
	'교육·학문': 1380.7295753839874,
	'국내여행': 1626.1315322342334,
	'드라마·방송': 1351.5803434321374,
	'등산·낚시·레저': 1542.4686354612543,
	'만화·애니': 1016.5578340849175,
	'맛집': 1341.5159389492333,
	'사진': 764.9451266549917,
	'스포츠': 1743.537016895028,
	'시사·인문·경제': 1863.716667424242,
	'어학·외국어': 12064.428153108505,
	'와인·술': 1041.2500004054054,
	'육아·결혼': 1268.576924326924,
	'자동차': 2040.659815323742,
	'차·커피·디저트': 1292.0935606075336,
	'패션·뷰티': 1270.7898993686888
}

# Data preprocessing
def Spacing_text(text_list):
	spacing_list = []
	for i in text_list:
		if len(i) < 197:
			spacing_list.append(spacing(i))
		else:
			iteration = int(len(i) / 197)
			mod = len(i) % 197
			start = 0
			end = 197
			check = 0
			while True:
				# 시행횟수 < 몫
				if check < iteration:
					spacing_list.append(spacing(i[start:end]))
					start += 197
					end += 197
					check += 1
				else:
					# 마지막 횟수 + 나머지 더 slice
					spacing_list.append(spacing(i[iteration * 197:(iteration * 197) + mod]))
					break
	return spacing_list

def remove_odd(x):
	x = re.sub("nbsp", " ", x)
	x = re.sub("\xa0", "", x)
	x = re.sub("\u200b", "", x)
	x = re.sub("\n", "", x)
	x = re.sub("\t", "", x)
	x = re.sub('   ', ' ', x)
	return x

def tfidf_vectorizer(Text):
	v_load = pickle.load(open("static/[Structure_tag]TFIDF_features_100.pkl", "rb"))
	try:
		return v_load.transform([Text]).toarray().flatten()
	except:
		return ''


class textclass:
	def Extract_structure_and_tag(User_id, Post_id):
		url = "http://blog.naver.com/PostView.nhn?blogId=" + User_id + "&logNo=" + Post_id + "&redirect=Dlog&widgetTypeCall=true"
		r = requests.get(url)
		bs = BeautifulSoup(re.sub('&nbsp;', ' ', r.text).encode("utf-8"), "html.parser")
		# structure
		structure = bs.find("div", {"id": "postViewArea"})
		if structure == None:
			structure = bs.find("div", {"class", "se_component_wrap sect_dsc __se_component_area"})

		if structure == None:
			structure = BeautifulSoup(r, "html.parser")
			

		# Title
		title = bs.find("h3", {"class": "se_textarea"})
		# 스마트에디터3 타이틀 제거 임시 적용 (클래스가 다름)
		if (title == None):
			title = bs.find("span", {"class": "pcol1 itemSubjectBoldfont"})
		if (title != None):
			title = title.text.strip()
		else:
			title = "TITLE ERROR"
	   
		#print("-----------------------Structure" + structure.text + "\n")
		#print(structure)
		structure_p_img_tag = structure.find_all(['p', 'img'])
		structure_dict = {'structure': structure, 'structure_p_img_tag': structure_p_img_tag,'Title':title}
		# structure_p_img_tag : p,img tag만 extract
		# structure : 모든 tag 가져오기
		return structure_dict

# Extract_structure_and_tag 함수의 'structure_p_img_tag' 값을 가져와야함.

	def HTML_preprocessing(structure_p_img_tag):
		# only tag & text extract
		tag_list = []
		text_list = []
		for i in structure_p_img_tag:
			# p_tag만 불러오기
			if "<p" in (str(i)):
				tag_list.append('<p>')
				# img만 있을 때

				if '<img' in str(i):
					for j in i:
						try:
							if len(j.text) > 1:
								tag_list.append('<br>')
								text_list.append(j.text)
						except:
							pass

				# img가 아닌 경우 span tag가 더 있을 때
				elif '<span' in str(i):
					for j in i:
						if '<br' in str(j):
							text_list.append(j.text)
							# br_tag가 2개 이상 있을 때

							if len(j.findAll('br')) > 2:
								for _ in range(0, len(j.findAll('br'))):
									tag_list.append('<br>')

							# br_tag가 1개 있을 때
							else:
								tag_list.append('<br>')

						# span은 있지만 br tag가 없을 때
						else:
							try:
								text_list.append(j.text)
							except:
								pass

				# 그냥 p_tag만 있을 때 br_tag 추가
				else:
					# 글이 있을 때
					if len(i.text) > 1:
						text_list.append(i.text)

					# 글 없이 br tag만 있을 때
					else:
						tag_list.append('<br>')
						text_list.append(i.text)

				# P_tag 끝맽음
				tag_list.append('</p>')

			else:
				tag_list.append('<img>')

		text_list = list(map(remove_odd, text_list))
		filter_text = list(filter(lambda x: len(x) > 1, text_list))

		Text = " ".join(list(filter(lambda x: len(x) > 1, map(lambda x: x.strip(), text_list))))
		Text = re.sub('\n', '', Text)
		Text = re.sub('\t', '', Text)
		Space_text = " ".join(Spacing_text(filter_text))
		Count_space_mistake = len(Space_text) - len(Text)

		# only tag
		Structure_only_tag = "|".join(tag_list)
		Structure_only_tag_df = pd.DataFrame({'text': [Structure_only_tag]})
		array_temp = Structure_only_tag_df['text'].apply(
			lambda x: " img ".join(list(map(lambda x: 'text' if len(x) > 3 else '', x.split('<img>')))).strip().replace(
				'  ', ' ')).values
		refined_structure = ''.join(array_temp)

		HTML_preprocessing = {'Text': Text, 'refined_structure': refined_structure,
							  'Count_space_mistake': Count_space_mistake}

		return HTML_preprocessing

	def sentimental_analysis(text):
		pos_word_list = []
		neg_word_list = []
		neut_word_list = []
		pos_ratio = 0.000000001
		neg_ratio = 0.000000001
		subjectivity = 0.000000001
		polarity = 0.000000001
		senti_diffs_per_ref = 0.000000001

		if text == '':
			sentiment_dict = {
				'pos_ratio': pos_ratio, 
				'neg_ratio': neg_ratio, 
				'subjectivity': subjectivity,
				'polarity': polarity,
				'senti_diffs_per_ref': senti_diffs_per_ref
			}

			return sentiment_dict, pos_word_list, neg_word_list, neut_word_list
		else:
			pos = 0
			neg = 0
			neut = 0

			text = text.split(' ')
			n = len(text)
			for i in text:
				i = remove_odd(i)
				jpype.attachThreadToJVM()
				pre = kkma.pos(i)
				test = ';'.join(['/'.join(i) for i in pre])
				if test in word_list:
					if label[word_list.index(test)] == 'POS':
						pos += 1
						pos_word_list.append(test)
					elif label[word_list.index(test)] == 'NEG':
						neg += 1
						neg_word_list.append(test)
					elif label[word_list.index(test)] == 'NEUT':
						neut += 1
						neut_word_list.append(test)
			try:
				pos_ratio = pos / n
			except:
				pass
			try:
				neg_ratio = neg / n
			except:
				pass
			try:
				subjectivity = (neg + pos) / n
			except:
				pass
			try:
				polarity = (neg - pos) / (neg + pos)
			except:
				pass
			try:
				senti_diffs_per_ref = (pos - neg) / n
			except:
				pass

			sentiment_dict = {
				'pos_ratio': pos_ratio, 
				'neg_ratio': neg_ratio, 
				'subjectivity': subjectivity,
				'polarity': polarity,
				'senti_diffs_per_ref': senti_diffs_per_ref
			}
			
			return sentiment_dict, pos_word_list, neg_word_list, neut_word_list

	def check_First_second(Text):
		first_person = ['나/NP', '저/NP', '내/NP', '제/NP', '저희/NP', '우리/NP']
		second_person = ['너/NP', '자네/NP', '당신/NP', '그대/NP', '그쪽/NP', '너희/NP', '자기/NP']
		First = 0
		Second = 0
		if Text == '':
			check_First_second_dict = {'First_ratio': First, 'Second_ratio': Second}
		
			return check_First_second_dict
		else:
			text = kkma.pos(Text)
			for i in text:
				temp = "/".join(i)
				if temp in first_person:
					First += len(temp.split('/')[0])
				if temp in second_person:
					Second += len(temp.split('/')[0])
			check_First_second_dict = {'First_ratio': First / len(Text), 'Second_ratio': Second / len(Text)}
			
			return check_First_second_dict

class otherclass:
	def effort_check(Category,Text_len,Img_count):
		effort_text = Text_len / Category_average_text_len[Category]
		effort_img = Img_count / Category_average_img_count[Category]

		effort_dict = {'effort_ratio':effort_text,'effort_img_ratio':effort_img}
		return effort_dict

	def Tag_count(url):        
#         driver = webdriver.Chrome('static/chromedriver')
#         driver.get(url)
#         driver.implicitly_wait(10)
#         tag_count = len(re.sub('\n','',driver.find_element_by_class_name('wrap_tag').text).strip().split('#')[1:])
		caps = DesiredCapabilities().CHROME
		caps["pageLoadStrategy"] = "normal"  #  complete
		options = ['--disk-cache=true']
		driver = webdriver.PhantomJS('static/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',service_args=options,desired_capabilities=caps)
		# URL 읽어 들이기
		driver.get(url)
		tag_count = len(driver.find_element_by_class_name('wrap_tag').text.split('#')[1:])
		tag_dict = {'tag_count':tag_count}
		driver.close()
		return tag_dict

	def check_dbdbdeep_type(text):
		detect_dbdbdeep_item = ['소정의', '원고료', '지원', '마케팅이즈', '의료광고']
		ls_dbdbdeep = 0
	
		# dbdbdeep 찾기
		for item in detect_dbdbdeep_item:
			p = re.compile(item)
			if p.search(text):
				ls_dbdbdeep = 1
				break
				
		if ls_dbdbdeep == 1:
			return 0
		else:
			return 1

	def check_blog_type(text):
		experience_item = ['당첨', '무상으로 제공받아', '무료로 제공받아', '직접검증', '품평단', '제공받아', '솔직하게', '주관적인', '선정', '르뷰', '서울오빠', '위블', '체험단', '블로그원정대', '블로그 잇']
		detect_dbdbdeep_item = ['소정의', '원고료', '지원받아', '마케팅이즈', '의료광고']
		ls_dbdbdeep = 0
		ls_experience = 0

# 체험형 찾기
		for item in experience_item:
			p = re.compile(item)
			if p.search(text):
				ls_experience = 1
				break

# dbdbdeep 찾기
		if ls_experience == 0:
			for item in detect_dbdbdeep_item:
				p = re.compile(item)
				if p.search(text):
					ls_dbdbdeep = 1
					break

		if ls_experience == 1:
			return 1
		elif ls_dbdbdeep == 1:
			return 2
		else:
			print("else")
			return 3



class htmlclass:
	def Extract_Alignment(structure):
		# Align
		split_structure =  remove_odd(str(structure)).split('>')
		center= 0
		left = 0
		right = 0
		justify = 0
		for item in split_structure:
			if 'align' or 'ALIGN' in str(item):
				if 'center' in str(item):
					center +=1
				if 'left' in str(item):
					left += 1
				if 'right' in str(item):
					right +=1
				if 'justify' in str(item):
					justify +=1
		Align = [left, center, right, justify]
		return Align

	def Extract_Sticker_count(structure):
		Sticker_count = 0
		# Sticker_count로 수정
		sticker_img = structure.find_all('a')
		for i in sticker_img:
			if 'sticker' in str(i):
				Sticker_count += 1
		return Sticker_count


def get_naver_post_all_data(User_id, Post_id):
	Category = np.array(['IT·컴퓨터', '건강·의학', '공연·전시', '교육·학문', '국내여행', '드라마·방송', '등산·낚시·레저',
		   '만화·애니', '맛집', '사진', '스포츠', '시사·인문·경제', '어학·외국어', '와인·술', '육아·결혼',
		   '자동차', '차·커피·디저트', '패션·뷰티'])

	#User_id = 'newpark314'
	#Post_id = '221387605004'
	#Category = '맛집'

	url = "http://blog.naver.com/PostView.nhn?blogId=" + User_id + "&logNo=" + Post_id + "&redirect=Dlog&widgetTypeCall=true"
	mobile_url = "http://m.blog.naver.com/PostView.nhn?blogId="+ User_id
	opening_url = 'http://blog.naver.com/profile/intro.nhn?blogId='+ User_id

	# Text_len, Question_count, Sentiment(pos_ratio, neg_ratio, subjectivity, polarity, sentiment_diff_ref)
	# Count_Space_mistake, First_ratio, Second_ratio

	structure = textclass.Extract_structure_and_tag(User_id, Post_id)
	all_tag = structure['structure']
	p_img_tag = structure['structure_p_img_tag']
	title = structure['Title']
	HTML_preprocessing = textclass.HTML_preprocessing(p_img_tag)
	text = HTML_preprocessing['Text']
	#check = otherclass.check_dbdbdeep_type(text)
	blog_type = otherclass.check_blog_type(text)

	# Category prediction
	#Tfidf_model로 교체
	tfidf_text = 'static/tfidf_text.pkl'
	tfidf_title = 'static/tfidf_title_.pkl'
	logreg_model = 'static/Category_model.pkl'
	logreg = pickle.load(open(logreg_model, 'rb'))
	vectorizer_Text = pickle.load(open(tfidf_text, 'rb'))
	vectorizer_Title = pickle.load(open(tfidf_title, 'rb'))

	text_vec = vectorizer_Text.transform([text])
	text_vec = pd.DataFrame(text_vec.toarray())
	title_vec = vectorizer_Title.transform([title])
	title_vec = pd.DataFrame(title_vec.toarray())
	x = pd.concat([text_vec,title_vec], axis=1)
	Category = Category[logreg.predict(x)[0]]

	print("User id: " + User_id + "\nPost id: " + Post_id + "\nCategory: " + Category)

	# variables
	Text_len = len(text)
	Count_Space_mistake = HTML_preprocessing['Count_space_mistake']
	Question_count = text.count('?')
	
	sentiment_pre = textclass.sentimental_analysis(text)
	sentiment = sentiment_pre[0]
	pos_word = sentiment_pre[1]
	neg_word = sentiment_pre[2]
	neut_word = sentiment_pre[3]
	
	first_second = textclass.check_First_second(text)
	# Alignment(Left,Center,Right,Justify), Sticker_count
	Alignment = htmlclass.Extract_Alignment(all_tag)
	Sticker_count = htmlclass.Extract_Sticker_count(all_tag)
	# Effort(effort_ratio,effort_img_ratio), Tag_count
	refined_structure = HTML_preprocessing['refined_structure']
	Img_count = refined_structure.count('img')
	Effort = otherclass.effort_check(Category,Text_len,Img_count)
	Tag_count = otherclass.Tag_count(url)['tag_count']

# user_information
# 사용자 정보
# user_information = chorme_class.user_information(mobile_url,opening_url)

##  user variables
#	Blog_name = user_information['Blog_name']
#	Blog_nickname = user_information['Blog_nickname']
#	Count_neighbors = user_information['Count_neighbors']
#	Count_visitors = user_information['Count_visitors']
#	blog_opening_date = user_information['blog_opening_date']


	# tfidf, keras model, cluster model
	# variable
	Structure_13 = tfidf_vectorizer(refined_structure)

	# Data organization
	list_1 = [
		Question_count, first_second['First_ratio'], first_second['Second_ratio'], Tag_count,
		sentiment['pos_ratio'], sentiment['neg_ratio'], sentiment['subjectivity'], sentiment['polarity'], sentiment['senti_diffs_per_ref'],
		Sticker_count, Text_len, Count_Space_mistake, Effort['effort_ratio'], Effort['effort_img_ratio'],
		Alignment[0], Alignment[1], Alignment[2], Alignment[3]
	]

	list_2 = Structure_13.tolist()

	total_dataset = list_1 + list_2
	origin_df = pd.DataFrame(total_dataset).T
	origin_df.columns = [
		'Question_count', 'First_ratio', 'Second_ratio', 'Tag_count', 
		'pos_ratio', 'neg_ratio', 'subjectivity', 'polarity', 'senti_diffs_per_ref',
		'Sticker_count', 'Text_len','Count_space_mistake',
	 	'effort_ratio', 'effort_img_ratio',
		'Left', 'Center','Right','Justify',
	 	'img img img img img', 'img img img img text', 'img img img text img','img img text img img','img img text img text',
	 	'img text img img img', 'img text img img text' ,'img text img text img','text img img img img','text img img img text',
	 	'text img img text img', 'text img text img img', 'text img text img text'
	]

	# keras
	## Standard scaler model load
	scalerfile = 'static/scaler.pkl'
	scaler = pickle.load(open(scalerfile, 'rb'))
	# transform data
	origin_df = origin_df.fillna(0)
	X_scaled = pd.DataFrame(scaler.transform(origin_df), columns = origin_df.columns)

	#check_df = pd.DataFrame({'check': [check]})
	#X_scaled = pd.concat([X_scaled, check_df], axis=1)

	# MLP model load
	mlp_clf_name = 'static/MLP.pkl'
	mlp_clf = pickle.load(open(mlp_clf_name, 'rb'))
	predict_classes = mlp_clf.predict(X_scaled.values.reshape((1, 31))).item()
	prob = mlp_clf.predict_proba(X_scaled.values.reshape((1, 31)))[0][1]
	   
# keras model load

#    graph = tf.get_default_graph()
#    with graph.as_default():
#        # data type reshape & predict probability
#        prob = model.predict(X_scaled.values.reshape((1, 31))).item()
#        predict_classes = model.predict_classes(X_scaled.values.reshape((1, 31))).item()
#
#    test = load_model(X_scaled)
#    prob = test['prob']
#    predict_classes = test['predict_classes']

	# Cluster는 cluster model자체가 scaler로 된 모델이라 그냥 origin 값 집어 넣어야함.

	clusterfile = 'static/8-means(0,1,2,5,6,7).pkl'
	cluster = pickle.load(open(clusterfile, 'rb'))
	# predict cluster class
	predict_cluster_class = cluster.predict(origin_df).item()
	if (predict_cluster_class == 3) or (predict_cluster_class == 4):
		predict_cluster_class = 1



	# Final save csv file
	Predict_df = pd.DataFrame({'prob':prob,'predict_classes':predict_classes,'predict_cluster_class':predict_cluster_class},index=[0])
	#user_df = pd.DataFrame({'Blog_name':Blog_name,'Blog_nickname':Blog_nickname,'Count_neighbors':Count_neighbors,'Count_visitors':Count_visitors,'blog_opening_date':blog_opening_date},index=[0])
	value = pd.concat([X_scaled,Predict_df],axis=1)
	# pos_word
	# neg_word

	Predict_dict = {
		'prob': prob,
		'predict_classes': predict_classes,
		'predict_cluster_class': predict_cluster_class,
		'blog_type': blog_type
	}
#user_dict = {'Blog_name':Blog_name,'Blog_nickname':Blog_nickname,'Count_neighbors':Count_neighbors,'Count_visitors':Count_visitors,'blog_opening_date':blog_opening_date}
#

#if Predict_dict.predict_

	refined_X_scaled = X_scaled.T.to_dict()[0]

	Structure = {
		'img img img img img': refined_X_scaled['img img img img img'],
		'img img img img text':refined_X_scaled['img img img img text'],
		'img img img text img':refined_X_scaled['img img img text img'],
		'img img text img img' :refined_X_scaled['img img text img img'],
		'img img text img text':refined_X_scaled['img img text img text'],
		'img text img img img':refined_X_scaled['img text img img img'],
		'img text img img text':refined_X_scaled['img text img img text'],
		'img text img text img':refined_X_scaled['img text img text img'],
		'text img img img img':refined_X_scaled['text img img img img'],
		'text img img img text':refined_X_scaled['text img img img text'],
		'text img img text img':refined_X_scaled['text img img text img'],
		'text img text img img':refined_X_scaled['text img text img img'],
		'text img text img text':refined_X_scaled['text img text img text']}

	Sentiment = {
		'pos_ratio': refined_X_scaled['pos_ratio'],
		'neg_ratio':refined_X_scaled['neg_ratio'],
		'subjectivity':refined_X_scaled['subjectivity'],
		'polarity' :refined_X_scaled['polarity'],
		'senti_diffs_per_ref':refined_X_scaled['senti_diffs_per_ref']
	}

	Other = {
		'Question_count':refined_X_scaled['Question_count'],
		'First_ratio': refined_X_scaled['First_ratio'],
		'Second_ratio':refined_X_scaled['Second_ratio'],
		'Tag_count':refined_X_scaled['Tag_count'],
		'Sticker_count':refined_X_scaled['Sticker_count'],
		'Text_len':refined_X_scaled['Text_len'],
		'Count_space_mistake':refined_X_scaled['Count_space_mistake'],
		'effort_ratio':refined_X_scaled['effort_ratio'],
		'effort_img_ratio':refined_X_scaled['effort_img_ratio'],
		'Left' :refined_X_scaled['Left'],
		'Center':refined_X_scaled['Center'],
		'Right':refined_X_scaled['Right'],
		'Justify':refined_X_scaled['Justify']}

	all_data = {
		'Structure': Structure,
		'Sentiment': Sentiment,
		'Other': Other,
		'Predict': Predict_dict,
		#'User': user_dict,
		'words': {
			'positive': pos_word,
			'negative': neg_word,
			'neutral' : neut_word
		}
	}

	return all_data
