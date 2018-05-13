My final project, a web application called Cookbook, was implemented using flask with a backend database. The database contains two
tables - one storing users and their login information, and another storing recipes with all their associated information. This
includes the recipe's title, type, URL of the website it comes from, ingredients, instructions, and the ID of the user who saved
the recipe.

The ingredients and instructions are saved to the database as strings in the format in which the user entered them. When the recipe
is displayed, however, the ingredients and instructions are composed into lists as recognized by line breaks and carriage returns in
the raw strings. Additionally, any empty lines are removed to display clean lists to the user.

If a user chooses to enter the URL of a webpage containing a recipe, the web application pulls the recipe data from the site into
the form. The application uses BeautifulSoup to employ web scraping in retrieving that data from the webpage. This functionality is
implemented in the 'parse_recipe' function within the helpers.py file. First, the title of the recipe is retrieved by accessing the
contents of the webpage's 'title' tag. In order to find the ingredients, the webpage is searched for a 'div' tag with a class
containing the term 'ingredients'. If one is found, all items within any lists inside that 'div' are found, and the contents of
those items are appended to a string, broken up by end lines. A string rather than a list was used to compile the ingredients so
that the ingredients would be properly displayed when viewing the recipe based on the logic used by the view page. Lastly, the
instructions are assembled using a similar means as the ingredients, but by first searching the webpage for a 'div' tag with a class
containing any of the terms 'instructions', 'directions', 'method', and 'steps'. These search terms were chosen by reviewing the
HTML of FoodNetwork.com.

Because recipe websites do not display recipes in the same formats, Cookbook may not be able to find the ingredients or
instructions for a given URL. In this situation, the form indicates to the user that one or both could not be found, and the user
must enter the data manually.

When the user clicks the 'Get Recipe' button on the 'Add Recipe' form after entering a URL, the data is passed to the client in JSON
format which then auto-populates the form.

In addition to adding recipes, Cookbook can also generate a shopping list for the user based on recipes they select. The
ingredients for each recipe are retrieved from the database using a SQL query, and are then concatenated into one list. Any empty
lines are removed to display the items as one cohesive list.
