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
    intro_text = "On this page, you'll discover a curated collection of nine distinct poems from various authors, each exploring different themes. This selection is designed to offer a glimpse into the essence of the Ukrainian spirit: love, courage and perseverance."
    nav_bar_text = "EXPERIENCE POETRY OF UKRAINE IN YOUR NATIVE LANGUAGE"
    select_lang_text = "Select your language"
    lang_text = "LANGUAGE"
    note_text = "Note: translations are powered by LLM models. They can be incomplete or incorrect."
    developed_by_text = "developed and maintained by"
    contact_text = "Contact me at"
    show_email_text = "Show Email"

    lang = request.args.get("lang")

    # Don't translate all parts for English and Ukrainian
    if lang is None:
        pass
    elif lang == "Ukrainian":
        _, intro_text, nav_bar_text, select_lang_text, lang_text, note_text, developed_by_text, contact_text, show_email_text = await helpers.get_translations(
            lang, [], intro_text, nav_bar_text, select_lang_text, lang_text, note_text, developed_by_text,
            contact_text, show_email_text,
        )
    elif lang == "English":
        poems = await helpers.get_translations(lang, poems)
        poems = poems[0]
    else:
        poems, intro_text, nav_bar_text, select_lang_text, lang_text, note_text, developed_by_text, contact_text, show_email_text = await helpers.get_translations(
            lang, poems, intro_text, nav_bar_text, select_lang_text, lang_text, note_text, developed_by_text,
            contact_text, show_email_text,
        )

    return render_template(
        "index.html",
        poems=poems,
        show_contact_email=email_is_set,
        intro_text=intro_text,
        nav_bar_text=nav_bar_text,
        select_lang_text=select_lang_text,
        lang_text=lang_text,
        note_text=note_text,
        developed_by_text=developed_by_text,
        contact_text=contact_text,
        show_email_text=show_email_text,
    )


@app.route('/get-contact-email')
def get_contact():
    return jsonify(email=os.environ.get('CONTACT_EMAIL'))


asgi_app = WsgiToAsgi(app)
