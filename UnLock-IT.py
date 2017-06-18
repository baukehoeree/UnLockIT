from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
import os
import RPi.GPIO as GPIO
import time
import datetime
import json

print("applicatie word geladen...")
from DbClass import DbClass
time.sleep(30)
print("applicatie geladen!")


GPIO.setwarnings(False)

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   12 : {'name' : 'lock', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
    print(pin)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route('/')
def dashboard():
    if 'email' in session:
        mail_session = escape(session['email'])

        database = DbClass()
        sloten = database.getLocks(mail_session)

        database = DbClass()
        dataAccess = database.getDataAccessDay(sloten[0][0])

        print(dataAccess)

        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins,
            'typeSlot': sloten,
            'data': dataAccess
        }
        return render_template('dashboard.html', mail_session=mail_session, **templateData)
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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'email' in session:
        mail_session = escape(session['email'])
        if request.method == 'POST':
            name_form = request.form['fullname']
            phone_form = request.form['phone']
            mail_form = request.form['mail']
            message_form = request.form['message']

            database = DbClass()
            database.setContact(name_form,phone_form,mail_form,message_form)

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

        database = DbClass()
        sloten = database.getLocks(mail_session)

        database = DbClass()
        dataAccess = database.getDataAccessDay(sloten[0][0])

        print(dataAccess)

        # For each pin, read the pin state and store it in the pins dictionary:
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        # Put the pin dictionary into the template data dictionary:
        templateData = {
            'pins': pins,
            'typeSlot': sloten,
            'data': dataAccess
        }
        return render_template('dashboard.html', mail_session=mail_session, **templateData)
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
        database = DbClass()
        sloten = database.getLocks(mail_session)

        database = DbClass()
        dataAccessPage = database.getDataAccess(sloten[0][0])
        database = DbClass()
        dataAccessChart = database.getDataAccessChart(sloten[0][0])
        templateData = {
            'data': dataAccessPage
        }
        return render_template('dataOpen.html', mail_session=mail_session,dataChart=json.dumps(dataAccessChart), **templateData)
    return redirect(url_for('login'))

@app.route('/dataMotion')
def dataMotion():
    if 'email' in session:
        mail_session = escape(session['email'])
        database = DbClass()
        sloten = database.getLocks(mail_session)

        database = DbClass()
        dataMotionPage = database.getDataMotion(sloten[0][0])

        templateData = {
            'data': dataMotionPage
        }
        return render_template('dataMotion.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'email' in session:
        mail_session = escape(session['email'])

        if request.method == 'POST':
            name_form = request.form['lastName']
            fname_form = request.form['firstName']
            postal_form = request.form['postal']
            address_form = request.form['address']
            country_form = request.form['country']
            city_form = request.form['city']
            email_form = request.form['email']
            email = mail_session

            database = DbClass()
            database.updateProfile(email, name_form, fname_form, email_form, address_form, city_form, postal_form, country_form)

            session['email'] = request.form['email']

        database = DbClass()
        list_users = database.getUser(mail_session)

        templateData = {
            'user': list_users
        }

        return render_template('profile.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))


# DATACOM PART

@app.route("/overview/<changePin>/<action>")
def action(changePin, action):
    if 'email' in session:
        mail_session = escape(session['email'])
        changePin = int(changePin)
        if action == "open":
            GPIO.output(changePin, GPIO.HIGH)
            status = 1
            database = DbClass()
            database.setLog(status)
        if action == "locked":
            GPIO.output(changePin, GPIO.LOW)
            status = 0
            database = DbClass()
            database.setLog(status)
        if action == "toggle":
            GPIO.output(changePin, not GPIO.input(changePin))
        for pin in pins:
            pins[pin]['state'] = GPIO.input(pin)
        templateData = {
          'pins' : pins
        }
        return render_template('overview.html', mail_session=mail_session, **templateData)
    return redirect(url_for('login'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT",8080))
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)
