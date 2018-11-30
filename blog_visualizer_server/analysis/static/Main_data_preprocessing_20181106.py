
# coding: utf-8

# In[29]:

from bs4 import BeautifulSoup 
import re
import requests
from selenium import webdriver
from pykospacing import spacing
import pandas as pd
from konlpy.tag import Kkma
import numpy as np
import pickle


# In[30]:

kkma = Kkma()
sentiment = pd.read_csv('polarity.csv')
word_list = sentiment['ngram'].tolist()
label = sentiment['max.value'].tolist()


# In[31]:

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
 '패션·뷰티': 14.654545454545454}

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
 '패션·뷰티': 1270.7898993686888}


# # Data preprocessing

# In[32]:

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
    try:
        return v_load.transform([Text]).toarray().flatten()
    except:
        return ''


# In[33]:

class textclass:
    def Extract_structure_and_tag(User_id, Post_id):
        url = "http://blog.naver.com/PostView.nhn?blogId=" + User_id + "&logNo=" + Post_id + "&redirect=Dlog&widgetTypeCall=true"
        r = requests.get(url)
        bs = BeautifulSoup(re.sub('&nbsp;', ' ', r.text).encode("utf-8"), "html.parser")
        # structure
        structure = bs.find("div", {"id": "postViewArea"})
        if structure == None:
            structure = bs.find("div", {"class", "se_component_wrap sect_dsc __se_component_area"})

        structure_p_img_tag = structure.find_all(['p', 'img'])
        structure_dict = {'structure': structure, 'structure_p_img_tag': structure_p_img_tag}
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
        
        pos_ratio = 0.000000001
        neg_ratio = 0.000000001
        subjectivity = 0.000000001
        polarity = 0.000000001
        senti_diffs_per_ref = 0.000000001

        if text == '':
            sentiment_dict = {'pos_ratio': pos_ratio, 'neg_ratio': neg_ratio, 'subjectivity': subjectivity,
                              'polarity': polarity, 'senti_diffs_per_ref': senti_diffs_per_ref}
            return sentiment_dict, pos_word_list, neg_word_list
        else:
            pos = 0
            neg = 0
            text = text.split(' ')
            n = len(text)
            for i in text:
                i = remove_odd(i)
                pre = kkma.pos(i)
                test = ';'.join(['/'.join(i) for i in pre])
                if test in word_list:
                    if label[word_list.index(test)] == 'POS':
                        pos += 1
                        pos_word_list.append(test)
                    elif label[word_list.index(test)] == 'NEG':
                        neg += 1
                        neg_word_list.append(test)
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

            sentiment_dict = {'pos_ratio': pos_ratio, 'neg_ratio': neg_ratio, 'subjectivity': subjectivity,
                              'polarity': polarity, 'senti_diffs_per_ref': senti_diffs_per_ref}
            return sentiment_dict, pos_word_list, neg_word_list

    def check_First_second(Text):
        first_person = ['나/NP', '저/NP', '내/NP', '제/NP', '저희/NP', '우리/NP']
        second_person = ['너/NP', '자네/NP', '당신/NP', '그대/NP', '그쪽/NP', '너희/NP', '자기/NP']
        First = 0
        Second = 0
        if Text == '':
            check_First_second_dict = {'First': First, 'Second': Second}
            return check_First_second_dict
        else:
            text = kkma.pos(Text)
            for i in text:
                temp = "/".join(i)
                if temp in first_person:
                    First += len(temp.split('/')[0])
                if temp in second_person:
                    Second += len(temp.split('/')[0])
            check_First_second_dict = {'First_ratio': First/len(Text), 'Second_ratio': Second/len(Text)}
            return check_First_second_dict


# In[34]:

class otherclass:
    def effort_check(Category,Text_len,Img_count):
        effort_text = Text_len / Category_average_text_len[Category]
        effort_img = Img_count / Category_average_img_count[Category]

        effort_dict = {'effort_ratio':effort_text,'effort_img_ratio':effort_img}
        return effort_dict

    def Tag_count(url):
        driver = webdriver.Chrome('./chromedriver.exe')
        driver.get(url)
        driver.implicitly_wait(10)
        tag_count = len(re.sub('\n','',driver.find_element_by_class_name('wrap_tag').text).strip().split('#')[1:])
        tag_dict = {'tag_count':tag_count}
        driver.close()
        return tag_dict


