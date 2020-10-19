import numpy as np
import pandas as pd
import functions as fn
from sklearn.model_selection import train_test_split
import sqlite3, json
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import functions as fn
import pickle

def reading_data(name):
	data = pd.read_csv('data/'+name+'.csv')
	return data

def db_connect():
	conn = sqlite3.connect("data/movie_reviews.db")
	cur = conn.cursor()
	cur.execute("CREATE TABLE raw_data (reviews TEXT, sentiment VARCHAR(15))")

	conn.commit()
	conn.close()

	return "Database connected"

def insert_raw_data(data):

	conn = sqlite3.connect("data/movie_reviews.db")
	cur = conn.cursor()
	cmd = f"INSERT INTO raw_data (reviews, sentiment) VALUES (?,?)"
	for i in range(data.shape[0]):
		cur.execute(cmd,(data.review.iloc[i], data.sentiment.iloc[i]))
	
	conn.commit()
	cur.execute("select count(*) from raw_data")

	return "Raw Data added"

def cleaning(data):
	data.review = data.review.apply(fn.clean_text)
	return data

def split_data(data):
	X_train, X_test, y_train, y_test = train_test_split(data.review,data.sentiment,random_state=0, test_size=0.20)
	
	# print("Train Features shape:",X_train.shape)
	# print("Train Target shape:",y_train.shape)
	# print("Test Features shape:",X_test.shape)
	# print("Test Target shape:",y_test.shape)

	return (X_train, X_test, y_train, y_test)

def clean_data_db():
	conn = sqlite3.connect("data/movie_reviews.db")
	cur = conn.cursor()
	
	cur.execute("CREATE TABLE train_clean_data (reviews TEXT, sentiment INT)")
	cur.execute("CREATE TABLE test_clean_data (reviews TEXT, sentiment INT)")

	conn.commit()
	conn.close()

def clean_data_to_db(X_train, X_test, y_train, y_test):
# Inserting raw data
	conn = sqlite3.connect("data/movie_reviews.db")
	cur = conn.cursor()

	# Train Data
	cmd = "INSERT INTO train_clean_data (reviews, sentiment) VALUES (?,?)"

	for i in range(X_train.shape[0]):
		cur.execute(cmd, (X_train.iloc[i], y_train[i]))

	# Test Data
	cmd = "INSERT INTO test_clean_data (reviews, sentiment) VALUES (?,?)"
	for i in range(X_test.shape[0]):
		cur.execute(cmd, (X_test.iloc[i], y_test[i]))

	conn.commit()
	conn.close()

	return "Clean data added to Database"

class Model():
	def __init__(self,X_train,y_train):
		self.X_train = X_train
		self.y_train = y_train

	def train(self):
		self.cv = CountVectorizer(binary=True,ngram_range=(1, 2))

		#transformed train reviews
		self.cv_train_reviews = self.cv.fit_transform(self.X_train)

		return (self.cv,self.cv_train_reviews)
		
		#transformed test reviews
		#cv_test_reviews=cv.transform(self.X_test)
		
		#print('BOW_cv_train:',cv_train_reviews.shape)
		#print('BOW_cv_test:',cv_test_reviews.shape)

	def model(self,cv_train_reviews):
		self.cv_train_reviews = cv_train_reviews
		self.lr = LogisticRegression(max_iter=500)
		self.lr.fit(self.cv_train_reviews,pd.Series(self.y_train))

		return self.lr

		# dumping model and vextorizer
		# with open('model.pkl', 'wb') as fout:
		# 	pickle.dump((cv, lr), fout)
		#pickle.dump(cv, open('countvect.sav', 'wb'))
		#pickle.dump(lr, open('lrmodel.sav', 'wb'))



if __name__ == '__main__':
# Reading the data
	data = reading_data('IMDB Dataset')

#connecting db
	#db_connect()

#Inserting raw_data to db
	#insert_raw_data(data)
# PreProcessing

# Cleaning
	data = cleaning(data)

# Splitting the Data
	X_train, X_test, y_train, y_test = split_data(data)

# Normalizing Sentiments
	y_train = [1 if i == 'positive' else 0 for i in y_train]
	y_test = [1 if i == 'positive' else 0 for i in y_test]
	
# Inserting clean data to db
	#clean_data_db()
	clean_data_to_db(X_train, X_test, y_train, y_test)

# Storing data to Json file
	d1 = {}
	d1['X_train'] = X_train.to_json()
	d1['y_train'] = pd.Series(y_train).to_json()

	with open('traindata.json','w') as fp:
		json.dump(d1,fp)
	
	#m = Model(X_train,y_train)
# training model
	#print(model(X_train,y_train))
