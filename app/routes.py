from flask import render_template
from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.forms import RegistrationForm
from flask import request
from werkzeug.urls import url_parse
import os
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from base64 import b64encode
import base64
from io import BytesIO
import imghdr
from datetime import datetime
import av
import cv2
from app import screenshot

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Sena'}
    # images =
    return render_template("index.html", title='Home Page', user=user)

@app.route('/anon')
@login_required
def anon():
    return render_template('anon.html', title='Anonymization' )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        dirName = 'C:\\Users\\Sena\\BSP06-WEB\\venv\\app\\static\\uploads\\{}\\'.format(user.username)
        os.makedirs(dirName)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/anon/pictures')
def pictures():
    users = User.query.all()
    username = []

    files = os.listdir('C:\\Users\\Sena\\BSP06-WEB\\venv\\app\\static\\uploads\\{}'.format(current_user.username))
    """for user in users:
        if user.id > 18:
            user_id.append(user.id)
            for i in (os.listdir('C:\\Users\\Sena\\microblog\\venv\\app\\static\\uploads/{}'.format(user.id))):
               files.append(i)
    print(files)"""

    return render_template('upload.html', files=files)

def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic

@app.route('/', methods=['POST'])
@login_required
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
        uploaded_file.save(os.path.join('C:\\Users\\Sena\\BSP06-WEB\\venv\\app\\static\\uploads\\{}'.format(current_user.username), filename))
    return redirect(url_for('pictures'))

@app.route('/uploads/<filename>')
def upload(filename):
       return send_from_directory(os.path.join('C:\\Users\\Sena\\BSP06-WEB\\venv\\app\\static\\uploads\\{}'.format(current_user.username)), filename)

@app.route('/record_video')
def record_video():
    return render_template('record.html')

import os
from flask import request

@app.route('/save_video', methods=['POST'])
def save_video():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    username = 'default_username'
    if current_user.is_authenticated:
        username = current_user.username

    # Save the video file to the appropriate user's folder
    video_folder = os.path.join(app.config['STATISTICS_FOLDER'], 'videos', username)
    os.makedirs(video_folder, exist_ok=True)
    video_path = os.path.join(video_folder, f"{timestamp}.webm")
    with open(video_path, 'wb') as f:
        f.write(request.data)

    # Save screenshots from the video
    screenshot_folder = os.path.join(video_folder, 'screenshots')
    screenshot.save_video_screenshots(video_path, screenshot_folder)

    return redirect(url_for('anon'))