from flask import Flask
import os


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="0.0.0.0")
