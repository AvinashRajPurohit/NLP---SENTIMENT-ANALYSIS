from flask import Flask, render_template, url_for, request
import pandas as pd
import numpy as np
from nltk.stem.porter import PorterStemmer
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


def remove_pattern(input_text, pattern):
    r = re.findall(pattern, input_text)
    for i in r:
        input_text = re.sub(i, '', input_text)
    return input_text


def count_punct(text):
    count = sum(1 for char in text if char in string.punctuation)
    return round(count / (len(text) - text.count(" ")), 3) * 100


app = Flask(__name__)
data = pd.read_csv("sentiment.tsv", sep='\t')
data.columns = ['label', 'body_text']

# Features and Labels

data['label'] = data['label'].map({'pos': 0, 'neg': 1})
data['tweet'] = np.vectorize(remove_pattern)(data['body_text'],"@[\w]*")
tokenized_tweet = data['tweet'].apply(lambda x: x.split())
stemmer = PorterStemmer()
tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x])
for i in range(len(tokenized_tweet)):
    tokenized_tweet[i] = ' '.join(tokenized_tweet[i])
data['tweet'] = tokenized_tweet
data['body_len'] = data['body_text'].apply(lambda x: len(x) - x.count(" "))
data['punct%'] = data['body_text'].apply(lambda x: count_punct(x))
X = data['tweet']
y = data['label']
cv = CountVectorizer()
X = cv.fit_transform(X)
X = pd.concat([data['body_len'], data['punct%'], pd.DataFrame(X.toarray())], axis=1)
from sklearn.model_selection import train_test_split

# X_train,X_test,y_train,y_test = train_test_split(X,y, test_size = 0.33, random_state = 42)
## Using Classifier
clf = LogisticRegression(C=0.1, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=100,
                   multi_class='auto', n_jobs=None, penalty='l2',
                   random_state=None, solver='lbfgs', tol=0.0001, verbose=0,
                   warm_start=False)
clf.fit(X, y)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])e9ecbfc2f73b 
def predict():
    if request.method == 'POST':
        message = request.form['message']e9ecbfc2f73b 
        data = [message]
        vect = pd.DataFrame(cv.transform(data).toarray())
        body_len = pd.DataFrame([len(data) - data.count(" ")])
        punct = pd.DataFrame([count_punct(data)])
        total_data = pd.concat([body_len, punct, vect], axis=1)
        my_prediction = clf.predict(total_data)
    return render_template('result.html', prediction=my_prediction)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000) 
 


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port =4000)
    

