#!/usr/bin/env python3
""" Labels new tweets using a trained model and store these 
into a new jsonl file """
import pickle
import argparse
import jsonlines
import numpy as np
from preprocessing import preprocess_tweet

def main(args):
    # Load the tokenizer
    tokenizer = pickle.load(args.tokenizer)
    # Load the model
    model = pickle.load(args.model)
    
    with jsonlines.open(args.input) as reader:
        with jsonlines.open(args.output, "w") as writer:
            i = 0
            while i < args.limit:
                tweet = reader.read()
                # Preprocess the tweet text
                text = preprocess_tweet(tweet)
                # Turn it into an input vector
                vector = tokenizer.transform([text])
                vector = vector.toarray()
                # Feed it into the model
                sentiment = model.predict(vector) 
                # Register the sentiment
                #tweet["sentiment"] = int(np.round(sentiment[0]))
                tweet["sentiment"] = float(sentiment[0])
                # Register the tweet into the writer
                writer.write(tweet)
                i += 1
                if i%500000==0:
                    print(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=argparse.FileType("rb"))
    parser.add_argument("--tokenizer", \
    type=argparse.FileType("rb"))
    parser.add_argument("--limit","-l",type=int)
    parser.add_argument("--input","-i")
    parser.add_argument("--output","-o")
    args = parser.parse_args()
    main(args)
