import random

import rouge
import json

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
with open('./data/val.jsonl', 'r') as json_file:
    json_list = list(json_file)
    for json_str in json_list:
        test = json.loads(json_str)
        n = len(test['text'])
        m = len(test['summary'])
        if n < m + 5:
            continue
        else:
            print(n, m)
            print(sum([len(s) for s in test['text']]))
            print(sum([len(s) for s in test['summary']]))
            print(test['section_belong'])
            print(test['section_names'])

        # ans = []
        # hypo = ""
        # for i in range(n):
        #     if random.random() < m * 1.0 / n:
        #         hypo += test['text'][i]
        #         ans.append(1)
        #     else:
        #         ans.append(0)
        # score = evaluator.get_scores([hypo], [" ".join(test['summary'])])
        # print(score)
