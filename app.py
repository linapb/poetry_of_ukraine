import os
from flask import Flask, render_template, request, jsonify
from asgiref.wsgi import WsgiToAsgi

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
    email_is_set = os.environ.get('CONTACT_EMAIL') is not None

    poems = helpers.get_poems()
    intro_text = "On this page, you'll discover a curated collection of nine distinct poems from various authors, each exploring different themes. This selection is designed to offer a glimpse into the essence of the <strong>Ukrainian spirit: love, courage and perseverance</strong>."
    nav_bar = "EXPERIENCE POETRY OF UKRAINE IN YOUR NATIVE LANGUAGE"

    lang = request.args.get("lang")
    if lang not in [None, "Ukrainian"]:
        poems, intro_text, nav_bar = await helpers.get_translations(lang, poems, intro_text, nav_bar)

    return render_template("index.html", poems=poems, show_contact_email=email_is_set, intro_text=intro_text, nav_bar=nav_bar)


@app.route('/get-contact-email')
def get_contact():
    return jsonify(email=os.environ.get('CONTACT_EMAIL'))


asgi_app = WsgiToAsgi(app)
