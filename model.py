from newspaper import Article
import pandas as pd
# from sklearn.model_selection import train_test_split




import pickle
from newsapi import NewsApiClient
from pymongo import MongoClient
from pymongo.collection import ObjectId
from clickbait import is_clickbait

newsapi = NewsApiClient(api_key='e5aeec0b412a4bb0b7b7d63eaad8bd04') 
linear_clf = pickle.load(open("model.pickle", "rb"))

tfidf_vectorizer = pickle.load(open("vectorizer.pickle", "rb"))

client = MongoClient("mongodb+srv://test:test@cluster0.dpcgx.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test

db = client.get_database("news_data")

k = db.fake_or_real

def predict_fake(title, text):
  
	data = {"Unnamed: 0": ["0000"], "title":[title], "text":[text], "label":["FAKE/REAL"]}
	frame = pd.DataFrame(data, columns = ["Unnamed: 0", "title", "text", "label"])
	frame = frame.set_index("Unnamed: 0")
	frame.drop("label", axis=1)
	tfidf_test = tfidf_vectorizer.transform(frame['text'])
	pred = linear_clf.predict(tfidf_test)
	return pred[0]

def compare(a, b):
  
  for i in a:
    if i.lower() in b:
      return "NOT CLICKBAIT"
  return "CLICKBAIT"


def predict(url):
  kk = ""
  try:
    article = Article(url)
    article.download()
    article.parse()
    if len(article.text) <= 500:
      return [str(article.title)] + (["INVALID"] * 3)
      
    article.nlp()
    if compare(article.title.split(), article.keywords) == "NOT CLICKBAIT" and is_clickbait(article.title) == 0:
      kk = "NOT CLICKBAIT"
    else:
		
      kk = "CLICKBAIT"
    
    
    return [str(article.title), predict_fake(str(article.title), str(article.text)), kk, str(article.summary)] 
  except ValueError:
    return (["INVALID"] * 4)
  finally:
    if len(article.text) <= 500:
      return [str(article.title)] + (["INVALID"] * 3)
    return [str(article.title), predict_fake(str(article.title), str(article.text)), kk, str(article.summary)] 


def get_headlines():
	final = []
	top_headlines = newsapi.get_top_headlines(language='en')
	
	for i in top_headlines['articles']:
		k = predict(i['url'])
		final.append([i['url'], i['title'], i['description'], i['source']['name'], i['urlToImage'], k[1], k[2]])

	return final

def update(x):
	if x == "REAL":
		k.update_one({ "_id": ObjectId("5ee46d8088b3ec0144d5801b") }, {'$inc':{'num_real':1}})
	elif x == "FAKE":
		k.update_one({ "_id": ObjectId("5ee46d8088b3ec0144d5801b") }, {'$inc':{'num_fake':1}})
	elif x == "CLICKBAIT":
		k.update_one({ "_id": ObjectId("5ee4d1691850cb02c0edc4cc") }, {'$inc':{'num_clickbait':1}})
	elif x == "NOT CLICKBAIT":
		k.update_one({ "_id": ObjectId("5ee4d1691850cb02c0edc4cc") }, {'$inc':{'num_notclickbait':1}})


def get_data(x):
	a = k.find({ "_id": ObjectId("5ee46d8088b3ec0144d5801b") })[0]
	b = k.find({ "_id": ObjectId("5ee4d1691850cb02c0edc4cc") })[0]

	
	if x == "FAKE":
		return(a['num_fake'])
	elif x == "REAL":
		return(a['num_real'])
	elif x == "CLICKBAIT":
		return(b['num_clickbait'])
	elif x == "NOT CLICKBAIT":
		return(b['num_notclickbait'])
	else:
		return "INVALID"
