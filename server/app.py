from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "http://localhost:3000"}})

def tokenization(txt):
    tokens = nltk.word_tokenize(txt)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    stemming = [stemr.stem(w) for w in tokens]
    return " ".join(stemming)

def cosine_sim(txt1, txt2):
    obj_tfidf = TfidfVectorizer(tokenizer=tokenization)
    tfidfmatrix = obj_tfidf.fit_transform([txt1, txt2])
    similarity = cosine_similarity(tfidfmatrix)[0][1]
    return similarity

def recommendation(query):
    tokenized_query = tokenization(query)
    df = pd.read_csv('Grocery Lists2mainmini.csv')
    df = df[['Name', 'Price', 'Type','Images_url']]
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df['similarity'] = df['Type'].apply(lambda x: cosine_sim(tokenized_query, x))
    final_df = df.sort_values(by=['similarity'], ascending=False).head(3)[['Name', 'Price','Images_url']]
    return final_df.to_dict(orient='records')

stemr = SnowballStemmer('english')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    query = data['query']
    recommendations = recommendation(query)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
