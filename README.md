# POETRY OF UKRAINE
## Description:

This is a Python Flask web app. It translates selected Ukrainian poems into your native language using ChatGPT API.
The main advantage of using ChatGPT instead of simple translation is that ChatGPT translates the poem with rhymes.
Before this technology, it was impossible to do automatic translation of poems with rhyming, it should have been done manually by people for each poem individually.
Now, we can experience beauty of poetry from any language in any language almost instantly.

In addition, there are photos of poets that are improved and colored using AI tool https://www.cutout.pro/.
In this way we can feel like they are just like us and not some strange people from the past.

### How to use the app:
Go to the web page, you will see a list of poems in Ukrainian. On top right corner there is a language selection button.
Select a language you want poems to be translated into and then wait couple of minutes and don't restart the page as ChatGPT API is translating poems and it takes some time.
Enjoy the beauty of Ukrainian poetry in your language!

#### Disclaimer:
As the translation is generated on the go and is random it's not proofread and may contain mistakes.
Nevertheless, it's still a great way to get a feeling of the poem.

Also ChatGPT was used to generate the language list therefore it may not be full or contain mistakes as well.



## Getting Started:

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites:

- Python 3.11 or later
- pip

### Installation:

1. Clone the repository:
git clone https://github.com/linapb/poetry_of_ukraine.git

2. Navigate into the cloned repository:
cd poetry_of_ukraine

3. Install the dependencies:
pip install -r requirements.txt

4. Get OpenAI API key from https://platform.openai.com/account/api-keys and set it as an environment variable:
export OPENAI_API_KEY="your_key"

5. Set the environment variable FLASK_APP to run the application:
export FLASK_APP=app.py

6. Set the environment variable FLASK_ENV to development:
export FLASK_ENV=development

6. Run the application:
flask run

## Note:
This project was done as a part of final project for the course CS50 from Harvard University.

## Documentation:

### Files:
In the main directory there are the following folders and files:
1. poems - contains poems in Ukrainian
2. static - contains static files: css, js, images
3. templates - contains html files
4. app.py - main file with the code
5. config.py - contains configuration for the app
6. helpers.py - contains helper functions
7. requirements.txt - contains all the dependencies
8. README.md - this file
9. .gitignore - contains files that should be ignored by git

Web app has responsive design and works on devices with different sizes.
It uses Bootstrap 5.0.2 framework. 

helpers.py contains the following functions: translate_poem, translate_title, translate_name. They use ChatGPT API for translation.

app.py is a standard Flask app with one root "/", error handling (404, 500) and configuration from config.py object.

The app uses Google Analytics to track visits and language selection events.

A sitemap.xml file is available at /static/sitemap.xml.
