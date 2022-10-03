# recipe-recommendation
A prototype of a program that recommends recipes according to the ingredients requested by the user, as well as a random daily menu

---------------------------------------------------------------------------------------------

To run the program, just run the python script: python nutricionist.py
Next, the program will ask you to enter the ingredients and the number of nutrients to show.

To get a daily menu with random recipes, use the key "--menu": python nutricionist.py --menu

---------------------------------------------------------------------------------------------
All work is divided into three stages: research (using Jupyter Notebook - recipes.ipynb), development (organization of all elements within a single module containing classes and methods - recipes.py) and work with the program itself (running a Python script - nutricionist. py).

<b> 1. Main program </b>
This program is a Python script (nutritionist.py).

It takes a list of ingredients as input.
It creates a prediction and gives a rating with a score (bad, so-so, great) for a dish that can be prepared based on the list of ingredients passed in - <b> using ML </b>.
It finds and displays information about all the nutrients (protein, fat, sodium, etc.) of foods from the list, as well as their amount as a percentage of the daily intake.
It displays three recipes that use the maximum number of products from the list, with their rating and links where the user can find complete information - <b> using parcing data from Epicurious.com </b>

The program uses a raw dataset from Epicurious prepared by HugoDarwood.

<b>2. Additional part </b>
Additional methods have been added to the classes that will help the script perform a new function: compiling the menu for the day.

The daily menu randomly lists the three recipes that cover the most nutritional needs (% of Daily Nutritional Value) and have the highest overall score.

<b> Tools </b>
1. Python, pandas, numpy, scikit-learn, joblib, requests, BeautifulSoup
2. Matplotlib
3. Jupyter Notebook, Pycharm
