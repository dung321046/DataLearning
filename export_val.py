import json
import json
import ipdb
import os
from tqdm import tqdm

tar_file_root = './data/'
splits = ['train', 'test', 'val']
file_name = "val.txt"
split = "val"
data_collect = {'train': [], 'test': [], 'val': []}

with open(file_name, 'r') as of:
    lines = of.readlines()
    print(len(lines))
    for i, line in enumerate(lines):
        # if i % 10 == 0:
        #     print(i)
        # if i >= 50000:
        #     break
        item = json.loads(line)
        # ipdb.set_trace()
        summary, text, section_belong = [], [], []
        for sent in item['abstract_text']:
            sent_ = sent.replace('<S> ', '').replace(' </S>', '')
            summary.append(sent_)

        for i, section in enumerate(item['sections']):
            for sent in section:
                text.append(sent)
                section_belong.append(i)

        assert len(item['sections']) == len(item['section_names'])
        ori_tokens = sum([len(s) for s in text])
        sum_tokens = sum([len(s) for s in summary])
        if 1.0 * ori_tokens / sum_tokens < 2.0:
            continue
        if 1.0 * ori_tokens / sum_tokens > 20.0:
            continue
        if len(summary) < 3:
            continue
        print(len(text), ori_tokens, "-", len(summary), sum_tokens)
        data_collect[split].append({
            'text': text,
            # 'summary': summary,
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
