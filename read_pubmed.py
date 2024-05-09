import ast
import json
from nltk.tokenize import sent_tokenize
import nltk


# nltk.download('punkt')

import re

def format_function(data):
    # replace citation with <cit> tag
	data = re.sub(r'[[][0-9]+[,0-9/-]*[]]',r' <cit> ',data)
	data = re.sub(r'[[][0-9]+[", ",0-9/-]*[]]',r' <cit> ',data)
    # remove text in brackets
	data = re.sub(r'\([^)]+\)','',data)
	data = re.sub(r'\[.*?\]','',data)
    # replace digits with <dig> tag
	data = re.sub(r'd <dig> ',' <dig> ', data)
	data = re.sub(r'(<dig> )+',' <dig> ', data)
    # remove table and figures
	data = re.sub(r'\ntable \d+.*?\n',r'',data)
	data = re.sub(r'.*\t.*?\n',r'',data)
	data = re.sub(r'\nfigure \d+.*?\n',r'',data)
	data = re.sub(r'[(]figure \g+.*?[)]',r'',data)
	data = re.sub(r'[(]fig. \d+.*?[)]',r'',data)
	data = re.sub(r'[(]fig . \d+.*?[)]',r'',data)
	data = re.sub(r'[(]table \d+.*?[)]',r'',data)
	return data

def text_to_sentences(text):
    print(text)
    return sent_tokenize(text)


with open("train.txt") as infile:
    for idx, line in enumerate(infile):
        # print(ast.literal_eval(line))
        res = json.loads(line)
        for k, v in res.items():
            print("Key:", k)
            if type(v) == list:
                if type(v[0]) == str:
                    print("VList ", text_to_sentences(v[0]))
        if idx > 0:
            break
