#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def main(args):
    df = pd.read_csv(args.input)
    dates, user_sentiments, tweet_sentiments = \
    df["dates"], df["user_sentiment"], df["tweet_sentiment"] 

    # Print figures
    plt.plot(dates, user_sentiments)
    plt.plot(dates, tweet_sentiments)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input","-i")
    args = parser.parse_args()
    main(args)

