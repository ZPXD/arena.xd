from flask import Flask, render_template
from flask import request

from flask_wtf import FlaskForm

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


# Terminal

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


# Notepad & effect example

@app.route('/notepad', methods=["GET", "POST"])
def notepad():
    form = NotepadForm()
    if form.validate_on_submit():
        notepad_text = form.notepad.data
        notepad_lines = notepad_text.split('\n')
        save_notepad(notepad_lines)
    return render_template("terminal.html", form=form)


@app.route('/output', methods=["GET", "POST"])
def output():
    output_lines = read_output()
    return render_template("output.html", output_lines=output_lines)


# Notepad Form

class NotepadForm(FlaskForm):
    notepad = TextAreaField('Notepad')
    submit = SubmitField('Submit')


# Moje zmiany MG

@app.route('/output/data', methods=['POST', 'OPTIONS'])
def output_data():
    data = read_output()
    return ''.join(data)

@app.route('/output_test')
def output_test():
    return render_template('test_button.html')

@app.route('/player_test', methods=['POST', 'GET', 'OPTIONS'])
def player_test():
    form = NotepadForm()
    if form.validate_on_submit():
        notepad_text = form.notepad.data
        notepad_lines = notepad_text.split('\n')
        save_notepad(notepad_lines)
    return render_template("player_test.html", form=form)

if __name__ == "__main__":
    app.run()
