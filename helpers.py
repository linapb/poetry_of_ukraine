import os
import openai
import json
from copy import deepcopy
import translitua
from natsort import natsorted

openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = "gpt-5"


def get_translations(poems, lang):
    translations = []
    for poem in poems:
        translation = deepcopy(poem)
        translation["title"] = translate_title(poem["title"], lang)
        translation["author"] = translate_name(poem["author"], lang)
        translation["topic"] = translate_title(poem["topic"], lang)
        translation["text"] = translate_poem(poem["text"], lang)
        translations.append(translation)

    return translations


def get_poems():
    poems = []
    files = os.listdir("poems")
    files = natsorted(files)
    for file in files:
        if file.endswith(".txt"):
            print(file)
            with open("poems/" + file, "r") as f:
                poems.append(json.load(f))
    return poems


def translate_poem(poem, lang):
    prompt = f"Hello! Please translate the following Ukrainian poem into {lang}. Make it rhyme well. " \
            "Keep HTML line and paragraph breaks. The poem:/n" + poem + "/n/n"

    response = openai.Completion.create(
      model=model_id,
      prompt=prompt,
      temperature=0,
      max_tokens=2500,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].text


def translate_name(name, lang):
    if lang == "English":
        return translitua.translit(name)

    prompt = f"Hello! Please translate the following Ukrainian name into {lang}: " + name + "/n/n"

    response = openai.Completion.create(
      model=model_id,
      prompt=prompt,
      temperature=0,
      max_tokens=2500,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].text


def translate_title(title, lang):
    prompt = f"Hello! Please translate the following Ukrainian poem's title into {lang}: " + title + "/n/n"

    response = openai.Completion.create(
      model=model_id,
      prompt=prompt,
      temperature=0,
      max_tokens=2500,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response.choices[0].text
