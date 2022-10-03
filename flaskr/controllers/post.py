from datetime import datetime
from importlib.resources import contents
from models.post import  Post
from models.model import db
from models.post import PostImage
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail
import cloudinary.uploader 
def load_post():
    author_id = session['id']
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
        return url_for('post_router.load_post',author_id = author_id)
    return url_for('post_router.load_post',author_id = author_id)

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

        post = Post(id = request.form['id'],content = request.form['caption'],author_id = request.form['author_id'])
        db.session.add(post)
        db.session.commit()

    return url_for('post_router.load_post',author_id = request.form["author_id"])

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

    post_image = PostImage(
        post_id = post.id,
        image_link = file_path,
    )
    db.session.add(post_image)
    db.session.commit()
    return render_template('post_detail.html')
def post_detail():
    post = Post.query.filter_by(id=id).first()
    return render_template('post_detail.html')