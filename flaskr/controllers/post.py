from models.post import Post
from models.model import db

from flask import Flask, redirect, url_for, json, render_template, request, session, flash
from flask_mail import Message
from controllers.mail_service import mail

def post(request):
    pass