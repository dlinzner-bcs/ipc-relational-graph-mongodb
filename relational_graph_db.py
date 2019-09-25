from pymongo import MongoClient

def import_prot(sum_of_spins, beta, tau):

    return


if __name__ == '__main__':

    client = MongoClient('mongodb://localhost:27017/')
    db = client['interactome-test']
    collection = db['ppi-test']