# In[35]:

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


# In[36]:

class chorme_class:
    def user_information(mobile_url,opening_url):
        driver = webdriver.Chrome('./chromedriver.exe')
        
        driver.get(mobile_url)
        driver.implicitly_wait(3)
        
        # 존재하지 않는 게시물 클릭
        driver.find_element_by_class_name("btn_area").click()
        driver.implicitly_wait(3)
        
        # Blog_name, Blog_nickname, Blog_mobile_profile_img, Blog_info_text
        Blog_name = driver.find_element_by_css_selector('#rego_cover > div.cover_cont > div.tit_area > h2 > a > span').text
        Blog_nickname =driver.find_element_by_class_name("user_name").text

        # Count_neighbors
        neighbors_string = re.sub(",","",driver.find_element_by_class_name("count_buddy").text)
        Count_neighbors = int(re.findall('\d+', neighbors_string)[0])

        # Count_visitors
        visitor_stirng = driver.find_elements_by_class_name('count')[0].text
        Count_visitors = re.sub(",","",visitor_stirng.split("전체")[1]).strip()
        # Opening URL
        driver.get(opening_url)
        driver.implicitly_wait(3)
        driver.find_element_by_id('category2').click()
        years = driver.find_elements_by_css_selector('#post-area > div:nth-child(4) > table:nth-child(2) > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td:nth-child(2)')
        for year in years:
            if len(year.text) > 4:
                blog_opening_date = year.text
        driver.close()
        
        user_information_dict = {'Blog_name':Blog_name, 'Blog_nickname':Blog_nickname, 'Count_neighbors':Count_neighbors, 'Count_visitors':Count_visitors, 'blog_opening_date':blog_opening_date}
        
        return user_information_dict


# # Test

# In[9]:

User_id = 'newpark314'
Post_id = '221387605004'
Category = '맛집'


# In[10]:

url = "http://blog.naver.com/PostView.nhn?blogId=" + User_id + "&logNo=" + Post_id + "&redirect=Dlog&widgetTypeCall=true"
mobile_url = "http://m.blog.naver.com/PostView.nhn?blogId="+ User_id
opening_url = 'http://blog.naver.com/profile/intro.nhn?blogId='+ User_id


# In[11]:

# Text_len,Question_count,Sentiment(pos_ratio,neg_ratio,subjectivity,polarity,sentiment_diff_ref)
# Count_Space_mistake, First_ratio, Second_ratio

structure = textclass.Extract_structure_and_tag(User_id,Post_id)
all_tag = structure['structure']
p_img_tag = structure['structure_p_img_tag']
HTML_preprocessing = textclass.HTML_preprocessing(p_img_tag)
text = HTML_preprocessing['Text']


# variables
Text_len = len(text)
Count_Space_mistake = HTML_preprocessing['Count_space_mistake']
Question_count = text.count('?')
sentiment_pre = textclass.sentimental_analysis(text)
sentiment = sentiment_pre[0]
pos_word = sentiment_pre[1]
neg_word = sentiment_pre[2]
first_second = textclass.check_First_second(text)


# In[12]:

# Alignment(Left,Center,Right,Justify), Sticker_count
# variables
Alignment = htmlclass.Extract_Alignment(all_tag)
Sticker_count = htmlclass.Extract_Sticker_count(all_tag)


# In[13]:

# Effort(effort_ratio,effort_img_ratio), Tag_count
refined_structure = HTML_preprocessing['refined_structure']

# variables
Img_count = refined_structure.count('img')
Effort = otherclass.effort_check(Category,Text_len,Img_count)
Tag_count = otherclass.Tag_count(url)['tag_count']


# # 사용자 정보

# In[14]:

# 사용자 정보
user_information = chorme_class.user_information(mobile_url,opening_url)

## user variables
Blog_name = user_information['Blog_name']
Blog_nickname = user_information['Blog_nickname']
Count_neighbors = user_information['Count_neighbors']
Count_visitors = user_information['Count_visitors']
blog_opening_date = user_information['blog_opening_date']


# ## TFIDF

# In[15]:

