import smtplib

import stripe
from flask import render_template, Blueprint, redirect, url_for, request

from models import Post

main = Blueprint("main", __name__)


@main.route('/')
def index():
    # get the latest post
    latest = []
    posts = Post.query.all()
    num = Post.query.count()
    i = 1
    for post in posts:
        if not (num < 0) and num <= 2:
            latest.append(post)
        else:
            if i == num - 1:
                latest.append(post)
            if i == num:
                latest.append(post)
        i += 1

    return render_template("index.html", latest=latest, length=len(latest))


@main.route('/team')
def team():
    return render_template("team.html")


@main.route('/blog')
def blog():
    records = []
    posts = Post.query.all()
    # append all records
    for post in posts:
        records.append(post)
    numberOfRows = len(records) // 3
    return render_template("blog.html", records=records, length=len(records), numberOfRows=numberOfRows)


@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    if request.method == "POST":
        email = request.form["email"]
        message = request.form["message"]

        gmail_user = 'alliancenshuti99@gmail.com'
        gmail_password = 'htfodcupycbzeebi'

        sent_from = email
        to = [gmail_user]
        subject = 'EMAIL FROM WESITE VISITOR'
        body = "From  " + email + "  :" + message

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(gmail_user, gmail_password)
            smtp_server.sendmail(sent_from, to, email_text)
            smtp_server.close()
            # use flash card to notify
        except Exception as ex:
            pass
            # use flash text to notify

        return redirect(url_for("main.contact"))


@main.route("/donate")
def donate():
    return render_template("donate.html")


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/success")
def checkout_success():
    return render_template("success.html")


@main.route("/cancel")
def cancel_checkout():
    return redirect(url_for("main.index"))


@main.route("/ourBackground")
def ourBackground():
    return render_template('whoweare.html')


@main.route('/create-checkout-session', methods=["POST"])
def create_checkout_session():
    DOMAIN = request.headers["host"]
    stripe.api_key = "sk_test_51MFlMSBN6xqoADok5im2WD4ZIE7LYnTYiy8sF8MA5E7d8DeK4agquKddkOhGxEohhcT3vQlJNhuuttZaH8qFEL0w00dWh4I9R3"
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': 'price_1MFs6TBN6xqoADokabKB3mhb',
                'quantity': 1,
            }],
            mode='payment',
            success_url="http://127.0.0.1:5000/" + url_for("main.checkout_success"),
            cancel_url="http://127.0.0.1:5000/" + url_for("main.cancel_checkout"),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@main.route("/programs")
def programs():
    return render_template("programs.html")


@main.route("/joinus")
def joinus():
    return render_template("joinUs.html")
