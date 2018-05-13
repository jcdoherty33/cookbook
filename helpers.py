import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps
from bs4 import BeautifulSoup


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def parse_recipe(soup):
    """Get recipe data by scraping web page."""

    # Get title
    title = soup.title.contents

    # Get ingredients
    # Find div with class that includes "ingredients"
    if soup.find("div", "ingredients"):

        # Find all lists of ingredients
        lists = soup.find("div", "ingredients").find_all("ul")
        ingredients = ""

        for list in lists:

            # Find all items in each list
            items = list.find_all("li")

            # Merge items into string with line breaks
            for item in items:
                if item.label:
                    ingredients += item.label.contents[0] + '\n'
                else:
                    ingredients += item.contents[0] + '\n'

    # If ingredients cannot be found
    else:
        ingredients = "Could not find ingredients."

    # Get instructions
    # Find div with class that includes "method"
    if soup.find("div", "method"):

        # Find all paragraphs of text
        text = soup.find("div", "method").find_all("p")
        instructions = ""

        # Merge paragraphs into string with line breaks
        for item in text:
            instructions += item.contents[0] + '\n'

    # Find div with class that includes "instructions"
    elif soup.find("div", "instructions"):

        # Find all paragraphs of text
        text = soup.find("div", "instructions").find_all("p")
        instructions = ""

        # Merge paragraphs into string with line breaks
        for item in text:
            instructions += item.contents[0] + '\n'

    # Find div with class that includes "directions"
    elif soup.find("div", "directions"):

        # Find all paragraphs of text
        text = soup.find("div", "directions").find_all("p")
        instructions = ""

        # Merge paragraphs into string with line breaks
        for item in text:
            instructions += item.contents[0] + '\n'

    # Find div with class that includes "steps"
    elif soup.find("div", "steps"):

        # Find all paragraphs of text
        text = soup.find("div", "steps").find_all("ol")
        instructions = ""

        for item in text:

            # Find all items in each list
            items = text.find_all("li")

            # Merge items into string with line breaks
            for item in items:
                if item.label:
                    ingredients += item.label.contents[0] + '\n'
                else:
                    ingredients += item.contents[0] + '\n'

    # If instructions cannot be found
    else:
        instructions = "Could not find instructions."

    # Return object containing recipe information
    recipe = {'title': title, 'ingredients': ingredients, 'instructions': instructions}
    return recipe
