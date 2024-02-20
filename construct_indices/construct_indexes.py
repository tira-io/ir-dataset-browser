#!/usr/bin/env python3
from pathlib import Path
import json
import pandas as pd
import requests
import gzip

DATASET_IDS = ['argsme-touche-2020-task-1-20230209-training']
CORPUS = []
from pathlib import Path
from typing import Dict, NamedTuple, List


def extract_from_file(path: Path, start: int, end: int) -> str:
    """
    Extracts the content of a file between the given start and end byte range.

    :param path: Path to the file
    :param start: Start byte range
    :param end: End byte range
    :return: Content of the file between the given byte range
    """
    with open(path, "rb") as file:
        file.seek(start)
        return file.read(end - start).decode('utf-8').strip()

def extract_from_remote(url: str, start: int, end: int) -> str:
    """
    Extracts the content of a url between the given start and end byte range.

    :param url: URL where the content is to be extracted from
    :param start: Start byte range
    :param end: End byte range
    :return: Content of the file between the given byte range
    """
    return requests.get(url, headers={'Range': f'bytes={start}-{end-1}'}).content.decode('utf-8').strip()

def parse_qrels(path: Path) -> Dict:
    """
    Parses a qrel file and returns a dictionary with the topic id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    :param path: Path to the qrel file
    :return: Dictionary with the topic id as key and the byte range as value
    """
    ret = {}
    current_qrel = None
    covered_qrels = set()

    with open(path, "rb") as file:
        start = file.tell()
        end_position = 0

        for _, line in enumerate(file):
            q = line.decode().split()[0].strip()
            if not q:
                continue

            if current_qrel is None:
                current_qrel = q
            print(q)
            if q != current_qrel and q in covered_qrels:
                raise ValueError(f'Qrel file is not sorted by topic id. Found multiple occurrences of {q}')

            covered_qrels.add(q)

            if q != current_qrel:
                ret[current_qrel] = {'start': start, 'end': end_position}
                current_qrel = q
                start = end_position + 1
            
            end_position = file.tell() -1

        if current_qrel is not None:
            ret[current_qrel] = {'start': start, 'end': file.tell()}

    return ret

def parse_topics(path: Path) -> Dict:
    """
    Parses a topics file and returns a dictionary with the topic id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    :param path: Path to the topics file in jsonl format as used in TIREx
    :return: Dictionary with the topic id as key and the byte range as value
    """
    ret = {}

    with open(path, "rb") as file:
        position = file.tell()

        for _, line in enumerate(file):
            q = json.loads(line.decode())['qid']
            
            if q is None or q in ret:
                raise ValueError(f'Topic contains duplicate or null query ids. Got {q}')

            ret[q] = {'start': position, 'end': file.tell()}
            position = file.tell()

    return ret

def parse_run_details(path: Path) -> Dict:
    """
    Parses a file with run details and returns a dictionary with the datasets and query id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    :param path: Path to the run detals file in jsonl format 
    :return: Dictionary with the dataset and query id as key and the byte range as value
    """
    ret = {}

    with open(path, "rb") as file:
        position = file.tell()

        for _, line in enumerate(file):
            line = json.loads(line.decode())

            if line['dataset'] not in ret:
                ret[line['dataset']] = {}

            if line['qid'] is None or line['qid'] in ret:
                raise ValueError(f'Run details contains duplicate or null document ids. Got {line["qid"]}')

            ret[line['dataset']][line['qid']] = {'start': position, 'end': file.tell()}
            position = file.tell()

    return ret


def parse_compressed_run_details(path: Path) -> Dict:
    """
    Compress a file with run details and returns a dictionary with the datasets and query id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    :param path: Path to the run detals file in jsonl format  that is re-compressed to gzip
    :return: Dictionary with the dataset and query id as key and the byte range as value
    """
    ret = {}
    position = 0

    with open(path.absolute() + '.gz', 'wb') as f_out, open(path, 'r') as f_in:
        for line in f_in:
            compressed = gzip.compress(line.encode('UTF-8'))
            f_out.write(compressed)
            line = json.loads(line)

            ret[line['dataset']][line['qid']] = {'start': position, 'end': position + len(compressed)}

    return ret

