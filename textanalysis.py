import sqlite3
from sqlite3 import Error

import matplotlib.pyplot as plt
import numpy as np

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def create_connection(db_file): # creates connection with database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_scores(conn, ordered, number): # selects the scores of all the reviews from the database
    scores = []
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    for score in cur.execute("SELECT score FROM reviews").fetchall(): # SQL command to extract scores
        scores.append(score)

    if ordered == True:
        return sorted(scores)
    else:
        return scores[:number] # only the first 300 reviews so program runs faster

def get_scores(scores, number): # get score frequencies
    freqs = {}
    for score in scores:
        if score in freqs:
            freqs[score] += 1
        else:
            freqs[score] = 1

    sorted_dict = sorted(freqs.items(),key = lambda x:x[1],reverse=True) # sorts frequencies
    x = [v[0] for v in sorted_dict[:number]]
    y = [v[1] for v in sorted_dict[:number]]

    return x, y # returns frequency data

def get_freqs(reviews): # get word frequencies for a review
    freqs_list = []

    for review in reviews:
        freqs = {}

        for word in review:
            if word in freqs:
                freqs[word] += 1
            else:
                freqs[word] = 1

        freqs_list.append(sorted(freqs.items(),key = lambda x:x[1],reverse=True))


    return freqs_list

def get_all_freqs(reviews): # get frequencies of words throughout all reviews
    freqs_list = []
    freqs = {}

    for word in reviews:
        if word in freqs:
            freqs[word] += 1
        else:
            freqs[word] = 1

    freqs = sorted(freqs.items(),key = lambda x:x[1],reverse=True)
    return freqs

def get_freqs_data(freqs_list, index, number): # get frequency data for graph
    freqs = freqs_list[index]

    # sorted_dict = sorted(freqs.items(),key = lambda x:x[1],reverse=True)
    x = [v[0] for v in freqs[:number]]
    y = [v[1] for v in freqs[:number]]

    return x, y

def get_all_freqs_data(freqs_list, number): # get all reviews frequency data for graph
    # sorted_dict = sorted(freqs.items(),key = lambda x:x[1],reverse=True)
    x = [v[0] for v in freqs_list[:number]]
    y = [v[1] for v in freqs_list[:number]]

    return x, y

def clean_text(reviews, number): # clean text (remove punctuation and stopwords)
    cleaned_reviews = []
    stop_words = set(stopwords.words('english')) # stopwords

    for review in reviews[:number]:
        tokens = word_tokenize(review) # splits review into list of words

        tokens = [w.lower() for w in tokens]

        words = [word for word in tokens if word.isalpha()] # removes punctuation
        words = [word for word in words if word not in stop_words] # removes stopwords

        cleaned_reviews.append(words)

    return cleaned_reviews

def select_corpus(conn): # select review content from database
    reviews = []

    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()

    for review in cur.execute("SELECT content FROM content").fetchall(): # SQL command to select text
        reviews.append(review)

    return reviews

def get_all_words(reviews): # get list of all words from all reviews
    all_words = []
    for review in reviews:
        for word in review:
            all_words.append(word)

    return all_words

def scores_graph(x,y): # graph of score frequencies
    plt.bar(x, y, align = 'edge', width = 0.1, edgecolor = 'black', color='cyan')
    x_ticks = np.array([0, 2.5, 5.0, 7.5, 10.0])
    plt.xlim(0, 10.1)
    plt.title("Frequencies of Scores, 0-10")
    plt.xlabel("Score")
    plt.ylabel("Score Frequency")
    plt.xticks(x_ticks, x_ticks)
    plt.tight_layout()
    plt.show()

def freqs_graph(x,y): # graph of word frequencies
    plt.bar(x, y, align = 'edge', width = 0.5, edgecolor = 'black', color='purple')
    plt.title("Frequencies of Words")
    plt.xlabel("Word")
    plt.ylabel("Word Frequency")
    plt.tight_layout()
    plt.show()

def select_genres(conn): # select genre from database
    genres = []
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    for genre in cur.execute("SELECT genre FROM genres").fetchall():
        genres.append(genre)

    return genres

def find_review_length(reviews): # find word length of each review
    review_lengths = []

    for review in reviews:
        review_lengths.append(len(review))

    return review_lengths

def scores_v_review_length_graph(x, y): # scores vs. word length graph
    plt.scatter(x, y, s=1, c='red')
    plt.title("Score vs. Review Length")
    plt.xlabel("Score")
    plt.ylabel("Review Length (# of Words)")
    plt.tight_layout()
    plt.xlim(0, 10.1)
    plt.show()


def main(): # I have commented out each graph so you can switch between graphs
    database = "database.sqlite"
    conn = create_connection(database) # establish connection

    cleaned = clean_text(select_corpus(conn), 500) # clean first 300 reviews

    all_words = get_all_words(cleaned) # get all words from all reviews

    all_freqs = get_all_freqs(all_words) # get word frequencies across all reviews

    individual_freqs_list = get_freqs(cleaned) # get word frequencies for one review

    x, y = get_all_freqs_data(all_freqs, 30) # all word frequencies graph
    freqs_graph(x, y)

    # x, y = get_freqs_data(individual_freqs_list, 1, 15) # word frequencies for one review graph (you can choose which review to graph)
    # freqs_graph(x, y)

    # x, y = get_scores(select_scores(conn, True), 300) # score frequencies graph
    # scores_graph(x, y)

    # x = select_scores(conn, False, 500) # scores vs. review length graph
    # y = find_review_length(cleaned)
    # scores_v_review_length_graph(x, y)
main()
