# coding=utf-8
#Código escrito em colaboração por Leonardo Izaú e Mariana Fortes.

import struct
import hashlib
import os
import sys
import time

def h(key, hashSize):
    return int(hashlib.sha1(key).hexdigest(),16)%hashSize

def buscaIndice(qtd, indexName, nisProcurado):
    start = time.time()
    fileName = "bolsa.csv"
    indexFormat = "14sLL"
    keyColumnIndex = 7
    indexStruct = struct.Struct(indexFormat)
    hashSize = qtd + (qtd/2)
	
    print "\n"
    print "Numero de chaves no hash: ", qtd 
    fi = open(indexName,"rb")
    f = open(fileName,"rb")
    fi = open(indexName,"r+b")
    p = h(nisProcurado, hashSize)
    list_of_lines = f.read().splitlines()
    offset = p*indexStruct.size
    i = 1
    while True:
        fi.seek(offset,os.SEEK_SET)
        indexRecord = indexStruct.unpack(fi.read(indexStruct.size))
        if indexRecord[0] == nisProcurado:
            print indexRecord[0]
            print indexRecord[1]
            pos = indexRecord[1]
            record = list_of_lines[pos].split('\t')
            for column in record:
                print column
            print "Numero de buscas: ", i
            break
        offset = indexRecord[2]
        if offset == 0:
            break
        i += 1
    fi.close()
    end = time.time()
    tempo = end - start
    print "Tempo: ", tempo

if len(sys.argv) >= 2:
    nisProcurado = sys.argv[1]
else:
    nisProcurado = raw_input("Entre com o NIS: ")
for x in range(1, 8):
    qtdChaves = 10 ** x
    indexName = "bolsa" + str(qtdChaves) + "-hash.dat"
    buscaIndice(qtdChaves, indexName, nisProcurado)	