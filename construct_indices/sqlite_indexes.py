import sqlite3
import gzip
import json
from tqdm import tqdm

def create_db(filename):
    con = sqlite3.connect(filename.replace('.json.gz', '.db'))
    cur = con.cursor()
    cur.execute("CREATE TABLE documents(id CHAR(50), start INT, end INT, PRIMARY KEY (id))")
    
    for k,v in tqdm(json.load(gzip.open(filename, 'rt')).items()):
        cur.execute("INSERT INTO documents VALUES (?, ?, ?);", (k, v['start'], v['end']))

    con.commit()
    cur.close()

if __name__ == '__main__':
    create_db('static/indexes/ms-marco.json.gz')
    create_db('static/indexes/argsme.json.gz')
