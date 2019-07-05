# coding=utf-8
#Código escrito em colaboração por Leonardo Izaú e Mariana Fortes.

import struct
import hashlib
import os

def h(key, hashSize):
    return int(hashlib.sha1(key).hexdigest(),16)%hashSize
	
def criaIndice(qtd, indexName):
    fileName = "bolsa.csv"
    indexFormat = "14sLL"
    keyColumnIndex = 7
    indexStruct = struct.Struct(indexFormat)
    hashSize = qtd + (qtd/2)
    fi = open(indexName,"wb")
    emptyIndexRecord = indexStruct.pack("",0,0)
    for i in range(0,hashSize):
        fi.write(emptyIndexRecord)
    fi.close()

    f = open(fileName,'r')
    fi = open(indexName,"r+b")
    fi.seek(0,os.SEEK_END)
    fileIndexSize = fi.tell()
    print ("IndexFileSize", fileIndexSize)
    list_of_lines = f.read().splitlines()
    recordNumber = 0
    for j in range(1, qtd):
        record = list_of_lines[j].split('\t')
        if record == "": # EOF
            break
        p = h(record[keyColumnIndex], hashSize)
        fi.seek(p*indexStruct.size,os.SEEK_SET)
        indexRecord = indexStruct.unpack(fi.read(indexStruct.size))
        fi.seek(p*indexStruct.size,os.SEEK_SET)
        if indexRecord[0][0] == "\0":
            fi.write(indexStruct.pack(record[keyColumnIndex],j,0))
        else:
            nextPointer = indexRecord[2]
            fi.write(indexStruct.pack(indexRecord[0],indexRecord[1],fileIndexSize))
            fi.seek(0,os.SEEK_END)
            fi.write(indexStruct.pack(record[keyColumnIndex],j,nextPointer))
            fileIndexSize = fi.tell()
    f.close()
    fi.close()
	
for x in range(1, 8):
    qtdChaves = 10 ** x
    indexName = "bolsa" + str(qtdChaves) + "-hash.dat"
    criaIndice(qtdChaves, indexName)	