"""Representation of a relation."""
from jsonschema import validate
from ..entities.entity import ENTITY_SCHEMA
from ..knowledge_unit import KnowledgeUnit

RELATION_SCHEMA = {
    'type': 'object',
    'properties':
        {
            'source': ENTITY_SCHEMA,
            'target': ENTITY_SCHEMA,
            'relation_type': {
                'type': 'string'
            },
            'weight': {
                'type': 'number'
            },
        },
    'required': ['source', 'target', 'relation_type', 'weight']
}


class Relation(KnowledgeUnit):
    """Basic relation."""

    def __init__(self, source, target, relation_type, weight=1):
        """Initialize the basic relation."""
        self.source = source
        self.target = target
        self.relation_type = relation_type
        self.weight = weight
        parameters = {
            'source': self.source,
            'target': self.target,
            'relation_type': self.relation_type,
            'weight': self.weight
        }
        validate(parameters, schema=RELATION_SCHEMA)
        super().__init__(parameters=parameters)