def parse_documents(path: Path) -> Dict:
    """
    Parses a documents file and returns a dictionary with the document id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    :param path: Path to the document file in jsonl format as used in TIREx
    :return: Dictionary with the document id as key and the byte range as value
    """
    ret = {}

    with open(path, "rb") as file:
        position = file.tell()

        for _, line in enumerate(file):
            q = json.loads(line.decode())['docno']
            
            if q is None or q in ret:
                raise ValueError(f'Documents contains duplicate or null document ids. Got {q}')

            ret[q] = {'start': position, 'end': file.tell()}
            position = file.tell()

    return ret

def parse_run(path: Path) -> Dict:
    """
    Parses a topics file and returns a dictionary with the topic id as key and the byte range as value.
     
    This method is inspired by indxr, please cite: https://github.com/AmenRa/indxr

    
    :param path: Path to the run file
    :return: Dictionary with the topic id as key and the byte range as value
    """
    ret = {}
    current_query_id = None
    covered_query_ids = set()

    with open(path, "rb") as file:
        start = file.tell()
        end_position = 0

        for _, line in enumerate(file):
            q = line.decode().split()[0].strip()
            if not q:
                continue

            if current_query_id is None:
                current_query_id = q
            print(q)
            if q != current_query_id and q in covered_query_ids:
                raise ValueError(f'Qrel file is not sorted by topic id. Found multiple occurrences of {q}')

            covered_query_ids.add(q)

            if q != current_query_id:
                ret[current_query_id] = {'start': start, 'end': end_position}
                current_query_id = q
                start = end_position + 1
            
            end_position = file.tell() -1

        if current_query_id is not None:
            ret[current_query_id] = {'start': start, 'end': file.tell()}

    return ret

class ArchivedRun(NamedTuple):
    name: str
    url: str
    local_copy: Path


class ArchivedDataset(NamedTuple):
    qrels_url: str
    qrels_local_copy: Path
    topics_url: str
    topics_local_copy: Path
    documents_url: str
    documents_local_copy: Path
    runs: List[ArchivedRun]


def process_archive(archive_dataset: ArchivedDataset):
    qrels_index = parse_qrels(archive_dataset.qrels_local_copy)
    topics_index = parse_topics(archive_dataset.topics_local_copy)
    documents_index = parse_documents(archive_dataset.documents_local_copy)
    runs = {i.name: {'index': parse_run(i.local_copy), 'url': i.url} for i in archive_dataset.runs}
    topics_entrypoint = pd.read_json(archive_dataset.topics_local_copy, lines=True, dtype={'qid': str, 'query': str})
    topics_entrypoint['offset'] = topics_entrypoint['qid'].apply(lambda i: topics_index[i])

    ret = {
        'qrels': {'index': qrels_index, 'url': archive_dataset.qrels_url},
        'topics': {'index': topics_index, 'url': archive_dataset.topics_url},
        'documents': {'index': documents_index, 'url': archive_dataset.documents_url},
        'runs': runs,
        'topics_entrypoint': {'ir_datasets_id': 'argsme/2020-04-01/touche-2020-task-1', 'display_name': 'Touche 2020 Task 1', 'url': archive_dataset.qrels_url, 'topics': [i.to_dict() for _, i in topics_entrypoint.iterrows()]},
    }
    
    return ret

if __name__ == '__main__':
    json.dump(open('documents.jsonl', 'w'), parse_documents('documents.jsonl'))


    #"S90fa8e6e-Adbcb0683": {"start": 40268149, "end": 40268557}
    #"Sc924bc14-A2325b06": {"start": 105587738, "end": 105588285}
    #"S12590484-Acbd7207f": {"start": 416924383, "end": 416925259}
    #"S151e639d-A433b698c": {"start": 682503141, "end": 682504292}

    # curl -H 'Range: bytes=40268149-40268556,105587738-105588284,416924383-416925258,682503141-682504291' 'https://zenodo.org/records/10406396/files/documents.jsonl?download=1'
    #curl -H 'Range: bytes=40268149-40268556,105587738-105588284,416924383-416925258,682503141-682504291' 'https://files.webis.de/data-in-progress/dataset-explorer-in-progress/documents.jsonl'
