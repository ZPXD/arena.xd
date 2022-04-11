from flask import Flask, render_template

app=Flask(__name__)


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


if __name__=="__main__":
    app.run()