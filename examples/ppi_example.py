"""Building a relational graph for proteins with MongoDB backend."""
import argparse
import matplotlib.pyplot as plt
from ipcrg.interfaces.mongo import MongoDBInterface
from ipcrg.io import parse_edge_list
from ipcrg.entities.protein import Protein
from ipcrg.relations.relation import Relation

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i', '--filepath', type=str, help='path to the edge list.', required=True
)
parser.add_argument(
    '-m',
    '--mongo_uri',
    type=str,
    default='mongodb://localhost:27017/',
    help='mongo uri.'
)
parser.add_argument(
    '-d',
    '--database_name',
    type=str,
    default='interactome-test',
    help='name of the database.'
)

if __name__ == '__main__':
    # parse arguments
    args = parser.parse_args()
    # start the interface
    interface = MongoDBInterface(
        mongo_uri=args.mongo_uri, database_name=args.database_name
    )
    # NOTE: start clean
    interface.delete_all_entities()
    interface.delete_all_relations()
    # parse edge list an update the graph
    interface.from_edge_list_filepath(args.filepath, Protein, 'ppi')
    # parse proteins
    proteins = [entity['name'] for entity in interface.get_all_entities()]
    # get adjacency
    adjacency = interface.get_adjacency(proteins, 'ppi')
    # look at it
    plt.matshow(adjacency.todense())
    plt.show()
