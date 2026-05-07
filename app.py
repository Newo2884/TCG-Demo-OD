from flask import Flask, jsonify, render_template, request
import os

app = Flask(__name__)

folder_path = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
