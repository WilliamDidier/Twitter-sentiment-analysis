#!/usr/bin/env python3
from datetime import datetime, timedelta
import jsonlines
import collections
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import user
import signal
import pdb

def collect(filename):
    """ Collects tweets from the input and turn date into
    date objects and returns a list sorted by tweet date to a
    list of tweets ( with the converted date aside )"""
    tweet_list = []
    with jsonlines.open(filename) as reader:
        for tweet in reader:
            date = tweet["created_at"]
            converted_date = datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
            date = converted_date
            tweet_list.append((date, tweet))
    # The list is suppose to be sorted already but in case it
    # is not, uncomment the line below
    # tweet_list.sort(key=lambda x: x[0])
    # You'd better not try to sort this on huge files though
    return tweet_list

def get_user_dict(tweet_list):
    """ Returns the user_dict associating users to
    the number of tweets they tweeted and the sentiment
    for each tweet """
    user_dict = collections.defaultdict(dict)
    for tweet in tweet_list:
        user_id = tweet["user_id"]
        sentiment = tweet["sentiment"]
        if user_id not in user_dict:
            user_dict[user_id]["tweets"] = 1
            user_dict[user_id]["sentiments"] = [sentiment]
        else:
            user_dict[user_id]["tweets"] += 1
            user_dict[user_id]["sentiments"].append(sentiment)
    return user_dict


def sliding_stats(filename, stride, width):
    """
    Computes and displays sliding statistics 
    of the % of user pro-Leave as a function of the date.
    
    Args:
        filename (str): Input jsonl file with labeled tweets
        
        stride (int): How many days to skip at each step
        
        width(int): How many days to take into account around 
                    the center
    Returns:
        Time serie of dates associated with mean sentiment
    """
    USER_SENTIMENTS = []
    TWEET_SENTIMENTS = []
    TWEET_COUNTS = []
    DATES = []

    dated_tweets = collect(filename)
    start_date = dated_tweets[0][0]
    end_date = dated_tweets[-1][0]
    current_date = start_date
    last_start_index = 0
    while current_date < end_date:
        # Add the date
        DATES.append(current_date)
        tweet_list = []

        # Collect tweets around the date wanted
        index = last_start_index
        while dated_tweets[index][0] < current_date \
        + timedelta(days=width/2):
            # Get the start index
            if dated_tweets[index][0] < current_date\
            - timedelta(days=width/2):
                index += 1
                if index == len(dated_tweets):
                    break
                continue
            if dated_tweets[index][0] == current_date\
            - timedelta(days=width/2):
                last_start_index = index
            tweet_list.append(dated_tweets[index][1])
            index += 1
            if index == len(dated_tweets):
                break

        # Get user dict
        user_dict = get_user_dict(tweet_list)
        user_sent, tweet_sent = user.insight(user_dict)
        USER_SENTIMENTS.append(user_sent)
        TWEET_SENTIMENTS.append(tweet_sent)
        TWEET_COUNTS.append(len(tweet_list))

        # Update the date
        current_date = current_date + timedelta(days=stride)
        print(current_date)

    return DATES, USER_SENTIMENTS, TWEET_SENTIMENTS, TWEET_COUNTS


def main(args):
    dates, user_sentiments, tweet_sentiments, tweet_count = \
    sliding_stats(args.input, args.stride, args.width)

    # Save the data
    d = {"dates":dates, "user_sentiment": user_sentiments, \
    "tweet_sentiment":tweet_sentiments, "n_tweets":tweet_count}
    frame = pd.DataFrame(data=d).to_csv(args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input","-i")
    parser.add_argument("--output","-o")
    parser.add_argument("--stride", type=float, default=3)
    parser.add_argument("--width", type=float, default=5)

    # Break in the debugger in case of interruption
    signal.signal(signal.SIGINT, lambda sig,\
    frame: pdb.Pdb().set_trace(frame))

    args = parser.parse_args()
    main(args)
