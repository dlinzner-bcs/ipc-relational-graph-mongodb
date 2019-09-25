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

def create_protein_node(bucket, prot_name,id_type,arg):
#fetch uniprot meta-data
#atm only add ENSEMB_ID
    if arg :
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
    else : res=''
#insert into database
    prot = {"Name": prot_name, "ACC": res}
    prots = bucket.proteins
    prot_id = prots.insert_one(prot).inserted_id

    #return print(prot)

def delete_all_proteins(bucket):
    bucket.proteins.delete_many({})

def create_protein_nodes(bucket, all_prots,id_type,arg):
    Anz_Prots = len(all_prots)
    Counter = 1
    for i in range(Counter, Anz_Prots+1):				#2. Element ist in range nicht enthalten (also z.B. list(range(1,3))----> [1,2])
	    create_protein_node(bucket,all_prots[i-1],id_type,arg)
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

def q_give_all_targets(bucket, source):
    rels = []
    row_iter = bucket.find({"Source": source})
    for row in row_iter:
        rels.append(row)
    Anz_Namen = len(rels)
    target_names = ['']*Anz_Namen
    Counter = 0
    for rel in rels:
        target_names[Counter] = rel['Target']
        Counter += 1
    return target_names

def create_adj_mat(bucket,all_prots):
    Anz_Namen = len(all_prots)
    dict_names = {v:i for i,v in enumerate(all_prots)}
    Adj = np.zeros(shape=(Anz_Namen,Anz_Namen))
    for i in range(0,Anz_Namen):
        prot = all_prots[i]
        Ind_i = dict_names[prot]
        targets = q_give_all_targets(bucket, prot)
        for j in targets:
            Ind_j = dict_names[j]
            Adj[Ind_i,Ind_j] = 1
    return (dict_names,Adj)

if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    db = client['interactome-test']
    ppi = db['ppi-test']
    delete_all_proteins(ppi)

    (data, all_prots) = read_csv('Interactions.csv')
    id_type='GENENAME'
    print(len(all_prots))
    create_protein_nodes(ppi, all_prots,id_type,0)
    rel_type='ppi'
    create_rel_source_target(ppi, rel_type, data)
  #  create_protein_node(ppi, 'P40925')
    print(ppi.proteins.count_documents({}))
    print(ppi.relations.find_one())
    print(create_adj_mat(ppi.relations, all_prots))