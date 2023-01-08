from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, login_required, current_user, logout_user
from __init__ import db, UPLOAD_FOLDER
from models import User, Post
import os
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', "svg"}


@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        newAdmin = User(name=name, username=username, email=email, password=password)
        db.session.add(newAdmin)
        db.session.commit()
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("adminSignup.html")


@auth.route('/admin', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        rememberStatus = request.args.get("remember-me")
        remember = False
        if rememberStatus == "toggled":
            remember = True

        user = User.query.filter(User.username == username and User.password == password).first()
        if user:
            login_user(user, remember=remember)
            return redirect(url_for("auth.dashboard"))
        else:
            return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("admin.html")


@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.admin"))


@login_required
@auth.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", current_user=current_user)


# to check whether the file extension is supportable
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_required
@auth.route("/newblog", methods=["GET", "POST"])
def newBlog():
    if request.method == "GET":
        return render_template("newblog.html")
    if request.method == "POST":
        body = request.form.get("body")
        # check if the post request has the file part
        if not request.files["thumbnail"]:
            print('No file part')
            return redirect(request.url)
        file = request.files['thumbnail']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        post = Post(body=body, thumbnail=filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("auth.viewBlog"))


@login_required
@auth.route("/viewblog")
def viewBlog():
    records = []
    posts = Post.query.all()
    # append all records
    for post in posts:
        records.append(post)
    numberOfRows = len(records) // 3
    print(UPLOAD_FOLDER)
    return render_template("viewblog.html", records=records, length=len(records), UPLOAD_FOLDER=UPLOAD_FOLDER)


@auth.route("/uploaded/<filename>")
def uploaded(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@login_required
@auth.route("/deletePost/<postId>")
def deletePost(postId):
    Post.query.filter(Post.id == postId).delete()
    db.session.commit()
    return redirect(url_for("auth.viewBlog"))
