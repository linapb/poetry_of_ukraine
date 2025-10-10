import os
import json
import asyncio
from copy import deepcopy
import translitua
from natsort import natsorted
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model_id = "gpt-3.5-turbo"


async def get_translations(poems, lang):
    """Translate all poems concurrently."""
    tasks = [translate_poem_data(poem, lang) for poem in poems]
    return await asyncio.gather(*tasks)


async def translate_poem_data(poem, lang):
    """Translate all fields (title, author, topic, text) of a single poem."""
    translation = deepcopy(poem)
    translation["title"] = await translate_title(poem["title"], lang)
    translation["author"] = await translate_name(poem["author"], lang)
    translation["topic"] = await translate_title(poem["topic"], lang)
    translation["text"] = await translate_poem(poem["text"], lang)
    return translation


def get_poems():
    """Load poem files as JSON."""
    poems = []
    files = natsorted(os.listdir("poems"))
    for file in files:
        if file.endswith(".txt"):
            print(file)
            with open(os.path.join("poems", file), "r") as f:
                poems.append(json.load(f))
    return poems


async def translate_poem(poem, lang):
    prompt = (
        f"Translate the following Ukrainian poem into {lang}. "
        f"Make it rhyme naturally in {lang}. "
        f"Very important, it contains html tags. Keep that html tags, under any condition don't change them (<br> and <p> tags) "
        f"and don't add any other html tags. If you do, it will break the web page. Don't change html tags!"
        f"Output only the translated poem — no explanations, no commentary, no quotes.\n\n"
        f"Poem:\n{poem}"
    )

    response = await client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "You are a poetic translator."},
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_completion_tokens=4096,
    )

    return response.choices[0].message.content.strip()


async def translate_name(name, lang):
    if lang == "English":
        return translitua.translit(name)

    prompt = (
        f"Translate the following Ukrainian personal name into {lang}. "
        f"If the name is Володимир, keep Ukrainian pronunciation, so not Vladimir. "
        f"Output only the translated name, without quotes, commentary, or explanation.\n\n"
        f"Name: {name}"
    )

    response = await client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "You are a name translator."},
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_completion_tokens=1000,
    )

    return response.choices[0].message.content.strip()


async def translate_title(title, lang):
    prompt = (
        f"Translate the following Ukrainian poem title into {lang}. "
        f"Output only the translated title text — no quotes, no commentary, no extra text.\n\n"
        f"Title: {title}"
    )

    response = await client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": "You translate poem titles accurately and beautifully."},
            {"role": "user", "content": prompt},
        ],
        temperature=1,
        max_completion_tokens=1000,
    )

    return response.choices[0].message.content.strip()
