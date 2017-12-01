from flask import Flask, redirect, url_for, \
				  request, render_template, json
from pymongo import MongoClient
import pymongo
import os
import socket
from bson import ObjectId



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


client = MongoClient('mongodb://backend:24242/dockerdemo')
db = client.blogpostDB

app = Flask(__name__)

@app.route("/")
def landing_page():
    posts = get_all_posts()
    
    return render_template('blog.html', posts=json.loads(posts))


@app.route('/add_post', methods=['POST'])
def add_post():

    new()
    return redirect(url_for('landing_page'))


@app.route('/remove_all')
def remove_all():
    db.blogpostDB.delete_many({})

    return redirect(url_for('landing_page'))


## Services

@app.route("/posts", methods=['GET'])
def get_all_posts():
    
    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]
    return JSONEncoder().encode(posts)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'title': request.form['title'],
        'post': request.form['post']
    }
    db.blogpostDB.insert_one(item_doc)

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    return JSONEncoder().encode(posts[-1])


@app.route("/edit_post", methods=['GET'])
def edit_post():
    # _posts = db.blogpostDB.find()
    titleData = request.args.get('title')
    postData = request.args.get('post')
    _id = request.args.get('mongo_id')
    _posts = db.blogpostDB.find({'_id':ObjectId(_id)})
    posts = [post for post in _posts]
    db.blogpostDB.update_one(
        {'_id':ObjectId(_id)}, 
        {"$set": 
        {'title':titleData,'post':postData}
        })
    return JSONEncoder().encode(posts)


@app.route("/get_id", methods=['GET'])
def get_id():
    # _posts = db.blogpostDB.find()
    titleData = request.args.get('title')
    postData = request.args.get('post')

    _posts = db.blogpostDB.find({'title':titleData,'post':postData})
    posts = [post for post in _posts]
    return JSONEncoder().encode(posts)



@app.route("/delete_post", methods=['GET'])
def delete_post():
    titleData = request.args.get('title')
    postData = request.args.get('post')
    
    db.blogpostDB.delete_one({'title':titleData,'post':postData})
    return redirect(url_for('landing_page'))


### Insert function here ###



############################



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
