# -*- coding: utf-8 -*-
"""
    Atomic Scala Seminar local network server
    Serves files for Seminar
    Produces & Displays Pair Programming pairs

    TODO: Clean duplicates from Attendees.txt before loading

"""
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, send_file, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import os, os.path

# configuration
DATABASE = 'AtomicScalaSeminar.db'
DEBUG = True
SECRET_KEY = '\xdb4\xaf\xcd\xec\xed\xad%\xa4\x03\xdf\xe7\xeb}\x07\x1d\xb1D\x93\xfb\xcd\x9c\xbb:'
PASSWORD = 'codemashrocks'

# Setup
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
db = SQLAlchemy(app)

##################################################

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)

    def __init__(self, initValue = -1):
        self.index = initValue
        print self

    def __repr__(self):
        return '<Counter id %r index %r>' % (self.id, self.index)

    def __str__(self): return self.__repr__()

__currentPairingNumber = -1

def nextPairingNumber(listSize):
    counter = Counter.query.filter_by(id=1).first()
    counter.index += 1
    if counter.index / listSize:
        counter.index = 0
    db.session.commit()
    print "nextPairingNumber:", counter.index
    global __currentPairingNumber
    __currentPairingNumber = counter.index
    return counter.index


##################################################

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    @staticmethod
    def showAll():
        for p in Person.query.all():
            print p

    @staticmethod
    def generateNextPairings():
        from RoundRobin import round_robin
        size = len(Person.query.all())
        if not size:
            print "empty database"
            return [[]]
        groups = round_robin(size)[nextPairingNumber(size)]
        teams = []
        for group in groups:
            teams.append([Person.query.all()[i] for i in group])
        return teams


def regenerate_new_database(nameList):
    checkAdmin()
    #counter = nextPairingNumber(len(Person.query.all()))
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    db.create_all()
    #db.session.add(Counter(counter))
    db.session.add(Counter(__currentPairingNumber))
    cleanList = []
    for name in nameList:
        first, last = name.rsplit(" ", 1)
        sanName = sanitize(first, last)
        if sanName not in cleanList: # Remove duplicates
            cleanList.append(sanName)
    for p in cleanList:
        db.session.add(Person(p))
    session.pop('name_entered', None)
    db.session.commit()
    return redirect(url_for('admin_tasks'))


######### URLs and Responses ##############################

@app.route('/')
def home():
   return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
            flash(error, 'error')
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

def sanitize(first, last):
    def san(nm):
        return " ".join([part.strip().capitalize().replace(",", "") for part in nm.split()])
    return san(first) + " " + san(last)

@app.route('/add', methods=['POST'])
def add_entry():
    if session.get('name_entered') or not session.get('logged_in'):
        abort(401)
    sname = sanitize(request.form['first'], request.form['last'])
    for p in Person.query.all():
        if p.name == sname:
            msg = "%s %s was already entered." % sname
            print(msg)
            flash(msg, 'error')
            return redirect(url_for('home'))
    person = Person(sname)
    print "entered", person
    session['name_entered'] = person.name
    db.session.add(person)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/download', methods=['GET'])
def download():
    fileRequested = "AtomicScala%s.zip" % request.args['platform']
    print fileRequested + " download"
    return send_file(fileRequested, as_attachment=True)


@app.route('/leave_seminar', methods=['GET'])
def leave_seminar():
    p = Person.query.filter_by(name=session['name_entered']).first()
    print p, "leaving"
    db.session.delete(p)
    session.pop('name_entered', None)
    flash('Your name has been removed')
    db.session.commit()
    return redirect(url_for('logout'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return redirect(url_for('home'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


######### Admin Operations ##############################

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    if request.method == 'POST':
        if request.form['adminPassword'] != "bobsyeruncle":
            error = 'Invalid password'
        else:
            session['admin_logged_in'] = True
            flash('Admin logged in')
            return redirect(url_for('admin_tasks'))
    return render_template('admin.html', error=error)


@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Admin logged out')
    return redirect(url_for('home'))


def checkAdmin():
    if not session.get('admin_logged_in'):
        abort(401)


@app.route('/admin_tasks', methods=['GET','POST'])
def admin_tasks():
    checkAdmin()
    if request.method == 'POST':
        deletes = request.form.getlist("do_delete")
        if not deletes:
            print "Nothing Selected"
        for name in deletes:
            p = Person.query.filter_by(name=name).first()
            print "deleting", p
            db.session.delete(p)
        db.session.commit()
    try:
        attendees = Person.query.all()
    except:
        attendees = []
    return render_template('admin_tasks.html', attendees=attendees)


@app.route('/create_attendee_database')
def create_attendee_database():
    if not os.path.exists("Attendees.txt"):
        print "Attendees.txt not found"
        abort(404)
    return regenerate_new_database(file("Attendees.txt").readlines())


################## Created and Display Pairings ################

def divideList(seq, num):
    avg = len(seq) / float(num)
    result = []
    last = 0.0
    while last < len(seq):
        result.append(seq[int(last):int(last + avg)])
        last += avg
    return result

@app.route('/generate_pairs')
def generate_pairs():
    checkAdmin()
    return render_template('PairProgramming.html',
        groups=divideList(Person.generateNextPairings(), 4))


####################### Testing #################################

testNames = [name.strip() for name in
"""Buckaroo Banzai
Emilio Lizardo
Penny Priddy
John Whorfin
John Parker
John Bigboote
John Bigboote
John Bigboote
John Emdall
John Yaya
John Smallberries
John Smallberries
John Smallberries
""".splitlines()]


@app.route('/regenerate_test_database')
def regenerate_test_database():
    return regenerate_new_database(testNames)

@app.route('/big_database')
def big_database():
    return regenerate_new_database(file("GeneratedNames.txt").readlines())

###################################################################
################ This must be last in the file ####################

if __name__ == '__main__':
    app.run()
