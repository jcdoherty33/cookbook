from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from bs4 import BeautifulSoup
import urllib.request

from helpers import apology, login_required, parse_recipe

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///cookbook.db")


@app.route("/")
@login_required
def index():
    """Show list of recipes"""

    # Get list of user's recipes
    recipes = db.execute("SELECT recipe_id, title, type FROM recipes WHERE user_id = :user ORDER BY title",
                         user=session["user_id"])

    return render_template("index.html", recipes=recipes)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add a recipe by hand."""

    # User reached route via POST
    if request.method == "POST":

        # Ensure title was entered
        if not request.form.get("title"):
            return apology("missing title", 400)

        # Add recipe to database
        db.execute("""INSERT INTO recipes (title, type, user_id, ingredients, instructions, url)
                   VALUES (:title, :type, :user_id, :ingredients, :instructions, :url)""",
                   title=request.form.get("title"), type=request.form.get("type"), user_id=session["user_id"],
                   ingredients=request.form.get("ingredients"), instructions=request.form.get("instructions"),
                   url=request.form.get("url"))

        # Redirect user to home page
        flash("Added!")
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("add.html")


@app.route("/getrecipe")
@login_required
def getrecipe():

    # Ensure url is submitted
    if not request.args.get("url"):
        raise RuntimeError("missing url")
    url = request.args.get("url")

    # Save document as soup
    page = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')

    # Send to helper function and get back recipe data
    recipe = parse_recipe(soup)
    return jsonify(recipe)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Query database for same username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username has not already been used
        if len(rows) != 0:
            return apology("username already in use", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation must match", 400)

        # Insert new user into database
        db.execute("INSERT INTO users ('username', 'hash') VALUES (:username, :hash)",
                   username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # Remember which user has logged in
        user_row = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))
        session["user_id"] = user_row[0]["id"]

        # Redirect user to home page
        flash("Registered!")
        return redirect("/",)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure old password was submitted
        if not request.form.get("old"):
            return apology("must provide old password", 400)

        # Ensure new password was submitted
        elif not request.form.get("new"):
            return apology("must provide new password", 400)

        # Ensure confimation password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure new password and confirmation match
        elif request.form.get("new") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Ensure new password is different than old password
        elif request.form.get("old") == request.form.get("new"):
            return apology("new password must be different than old password", 400)

        # Query database for user's data
        user = db.execute("SELECT * FROM users WHERE id = :id",
                          id=session["user_id"])

        # Ensure old password input matches stored password
        if not check_password_hash(user[0]["hash"], request.form.get("old")):
            return apology("invalid old password", 400)

        # Store new password
        else:
            db.execute("UPDATE users SET hash = :new WHERE id = :id",
                       new=generate_password_hash(request.form.get("new")),
                       id=session["user_id"])

        # Redirect user to home page
        flash("Password changed!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")


@app.route("/view", methods=["POST"])
@login_required
def view():
    """Display selected recipe"""

    # Ensure recipe is selected
    if not request.form.get("recipe"):
        return apology("must select recipe", 400)

    # Get information for chosen recipe
    recipe = db.execute("SELECT * FROM recipes WHERE recipe_id = :id",
                        id=request.form.get("recipe"))
    ingredients = recipe[0]['ingredients'].splitlines()
    instructions = recipe[0]['instructions'].splitlines()

    # Remove any empty ingredients and instructions
    ingredients = list(filter(None, ingredients))
    ingredients = [i for i in ingredients if i.isspace() == False]
    instructions = list(filter(None, instructions))
    instructions = [x for x in instructions if x.isspace() == False]

    return render_template("view.html", recipe=recipe[0], ingredients=ingredients, instructions=instructions)


@app.route("/edit", methods=["POST"])
@login_required
def edit():
    """Edit selected recipe"""

    # Ensure title was entered
    if not request.form.get("title"):
        return apology("missing title", 400)

    # Add recipe to database
    db.execute("""UPDATE recipes SET title = :title, type = :type, ingredients = :ingredients, instructions = :instructions
               WHERE recipe_id = :id""", title=request.form.get("title"), type=request.form.get("type"),
               ingredients=request.form.get("ingredients"), instructions=request.form.get("instructions"),
               id=request.form.get("recipe_id"))

    # Redirect user to home page
    flash("Edited!")
    return redirect("/")


@app.route("/viewform", methods=["POST"])
@login_required
def viewform():
    """Redirect to edit page for selected recipe or delete"""

    # Edit selected
    if request.form.get("edit"):
        recipe = db.execute("SELECT * FROM recipes WHERE recipe_id = :id",
                            id=request.form.get("edit"))
        return render_template("edit.html", recipe=recipe[0])

    # Deleted selected
    elif request.form.get("delete"):
        db.execute("DELETE FROM recipes WHERE recipe_id = :id", id=request.form.get("delete"))
        flash("Deleted!")
        return redirect("/")


@app.route("/shop", methods=["GET", "POST"])
@login_required
def shop():
    """Generate shopping list based on selected recipes"""

    # User reached route via POST
    if request.method == "POST":

        # Retrieve selected recipes
        recipe_list = request.form.getlist("list")

        # Find all ingredients in selected recipes
        all_ingredients = db.execute("SELECT ingredients FROM recipes WHERE recipe_id IN (:list)",
                                     list=recipe_list)
        ingredient_list = []
        for ingredients in all_ingredients:
            ingredients = ingredients['ingredients'].splitlines()
            ingredients = list(filter(None, ingredients))
            ingredients = [i for i in ingredients if i.isspace() == False]
            for ingredient in ingredients:
                ingredient_list.append(ingredient)

        return render_template("list.html", ingredients=ingredient_list)

    # User reached route via GET
    else:

        # Get list of user's recipes
        recipes = db.execute("SELECT recipe_id, title, type FROM recipes WHERE user_id = :user ORDER BY title",
                             user=session["user_id"])

        return render_template("shop.html", recipes=recipes)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
