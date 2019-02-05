#!/usr/bin/env python3
""" Trains a multi layer perceptron """
import argparse
import numpy as np
import pickle
import evaluate
import tensorflow as tf
from sklearn.utils import class_weight
from preprocessing import get_doc_list
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from create_tokenizer import StemmedCountVectorizer

def batch_generator(X, y, batch_size):
    """
    Creates the batches of data to feed into Keras
    
    Args:
        X (sparse.csr_matrix): Training data under sparse format
        
        y (sparse.csr_matrix): Training labels
        
        batch_size(int): the size of the batch to create
    
    Returns:
        X of the batch size under np.array (dense) format
    """
    n = X.shape[0]
    n_batches_for_epoch = n//batch_size
    i = 0
    while True:
        index_batch =\
        range(n)[batch_size*i:batch_size*(i+1)]
        X_batch = X[index_batch,:].toarray()
        y_batch = y[index_batch]
        i += 1
        if i%n_batches_for_epoch == 0:
            i = 0
        yield(X_batch,y_batch)

def simple_mlp_model(input_shape):
    # Create the keras model
    model = Sequential()
    model.add(Dropout(0.3, input_shape=(input_shape,)))
    model.add(Dense(100, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(optimizer="adam", \
    loss='binary_crossentropy',\
    metrics=['accuracy'])
    return model

def main(args):
    
    # Load the tokenizer
    tokenizer = pickle.load(args.tokenizer)

    encoded_docs, labels = get_doc_list(args.input, tokenizer)

    batch_size = 128

    model = simple_mlp_model(encoded_docs.shape[1])

    # Split into test/training data
    X_train_val, X_test, y_train_val, y_test = \
    train_test_split(encoded_docs, labels, test_size=0.20)

    # Split into training/validation data
    X_train, X_val, y_train, y_val = \
    train_test_split(X_train_val, y_train_val, test_size=0.10)

    print(model.summary())

    # Assign weights to balance the training

    class_weights = class_weight.\
    compute_class_weight('balanced',\
    np.unique(y_train), y_train)

    # Train
    try:
        history = model.fit_generator(\
        generator=batch_generator(X_train, y_train, batch_size), \
        epochs=10,\
        steps_per_epoch=X_train.shape[0]//batch_size,\
        validation_data=(X_val, y_val),\
        class_weight = class_weights,\
        use_multiprocessing=True, workers=4)
    except KeyboardInterrupt:
        history = False
        pass 
    
    if history:
        evaluate.plot_metrics(history)

    # Compute the error on the test set
    test_loss, test_acc = model.evaluate(X_test, y_test)

    print("Test accuracy:", test_acc)

    # Compute precision and recall
    y_pred = model.predict(X_test)
    evaluate.evaluate(X_test, y_test, y_pred)

    # Save the model
    pickle.dump(model, args.model)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=argparse.FileType("wb"))
    parser.add_argument("--tokenizer", \
    type=argparse.FileType("rb"))
    parser.add_argument("--input","-i")
    args = parser.parse_args()
    main(args)
