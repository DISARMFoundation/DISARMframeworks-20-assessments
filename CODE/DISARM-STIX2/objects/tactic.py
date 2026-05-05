from stix2 import CustomObject, properties, ExternalReference

import objects.marking_definition
from objects import identity, marking_definition

valid_tactics = ["plan-strategy", "plan-objectives", "microtarget", "develop-content",
                 "select-channels-and-affordances", "deliver-content",
                 "drive-offline-activity", "persist-in-the-information-environment", "assess-effectiveness",
                 "target-audience-analysis", "develop-narratives", "establish-assets", "establish-legitimacy",
                 "maximise-exposure", "drive-online-harms"]

@CustomObject('x-mitre-tactic', [
    ('name', properties.StringProperty(required=True)),
    ('description', properties.StringProperty(required=True)),
    ('x_mitre_shortname', properties.StringProperty(required=True)),
    ('external_references', properties.ListProperty(ExternalReference))
])
class Tactic(object):
    def __init__(self, x_mitre_shortname=None, **kwargs):
        if x_mitre_shortname and x_mitre_shortname not in valid_tactics:
            pass
#            raise ValueError("'%s' is not a recognized DISARM Tactic." % x_mitre_shortname)


def find_tactic_id(stix_ids, name):
    for tactic_name, tactic_id in stix_ids["x-mitre-tactic"].items():
        if tactic_name == name:
            return tactic_id


def make_disarm_tactics(data, stix_ids):
    """Create all DISARM tactic objects.

    Args:
        data: The xlsx tactic sheet.

    Returns:
        A list of Tactics.

    """
    tactics = []
    marking_id = stix_ids["marking-definition"]["DISARM Foundation"]
    identity_id = stix_ids["identity"]["DISARM Foundation"]

    for t in data["tactics"].values.tolist():
        external_references = [
            {
                'external_id': f'{t[0]}',
                'source_name': 'DISARM',
                'url': f'https://github.com/DISARMFoundation/DISARMframeworks-20-assessments/blob/main/generated_pages/tactics/{t[0]}.md'
            }
        ]

        tactic_id = find_tactic_id(stix_ids, t[1])

        if tactic_id:
            tactic = Tactic(
                id=tactic_id,
                name=f"{t[1]}",
                description=f"{t[5]}",
                x_mitre_shortname=f'{t[1].lower().replace(" ", "-")}',
                external_references=external_references,
                object_marking_refs=marking_id,
                created_by_ref=identity_id
            )
        else:
            tactic = Tactic(
                name=f"{t[1]}",
                description=f"{t[5]}",
                x_mitre_shortname=f'{t[1].lower().replace(" ", "-")}',
                external_references=external_references,
                object_marking_refs=marking_id,
                created_by_ref=identity_id
            )

        tactics.append(tactic)

    return tactics

