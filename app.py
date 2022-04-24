from flask import Flask, render_template, request, redirect, url_for 

import flask_wtf
from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager
from flask_login import login_required, current_user, login_user, logout_user

import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/arenaxd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = ':)'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


# Main

@app.route('/')
def index():
    return render_template("index.html")

# Login

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if user.check_password(password):
                login_user(user, force=True)
                return redirect( url_for('index'))
        else:
            return "user not found"

    return render_template("login.html", form=form)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if User.query.filter_by(email=email).first():
            return 'taki email już istnieje'

        user = User(name=name, email=email, password=password)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect( url_for('index'))
    return render_template("signup.html", form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return render_template("logout.html")

@login_required
@app.route('/profile/<name>')
def user(name):
    if name == current_user.name:
        return "ok"
    else:
        return "no"


# Matches

@app.route('/matches')
def matches():
    return render_template("matches.html")


@app.route('/create_match')
def create_match():
    return render_template("create_match.html")


# Match

@app.route('/match')
def match():
    return render_template("create_match.html")


@app.route('/match/antechamber/<match>')
def antechamber(match):
    return render_template("antechamber.html", match=match)


@app.route('/match/<match>')
def match_view(match):
    return render_template("match_view.html", match=match)


@app.route('/match/<match>/<player>')
def player_view(match, player):
    return render_template("player_view.html", match=match, player=player)


@app.route('/match/<match>/<player>/result')
def result(match, player):
    return render_template("result.html", match=match, player=player)


# Terminal & notepad & effect minimal version sketch.

def save_notepad(file_lines):
    program_file = 'notepad.py'
    program_file_backup = 'notepad_last.py'

    output_file = 'output.txt'
    output_file_backup = 'output_last.txt'

    # Notepad
    os.system('rm {}'.format(program_file_backup))
    os.system('cp {} {}'.format(program_file, program_file_backup))
    os.system('rm {}'.format(program_file))

    # Output
    os.system('rm {}'.format(output_file_backup))
    os.system('cp {} {}'.format(output_file, output_file_backup))
    os.system('rm {}'.format(output_file))

    with open(program_file, 'w+') as f:
        for line in file_lines:
            f.write(line)
    os.system('python3 {} > {}'.format(program_file, output_file))

def read_output():
    output_file = 'output.txt'
    with open(output_file, 'r+') as f:
        output_lines = f.readlines()
    return output_lines

@app.route('/player_test', methods=['POST', 'GET', 'OPTIONS'])
def player_test():
    output = ''
    form = NotepadForm()
    if form.validate_on_submit():
        notepad_text = form.notepad.data
        notepad_lines = notepad_text.split('\n')
        save_notepad(notepad_lines)
        output = ''.join(read_output())
    return render_template("player_test.html", form=form, output=output)

@app.route('/output/data', methods=['POST', 'OPTIONS'])
def output_data():
    data = read_output()
    return ''.join(data)

@app.route('/output_test')
def output_test():
    return render_template('test_button.html')


# DB Models

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self,password):
        self.password = generate_password_hash(password)
     
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)
 
@app.before_first_request
def create_all():
    db.create_all()


# Forms

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('hasło', validators=[DataRequired()])
    submit = SubmitField('zaloguj się')

class SignupForm(FlaskForm):
    name = StringField('nazwa użytkownika', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('hasło', validators=[DataRequired()])
    confirm_password = StringField('powtórz hasło', validators=[DataRequired()])
    submit = SubmitField('załóż konto')


# Testing

def player1_test():
    pass

def player2_test():
    pass

def match_view_test():
    pass

# Notepad Form

class NotepadForm(FlaskForm):
    notepad = TextAreaField()
    submit = SubmitField('Uruchom')


# Errors

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500


if __name__=="__main__":
    app.run(debug=True)
