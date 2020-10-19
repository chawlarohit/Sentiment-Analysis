from flask import Flask, request, render_template, send_from_directory
import pandas as pd
import os
import functions as fn
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import sqlite3, json
import pickle


app = Flask(__name__)

with open('model.pkl', 'rb') as f:
	cv, lr = pickle.load(f)
	print(cv,lr)

app.config["FILE_DOWNLOADS"] = os.path.splitdrive(os.getcwd())[1]+'\\static\\client\\downloads'

#Home Page
@app.route('/')
def home():
	return render_template("index.html")

#About Page
@app.route('/about')
def about():
	return render_template("about.html")

# Post review/Analyse Page
@app.route('/rev', methods=['POST','GET'])
def rev():

	if request.method == 'POST':
		try:
			name = request.form['name']
			review = request.form['review']
			file = request.files['file']

			with sqlite3.connect("data/movie_reviews.db") as con:
				cur = con.cursor()
				cur.execute("CREATE TABLE new_reviews (movie_name TEXT, review TEXT, sentiment VARCHAR(15))")

			con.commit()
			con.close()

		except:
			con.rollback()

		finally:
			if review is not '' and file.filename is not '':
				return render_template("rev.html", message = 'Please either write the review or choose a file', sentiment = 'img/initial_result.gif', name = name)

			elif review is not '':
				review_transform = pd.Series(review).apply(fn.clean_text)
				cv_review = cv.transform(review_transform)
				review_analyze = lr.predict(cv_review)

				if review_analyze == 0:
					result_img = "img/negative.gif"
					s = 'Negative'
				else:
					result_img = "img/positive.gif"
					s = 'Positive'
				
				with sqlite3.connect("data/movie_reviews.db") as con:
					cur = con.cursor()

					cur.execute("INSERT INTO new_reviews (movie_name, review, sentiment) VALUES (?,?,?)",(name ,review, s) )
				
				con.commit()
				con.close()

				return render_template("rev.html", sentiment = result_img, name = name, review = review)
			
			else:
				file.save('static/client/uploads/'+file.filename)
				data = pd.read_excel('static/client/uploads/'+file.filename, header=None)
				X = data.iloc[:,0].apply(fn.clean_text)
				cv_X = cv.transform(X)
				y = lr.predict(cv_X)

				out = pd.concat([data,pd.Series(y,name='Sentiment').replace({0:'Negative',1:'Positive'})],axis=1)
				out.to_excel('static/client/downloads/Result.xlsx',index=False,header=False)

				return render_template("rev.html", message = 'Your file is ready for download', fname = 'Result.xlsx', sentiment = 'img/initial_result.gif', name = name)

	else:
		return render_template("rev.html", sentiment = 'img/initial_result.gif')

# Download file for review page
@app.route('/get-file/<fname>')
def get_file(fname):
	return send_from_directory(app.config["FILE_DOWNLOADS"], filename=fname, as_attachment=True, cache_timeout=0)

# Rating page
@app.route('/rate', methods=['POST','GET'])
def rating():

	if request.method == 'POST':
		try:
			name = request.form['name']
		except:
			pass
		finally:
			if os.path.isfile('static/client/movies/'+str(name)+'.xlsx'):
				data = pd.read_excel('static/client/movies/'+str(name)+'.xlsx')

				X = data.iloc[:,0].apply(fn.clean_text)
				cv_X = cv.transform(X)
				y = lr.predict(cv_X)

				rating = round(y.sum()/y.size * 5, 1)

				return render_template("rate.html", message = f'Rating is {rating}/5', rating = rating, name = name)
			else:
				return render_template("rate.html", message = "We Don't have this movie in our database. Please try another movie.", name = name)
	else:
		return render_template("rate.html", sentiment = 'img/initial_result.gif')

if __name__ == '__main__':
	app.run(port=5000, debug=False)