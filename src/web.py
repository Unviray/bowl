from flask import Flask, render_template, request
from icecream import ic
from main import Game


app = Flask(__name__)
game = Game()


@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        touched = request.form.get("touched")
        try:
            game.launch(int(request.form['touched']))
        except ValueError:
            pass

    return render_template("index.html", game=game)


if __name__ == "__main__":
    app.run(debug=True)
