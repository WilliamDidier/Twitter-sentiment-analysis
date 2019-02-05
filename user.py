#!/usr/bin/env python3
import pickle
import argparse
import jsonlines
import numpy as np
import matplotlib.pyplot as plt
import collections


def user_sentiment(user_dict):
    user_sentiment = [np.round(np.mean(user["sentiments"])) for \
    user in user_dict.values()]
    return user_sentiment  

def tweet_sentiment(user_dict):
    tweet_sentiment = []
    for user in user_dict.values():
        tweet_sentiment = tweet_sentiment + user["sentiments"]
    return tweet_sentiment

def count_distribution(user_dict):
    plt.hist([user["tweets"] for user in user_dict.values()])
    plt.show()

def insight(user_dict):
    """ returns (user sentiment, tweet sentiment) """
    users_sent = user_sentiment(user_dict)
    tweet_sent = tweet_sentiment(user_dict)
    return np.mean(users_sent), np.mean(tweet_sent)

def collect(args):
    user_dict = collections.defaultdict(dict)
    with jsonlines.open(args.input) as reader:
        for tweet in reader:
            user_id = tweet["user_id"]
            sentiment = tweet["sentiment"]
            if user_id not in user_dict:
                user_dict[user_id]["tweets"] = 1
                user_dict[user_id]["sentiments"] = [sentiment]
            else:
                user_dict[user_id]["tweets"] += 1
                user_dict[user_id]["sentiments"].append(sentiment)
    return user_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input","-i")
    args = parser.parse_args()
    user_dict = collect(args)
    print(insight(user_dict))
    count_distribution()

