from os import listdir
from numpy import asarray

def gs_to_tsv(gssheet):
    pass

def load_local():
    filess=open(listdir("./local_data")[0], 'r')
    txt=filess.read()
    txt=[n.split('\t') for n in txt.split('\n') if len(n) > 0]
    filess.close()
    return asarray(txt)