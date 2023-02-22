from werkzeug.utils import secure_filename
from .flaskapp import *
from flask import request, session, send_file
from .database.models import User, db, Flights
from .database import crud
from flask import render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
import os


app.secret_key = os.urandom(12)

oauth = OAuth(app)

@app.route('/google/')
def google():

    GOOGLE_CLIENT_ID = "270532100886-cmf9vubvqp23e24lec5gfopps3f2q6a7.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = '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'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():

    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, None)
    crud.add_user(User(login=user["email"],
                       user_name=user['name'],
                       password='12345678'))
    query = db.session.query(User).filter_by(login=user.email, password='12345678').first()
    if query:
    #     session['authenticated'] = True
    #     session['uid'] = query.used_id
    #     session['name'] = user.name
    #     session['login'] = user.email
        return redirect(url_for("home", user_id=query.user_id))
    # else:
    #     return render_template("login.html", context="The login or username were wrong")
    return render_template("login.html")

@app.route("/")
def home(context=None):
    return render_template("index.html", context=None)


@app.route("/about")
def about(context=None):
    return render_template("about.html", context=context)


@app.route("/packages")
def packages(context=None):
    return render_template("packages.html", context=context)


@app.route("/hotels")
def hotels(context=None):
    return render_template("hotels.html", context=context)


@app.route("/insurance")
def insurance(context=None):
    return render_template("insurance.html", context=context)


@app.route("/blog-home")
def blog_home(context=None):
    return render_template("blog-home.html", context=context)


@app.route("/blog_single")
def blog_single(context=None):
    return render_template("blog-single.html", context=context)


@app.route("/contact")
def contact(context=None):
    return render_template("contact.html", context=context)


@app.route("/my_booking/<int:user_id>")
def mybooking(user_id, context=None):
    query = db.session.query(User).join(Flights).filter(Flights.user_id == user_id).first()
    if query:
        return render_template("booking.html", context=query)
    else:
        query = db.session.query(User).filter(User.user_id == user_id).first()
        return render_template("booking.html", context=query)


@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def user_page(user_id, context=None):
    if request.method == "POST":
        flight_from = request.form['flight_from']
        flight_to = request.form['flight_to']
        flight_start = request.form['flight_start']
        flight_end = request.form['flight_end']
        flight_adults = request.form['flight_adults']
        flight_child = request.form['flight_child']
        identification = request.files['identification']
        identification.save(f"C:/Users/77471/PycharmProjects/final/Project/web/identifications/{secure_filename(identification.filename)}")
        crud.add_flight(Flights(flight_from=flight_from,
                                flight_to=flight_to,
                                start=flight_start,
                                end=flight_end,
                                adults=flight_adults,
                                child=flight_child,
                                identification=identification.filename,
                                user_id=session["uid"]))
    return render_template("user_page.html")

@app.route('/download/<int:flight_id>')
def download_file(flight_id):
    query = db.session.query(Flights).filter(Flights.flight_id == flight_id).first()
    fname = '_'.join(query.identification.split())
    print(fname)
    p = f"C:/Users/77471/PycharmProjects/final/Project/web/identifications/{fname}"

    return send_file(p, as_attachment=True)


@app.route("/login", methods=["GET", "POST"])
def login(context=None):
    if request.method == "POST":
        user = db.session.query(User).filter_by(login=request.form['email'], password=request.form['password']).first()
        if user:
            session['authenticated'] = True
            session['uid'] = user.user_id
            session['name'] = user.user_name
            session['login'] = user.login
            return redirect(url_for("home", user_id=user.user_id))
        else:
            return render_template("login.html", context="The login or username were wrong")

    return render_template("login.html", context=context)


@app.route("/logout")
def logout():
    session.pop('authenticated', None)
    session.pop('uid', None)
    session.pop('login', None)
    return redirect(url_for('home'))


@app.route("/elements")
def elements(context=None):
    return render_template("elements.html", context=context)


@app.route("/register", methods=["GET", "POST"])
def register(context=None):
    if request.method == "POST":
        login = request.form['email']
        name = request.form['name']
        pass1 = request.form['password']
        pass2 = request.form['password_conf']

        data = db.session.query(User).filter_by(login=request.form['email']).first()

        if data:
            return redirect(url_for("register", error="Already registered!"))
        elif pass1 != pass2:
            return redirect(url_for("register", error="Passwords do not match!"))
        else:
            crud.add_user(User(login=login,
                               user_name=name,
                               password=pass1))

            return redirect(url_for("login", context="Successfully registered!"))
    return render_template("register.html", context=context)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)