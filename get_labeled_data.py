#!/usr/bin/env python3
import argparse
import sys
import jsonlines
import json

simple_keys = ['created_at', 'full_text']

def main(args):
    config_dict = json.load(args.config)
    # Dictionnary storing the text so that 
    # you don't extract two times the same text
    reminder = set()
    with jsonlines.open(args.input) as reader:
        with jsonlines.open(args.output, "w") as writer:
            # Only fetch the wanted hashtags ( specified in the config file ) and label the tweet for (1) or against (0)
            i = 0
            while i < args.limit:
            #for tweet in reader:
                tweet = reader.read()
                if tweet['lang']=='en':
                    my_dict={}
                    for key in simple_keys:
                        my_dict[key]=tweet[key]
                    my_dict['user_id'] = tweet['user']['id']
                    my_dict['hashtags'] = tweet['entities']['hashtags']
                    for hashtag in my_dict['hashtags']:
                        hashtag['text'] = hashtag['text'].lower()
                    my_dict['symbols'] = tweet['entities']['symbols']
                else:
                    continue
                # Here it means tweet has been selected
                # and you can select hashtags
                tweet = my_dict
                for_flag = False
                against_flag = False
                for hashtag in tweet["hashtags"]:
                    # Problem: Some will be labeled both for and
                    # against ? It could be interesting to study
                    # the hashtag coocurence 
                    # of "for" and "against"
                    # chosen hashtags and try to minimize it
                    # for the moment, we just don't choose tweets
                    # that have both in the training set
                    text = hashtag["text"]
                    for informative_for in config_dict["for"]:
                        if text == informative_for:
                            for_flag = True
                    for informative_against in \
                    config_dict["against"]:
                        if text == informative_against:
                            against_flag = True

                # Only select the tweet if it has
                # one type of flag active
                if against_flag ^ for_flag:
                    # Means we are going to choose
                    # this tweet and label it
                    # sentiment = 1 if the tweet supports 
                    # brexit and 0 otherwise
                    sentiment = [1, 0][against_flag]
                    tweet["sentiment"] = sentiment
                    # Check that we have not already chosen it
                    code = hash(tweet["full_text"])
                    if code not in reminder:
                        writer.write(tweet)
                        reminder.add(code)
                        # Increase the count of tweets 
                        # in the training set
                        i += 1
                        if i%10000 == 0:
                            print(i)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input","-i")
    parser.add_argument("--output","-o")
    parser.add_argument("--limit","-l",type=int)
    parser.add_argument("--config", type=argparse.FileType("r"))
    args = parser.parse_args()
    main(args)

