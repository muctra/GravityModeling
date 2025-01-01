import math


def len_line(doc1, doc2):
    return math.sqrt(((doc1[0] - doc2[0]) ** 2) + ((doc1[1] - doc2[1]) ** 2))


def sum_vectors(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def minus_vectors(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]


def multiply_vectors(v1, num):
    return v1[0] * num, v1[1] * num


def len_vector(v1):
    return math.sqrt((v1[0] ** 2) + (v1[1] ** 2))
