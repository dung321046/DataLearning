import random

import rouge
import json
import numpy as np
import os
from tqdm import tqdm
import time
import ipdb
import argparse
import bert_score

apply_avg = True
apply_best = False
evaluator = rouge.Rouge(metrics=['rouge-n', 'rouge-l', 'rouge-w'],
                        max_n=4,
                        limit_length=False,
                        length_limit_type='words',
                        apply_avg=apply_avg,
                        apply_best=apply_best,
                        alpha=0.5,  # Default F1_score
                        weight_factor=1.2,
                        stemming=True)
with open('./data/train.jsonl', 'r') as json_file:
    json_list = list(json_file)
    for json_str in json_list:
        test = json.loads(json_str)
        print("+++ ", len(test['text']))
        print("+-+ ", len(test['summary']))
        n = len(test['text'])
        m = len(test['summary'])
        ans = []
        hypo = ""
        for i in range(n):
            if random.random() < m * 1.0 / n:
                hypo += test['text'][i]
                ans.append(1)
            else:
                ans.append(0)
        score = evaluator.get_scores([hypo], [" ".join(test['summary'])])
        print(score)
        print(bert_score.score(hypo, test['summary']))

# scores = evaluator.get_scores(all_hypothesis, all_references)
