"""Protein entity."""
import copy
import urllib.parse
import urllib.request
import pandas as pd
from jsonschema import validate
from .entity import Entity

UNIPROT_ID_MAPPING_URL = 'https://www.uniprot.org/uploadlists/'

UNIPROT_ID_MAPPING_PARAMETERS_SCHEMA = {
    'type': 'object',
    'properties':
        {
            'from': {
                'type': 'string'
            },
            'to': {
                'type': 'string'
            },
            'format': {
                'type': 'string',
                'enum': ['tab']
            }
        },
    'required': ['from', 'to', 'format']
}


class Protein(Entity):
    """Protein entity."""

    def __init__(self, name, id_mapping_parameters={}):
        """Initialize the protein entity."""
        parameters = {}
        # TODO: add some logic in case some other info from a DB
        # like UniProt has to be retrieved. For example, we
        # could parse the UniProt protein entry in xml and convert it
        # to a dictionary that can be added to the parameters.
        if id_mapping_parameters:
            validate(
                id_mapping_parameters,
                schema=UNIPROT_ID_MAPPING_PARAMETERS_SCHEMA
            )
            query = copy.deepcopy(id_mapping_parameters)
            query['query'] = name
            data = urllib.parse.urlencode(query).encode('utf-8')
            request = urllib.request.Request(UNIPROT_ID_MAPPING_URL, data)
            with urllib.request.urlopen(request) as fp:
                df = pd.read_csv(fp, sep='\t')
            parameters[query['to']] = df['To'].tolist()
        super().__init__(name=name, entity_type='protein', **parameters)
