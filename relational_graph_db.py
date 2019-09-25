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
    all_prots = [s.upper() for s in all_prots]
    all_prots = sorted(all_prots)
    return (Daten, all_prots)

def create_protein_node(bucket, prot_name,id_type):
#fetch uniprot meta-data
#atm only add ENSEMB_ID
    params = {
    'from': id_type,
    'to': 'ACC',
    'format': 'tab',
    'query': prot_name
    }
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()
    s=response.decode('utf-8')
    s=s.replace('From','')
    s=s.replace('To','')
    s=s.replace(prot_name,'')
    slist= s.split('\t')
    res = [i.rstrip() for i in slist]
    res = list(filter(None, res))
    print(res)
#insert into database
    prot = {"Name": prot_name, "ACC": res}
    prots = bucket.proteins
    prot_id = prots.insert_one(prot).inserted_id

    #return print(prot)

def delete_all_proteins(bucket):
    return 0

def create_protein_nodes(bucket, all_prots,id_type):
    Anz_Prots = len(all_prots)
    Counter = 1
    for i in range(Counter, Anz_Prots+1):				#2. Element ist in range nicht enthalten (also z.B. list(range(1,3))----> [1,2])
	    create_protein_node(bucket,all_prots[i-1],id_type)
	    Counter += 1

def create_rel_source_target(bucket,rel_type ,data):
    Counter = 1
    for i in range(0,(data.shape[0])):
        source = data[i,0].upper()
        target = data[i,1].upper()
        relation = {"type": rel_type,"Source": source, "Target": target}
        relations = bucket.relations
        relation_id = relations.insert_one(relation).inserted_id
        Counter += 1

if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    db = client['interactome-test']
    ppi = db['ppi-test']
    ppi.proteins.delete_many({})

    (data, all_prots) = read_csv('Interactions.csv')
    id_type='GENENAME'
    print(len(all_prots))
    create_protein_nodes(ppi, all_prots,id_type)

    rel_type='ppi'
    create_rel_source_target(bucket, rel_type, data)
  #  create_protein_node(ppi, 'P40925')
    print(ppi.proteins.count_documents({}))