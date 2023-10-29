from flask import jsonify, request

from . import db
from .models import Article
from .schemas import ArticleSchema

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


def setup_routes(app):
    @app.route("/get", methods=["GET"])
    def get_articles():
        all_articles = Article.query.all()
        results = articles_schema.dump(all_articles)
        return jsonify(results)

    @app.route("/get/<id>", methods=["GET"])
    def article_details(id):
        article = Article.query.get(id)
        return article_schema.jsonify(article)

    @app.route("/add", methods=["POST"])
    def add_article():
        title = request.json["title"]
        description = request.json["description"]

        article = Article(title, description)
        db.session.add(article)
        db.session.commit()
        return article_schema.jsonify(article)

    @app.route("/update/<id>", methods=["PUT"])
    def update_article(id):
        article = Article.query.get(id)

        title = request.json["title"]
        description = request.json["description"]

        article.title = title
        article.description = description

        db.session.commit()
        return article_schema.jsonify(article)

    @app.route("/delete/<id>", methods=["DELETE"])
    def article_delete(id):
        article = Article.query.get(id)
        db.session.delete(article)
        db.session.commit()

        return article_schema.jsonify(article)
