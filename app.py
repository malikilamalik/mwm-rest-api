from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

#Post Model
class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100),unique = True)
    html = db.Column(db.Text)
    createDate = db.Column(db.String(50))

    def __init__(self,title,html,createDate):
        self.title = title
        self.html = html
        self.createDate = createDate

#Post Schema
class PostSchema(ma.Schema):
    class Meta:
        fields = ('id','title','html','createDate')

#Init Schema
db.create_all()
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

#Create a Post
@app.route('/post',methods=['POST'])
def add_post():
    title = request.json['title']
    html = request.json['html']
    createDate = request.json['createDate']

    new_post = Post(title,html,createDate)

    db.session.add(new_post)
    db.session.commit()
    
    return post_schema.jsonify(new_post)

#Get Posts
@app.route('/posts',methods=['GET'])
def get_posts():
    all_post = Post.query.all()
    result = posts_schema.dump(all_post)

    return jsonify(result)

#Get a Post
@app.route('/post/<id>',methods=['GET'])
def get_post(id):
    post = Post.query.get(id)

    return post_schema.jsonify(post)

#Delete a Post
@app.route('/post/<id>',methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return post_schema.jsonify(post)


#Run Server
if __name__ == '__main__':
    app.run(debug=True)