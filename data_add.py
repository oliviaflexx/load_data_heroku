import csv

genres = {
    'breakfast': 1,
    'vegeterian': 2,
    'vegan': 3,
    'dessert': 4,
    'gluten free': 5
}
# make a dictionary to store pk values of genres
genres_dict = {}
with open('genres.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    old_row = 'breakfast'
    for row in csv_reader:
        recipe = row['recipe_name']
        if recipe in genres_dict:
            genres_dict[recipe].append(genres[row['genre']])
        else:
            genres_dict[recipe] = [genres[row['genre']]]

# make a dictionary to store pk values of ingredients
ingredient_dict = {}
with open('names.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        ingredient = row['ingredient']
        ingredient_dict[ingredient] = row['id']

# make a dictionary to store pk values of recipes
recipe_dict = {}
with open('recipes3.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        recipe = row['name']
        recipe_dict[recipe] = {'id': row['id'], 'time': row['time'], 'url': row['url'], 'image': row['image'], 'calories': row['calories']}

recipe_ing_dict = {}
with open('recipe_ingredients.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        recipe = row['name']
        if recipe in recipe_ing_dict:
            recipe_ing_dict[recipe].append({'ingredient': row['ingredient'], 'amount': row['amount'], 'unit': row['unit']})
        else:
            recipe_ing_dict[recipe] = [{'ingredient': row['ingredient'], 'amount': row['amount'], 'unit': row['unit']}]
    # for key in recipe_ing_dict:
        # for listy in recipe_ing_dict[key]:
            # print(listy['unit'])
        # print(key)

# append recipe_dict for ingredients and genres
for key in recipe_dict:
    ing_list = []
    for listy in recipe_ing_dict[key]:
        ing = listy['ingredient']
        try:
            ing_list.append(ingredient_dict[ing])
        except KeyError:
            print(ing)
    recipe_dict[key]['ingredients'] = ing_list
    try:
        recipe_dict[key]['genre'] = genres_dict[key]
        print(recipe_dict[key]['genre'])
    except KeyError:
        print(key)
    
# or ing dictionary
or_ing_dict = {}
with open('or_ingredients.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        or_ingredient = row['or_name']
        if or_ingredient in or_ing_dict:
            or_ing_dict[or_ingredient].append(row['in_name'])
        else:
            or_ing_dict[or_ingredient] = [row['in_name']]


f = open("data1.json", "w")
f.write('[\n')

for key in genres:
    f.write('\t{\n')
    f.write('\t\t"model": "main.genres3",\n')
    f.write('\t\t"pk": ' + str(genres[key]) + ',\n')
    f.write('\t\t"fields": { "name": ' + '"' + key + '"' + '}\n')
    f.write('\t},\n')

for key in ingredient_dict:
    f.write('\t{\n')
    f.write('\t\t"model": "main.ingredients3",\n')
    f.write('\t\t"pk": ' + str(ingredient_dict[key]) + ',\n')
    try: 
        or_ing_dict[key]
        f.write('\t\t"fields": { "name": ' + '"' + key + '",' + '\n\t\t\t' + '"or_ing": "True"' '\n\t\t}\n')
    except KeyError:
        f.write('\t\t"fields": { "name": ' + '"' + key + '",' + '\n\t\t\t' + '"or_ing": "False"' '\n\t\t}\n')
    f.write('\t},\n')

for key in or_ing_dict:
    or_ing = str(ingredient_dict[key])
    for listy in or_ing_dict[key]:
        in_ing = str(ingredient_dict[listy])
        f.write('\t{\n')
        f.write('\t\t"model": "main.or_ingredients",\n')
        f.write('\t\t"fields": { "or_name": ' + or_ing + ',' + '\n\t\t\t' + '"in_name": ' + in_ing + '\n\t\t}\n')
        f.write('\t},\n')

for key in recipe_ing_dict:
    recipe = str(recipe_dict[key]['id'])
    for listy in recipe_ing_dict[key]:
        try: 
            ingredient = str(ingredient_dict[listy['ingredient']])
            amount = str(listy['amount'])
            unit = str(listy['unit'])
            f.write('\t{\n')
            f.write('\t\t"model": "main.recipe_ingredients3",\n')
            if amount == '':
                f.write('\t\t"fields": { "recipe": ' + recipe + ',' + '\n\t\t\t' + '"ingredient": ' + ingredient +  ',' + '\n\t\t\t' + '"unit": ' + '"' + unit + '"' + '\n\t\t}\n')
            else:
                f.write('\t\t"fields": { "recipe": ' + recipe + ',' + '\n\t\t\t' + '"ingredient": ' + ingredient +  ',' + '\n\t\t\t' + '"amount": ' + amount + ',' + '\n\t\t\t' + '"unit": ' + '"' + unit + '"' + '\n\t\t}\n')
            f.write('\t},\n')
        except KeyError:
            pass

for key in recipe_dict:
    pk = str(recipe_dict[key]['id'])
    name = key.replace('"', '')
    time = str(recipe_dict[key]['time'])
    url = recipe_dict[key]['url']
    image = recipe_dict[key]['image']
    calories = str(recipe_dict[key]['calories'])
    ingredients = str(recipe_dict[key]['ingredients'])
    ingredients = ingredients.replace('\'', '')
    try:
        genre = str(recipe_dict[key]['genre'])
    except KeyError:
        genre = '[]'

    f.write('\t{\n')
    f.write('\t\t"model": "main.recipes3",\n')
    f.write('\t\t"pk": ' + pk + ',\n')
    if time == '':
        f.write('\t\t"fields": { "name": ' + '"' + name + '"' + ',' + '\n\t\t\t' + '"url": ' + '"' + url + '"' + ',' + '\n\t\t\t' + '"image": ' + '"' + image + '"' + ',' + '\n\t\t\t' + '"calories": ' + calories + ',' + '\n\t\t\t' + '"ingredients": ' + ingredients + ',' + '\n\t\t\t' + '"genre": ' + genre + '\n\t\t}\n')
    elif calories == '':
        f.write('\t\t"fields": { "name": ' + '"' + name + '"' + ',' + '\n\t\t\t' + '"time": ' + time +  ',' + '\n\t\t\t' + '"url": ' + '"' + url + '"' + ',' + '\n\t\t\t' + '"image": ' + '"' + image + '"' + ',' + '\n\t\t\t' + '"ingredients": ' + ingredients + ',' + '\n\t\t\t' + '"genre": ' + genre + '\n\t\t}\n')
    else:
        f.write('\t\t"fields": { "name": ' + '"' + name + '"' + ',' + '\n\t\t\t' + '"time": ' + time +  ',' + '\n\t\t\t' + '"url": ' + '"' + url + '"' + ',' + '\n\t\t\t' + '"image": ' + '"' + image + '"' + ',' + '\n\t\t\t' + '"calories": ' + calories + ',' + '\n\t\t\t' + '"ingredients": ' + ingredients + ',' + '\n\t\t\t' + '"genre": ' + genre + '\n\t\t}\n')
    f.write('\t},\n')

f.write(']')
f.close()