import recipe as r
import argparse
import warnings
warnings.filterwarnings('ignore')


parser = argparse.ArgumentParser(description="Use key --menu for daily menu")
parser.add_argument('--menu', nargs='?', const="bar", default=False)
args = parser.parse_args()

if args.menu:

    # get daily menu
    print('------------------------------')
    print('DAILY MENU')
    print('------------------------------')
    top = r.SimilarRecipes(list_of_ingredients=None)
    top.daily_menu()

else:

    #  input ingredients
    a = input("Введите список ингредиентов через ',': ")
    list_of_ingredients = a.split(",")   # Разбиваем строку по ,
    list_of_ingredients = [x.strip(' ') for x in list_of_ingredients]
    if len(list_of_ingredients) <=1:
        print('Список ингредиентов слишком короткий, добавь ещё')
        a = input("Введите список ингредиентов через ',': ")
        list_of_ingredients = a.split(",")  # Разбиваем строку по ,
        list_of_ingredients = [x.strip(' ') for x in list_of_ingredients]

    #  make forecast
    print('I. OUR FORECAST')
    recipe = r.Forecast(list_of_ingredients)
    recipe.preprocess()
    rating_cat, text = recipe.predict_rating_category()
    print('')

    # info about nutrition
    nutrition = r.NutritionFacts(list_of_ingredients)
    nutrition.retrieve()
    n = int(input("Введите количество нутриентов: "))
    print('II. THE NUTRITIONAL VALUE')
    nutrition.filter(n)
    print('')

    #  get recipes
    top = r.SimilarRecipes(list_of_ingredients)
    top.find_all()
    print('III. TOP-3 SIMILAR RECIPES')
    top.top_similar(3)
    print('')
