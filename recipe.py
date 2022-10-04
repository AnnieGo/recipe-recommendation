import pandas as pd
import numpy as np
import joblib
import random

# 0 - список признаков, используемых ниже в функциях (=список всех ингредиентов),
cols = pd.read_csv('data/dataset_clean.csv').columns[3:295]


class Forecast:
    """
    Предсказание рейтинга блюда или его класса
    """

    def __init__(self, list_of_ingredients):
        """
        Добавь сюда любые поля и строчки кода, которые тебе покажутся нужными.
        """
        self.list_of_ingredients = list_of_ingredients

    def preprocess(self):
        """
        Этот метод преобразует список ингредиентов в структуры данных,
        которые используются в алгоритмах машинного обучения, чтобы сделать предсказание.
        """

        # 0 - список признаков, используемых в модели (=список всех ингредиентов)
        global cols

        # 1 - создаем датафрейм с нулями
        self.vector = pd.DataFrame(data=np.zeros((1, len(cols))), columns=cols)

        # 2 - на место ингредиентов из списка ставим 1
        for ingredient in self.list_of_ingredients:  # заменяем в датасете 0 на 1 для признаков из списка
            if ingredient in cols:
                self.vector[ingredient] = 1.0
            else:
                print(f'{ingredient} is not found')
        return self.vector

    def predict_rating_category(self):
        """
        Этот метод возращает рейтинговую категорию для списка ингредиентов, используя классификационную модель,
        которая была обучена заранее. Помимо самого рейтинга, метод возвращает также и текст,
        который дает интерпретацию этой категории и дает рекомендации, как в примере выше.
        """

        clf_model = joblib.load('best_clf.joblib')
        rating_cat = clf_model.predict(self.vector)

        if rating_cat == 'bad':
            text = f"This list of ingredients is {rating_cat[0]}. You can cook it, but you probably won't like it"
        elif rating_cat == 'so-so':
            text = f"This list of ingredients is {rating_cat[0]}. Nothing special, it's edible"
        else:
            text = f"This list of ingredients is {rating_cat[0]}. It will be insanely delicious"

        print(rating_cat[0].capitalize(), '. ', text)
        return rating_cat, text


class NutritionFacts:
    """
    Выдает информацию о пищевой ценности ингредиентов.
    """

    def __init__(self, list_of_ingredients):
        """
        Добавь сюда любые поля и строчки кода, которые тебе покажутся нужными.
        """
        self.list_of_ingredients = list_of_ingredients

    def retrieve(self):
        """
        Этот метод получает всю имеющуюся информацию о пищевой ценности из файла с заранее собранной информацией
        по заданным ингредиентам.
        Он возвращает ее в том виде, который вам кажется наиболее удобным и подходящим.
        """
        nutrients = pd.read_csv('data/daily_norms.csv')
        nutrients = nutrients.set_index('ingredient')

        self.facts = {}

        for ingredient in self.list_of_ingredients:
            if ingredient in list(nutrients.index):

                nutrients_by_ingredient = (nutrients.loc[ingredient].sort_values(ascending=False))\
                                         .round(2) * 100  # таблица с нутриентами по 1 ингредиенту
                self.facts[ingredient] = nutrients_by_ingredient

            else:
                self.list_of_ingredients.remove(ingredient)
                # print(f'{ingredient} is not found')

        return self.facts

    def filter(self, n):
        """
        Этот метод отбирает из всей информации о пищевой ценности только те нутриенты, которые были заданы
        в must_nutrients (пример в PDF-файле ниже),
        а также топ-n нутриентов с наибольшим значением дневной нормы потребления для заданного ингредиента.
        Он возвращает текст, отформатированный как в примере выше.
        """

        text_with_facts = []
        global cols

        for i in self.list_of_ingredients:
            if i not in cols:
                self.list_of_ingredients.remove(i)

        dict_res = {}
        for ingredient in self.list_of_ingredients:
            try:
                print(ingredient.capitalize())
                res = self.facts[ingredient].head(n)

                dict_res[ingredient] = res
                res2 = pd.DataFrame(dict_res)
                for i, row in res2.iterrows():
                    text_with_fact = f'{i} – {row[0]:.0f}% of Daily Value'
                    text_with_facts.append(text_with_fact)
                    print(text_with_fact)
                print('')
                dict_res = {}

            except:
                print(f'No information about {ingredient} is found')
                print('')
                pass

        return text_with_facts


