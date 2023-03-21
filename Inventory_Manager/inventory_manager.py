import json
import heapq
from dateutil import parser


def get_sorted_categories(json_input):
    '''
    input is list of json objects
    a new dict is created which has a list of category obj 
    objects, [category: first Object, second Object]

    returns an object consisting of 5 list of items
    where each list contains the 5 most expensive items for a
    given category (e.g. cd, book, or dvd) based on the inventory 
    list input passed to the function.
    '''
    categories = {}
    obj_json_input = json.load(json_input)
    for obj in obj_json_input:
        # determine if category exists, if not create new key
        item = obj['type']
        if (item):
            # check if our new list of objects needs a new key,
            # i.e. check if item exists in our categories list
            if (item in categories):
                categories[item].append(obj)
                #no need for second arg. already inserted obj
                #top_five_items = get_top_five_items_by_price(categories[item], obj)
                top_five_items = get_top_five_items_by_price(
                    categories[item])
                categories[item] = top_five_items
            else:
                categories[item] = []
                categories[item].append(obj)

    return categories

#no need for second arg. already inserted obj
#def get_top_five_items_by_price(list_of_objs, obj_to_insert):

def get_top_five_items_by_price(list_of_objs):
    '''
    input is list of python json objects
    returns a list of top five items by price
    '''
    sorted_items_by_price = heapq.nlargest(
        5, list_of_objs, key=lambda x: x['price'])
    return sorted_items_by_price


def cds_greater_than_sixty_min(json_input):
    '''
    input is list of json objects
    returns a list of cd objs with a total running time longer than 60 minutes
    '''
    obj_json_input = json.load(json_input)
    cds = []

    for obj in obj_json_input:
        item = obj['type']
        if item == 'cd' and obj['tracks']:
            # calculate total running time in cd
            total_time = 0
            for i in obj['tracks']:
                total_time += i['seconds']

            if total_time > 3600:
                cds.append(obj)
    return cds


def authors_with_cds(json_input):
    '''
    input is a list of json objs

    we use a dictionary of authors as hashmap where
    key is an author and value is an array with 2 numbers
    first index represents number of books
    second index represents number of cds

    returns a list of author names who have also released cds
    '''
    # example structure of authors dict:
    # authors{ author_name: 2 books, 1 cd}
    authors = {}
    results = []
    obj_json_input = json.load(json_input)
    for obj in obj_json_input:
        
        if obj['type'] == 'book' and obj['author']:
            author_name = obj['author']
            # check if we encounter a new book_author. If yes,
            # initialize hashmap key's value, increment book_author counter
            if author_name not in authors:
                authors[author_name] = [0, 0]
                authors[author_name][0] += 1

            # increment our book counter
            else:
                authors[author_name][0] += 1
                # check if author_name has a book and cd
                # (value of 1 in each index), append to our results
                #if authors[author_name][0] >= 1 and authors[author_name][1] >= 1:
                    #results.append(author_name)


        if obj['type'] == 'cd' and obj['author']:
            author_name = obj['author']
           # check if we encounter a new cd_author. If yes, initialize hashmap key's value, increment cd_author counter
            if author_name not in authors:
                authors[author_name] = [0, 0]
                authors[author_name][1] += 1

            # increment our cd_author counter
            else:
                authors[author_name][1] += 1
                # check if author_name has a book and cd (value of 1 in each index), append to our results
                #if authors[author_name][0] >= 1 and authors[author_name][1] >= 1:
                    #results.append(author_name)


    for key, value in authors.items():
        if value[0] > 0 and value[1] > 0:
            #print(key)
            results.append(key)


    # print(authors)
    return results


def title_track_chapter_with_year(json_input):
    '''
    input is list of json objs

    Assume we are looking at name in tracks, not seconds 

    returns items that have a title, track, or chapter that contains a year.
    '''

    results = []
    obj_json_input = json.load(json_input)
    for obj in obj_json_input:
        # use 'in' syntax to avoid key error
        if 'title' in obj:
            x = get_year(obj['title'])
            if x == True:
                results.append(obj)
        if 'tracks' in obj:
            for i in obj['tracks']:
                #sec = str(i['seconds'])
                #y = get_year(sec)
                name = i['name']
                x = get_year(name)
                if x == True:
                    results.append(obj)
        if 'chapter' in obj:
            x = get_year(obj['title'])
            if x == True:
                results.append(obj)
    return results


def get_year(string):
    try:
        date = parser.parse(string)
        return True
    except ValueError:
        return False


f = open('data.json', 'r')
q1 = get_sorted_categories(f)
f.close()
json_data = json.dumps(q1, indent=2)
#print(json_data)


f = open('data.json', 'r')
q2 = cds_greater_than_sixty_min(f)
f.close()
json_data = json.dumps(q2, indent=2)
#print(json_data)

f = open('data.json', 'r')
q3 = authors_with_cds(f)
f.close()
json_data = json.dumps(q3, indent=2)
#print(json_data)

f = open('data.json', 'r')
q4 = title_track_chapter_with_year(f)
f.close()
json_data = json.dumps(q4, indent=2)
#print(json_data)
