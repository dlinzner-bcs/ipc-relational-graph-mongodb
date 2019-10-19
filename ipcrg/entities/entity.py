"""Representation of an entity."""
import copy
from jsonschema import validate
from ..knowledge_unit import KnowledgeUnit

ENTITY_SCHEMA = {
    'type': 'object',
    'properties':
        {
            'name': {
                'type': 'string'
            },
            'entity_type': {
                'type': 'string'
            },
        },
    'required': ['name', 'entity_type']
}


class Entity(KnowledgeUnit):
    """Basic entity."""

    def __init__(self, name, entity_type, **kwargs):
        """Initialize the basic entity."""
        self.name = name
        self.entity_type = entity_type
        parameters = copy.deepcopy(kwargs)
        parameters['name'] = self.name
        parameters['entity_type'] = self.entity_type
        validate(parameters, schema=ENTITY_SCHEMA)
        super().__init__(**parameters)
