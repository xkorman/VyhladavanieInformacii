import json
from itertools import islice
from random import paretovariate
from reviewer import Reviewer
from review import Review
from movie import Movie
import regex as re
import requests # to import stopwords database
import ast
from textblob import TextBlob

from nltk.corpus import sentiwordnet as swn
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

sid = SentimentIntensityAnalyzer()

file = open('data/sample.json', )

# f_10 = open('words_10.txt', 'w+')
with open('words_10.json', 'r') as fp:
    words = json.load(fp)
# f_10 = open('dict_of_words', 'w+')

data = json.load(file)

reviewers = []
list_of_movies = []
list_of_reviews = []

dictionary = {}

stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
stopwords = set(stopwords_list.decode().splitlines())
stopwords.add('movie')
stopwords.add('film')
stopwords.add('the')
stopwords.add('a')
stopwords.add('of')
stopwords.add('to')

temp = set()

for index, item in enumerate(islice(data, 200)):
    temp.add(item['rating'])
    person = Reviewer(item['reviewer'])

    if person not in reviewers:
        person.id = len(reviewers)
        reviewers.append(person)
        person.add_to_list(item['movie'], item['review_id'])
    else:
        person = next(x for x in reviewers if x==person)
        person.add_to_list(item['movie'], item['review_id'])

    review = Review(item['review_id'], item['reviewer'], item['movie'], item['rating'], item['review_summary'],
                    item['review_date'], item['review_detail'], item['helpful'])
    if review not in list_of_reviews:
        review.tokenize()
        review.stopWordsDelete(stopwords) 
        # ANALYZA - DICTIONARY
        # review.analyze(words)
        list_of_reviews.append(review)

    movie = Movie(item['movie'])
    if movie not in list_of_movies:
        movie.rank_it(review.rating)
        movie.reviews.append(review.id)
        list_of_movies.append(movie)
    else:
        movie = next((x for x in list_of_movies if x.name == item['movie']),1)
        movie.rank_it(review.rating)
        movie.reviews.append(review.id)


print(f'{temp}')


# OHODNOTENIE SLOVICOK V DICTIONARY
def evaluate(dictionary):
    for item in dictionary:
        dictionary[item]['sum'] = 0
        dictionary[item]['len'] = 0
        for index in range(11):
            if index in dictionary[item]:
                dictionary[item]['sum'] += dictionary[item][index]*index
                dictionary[item]['len'] += dictionary[item][index]
                # dictionary[item].pop(index)
        dictionary[item]['sum'] = dictionary[item]['sum'] / dictionary[item]['len']

# evaluate(dictionary)

# OHODNOTENIE REVIEW
for review in list_of_reviews:
    sum = 0
    len = 0
    for word in review.summary and review.text:
        if word in words:
            # sum += words[word]['sum'] ODKOMENTOVAT V PRIPADE GENEROVANIA DICTIONARY
            sum += words[word]
            len += 1
    if sum != 0:
        rvwr = next((k for k in reviewers if k.name == review.reviewer))
        temp = next((x for x in list_of_movies if x.name == review.movie), None)

        rvwr.trust = ( 1 - (abs(review.rating - temp.rank) + abs((sum/len) - temp.rank)) / 10) + rvwr.trust
        text = review.tmp2
        sentiment = TextBlob(text).sentiment
        print(f'TF- {rvwr.name} = {rvwr.trust}\n{review.rating} {sum/len} {temp.rank} {temp.reviews} {rvwr.reviews} \n{sid.polarity_scores(text)}\n{sentiment}')
        summ = 0
        lenn = 0
        for word in review.text:
            sentiment = TextBlob(word).sentiment
            summ += (sentiment.polarity*sentiment.subjectivity + 1)*5
            lenn += 1
        print(f'{summ/len}\n\n')
    
#CISTENIE SLOVNIKA
def clear_dict(dictionary):
    for item in dictionary:
        for i in range(11):
            if i in dictionary[item]:
                dictionary[item].pop(i)
        dictionary[item].pop('len')
        dictionary[item] = round(dictionary[item]['sum'], 2)

# clear_dict(dictionary)
# ZAPIS SLOVNIKA
# json.dump(dictionary, f_10)
# f_10.write(f'{dictionary}')


def show_movie(name):
    my_regex = r'(?i).*(' + name + r').*'
    r = re.compile(my_regex)

    matched_movies = [x for x in list_of_movies if r.match(x.name)]
    for i, m in enumerate(matched_movies):
        print(f'{i}. {m}')

    index = int(input('Write index of movie from list above: '))
    print(f'{matched_movies[index]}\nRank: {matched_movies[index].rank}\n')
    main_menu()


def show_reviewer(name):
    print(f'{[x for x in reviewers if x.name == name ]}')
    main_menu()


def show_review(identifier):
    review = [x for x in list_of_reviews if x.id == identifier][0]

    print(f'Movie name: {review.movie}\nName of reviewer:{review.reviewer}\n{review.tmp1}\n\n{review.tmp2}\n\n{review.rating} - {review.likes}')
    main_menu()


def show_top_reviewers():
    reviewers.sort(key=lambda x: x.trust, reverse=True)
    for i in range(20):
        print(f'#{reviewers[i].id} - {reviewers[i].name}\nTRUST: {reviewers[i].trust}\n{reviewers[i].movies}\n{reviewers[i].reviews}\n')
    main_menu()


def show_top_reviews():
    list_of_reviews.sort(key=lambda x: x.likes, reverse=True)
    for i in range(20):
        review = list_of_reviews[i]
        print(f'#{review.id} - {review.reviewer}\n{review.movie}\nRating: {review.rating} |||| Likes: {review.likes}\n')
    main_menu()


def main_menu():
    print(f'==============')
    print(f'1. Search for a movie')
    print(f'2. Searcn for a reviewer')
    print(f'3. Search for a review (id)')
    print(f'4. Top 5 reviewers')
    print(f'5. Top 20 reviews (count of likes)')
    print(f'Write "exit" to close program')
    print(f'==============')
    option = input('Option: ')

    if option == '1':
        name = input('Name of movie: ')
        show_movie(name)
    elif option == '2':
        name = input('Name of a reviewer: ')
        show_reviewer(name)
    elif option == '3':
        name = input('ID of review: ')
        show_review(name)
    elif option == '4':
        show_top_reviewers()
    elif option == '5':
        show_top_reviews()
    elif option == 'exit':
        return False
    else:
        main_menu()

main_menu()

# print(f'\n\n{list_of_reviews[:20]}')
# print(f'\n\n\n{temp}')