from pymongo import MongoClient
import numpy as np

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

#prot_name: string
def create_protein_node(bucket, prot_name):
    prot={"Name": prot_name}
    prots=bucket.proteins
    prot_id = prots.insert_one(prot).inserted_id
    #return print(prot)

def delete_all_proteins(bucket):
    return 0


if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    db = client['interactome-test']
    ppi = db['ppi-test']

    create_protein_node(ppi, 'AGT')
    create_protein_node(ppi, 'TAA')
    print(ppi.proteins.find())