class SimilarRecipes:
    """
    Рекомендация похожих рецептов с дополнительной информацией
    """

    def __init__(self, list_of_ingredients):
        """
        Добавь сюда любые поля и строчки кода, которые тебе покажутся нужными.
        """
        self.list_of_ingredients = list_of_ingredients

    def find_all(self):
        """
        Этот метод возвращает список индексов рецептов, которые содержат заданный список ингредиентов.
        Если нет ни одного рецепта, содержащего все эти ингредиенты, то сделайте обработку ошибки, чтобы программа
        не ломалась.
        """

        df = pd.read_csv('data/dataset_clean.csv')
        df.drop('Unnamed: 0', axis=1, inplace=True)

        for i in self.list_of_ingredients:
            if i not in list(df.columns):
                self.list_of_ingredients.remove(i)  # если ингредиента нет в списке, то он удаляется из списка
                print(f'Try another ingredient, {i} is not found')

        df['sum_in'] = df[self.list_of_ingredients].sum(axis=1)
        self.res = df[df['sum_in'] >= len(self.list_of_ingredients)]
        self.indexes = list(self.res['title'])

        return self.indexes

    def top_similar(self, n=3):
        """
        Этот метод возвращает текст, форматированный как в примере выше: с заголовком, рейтингом и URL.
        Чтобы это сделать, он вначале находит топ-n наиболее похожих рецептов с точки зрения количества дополнительных
        ингредиентов,
        которые потребуются в этих рецептах. Наиболее похожим будет тот, в котором не требуется никаких других
        ингредиентов.
        Далее идет тот, у которого появляется 1 доп. ингредиент. Далее – 2.
        Если рецепт нуждается в более, чем 5 доп. ингредиентах, то такой рецепт не выводится.
        """

        recipes = pd.read_csv('data/recipes_info.csv')  # файл содержит информацию title, rating, url
        recipes.drop('Unnamed: 0', axis=1, inplace=True)

        global cols

        self.res['sum_all'] = self.res[cols].sum(axis=1)  # просуммировали все ингредиенты
        self.res['sum_add'] = self.res.sum_all - self.res.sum_in  # получили кол-во доп.игредиентов

        res2 = self.res.sort_values(by='sum_add')  # отсортировали по кол-ву доп ингредиентов по возврастанию
        res2 = res2[res2['sum_add'] <= 5]  # отсекли рецепты с более чем 5 доп. ингредиентами
        res_5i = res2[res2['sum_add'] > 5]  # рецепты с более чем 5 доп.ингредиентами
        res2 = res2.head(n)  # оставили топ-3 по заданию

        res3 = res2.merge(recipes, how='inner')  # подтянули информацию о рейтинге и url
        res3.drop(cols, axis=1, inplace=True, errors='ignore')
        res3.drop(['sum_in', 'sum_all', 'sum_add', 'Unnamed: 0'], axis=1, inplace=True, errors='ignore')
        res3.drop_duplicates(subset='title', inplace=True)

        text_with_recipes = []

        for i, row in res3.iterrows():
            text_with_recipe = f"- {row['title']}, рейтинг: {row['rating']}, URL: {row['url']}"
            print(text_with_recipe)
            text_with_recipes.append(text_with_recipe)
        if len(self.indexes) == 0:
            print('There is no recipes with such ingredients')
        if len(res_5i) != 0:
            print('There are recipes in our cookbook that require more than 5 additional ingredients')
        return text_with_recipes

    @staticmethod
    def daily_menu():

        print('Breakfast')
        print('------------------------------')
        breakfast_selected = pd.read_csv('data/breakfast.csv')
        res = breakfast_selected.loc[random.choice(list(breakfast_selected.index))]  # выбор случайного рецепта
        print(f'{res[1]} (rating: {res[2]} )')
        print('')
        print('Ingredients: ')
        ingredients = res[7:298].astype('float').sort_values(ascending=False)
        ingredients = ingredients.loc[lambda x: x == 1.0]

        for i in list(ingredients.index):
            print(f'- {i}')
        print('')
        print('Nutrients:')
        print(f'- calories: {res[3]}%')
        print(f'- protein: {res[4]}%')
        print(f'- fat: {res[5]}%')
        print(f'- sodium: {res[6]}%')
        print('')
        print(f'URL: {res[-1]}')
        print('')

        print('Lunch')
        print('------------------------------')
        lunch_selected = pd.read_csv('data/lunch.csv')
        res = lunch_selected.loc[random.choice(list(lunch_selected.index))]  # выбор случайного рецепта
        print(f'{res[1]} (rating: {res[2]} )')
        print('')
        print('Ingredients: ')
        ingredients = res[7:298].astype('float').sort_values(ascending=False)
        ingredients = ingredients.loc[lambda x: x == 1.0]

        for i in list(ingredients.index):
            print(f'- {i}')
        print('')
        print('Nutrients:')
        print(f'- calories: {res[3]}%')
        print(f'- protein: {res[4]}%')
        print(f'- fat: {res[5]}%')
        print(f'- sodium: {res[6]}%')
        print('')
        print(f'URL: {res[-1]}')
        print('')

        print('Dinner')
        print('------------------------------')
        dinner_selected = pd.read_csv('data/dinner.csv')
        res = dinner_selected.loc[random.choice(list(dinner_selected.index))]  # выбор случайного рецепта
        print(f'{res[1]} (rating: {res[2]} )')
        print('')
        print('Ingredients: ')
        ingredients = res[7:298].astype('float').sort_values(ascending=False)
        ingredients = ingredients.loc[lambda x: x == 1.0]

        for i in list(ingredients.index):
            print(f'- {i}')
        print('')
        print('Nutrients:')
        print(f'- calories: {res[3]}%')
        print(f'- protein: {res[4]}%')
        print(f'- fat: {res[5]}%')
        print(f'- sodium: {res[6]}%')
        print('')
        print(f'URL: {res[-1]}')
        print('')
