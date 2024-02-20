#!/usr/bin/env python3
import gzip
from tqdm import tqdm
import json

def compress_file(file_name):
    with open(file_name + '.gz', 'wb') as f_out, open(file_name, 'r') as f_in:
        for line in tqdm(f_in, f'Compress {file_name}'):
            compressed = gzip.compress(line.encode('UTF-8'))
            f_out.write(compressed)
    
    #os.remove(file_name)

def flatten(file_name : str, dir_name : str):
    with gzip.open(file_name, 'rt') as f:
        for line in tqdm(f, f'Flatten {file_name}'):
            parsed_line = json.loads(line)
            dataset = parsed_line['dataset'].replace('/', '-')
            qid = parsed_line['qid'].replace('/', '-')
            output_file_name = f'{dir_name}/' + file_name.split('/')[1].split('.jsonl')[0] + f'-{dataset}-{qid}.json'
            with open(output_file_name, 'w') as f_out:
                f_out.write(line)

if __name__ == '__main__':
    for f in ['ui/run-details.jsonl', 'ui/qrel-details.jsonl', 'ui/topic-details.jsonl']:
        compress_file(f)
    for f in ['ui/run-details.jsonl.gz', 'ui/qrel-details.jsonl.gz']:
        flatten(f, 'ui/')

