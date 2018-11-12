from struct import pack, unpack
import numpy as np


# Generate a one-hot row given a row and the target value
def in_hot(t, row):
    return [int(x == t) for x in row]


# Generate one-hot rows for 2-2048 + 4096 as padding
def in_hots(matrix):
    flat = matrix.reshape((16,)).tolist()
    return [in_hot(pow(2, n), flat) for n in range(1, 13)]


# Convert a one-hot from 16 bits to a 16-bit integer
def bits_to_byte(one_hot):
    return int("0b" + "".join(map(str, one_hot)), 2)


# Convert a matrix into a binary representation
def mat2bin(matrix):
    one_hots = in_hots(matrix)
    packed = [bits_to_byte(one_hot) for one_hot in one_hots]
    return pack('H'*12, *packed)


# Convert binary representation into human-readable format
def bin2human(bin):
    hexstrs = [("%x" % n).upper() for n in unpack('Q'*int(len(bin) / 8), bin)]
    for i, hexstr in enumerate(hexstrs):
        if hexstr == "0":
            hexstrs[i] = ""
    return ":".join(hexstrs)


# Convert a 16-bit integer into a 16 bit one-hot
def byte_to_bits(short):
    btext = "{0:016b}".format(short)
    return [int(b) for b in btext]


# Convert one hots to a matrix
def out_hots(one_hots):
    out_mat = np.zeros((4, 4))
    for n in range(len(one_hots)):
        for y in range(4):
            for x in range(4):
                if one_hots[n][(y*4)+x] == 1:
                    out_mat[y][x] = pow(2, n + 1)
    return out_mat


# Convert a binary board into a matrix
def bin2mat(bin):
    shorts = list(unpack('H' * int(len(bin) / 2), bin))
    while len(shorts) < 12:
        shorts.append(0)
    one_hots = [byte_to_bits(short) for short in shorts]
    return out_hots(one_hots)


# Convert human readable representation into a binary board
def human2bin(human):
    human = list(filter(lambda x: len(x) > 0, human.split(":")))
    tmp = [int(row, 16) for row in human]
    while len(tmp) < 3:
        tmp.append(0)
    return pack('Q'*len(tmp), *tmp)
