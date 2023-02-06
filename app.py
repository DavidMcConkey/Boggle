from boggle import Boggle
from flask import Flask, session, jsonify, request, render_template

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdl'


@app.route('/')
def home():
    """Displays board"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore',0)
    nplays = session.get('nplays',0)

    return render_template('index.html', board=board,highscore=highscore,nplays=nplays)

@app.route('/check-word')
def check_word():
    """Checks if word is within dictionary"""
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board,word)

    return jsonify({'result':response})

@app.route('/post-score', methods=['POST'])
def post_score():
    """Collect score, update nplays, as well as update score if needed"""
    score = request.json['score']
    highscore=session.get('highschore',0)
    nplays = session.get('nplays',0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)