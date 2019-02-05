#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn.metrics import precision_recall_curve

def evaluate(X_test, y_test, y_pred):

    # Turn the prediction into round numbers
    y_pred = np.round(y_pred)
    
    recall_leave = recall_score(y_test, y_pred, pos_label = 1)
    precision_leave = precision_score(y_test, y_pred,\
    pos_label = 1)

    recall_stay = recall_score(y_test, y_pred, pos_label = 0)
    precision_stay = precision_score(y_test, y_pred,\
    pos_label = 0)

    print("Recall Leave:", recall_leave)
    print("Precision Leave:", precision_leave)
    print("Recall Stay:", recall_stay)
    print("Precision Stay:", precision_stay)

    precision, recall, tresholds = \
    precision_recall_curve(y_test, y_pred)

    # Print the curves
    plt.figure()
    plt.title("Precision and Recall w.r.t tresholds")
    plt.plot(precision[:-1], tresholds)
    plt.plot(recall[:-1], tresholds)

    plt.show()

    plt.figure()
    plt.title("Precision vs Recall")
    plt.plot(precision, recall)
    plt.show()

def plot_metrics(history):
    # Plot training & validation accuracy values
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()
