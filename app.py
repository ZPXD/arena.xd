from flask import Flask, render_template
from flask import request

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    DateField,
    SelectField
)
import os

app = Flask(__name__)

app.secret_key = 'super secret key'


# Main

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/logout')
def logout():
    return render_template("logout.html")


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

if __name__ == "__main__":
    app.run()