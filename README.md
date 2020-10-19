Sentiment Anslysis for IMDB Movie Reviews

Libraries needed
  1. numpy
  2. pandas
  3. re
  4. string
  5. nltk
  6. pickle
  7. json
  8. sqlite3
  9. sklearn
  10. Flask

File/Folder Structure:
static:
  Handles all necessary files used for UI.
  
templates:
 contains all the html pages
 
train.py
  1. import the raw data.
  2. pre-process
  3. dump the features to train.json
  
functions.py:
  1. have all the fuctions required for cleaning the data
 
pickle_dump.py
  1. reads the json data.
  2. vectorize it
  3. trains the model
  4. dump instance of vector and model to pickle file called (model.pkl)

app.py
  1. Flask app handles user data.
  2. reads the model.pkl file
  3. Accepts user data
  4. Process the user data and return the prediction result back to UI.
