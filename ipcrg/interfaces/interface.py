"""Abstract interface definition."""
import numpy as np
from scipy.sparse import coo_matrix
from ..io import parse_edge_list
from ..relations.relation import Relation


class Interface:
    """Abstract definition of a db interface."""

    def __init__(self, **parameters):
        """Initialize the interface."""
        self.parameters = parameters

    def create_entity(self, entity):
        """Create an entity."""
        raise NotImplementedError

    def create_entities(self, entities):
        """Create entities."""
        raise NotImplementedError

    def get_all_entities(self):
        """Get all entities."""
        raise NotImplementedError

    def delete_all_entities(self):
        """Delete all entities."""
        raise NotImplementedError

    def create_relation(self, relation):
        """Create a relation."""
        raise NotImplementedError

    def create_relations(self, relations):
        """Create relations."""
        raise NotImplementedError

    def get_all_relations(self):
        """Get all relations."""
        raise NotImplementedError

    def delete_all_relations(self):
        """Delete all relations."""
        raise NotImplementedError

    def get_entity_out_neighbors(
        self, entity_name, relation_types, weight='weight'
    ):
        """Get outgoing neighbors from an entity."""
        raise NotImplementedError

    def get_entity_in_neighbors(
        self, entity_name, relation_types, weight='weight'
    ):
        """Get incoming neighbors from an entity."""
        raise NotImplementedError

    def get_adjacency(self, entity_names, relation_type, weight='weight'):
        """Get adjacency given relation and entity types."""
        sources, targets, weights = zip(
            *[
                (entity_name, target_entity_name, a_weight)
                for entity_name in entity_names
                for (target_entity_name,
                     a_weight) in self.get_entity_out_neighbors(
                         entity_name, [relation_type], weight=weight
                     )
            ]
        )
        connected_entities = list(set(sources) | set(targets))
        n = len(connected_entities)
        index_to_entity_name = dict(enumerate(connected_entities))
        entity_name_to_index = {
            entity_name: index
            for index, entity_name in index_to_entity_name.items()
        }
        return coo_matrix(
            (
                np.array(weights), (
                    np.array(
                        [
                            entity_name_to_index[entity_name]
                            for entity_name in sources
                        ]
                    ),
                    np.array(
                        [
                            entity_name_to_index[entity_name]
                            for entity_name in targets
                        ]
                    )
                )
            ),
            shape=(n, n)
        )

    def from_edge_list_filepath(self, filepath, entity_class, relation_type):
        """Insert entities and relations from filepath."""
        df, names = parse_edge_list(filepath)
        # construct protein to entity mapping
        name_to_entity = {name: entity_class(name=name) for name in names}
        # create them in the relational graph
        self.create_entities(name_to_entity.values())
        # construct relations
        columns = df.columns
        relations = [
            Relation(
                source=name_to_entity[source_name],
                target=name_to_entity[target_name],
                relation_type=relation_type
            ) for source_name, target_name in
            zip(df[columns[0]], df[columns[1]])
        ]
        # create them in the relational graph
        self.create_relations(relations)
