import numpy as np

import urllib.parse
import urllib.request
url = 'https://www.uniprot.org/uploadlists/'


def read_csv(file):
    data = np.loadtxt(file,dtype=str, delimiter=",")
    tmp1 = data[:,0]
    tmp2 = data[:,1]
    tmp3=list(tmp1)+list(tmp2)		#Concatenate
    all_entities = set(tmp3)
    all_entities = [s.upper() for s in all_entities]
    all_entities = sorted(all_entities)
    return (data, all_entities)

def create_entity_node(bucket, entity_name,id_type,arg):
    #fetch uniprot meta-data
    #atm only add ENSEMB_ID
    if arg :
        params = {
        'from': id_type,
        'to': 'ACC',
        'format': 'tab',
        'query': entity_name
        }
        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as f:
            response = f.read()
        s=response.decode('utf-8')
        s=s.replace('From','')
        s=s.replace('To','')
        s=s.replace(entity_name,'')
        slist= s.split('\t')
        res = [i.rstrip() for i in slist]
        res = list(filter(None, res))
    else : res=''
    #insert into database
    entity = {"name": entity_name, "ACC": res}
    entities = bucket
    entity_id = entities.insert_one(entity).inserted_id

    return print(entity)

def delete_all_entities(bucket):
    bucket.delete_many({})

def create_entities(bucket, all_entities,id_type,arg):
    #store multiple entities
    num_prots = len(all_entities)
    counter = 1
    for i in range(counter, num_prots+1):
	    create_entity_node(bucket,all_entities[i-1],id_type,arg)
	    counter += 1

def create_rel_source_target(bucket,rel_type ,data):
    for i in range(0,(data.shape[0])):
        source = data[i,0].upper()
        target = data[i,1].upper()
        relation = {"type": rel_type,"Source": source, "Target": target}
        relations = bucket.relations
        relation_id = relations.insert_one(relation).inserted_id

def q_give_all_targets(bucket, source):
    rels = []
    row_iter = bucket.find({"Source": source})
    for row in row_iter:
        rels.append(row)
    num_names = len(rels)
    target_names = ['']*num_names
    counter = 0
    for rel in rels:
        target_names[counter] = rel['Target']
        counter += 1
    return target_names

def create_adj_mat(bucket,all_entities):
    num_names = len(all_entities)
    dict_names = {v:i for i,v in enumerate(all_entities)}
    adj = np.zeros(shape=(num_names,num_names))
    for i in range(0,num_names):
        node = all_entities[i]
        ind_i = dict_names[node]
        targets = q_give_all_targets(bucket, node)
        for j in targets:
            ind_j = dict_names[j]
            adj[ind_i,ind_j] = 1
    return (dict_names,adj)