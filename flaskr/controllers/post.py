from datetime import datetime
from models.post import  Post
from models.model import db
from flask import url_for,render_template,request,session,flash
import cloudinary.uploader 
def load_post():
    author_id = request.args.get("author_id")
    list_post = Post.query.filter_by(author_id = author_id)
    if list_post:
        return render_template('manage_posted.html', list = list_post)
    flash("you haven't posted anything yet","info")
    return render_template('manage_posted.html')


def delete_post():
    id = request.form.get("id")
    author_id = request.form.get("author_id")
    post = Post.query.filter_by(id = id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        return url_for('load_post',author_id = author_id)
    return url_for('load_post',author_id = author_id)

def load_for_update():
    id  = request.form['id']
    post = Post.query.filter_by(id = id).first()
    return render_template('update.html',post = post)


def update_post():
    id  = request.form['id']
    post = Post.query.filter_by(id=id).first()
    if post:
        db.session.delete(post)
        db.session.commit()

        post = Post(id = request.form['id'],caption = request.form['caption'],image = request.form['image'],author_id = request.form['author_id'])
        db.session.add(post)
        db.session.commit()
    
    return url_for('load_post',author_id = request.form["author_id"])

def create_post():
    file = request.form.get('file')
    file_path = None
    if file:
        response = cloudinary.uploader.upload(file)
        file_path = response['secure_url']
    post = Post(
        content=request.form.get('content'),
        author_id= session['id'],
        timestamp= datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
    db.session.add(post)
    db.session.commit()
    return render_template('post_detail.html')
def post_detail():
    id = session['post_id']
    post = Post.query.filter_by(id=id).first()
    db.session.commit()
    return render_template('post_detail.html')
    

