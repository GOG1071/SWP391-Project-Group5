

from models.post import  Post
from models.model import db
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail

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

