from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from lib.database.db_utils import get_db
from game_algorithm import generate_game

app = Flask(__name__)
app.config["SECRET_KEY"] = "jerry-garcia"
global_game = None
db = get_db()

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        global global_game
        global_game = generate_game()
        constraints_displays = [str(c) for c in global_game.top_constraints] + [str(c) for c in global_game.side_constraints]
        all_song_names: list[str] = [songname for _, songname in db["songs"].items()]
        return render_template("index.html", 
                constraints=constraints_displays, 
                autocomplete_list=all_song_names
                ), 200
    
@app.route('/rules')
def rules_page():
    return render_template("rules.html"), 200
    
# @app.route('/popup', 'index/popup')
# def grid_popup():
#     form = GridForm()
#     all_song_names: list[str] = [songname for _, songname in db["songs"].items()]
#     return render_template('grid_popup.html', autocomplete_list=all_song_names)

class GridForm(FlaskForm):
    guess = StringField('Guess', validators=[DataRequired()])
    enter = SubmitField('Enter')
    

if __name__ == "__main__":
    app.run()