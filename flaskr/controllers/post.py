from datetime import datetime
from importlib.resources import contents

from models.post import PostImage
from models.post import  Post
from models.user import User
from models.report import ReportPost
from models.model import db
from models.post import PostImage
from flask import Flask,redirect,url_for,json,render_template,request,session,flash
from flask_mail import Message
from controllers.mail_service import mail
import cloudinary.uploader 

def load_post():
    author_id = session['id']
    list_post = Post.query.filter_by(author_id = author_id)
    list_img = []
    for i in list_post: 
        img = PostImage.query.filter_by(post_id = i.id).first()
        list_img.append(img)
    if list_img:
        return render_template('manage_posted.html', list = list_post,list_img = list_img)
    if list_post:
        return render_template('manage_posted.html', list = list_post)
    flash("you haven't posted anything yet","info")
    return render_template('manage_posted.html')


def delete_post():
    id = request.form.get("id")
    author_id = request.form.get("author_id")
    post_img = PostImage.query.filter_by(post_id = id)
    if post_img:
        for img in post_img:
            db.session.delete(img)
            db.session.commit()

    post = Post.query.filter_by(id = id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        
        return redirect( url_for('post_router.load_post',author_id = author_id) )
    return redirect( url_for('post_router.load_post',author_id = author_id) )

def load_for_update():
    id  = request.form['id']
    post = Post.query.filter_by(id = id).first()
    post_img = PostImage.query.filter_by(post_id = id)
    return render_template('update.html',post = post,post_img = post_img)


def update_post():
    id  = request.form['id']
    post = Post.query.filter_by(id=id).first()
    timestamp = datetime.now()
    post_image = PostImage.query.filter_by(post_id = id)
    image_link = request.files.getlist('files[]')
    file_path = None
    list_file_path = []
    # lấy 1 list link img rồi đẩy hết lên cloudinary rồi lấy link sau khi đẩy add vào list_file_path
    if image_link:
        for img in image_link:
            response = cloudinary.uploader.upload(img)
            file_path = response['secure_url']
            list_file_path.append(file_path)


    if post_image:
        for i in post_image:
            
            db.session.delete(i)
            db.session.commit()
            

   
    for file in list_file_path:
        post_img = PostImage( post_id = id, image_link = file )
        db.session.add(post_img)
        db.session.commit()



    if post:
        db.session.delete(post)
        db.session.commit()

        post = Post(id = request.form['id'],content = request.form['caption'],author_id = request.form['author_id'],timestamp = timestamp)
        db.session.add(post)
        db.session.commit()
    return redirect( url_for('post_router.load_post',author_id = request.form["author_id"], img_link = image_link) )


def report_post():
    author_id = session["id"]
    post_id = request.form["post_id"]
    timestamp = datetime.now()
    reason = request.form['reason']
    report_post = ReportPost(post_id = post_id, user_id = author_id, timestamp = timestamp, reason = reason)
    db.session.add(report_post)
    db.session.commit()
    return redirect(url_for("user_router.home"))
    
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
    post = Post.query.filter_by()
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

    
    
def search_post():
    value = request.form.get('content')
    searchBy = request.form.get('searchBy')
    if searchBy == "Content":
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter(Post.content.contains(value))\
        .order_by(Post.timestamp.desc())\
        .paginate(page=page, per_page=5)
        return render_template('postSearch.html', posts=posts)   
    else:
        page = request.args.get('page', 1, type=int)
        user = User.query.filter(User.username==value).first()
        posts = Post.query.filter(Post.author_id==user.id)\
        .order_by(Post.timestamp.desc())\
        .paginate(page=page, per_page=5)
        return render_template('postSearch.html', posts=posts)   
    
    
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

def newsfeed():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5)
    return render_template('newsfeed.html', posts=posts)

