from datetime import datetime
from flask import Flask, abort, request, jsonify
import sqlite3
import json

app = Flask(__name__)

SANTIMENTS = [{"хорош": "positive"}, {"люблю": "positive"}, {"плохо": "negative"}, {"ненавиж": "negative"}]

def table_init():        
    table_sql = """
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        text TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        created_at TEXT NOT NULL
        )
    """
    cursor.execute(table_sql)

def write_data():    
    reviews = [("Хорошая погода", "positive", datetime.utcnow().isoformat()),
                ("Ненавижу жару в Краснодаре", "negative", datetime.utcnow().isoformat()),
                ("Постоянные сбои интернета", "neutral", datetime.utcnow().isoformat()),
            ]
    cursor.executemany('INSERT INTO reviews(text, sentiment, created_at) VALUES (?,?,?)', reviews)

def read_reviews(sentiment=None):    
    if sentiment == None:
        return cursor.execute("SELECT id, text, sentiment, created_at FROM reviews").fetchall()
        
    return cursor.execute("SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment =:sentiment",  {"sentiment": sentiment}).fetchall()    

def create_review(review):
    santiment = find_santiment(review['text'])
    if 'text' not in review:
        abort(404)
        
    cursor.execute("INSERT INTO reviews(text, sentiment, created_at) VALUES (?, ?, ?)", 
                    (review['text'], santiment, datetime.utcnow().isoformat())
                )
    connect.commit()
    return 'ok'

def find_santiment(review):
    for santiment in SANTIMENTS:
        find_key = list(santiment.keys())[0]
        find_santiment = review.find(find_key)
        if find_santiment != -1:
            return santiment.get(find_key)
    return "neutral"

connect = sqlite3.connect("reviews.db", check_same_thread=False)
cursor = connect.cursor()

if __name__ == "main":    
    table_init()
    write_data()

@app.route("/reviews", methods=['GET', 'POST'])
def reviews():    
    if request.method == 'GET':
        return json.dumps(read_reviews(request.args.get('sentiment')))
    
    return create_review(request.json)


