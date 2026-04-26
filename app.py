import os
from flask import Flask, render_template, request, jsonify
from asgiref.wsgi import WsgiToAsgi

import helpers

# Consts: Texts in English
intro_text_eng = "On this page, you'll discover a curated collection of nine distinct poems from various authors, each exploring different themes. This selection is designed to offer a glimpse into the essence of the Ukrainian spirit: love, courage and perseverance."
nav_bar_text_eng = "EXPERIENCE POETRY OF UKRAINE IN YOUR NATIVE LANGUAGE"
select_lang_text_eng = "Select your language"
lang_text_eng = "LANGUAGE"
note_text_eng = "Note: translations are powered by LLM models. They can be incomplete or incorrect."
developed_by_text_eng = "developed and maintained by"
contact_text_eng = "Contact me at"
show_email_text_eng = "Show Email"

# Consts: Texts in Ukrainian
intro_text_ua = "На данній сторінці ви знайдете добірку з девʼяти поезій різних авторів, кожна з яких досліджує різну тему. Ця колекція створена для того, щоб підсвітити сутність Укранського духу: любов, смітивість і витримка."
nav_bar_text_ua = "ВІДЧУЙТЕ УКРАЇНСЬКУ ПОЕЗІЮ ВАШОЮ РІДНОЮ МОВОЮ"
select_lang_text_ua = "Оберіть вашу мову"
lang_text_ua = "МОВА"
note_text_ua = "Зауважте: переклади зроблені за допомогою штучного інтелекту. Вони можуть бути неповні чи некоректні."
developed_by_text_ua = "розроблено і підтримується"
contact_text_ua = "Звʼязатися зі мною"
show_email_text_ua = "Показати імейл"

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


@app.route('/get-contact-email')
def get_contact():
    return jsonify(email=os.environ.get('CONTACT_EMAIL'))


@app.route("/")
async def index():
    email_is_set = os.environ.get('CONTACT_EMAIL') is not None
    poems_ua_originals = helpers.get_poems()

    lang = request.args.get("lang")

    if lang is None:
        # Default version combines English texts and poems in Ukrainian
        poems = poems_ua_originals
        intro_text, nav_bar_text, select_lang_text, lang_text, note_text, developed_by_text, contact_text, show_email_text = intro_text_eng, nav_bar_text_eng, select_lang_text_eng, lang_text_eng, note_text_eng, developed_by_text_eng, contact_text_eng, show_email_text_eng
    elif lang == "Ukrainian":
        # Everything in Ukrainian
        poems = poems_ua_originals
        intro_text, nav_bar_text, select_lang_text, lang_text, note_text, developed_by_text, contact_text, show_email_text = intro_text_ua, nav_bar_text_ua, select_lang_text_ua, lang_text_ua, note_text_ua, developed_by_text_ua, contact_text_ua, show_email_text_ua
    elif lang == "English":
        # Everything in English
        (poems,) = await helpers.get_translations(lang, poems_ua_originals)
        intro_text, nav_bar_text, select_lang_text, lang_text, note_text, developed_by_text, contact_text, show_email_text = intro_text_eng, nav_bar_text_eng, select_lang_text_eng, lang_text_eng, note_text_eng, developed_by_text_eng, contact_text_eng, show_email_text_eng
    else:
        # Translates everything for all other languages
        poems, intro_text, nav_bar_text, select_lang_text, lang_text, note_text, developed_by_text, contact_text, show_email_text = await helpers.get_translations(lang, poems_ua_originals, intro_text_eng, nav_bar_text_eng, select_lang_text_eng, lang_text_eng, note_text_eng, developed_by_text_eng, contact_text_eng, show_email_text_eng)

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


asgi_app = WsgiToAsgi(app)
