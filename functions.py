import re,string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = stopwords.words('english')
lmt = WordNetLemmatizer()

def remove_html(text):
    tags = re.compile("<.*?>")
    return re.sub(tags,"",text)
    
def remove_punctuation(text):
    pun = re.compile(rf"[{string.punctuation}]")
    return re.sub(pun,"",text)

def clean_text(text):
    text.lower()
    text = remove_html(text)
    text = remove_punctuation(text)
    text_list = text.split()
    filtered_list = [lmt.lemmatize(word) for word in text_list if lmt.lemmatize(word) not in stop_words or word in ['not','but']]
    return " ".join(filtered_list)