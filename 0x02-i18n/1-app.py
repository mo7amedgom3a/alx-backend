from flask_babel import Babel
from flask import Flask, render_template
"""Basic Babel setup"""
babel = Babel()
app = Flask(__name__)


class Config:
    """Config app class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_TIMEZONE = "UTC"
    BABEL_DEFAULT_LOCALE = "en"


app.config.from_object(Config)


@app.route('/')
def index():
    """Return index.html"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
