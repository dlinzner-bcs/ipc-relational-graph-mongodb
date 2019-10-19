"""MongoDB interface."""
from pymongo import MongoClient
from .interface import Interface


class MongoDBInterface(Interface):
    """Mongo DB interface interface."""

    def __init__(self, mongo_uri, **parameters):
        """Initialize the interface."""
        self.mongo_uri = mongo_uri
        self.client = MongoClient(mongo_uri)
        self.entities_db = 'entities'
        self.relations_db = 'relations'
        super().__init__(**parameters)

    def _create_one(self, knowledge_unit, database_name):
        """Create one object in a database."""
        self.client[database_name].insert_one(knowledge_unit.to_dict())

    def _create_many(self, knowledge_units, database_name):
        """Create many objects in a database."""
        self.client[database_name].insert_many(
            [knowledge_unit.to_dict() for knowledge_unit in knowledge_units]
        )

    def _get_entity_neighbors(
        self,
        entity_name,
        relation_types,
        key_search,
        key_to_return,
        weight='weight'
    ):
        """Get neighbors from an entity using keys."""
        cursor = self.client[self.relations_db].find(
            {
                key_search: entity_name,
                'type': {
                    "$in": relation_types
                }
            }
        )
        return [
            (document[key_to_return], document.get(weight, 1))
            for document in cursor
        ]

    def create_entity(self, entity):
        """Create an entity."""
        self._create_one(entity, self.entities_db)

    def create_entities(self, entities):
        """Create entities."""
        self._create_many(entities, self.entities_db)

    def delete_all_entities(self):
        """Delete all entities."""
        self.client[self.entities_db].delete_many({})

    def create_relation(self, relation):
        """Create a relation."""
        self._create_one(relation, self.relations_db)

    def create_relations(self, relations):
        """Create relations."""
        self._create_many(relations, self.relations_db)

    def delete_all_relations(self):
        """Delete all relations."""
        self.client[self.relations_db].delete_many({})

    def get_entity_out_neighbors(
        self, entity_name, relation_types, weight='weight'
    ):
        """Get outgoing neighbors from an entity."""
        return self._get_entity_neighbors(
            entity_name,
            relation_types,
            key_search='source.name',
            key_to_return='target.name',
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
            key_to_return='source.name',
            weight=weight
        )
