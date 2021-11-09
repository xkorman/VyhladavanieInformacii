import regex as re
import functools
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

lemmatizer = WordNetLemmatizer()
stemer = PorterStemmer()

class Review:
    def __init__(self, review_id, reviewer, movie, rating, summary, date, text, likes):
        self.id = review_id
        self.reviewer = reviewer
        self.movie = movie
        if rating == None:
            self.rating = 5
        else:
            self.rating = int(rating)
        self.summary = summary
        self.date = date
        self.text = text
        self.tmp1 = summary
        self.tmp2 = text

        # KOEFICIENT HODNOVERNOSTI
        likes[0] = int(''.join(re.findall(r'[^\W]+', likes[0])))
        likes[1] = int(''.join(re.findall(r'[^\W]+', likes[1])))
        if likes[0] == 0:
            likes[0] += 1
            likes[1] += 1
        if likes[1] == 0:
            likes[0] += 1
            likes[1] += 1
        self.likes = likes[1]/likes[0]
        # KOEFICIENT HODNOVERNOSTI

        self.textRank = 0

    def __str__(self):
        return '%s / %s' % (self.id, self.movie)

    def __repr__(self):
        return '#%s %s' % (self.id, self.movie)

    def tokenize(self):
        if self.movie in self.summary:
            self.summary = self.summary.replace(self.movie, '')
        if self.movie in self.text:
            self.text = self.text.replace(self.movie, '')

        self.summary = re.findall(r'[^\d\W]+', self.summary)
        self.text = re.findall(r'[^\d\W]+', self.text)
        self.summary = [x.lower() for x in self.summary]
        self.text = [x.lower() for x in self.text]
        # sum = 0
        # for word in self.summary:
        #     sentiment = TextBlob(word).sentiment
        #     sum += sentiment.polarity*sentiment.subjectivity
        #     print(f'{sentiment} {word}')
        # print(f'{sum}')

    def stopWordsDelete(self, stopwords):
        if self.summary == [] or self.text == []:
            return
        
        lst = functools.reduce(lambda x,y: x+y, [i.split() for i in self.summary])
        self.summary = [word for word in lst if word not in stopwords]

        lst = functools.reduce(lambda x,y: x+y, [i.split() for i in self.text])
        self.text = [word for word in lst if word not in stopwords]

        for word in self.summary:
            self.summary.remove(word)
            self.summary.append(stemer.stem(lemmatizer.lemmatize(word)))

        for word in self.text:
            self.text.remove(word)
            self.text.append(stemer.stem(lemmatizer.lemmatize(word)))

    # ANALYZA SLOV V TEXTE
    def analyze(self, new_dict):
        # if int(self.rating) == rating:
            for word in self.summary:
                if word in new_dict:
                    if self.rating in new_dict[word]:
                        new_dict[word][self.rating] += 1*self.likes
                    else:
                        new_dict[word][self.rating] = 1*self.likes
                else:
                    new_dict[word] = {}
                    new_dict[word][self.rating] = 1*self.likes

            for word in self.text:
                if word in new_dict:
                    if self.rating in new_dict[word]:
                        new_dict[word][self.rating] += 1*self.likes
                    else:
                        new_dict[word][self.rating] = 1*self.likes
                else:
                    new_dict[word] = {}
                    new_dict[word][self.rating] = 1*self.likes