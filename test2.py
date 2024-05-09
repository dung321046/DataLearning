import json
import json
import ipdb
import os
from tqdm import tqdm
tar_file_root = './data/'
splits = ['train', 'test', 'val']
file_name = "train.txt"
split = "train"
data_collect = {'train':[], 'test':[], 'val':[]}

with open(file_name, 'r') as of:
    lines = of.readlines()
    for line in lines[:10]:
        item = json.loads(line)
        summary, text, section_belong = [], [], []

        for sent in item['abstract_text']:
            sent_ = sent.replace('<S> ', '').replace(' </S>', '')
            summary.append(sent_)

        for i, section in enumerate(item['sections']):
            for sent in section:
                text.append(sent)
                section_belong.append(i)

        assert len(item['sections']) == len(item['section_names'])

        data_collect[split].append({
            'text': text,
            'summary': summary,
            'section_belong': section_belong,
            'section_names': item['section_names']
        })

for split in splits:
    fname = split + '.jsonl'
    tar_file_path = os.path.join(tar_file_root, fname)
    print(split)
    print(len(data_collect[split]))
    with open(tar_file_path, 'w', encoding='utf-8') as wf:
        for item in data_collect[split]:
            json.dump(item, wf)
            wf.write('\n')