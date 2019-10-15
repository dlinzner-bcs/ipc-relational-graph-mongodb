from pymongo import MongoClient
import interface_mongo as im
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    db = client['interactome-test']
    ppi = db['ppi-test']
    im.delete_all_entities(ppi)

    (data, all_prots) = im.read_csv('Interactions.csv')
    id_type='GENENAME'
    im.create_entities(ppi, all_prots,id_type,0)
    rel_type='ppi'
    im.create_rel_source_target(ppi, rel_type, data)

    (dict,A)=im.create_adj_mat(ppi.relations, all_prots)

    plt.matshow(A)
    plt.show()

    np.save('Interactions_adj',A)
    print(len(A))