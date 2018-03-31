# -*- coding: utf-8 -*-
"""
    Produces & Displays Pair Programming pairs
    TODO: Clean duplicates from Attendees.txt before loading
"""
# from flask import Flask, request, session, g, redirect, url_for, abort, \
#      render_template, flash, _app_ctx_stack, send_file, send_from_directory
# from flask.ext.sqlalchemy import SQLAlchemy
from pathlib import Path
import sys
import click
# # configuration
database = Path('SeminarAttendees.txt')
attendees = Path("Attendees.txt")
# DEBUG = True
# SECRET_KEY = '\xdb4\xaf\xcd\xec\xed\xad%\xa4\x03\xdf\xe7\xeb}\x07\x1d\xb1D\x93\xfb\xcd\x9c\xbb:'
# PASSWORD = 'codemashrocks'

# # Setup
# app = Flask(__name__)
# app.config.from_object(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
# db = SQLAlchemy(app)

@click.group()
@click.version_option()
def cli():
    """Pair Programming

    Generates and displays pair-programming teams using a round-robin algorithm.
    """


##################################################

class Counter: #(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # index = db.Column(db.Integer)

    def __init__(self, initValue = -1):
        self.index = initValue
        print(self)

    def __repr__(self):
        return '<Counter index %r>' % (self.index)

    def __str__(self): return self.__repr__()

__currentPairingNumber = -1

def nextPairingNumber(listSize):
    counter = Counter.query.filter_by(id=1).first()
    counter.index += 1
    if counter.index / listSize:
        counter.index = 0
    # db.session.commit()
    print("nextPairingNumber:", counter.index)
    global __currentPairingNumber
    __currentPairingNumber = counter.index
    return counter.index


##################################################

class Person: #(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(80), unique=True)

    all = []

    def __init__(self, name):
        self.name = name
        Person.all.append(name)

    def __repr__(self):
        return self.name

    @staticmethod
    def showAll():
        for p in Person.all:
            print(p)

    @staticmethod
    def generateNextPairings():
        from RoundRobin import round_robin
        size = len(Person.all)
        assert size, "empty database"
        groups = round_robin(size)[nextPairingNumber(size)]
        teams = []
        for group in groups:
            teams.append([Person.all[i] for i in group])
        return teams

@cli.command("regenDB")
def regenerate_new_database(nameList):
    "Regenerate new database"
    # checkAdmin()
    if database.exists():
        database.unlink()
    # db.create_all()
    # db.session.add(Counter(__currentPairingNumber))
    cleanList = []
    for name in nameList:
        first, last = name.rsplit(" ", 1)
        sanName = sanitize(first, last)
        if sanName not in cleanList: # Remove duplicates
            cleanList.append(sanName)
    # for p in cleanList:
    #     db.session.add(Person(p))
    # session.pop('name_entered', None)
    # db.session.commit()
    # return redirect(url_for('admin_tasks'))


######### URLs and Responses ##############################

# @app.route('/')
# def home():
#    return render_template('home.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#             flash(error, 'error')
#         else:
#             session['logged_in'] = True
#             flash('You are logged in')
#             return redirect(url_for('home'))
#     return render_template('login.html', error=error)

def sanitize(first, last):
    def san(nm):
        return " ".join([part.strip().capitalize().replace(",", "") for part in nm.split()])
    return san(first) + " " + san(last)

# @app.route('/add', methods=['POST'])
# def add_entry():
#     if session.get('name_entered') or not session.get('logged_in'):
#         abort(401)
#     sname = sanitize(request.form['first'], request.form['last'])
#     for p in Person.all:
#         if p.name == sname:
#             msg = "%s %s was already entered." % sname
#             print(msg)
#             flash(msg, 'error')
#             return redirect(url_for('home'))
#     person = Person(sname)
#     print("entered", person)
#     session['name_entered'] = person.name
#     db.session.add(person)
#     db.session.commit()
#     return redirect(url_for('home'))


# @app.route('/download', methods=['GET'])
# def download():
#     fileRequested = "AtomicScala%s.zip" % request.args['platform']
#     print(fileRequested + " download")
#     return send_file(fileRequested, as_attachment=True)


# @app.route('/leave_seminar', methods=['GET'])
# def leave_seminar():
#     p = Person.query.filter_by(name=session['name_entered']).first()
#     print(p, "leaving")
#     db.session.delete(p)
#     session.pop('name_entered', None)
#     flash('Your name has been removed')
#     db.session.commit()
#     return redirect(url_for('logout'))


# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You are logged out')
#     return redirect(url_for('home'))


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')


######### Admin Operations ##############################

# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     error = None
#     if request.method == 'POST':
#         if request.form['adminPassword'] != "bobsyeruncle":
#             error = 'Invalid password'
#         else:
#             session['admin_logged_in'] = True
#             flash('Admin logged in')
#             return redirect(url_for('admin_tasks'))
#     return render_template('admin.html', error=error)


# @app.route('/admin_logout')
# def admin_logout():
#     session.pop('admin_logged_in', None)
#     flash('Admin logged out')
#     return redirect(url_for('home'))


# def checkAdmin():
#     if not session.get('admin_logged_in'):
#         abort(401)


# @app.route('/admin_tasks', methods=['GET','POST'])
# def admin_tasks():
#     checkAdmin()
#     if request.method == 'POST':
#         deletes = request.form.getlist("do_delete")
#         if not deletes:
#             print("Nothing Selected")
#         for name in deletes:
#             p = Person.query.filter_by(name=name).first()
#             print("deleting", p)
#             db.session.delete(p)
#         db.session.commit()
#     try:
#         attendees = Person.all
#     except:
#         attendees = []
#     return render_template('admin_tasks.html', attendees=attendees)


# @app.route('/create_attendee_database')
@cli.command()
def create_attendee_database():
    if not attendees.exists():
        print("Attendees.txt not found")
        sys.exit(1)
    return regenerate_new_database(attendees.read_text().splitlines())


################## Create and Display Pairings ################

def divideList(seq, num):
    avg = len(seq) / float(num)
    result = []
    last = 0.0
    while last < len(seq):
        result.append(seq[int(last):int(last + avg)])
        last += avg
    return result

# @app.route('/generate_pairs')
@cli.command()
def generate_pairs():
    "Generate new pairs"
    # checkAdmin()
    # return render_template('PairProgramming.html',
    #     groups=divideList(Person.generateNextPairings(), 4))
    return divideList(Person.generateNextPairings(), 4)


####################### Testing #################################

# @app.route('/regenerate_test_database')
# def regenerate_test_database():
#     return regenerate_new_database(testNames)

# @app.route('/big_database')
# def big_database():
#     return regenerate_new_database(file("GeneratedNames.txt").readlines())

###################################################################
################ This must be last in the file ####################

if __name__ == '__main__':
    cli()
