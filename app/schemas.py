from flask_marshmallow import Marshmallow

ma = Marshmallow()


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "date")
