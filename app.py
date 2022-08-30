# GET load_only=True
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList, ResourceRelationship

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news/my_news.db'
db = SQLAlchemy(app)


class NewsList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    link = db.Column(db.String)
    news_list_id = db.relationship('News', backref=db.backref('newslist'))

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subtitle = db.Column(db.String)
    text = db.Column(db.String)
    news_id = db.Column(db.Integer, db.ForeignKey('news_list.id'))

    

class NewsListSchema(Schema):
    class Meta:
        type_ = 'news_list'
        self_view = 'news_many'
        self_view_kwargs = {'id':'<id>'}

    id = fields.Integer()
    title = fields.Str(required=True)
    link = fields.Str(required=True)
    display_name = fields.Function(lambda obj: f"{obj.id} <{obj.title}>")


class NewsSchema(Schema):
    class Meta:
        type_ = 'news'
        self_view = 'one_news'
        self_view_kwargs = {'id':'<id>'}
    id = fields.Integer()
    subtitle = fields.Str()
    text = fields.Str()
    news_id = fields.Integer(required=True)


class NewsMany(ResourceList):
    schema = NewsListSchema
    data_layer = {'session':db.session,
                  'model':NewsList}


class NewsOne(ResourceDetail):
    schema = NewsSchema
    data_layer = {'session':db.session,
                  'model':News}

print('\n\n\n')

api = Api(app)
api.route(NewsMany, 'news_many', '/news_list')
api.route(NewsOne, 'one_news', '/news_list/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)