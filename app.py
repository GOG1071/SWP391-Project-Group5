from flask import Flask, render_template, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os

import routers.user
import models
import controllers

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)


app.run("0.0.0.0", port=os.environ["port"], debug=True)