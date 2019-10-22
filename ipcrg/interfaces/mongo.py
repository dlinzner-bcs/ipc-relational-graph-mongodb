"""MongoDB interface."""
from pymongo import MongoClient
from .interface import Interface


class MongoDBInterface(Interface):
    """Mongo DB interface interface."""

    def __init__(self, mongo_uri, database_name, **parameters):
        """Initialize the interface."""
        self.mongo_uri = mongo_uri
        self.client = MongoClient(mongo_uri)
        self.database_name = database_name
        self.entities_collection = 'entities'
        self.relations_collection = 'relations'
        super().__init__(**parameters)

    def _create_one(self, knowledge_unit, collection_name):
        """Create one object in a database."""
        self.client[self.database_name][collection_name].insert_one(
            knowledge_unit.to_dict()
        )

    def _create_many(self, knowledge_units, collection_name):
        """Create many objects in a database."""
        self.client[self.database_name][collection_name].insert_many(
            [knowledge_unit.to_dict() for knowledge_unit in knowledge_units]
        )

    def _get_entity_neighbors(
        self,
        entity_name,
        relation_types,
        key_search,
        name_fn,
        weight='weight'
    ):
        """Get neighbors from an entity using keys."""
        cursor = self.client[self.database_name][
            self.relations_collection].find(
                {
                    key_search: entity_name,
                    'relation_type': {
                        "$in": relation_types
                    }
                }
            )
        return [
            (name_fn(document), document.get(weight, 1)) for document in cursor
        ]

    def create_entity(self, entity):
        """Create an entity."""
        self._create_one(entity, self.entities_collection)

    def create_entities(self, entities):
        """Create entities."""
        self._create_many(entities, self.entities_collection)

    def get_all_entities(self):
        """Get all entities."""
        return self.client[self.database_name][self.entities_collection].find(
            {}
        )

    def delete_all_entities(self):
        """Delete all entities."""
        self.client[self.database_name][self.entities_collection].delete_many(
            {}
        )

    def create_relation(self, relation):
        """Create a relation."""
        self._create_one(relation, self.relations_collection)

    def create_relations(self, relations):
        """Create relations."""
        self._create_many(relations, self.relations_collection)

    def get_all_relations(self):
        """Get all relations."""
        return self.client[self.database_name][self.relations_collection].find(
            {}
        )

    def delete_all_relations(self):
        """Delete all relations."""
        self.client[self.database_name][self.relations_collection].delete_many(
            {}
        )

    def get_entity_out_neighbors(
        self, entity_name, relation_types, weight='weight'
    ):
        """Get outgoing neighbors from an entity."""
        return self._get_entity_neighbors(
            entity_name,
            relation_types,
            key_search='source.name',
            name_fn=lambda document: document['target']['name'],
            weight=weight
        )

    def get_entity_in_neighbors(
        self, entity_name, relation_types, weight='weight'
    ):
        """Get incoming neighbors from an entity."""
        return self._get_entity_neighbors(
            entity_name,
            relation_types,
            key_search='target.name',
            name_fn=lambda document: document['source']['name'],
            weight=weight
        )