# tfidf, keras model, cluster model
#Load it later
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
transformer = TfidfTransformer()
loaded_vec = TfidfVectorizer(decode_error="replace",vocabulary=pickle.load(open("[Structure_tag]TFIDF_features_100.pkl", "rb")))
transformer = TfidfTransformer()
v_load = pickle.load(open("[Structure_tag]TFIDF_features_100.pkl", "rb"))

# variable
Structure_13 = tfidf_vectorizer(refined_structure)


# # Data organization

# In[16]:

list_1 = [Question_count,first_second['First_ratio'],first_second['Second_ratio'],Tag_count,
sentiment['pos_ratio'],sentiment['neg_ratio'],sentiment['subjectivity'],sentiment['polarity'],sentiment['senti_diffs_per_ref'],
Sticker_count,Text_len,Count_Space_mistake,Effort['effort_ratio'],Effort['effort_img_ratio'],
Alignment[0],Alignment[1],Alignment[2],Alignment[3]]
list_2 = Structure_13.tolist()


# In[17]:

total_dataset = list_1 + list_2 


# In[18]:

origin_df = pd.DataFrame(total_dataset).T
origin_df.columns = ['Question_count','First_ratio','Second_ratio','Tag_count','pos_ratio',
 'neg_ratio','subjectivity','polarity','senti_diffs_per_ref','Sticker_count','Text_len','Count_space_mistake',
   'effort_ratio','effort_img_ratio','Left','Center','Right','Justify',
   'img img img img img','img img img img text','img img img text img','img img text img img','img img text img text',
 'img text img img img','img text img img text','img text img text img','text img img img img','text img img img text',
 'text img img text img','text img text img img','text img text img text']


# In[19]:

# Total_df = pd.read_csv('[Final]Total_csv.csv',sep='\t')
# Total_df = Total_df[['Question_count','First_ratio','Second_ratio','Tag_count','pos_ratio',
#  'neg_ratio','subjectivity','polarity','senti_diffs_per_ref','Sticker_count','Text_len','Count_space_mistake',
#    'effort_ratio','effort_img_ratio','Left','Center','Right','Justify',
#  'img img img img img','img img img img text','img img img text img','img img text img img','img img text img text',
#  'img text img img img','img text img img text','img text img text img','text img img img img','text img img img text',
#  'text img img text img','text img text img img','text img text img text']]
# x = Total_df.dropna()
# col_name = x.columns.tolist()
# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# scaler.fit(x)
# scaled_x = scaler.transform(x)
# scaled_x_df = pd.DataFrame(scaled_x)
# scaled_x_df.columns = col_name
# scalerfile = 'scaler.pkl'
# pickle.dump(scaler, open(scalerfile, 'wb'))
# scaler = pickle.load(open(scalerfile, 'rb'))
# test_scaled_set = scaler.transform(test_set)


# # Keras

# In[20]:

## Standard scaler model load
import pickle
scalerfile = 'scaler.pkl'
scaler = pickle.load(open(scalerfile, 'rb'))
# transform data
origin_df = origin_df.fillna(0)
X_scaled = pd.DataFrame(scaler.transform(origin_df),columns = origin_df.columns)

# keras model load
from keras.models import load_model
model = load_model('keras_model.h5')

# data type reshape & predict probability
prob = model.predict(X_scaled.values.reshape((1, 31))).item()
# predict classes
predict_classes = model.predict_classes(X_scaled.values.reshape((1, 31))).item()


# # Clustering

# In[21]:

# Cluster는 cluster model자체가 scaler로 된 모델이라 그냥 origin 값 집어 넣어야함.
clusterfile = '8-means(0,1,2,5,6,7).pkl'
cluster = pickle.load(open(clusterfile, 'rb'))
# predict cluster class
predict_cluster_class = cluster.predict(origin_df).item()


# # Final save csv_file

# In[22]:

Predict_df = pd.DataFrame({'prob':prob,'predict_classes':predict_classes,'predict_cluster_class':predict_cluster_class},index=[0])
user_df = pd.DataFrame({'Blog_name':Blog_name,'Blog_nickname':Blog_nickname,'Count_neighbors':Count_neighbors,'Count_visitors':Count_visitors,'blog_opening_date':blog_opening_date},index=[0])


# In[23]:

value = pd.concat([X_scaled,Predict_df],axis=1)


# In[24]:

value.to_csv('test_csv.csv')


# In[25]:

value


# In[26]:

pos_word


# In[27]:

neg_word
