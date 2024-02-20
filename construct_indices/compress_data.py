#!/usr/bin/env python3
import gzip
import os

def compress_file(file_name):
    with open(file_name + '.gz', 'wb') as f_out, open(file_name, 'r') as f_in:
        for line in f_in:
            compressed = gzip.compress(line.encode('UTF-8'))
            print(len(compressed))
            f_out.write(compressed)
    
    #os.remove(file_name)

if __name__ == '__main__':
    for f in ['ui/run-details.jsonl', 'ui/qrel-details.jsonl', 'ui/topic-details.jsonl']:
        compress_file(f)
