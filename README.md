My final project is a web application called Cookbook. The application runs from CS50 IDE and uses flask; it can be run by moving
into the "cookbook" directory and executing "flask run". The website opens to a login screen, through which existing users can
access their accounts. New users can register by selecting "Register" in the upper right hand corner.

The home screen that a user sees upon logging in is a list of their saved recipes. Upon selection of a recipe from the list, the
recipe is displayed with all its associated information - the recipe's title, the type of recipe (e.g. appetizer or dessert), a link
to the source of the recipe if applicable, a list of ingredients, and the recipe's instructions. From this screen, the user also has
the options of editing and deleting the recipe. When deleting the recipe, the user will be returned to the home screen and the
recipe will be removed from their recipe list. If the user chooses to edit the recipe, they will see a form filled in with the
recipe's current information, which can then be updated.

In order to add a new recipe, the user can select the "Add Recipe" button from the navigation bar. This selection opens a form with
several input fields. The user can input a recipe manually by directly filling out the Title, Type, Ingredients, and Instructions
fields. However, if the user is saving a recipe from a webpage, they can enter the URL of the webpage in the URL field and select
the Get Recipe button. This button extracts the recipe data from the webpage and auto-fills the fields in the remainder of the form,
with the exception of the Type field, which must be chosen manually by the user. While not all recipe websites are supported by the
auto-fill feature due to differing formats, recipes on the Food Network website are accurately extracted. When the form is
submitted, the recipe is saved to the user's list of saved recipes.

Additionally, the web application has the capability of generating a shopping list. When the user selects "Shopping List" from the
navigation bar, they are brought to a multi-select list of their saved recipes. After selecting any number of recipes on the list
and clicking "Shop," the user is given an interactive list of all ingredients in the selected recipes from which they can track
their shopping.