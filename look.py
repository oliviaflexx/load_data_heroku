
with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/names.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                ingredient = row['ingredient']
                entry = ingredients3(name=ingredient)
                entry.save()

        with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/recipes3.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                recipe_name = row['name']
                time = row['time']
                if time == '':
                    time = 0
                url = row['url'].replace('\'','')
                print(url)
                image = row['image']
                calories = row['calories']
                if calories == '':
                    calories = 0
                recipe = recipes3.objects.create(name=recipe_name,time=time,url=url,image=image,calories=calories)
                recipe.save()

                with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/recipe_ingredients.csv', mode='r') as ing_csv_file:
                    ing_csv_reader = csv.DictReader(ing_csv_file)
                    for ing_row in ing_csv_reader:
                        ing_recipe_name = ing_row['name']
                        ingredient = ing_row['ingredient']
                        amount = ing_row['amount']
                        if not amount:
                            amount = None
                        unit = ing_row['unit']
                        if not unit:
                            unit = None
                        if ing_recipe_name == recipe_name:
                            try:
                                ingredient_query = ingredients3.objects.get(name=ingredient)
                                recipe.ingredients.add(ingredient_query)
                                recipe_ingredients = recipe_ingredients3.objects.create(recipe=recipe, ingredient=ingredient_query, amount=amount, unit=unit)
                                recipe_ingredients.save()
                            except ingredients3.DoesNotExist:
                                print(ingredient)

                with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/genres.csv', mode='r') as genre_csv_file:
                    genre_csv_reader = csv.DictReader(genre_csv_file)
                    for genre_row in genre_csv_reader:
                        genre_recipe_name = genre_row['recipe_name']
                        genre = genre_row['genre']
                        if genre_recipe_name == recipe_name:
                            try:
                                genre_query = genres3.objects.get(name=genre)
                                recipe.genre.add(genre_query)
                            except genres3.DoesNotExist:
                                print(genre_recipe_name)

        with open('/Users/oliviafelix/recipe-2/django_recipe/mysite/main/or_ingredients.csv', mode='r') as or_csv_file:
            or_csv_reader = csv.DictReader(or_csv_file)
            for or_row in or_csv_reader:
                or_name = or_row['or_name']
                or_name = ingredients3.objects.get(name=or_name)
                in_name = or_row['in_name']
                in_name = ingredients3.objects.get(name=in_name)
                entry = or_ingredients.objects.create(or_name=or_name, in_name=in_name)
                entry.save()