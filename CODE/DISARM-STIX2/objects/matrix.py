from stix2 import CustomObject, properties, ExternalReference

import objects.marking_definition
from objects import identity, marking_definition


@CustomObject('x-mitre-matrix', [
    ('name', properties.StringProperty(required=True)),
    ('description', properties.StringProperty(required=True)),
    ('tactic_refs', properties.ListProperty(properties.ReferenceProperty(valid_types="SDO"), required=True))
])
class Matrix(object):
    def __init__(self, **kwargs):
        if True:
            pass


def make_disarm_matrix(data, tactics, stix_ids):
    """Creates a Matrix object.

    Args:
        tactics: A list of Tactic objects.

    Returns:

    """
    identity_id = stix_ids["x-mitre-matrix"]["DISARM Framework"]
    description = 'The DISARM V2 Assessments Framework standardizes the descriptions of assessments made by analysts which pertain to suspected adversary operations or campaigns.'
    external_references = [
        {
            "external_id": "DISARM",
            "source_name": "DISARM",
            "url": "https://github.com/DISARMFoundation"
        }
    ]
    name = 'DISARM V2 Assessments Framework'

    tactics_data = data["tactics"].sort_values('rank').values.tolist()

    tactic_refs = []
    for i in tactics_data:
        for t in tactics:
            if i[1] == t.name:
                tactic_refs.append(t.id)


    matrix = Matrix(
        id=identity_id,
        name=name,
        description=description,
        external_references=external_references,
        tactic_refs=tactic_refs,
        allow_custom=True
    )
    return [matrix]
