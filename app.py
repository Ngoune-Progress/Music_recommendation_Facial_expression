from flask import Flask,redirect, render_template, request, session, abort, url_for,flash,Response, jsonify,stream_with_context
import pyrebase
import gunicorn
from camera import *

app= Flask(__name__)


#Add your own details
config = {
  "apiKey": "AIzaSyAJX9XWgFcdRE_Ezf2re9HaKqRg6U4nNbo",
  "authDomain": "music-recommendation-aca06.firebaseapp.com",
  "databaseURL": "https://music-recommendation-aca06-default-rtdb.firebaseio.com",
  "storageBucket": "music-recommendation-aca06.appspot.com"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}


@app.route("/")
def login():
    return render_template('login.html')


# @app.route("/login")
# def index():
#     return render_template('index.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/forget")
def forget():
    return render_template('forget.html')

@app.route('/welcome')
def welcome():
    if person["is_logged_in"] == True:
        return render_template("index.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('/'))
@app.route('/admin')
def admin():
    if person["is_logged_in"] == True:
        nodes = db.child('users').get().val().keys()

        return render_template("admin.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('/'))

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["username"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            person["role"] = "simple_user"
            #Append data to the firebase realtime database
            data = {"name": name, "email": email,"role":'simple_user'}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('signup'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('signup'))

@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            role = data.val()[person["uid"]]["role"]
            #Redirect to welcome page
            if role=='simple_user':
                return redirect(url_for('welcome'))
            else:
                return redirect(url_for('admin'))

            
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))


headings = ("Name","Album","Artist")
df1 = music_rec()
df1 = df1.head(15)
@app.route('/index')
def index():
    print(df1.to_json(orient='records'))
    return render_template('index.html', headings=headings, data=df1)
    

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    # return Response(stream_with_context(VideoCamera()),
    #                 mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')

