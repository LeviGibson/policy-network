import tensorflow as tf
from halfkp import get_halfkp_indeicies
import chess
from chess import Board
import numpy as np
from halfkp import flipPers

def load_params():
    weights, biases = [], []

    model = tf.keras.models.load_model("production/")
    params = model.get_weights()

    for p in params:
        if len(p.shape) == 2:
            weights.append(p)
        else:
            biases.append(p)

    return weights, biases

weights, biases = load_params()

def activation(x):
    x[x < 0] = 0
    return x

def propogate(a):
    global weights, biases
    for w,b in zip(weights,biases):
        a = activation(np.matmul(w.T,a) + b)
    return a

def ipropogate(a):
    global weights, biases
    for w,b in zip(weights,biases):
        a = activation(np.matmul(w.T,a) + b)//64
    return a

indicies = get_halfkp_indeicies(Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
fp = propogate(indicies)


for id, w in enumerate(weights):
    weights[id] = (w*64).astype(int)

for id, b in enumerate(biases):
    biases[id] = (b*64).astype(int)

ip = ipropogate(indicies)

for i in range(len(ip)):
    print(ip[i], fp[i])
