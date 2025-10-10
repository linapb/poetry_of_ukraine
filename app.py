import os
import asyncio
from flask import Flask, redirect, render_template, request

import helpers

# Create app
app = Flask(__name__)


# Configure application. Check in terminal with $ printenv | grep FLASK_ENV
if os.environ.get("FLASK_ENV") == "production":
    app.config.from_object("config.ProductionConfig")
elif os.environ.get("FLASK_ENV") == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")  # default


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
async def index():
    poems = helpers.get_poems()

    lang = request.args.get("lang")
    if lang not in [None, "Ukrainian"]:
        poems = await helpers.get_translations(poems, lang)

    return render_template("index.html", poems=poems)
