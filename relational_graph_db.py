from pymongo import MongoClient
import numpy as np

import urllib.parse
import urllib.request
url = 'https://www.uniprot.org/uploadlists/'

def read_csv(file):
    Daten = np.loadtxt(file,dtype=str, delimiter=",")
    (Anz_Zeilen, Anz_Spalten) = Daten.shape
    tmp1 = Daten[:,0]
    tmp2 = Daten[:,1]
    tmp3=list(tmp1)+list(tmp2)		#Concatenate
    all_prots = set(tmp3)
    all_prots = [s.lower() for s in all_prots]
    all_prots = sorted(all_prots)
    return (Daten, all_prots)

def create_protein_node(bucket, prot_name):
#fetch uniprot meta-data
#atm only add ENSEMB_ID
    params = {
    'from': 'ACC + ID',
    'to': 'ENSEMBL_ID',
    'format': 'tab',
    'query': prot_name
    }
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()
    print(response.decode('utf-8'))
#insert into database
    prot = {"Name": prot_name, "ESEMBL_ID": response.decode('utf-8')}
    prots = bucket.proteins
    prot_id = prots.insert_one(prot).inserted_id

    #return print(prot)

def delete_all_proteins(bucket):
    return 0


if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    db = client['interactome-test']
    ppi = db['ppi-test']
    ppi.proteins.delete_many({})

    create_protein_node(ppi, 'P40925')
    print(ppi.proteins.count_documents({}))