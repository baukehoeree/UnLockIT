from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
import os
import RPi.GPIO as GPIO
from DbClass import DbClass

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   12 : {'name' : 'lock', 'state' : GPIO.HIGH}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route('/')
def dashboard():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('dashboard.html', mail_session=mail_session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    database = DbClass()
    error = None
    if 'email' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email_form  = request.form['email']
        password_form  = request.form['password']

        list_user = database.getUser(email_form)

        for user in list_user:
            if email_form == user[3]:
                UserTrying = user

                password = password_form
                salt = "16nov1998@Oudenaarde"
                password = password.encode('utf-8')
                salt = salt.encode('utf-8')

                sha = hashlib.sha256()
                sha.update(password)
                sha.update(salt)
                fullpassword = sha.hexdigest()

                if fullpassword == UserTrying[4]:
                    session['email'] = request.form['email']
                    return redirect(url_for('dashboard'))
                else:
                    error = "Dit wachtwoord komt niet overeen met deze gebruiker"
            else:
                error = "Deze gegevens bestaan niet in onze database"

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('dashboard'))

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/contact')
def contact():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('contact.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/register' , methods=['GET', 'POST'])
def register():
    database = DbClass()
    error = None
    if request.method == 'POST':
        name_form = request.form['lastName']
        fname_form = request.form['firstName']
        email_form = request.form['email']
        password_form = request.form['password']
        passwordConf_form = request.form['confPassword']

        list_user = database.getUser(email_form)

        if list_user == []:
            if password_form == passwordConf_form:

                password = password_form
                salt = "16nov1998@Oudenaarde"
                password = password.encode('utf-8')
                salt = salt.encode('utf-8')

                sha = hashlib.sha256()
                sha.update(password)
                sha.update(salt)
                fullpassword = sha.hexdigest()

                database = DbClass()
                database.setNewUser(name_form,fname_form,email_form,fullpassword)
                return render_template('login.html')
            else:
                error = "De 2 wachtwoorden komen niet overeen."
        else:
            error = "Deze gegevens bestaan al in onze database"

    return render_template('register.html', error=error)

@app.route('/dashboard')
def home():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('dashboard.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/overview')
def overview():
    if 'email' in session:
        mail_session = escape(session['email'])
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        templateData = {
            'pins': pins
        }
        return render_template('overview.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route('/dataOpen')
def dataOpen():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('dataOpen.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/dataMotion')
def dataMotion():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('dataMotion.html', mail_session=mail_session)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'email' in session:
        mail_session = escape(session['email'])
        return render_template('profile.html', mail_session=mail_session)
    return redirect(url_for('login'))


# DATACOM PART

@app.route("/overview/<changePin>/<action>")
def action(changePin, action):
    if 'email' in session:
        mail_session = escape(session['email'])
        changePin = int(changePin)
        if action == "open":
          GPIO.output(changePin, GPIO.HIGH)
        if action == "locked":
          GPIO.output(changePin, GPIO.LOW)
        if action == "toggle":
          GPIO.output(changePin, not GPIO.input(changePin))
        for pin in pins:
          pins[pin]['state'] = GPIO.input(pin)
        templateData = {
          'pins' : pins
        }

        return render_template('overview.html', mail_session=mail_session, **templateData)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",8080))
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)
