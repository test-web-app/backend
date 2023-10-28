from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv
import datetime
import os


load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, title, description):
        self.title = title
        self.description = description


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/get', methods = ['GET'])
def get_articles():
    all_articles = Article.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)


@app.route('/get/<id>/', methods = ['GET'])
def article_details(id):
    article = Article.query.get(id)
    return article_schema.jsonify(article)


@app.route('/add', methods = ['POST'])
def add_article():
    title = request.json['title']
    description = request.json['description']

    article = Article(title, description)
    db.session.add(article)
    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/update/<id>/', methods = ['PUT'])
def update_article(id):
    article = Article.query.get(id)

    title = request.json['title']
    description = request.json['description']

    article.title = title
    article.description = description

    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/delete/<id>/', methods = ['DELETE'])
def article_delete(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify(article)


if __name__ == '__main__':
    app.run(debug=True)