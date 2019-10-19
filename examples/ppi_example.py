"""Building a relational graph for proteins with MongoDB backend."""
import argparse
import matplotlib.pyplot as plt
from ipcrg.interfaces.mongo import MongoDBInterface
from ipcrg.io import parse_edge_list
from ipcrg.entities.protein import Protein
from ipcrg.relations.relation import Relation

parser = argparse.ArgumentParser()
parser.add_argument(
    '-i', '--filepath', type=str, help='path to the edge list.',
    required=True
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
    # parse edge list
    df, proteins = parse_edge_list(args.filepath)
    # start the interface
    interface = MongoDBInterface(
        mongo_uri=args.mongo_uri, database_name=args.database_name
    )
    # NOTE: start clean
    interface.delete_all_entities()
    interface.delete_all_relations()
    # construct protein to entity mapping
    protein_to_entity = {
        protein: Protein(name=protein)
        for protein in proteins
    }
    # create them in the relational graph
    interface.create_entities(protein_to_entity.values())
    # construct relations
    relation_type = 'ppi'
    columns = df.columns
    relations = [
        Relation(
            source=protein_to_entity[source_protein],
            target=protein_to_entity[target_protein],
            relation_type=relation_type
        )
        for source_protein, target_protein in zip(df[columns[0]], df[columns[1]])
    ]
    # create them in the relational graph
    interface.create_relations(relations)
    # get adjacency
    adjacency = interface.get_adjacency(proteins, relation_type)
    # look at it
    plt.matshow(adjacency.todense())
    plt.show()
