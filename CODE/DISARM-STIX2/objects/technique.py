from stix2 import AttackPattern, properties, ExternalReference
import objects.marking_definition
import pandas as pd
from objects import identity, marking_definition


def find_technique_id(stix_ids, t_id):
    for technique_id, stix_technique_id in stix_ids["attack-pattern"].items():
        if technique_id == t_id:
            return stix_technique_id

def make_disarm_techniques(data, stix_ids):
    """Create all DISARM Techniques objects.

    Args:
        data: The xlsx technique sheet.

    Returns:
        A list of Techniques.

    """
    tacdict = pd.Series(data["tactics"].name.values, index=data["tactics"].disarm_id).to_dict()
    techniques = []
    marking_id = stix_ids["marking-definition"]["DISARM Foundation"]
    identity_id = stix_ids["identity"]["DISARM Foundation"]
    seen_technique_ids = set()

    for _, t in data["techniques"].iterrows():
        technique_id_str = f'{t["disarm_id"]}'.strip()

        # Check for duplicates
        if technique_id_str in seen_technique_ids:
            print(f"Warning: Duplicate technique detected: {technique_id_str} - {t['name']}. Skipping.")
            continue

        seen_technique_ids.add(technique_id_str)
        external_references = [
            {
                'external_id': technique_id_str,
                'source_name': 'mitre-attack',
                'url': f'https://github.com/DISARMFoundation/DISARMframeworks-20-assessments/blob/main/generated_pages/techniques/{technique_id_str}.md'
            }
        ]

        tactic_id = t["tactic_id"]
        if pd.isna(tactic_id) or tactic_id not in tacdict:
            print(f"WARNING: technique {technique_id_str} has missing or unrecognised tactic_id '{tactic_id}' - skipping.", flush=True)
            continue

        kill_chain_phases = [
            {
                'phase_name': tacdict[tactic_id].replace(' ', '-').lower(),
                'kill_chain_name': 'mitre-attack'
            }
        ]

        x_mitre_is_subtechnique = "." in technique_id_str

        # MITRE ATT&CK Navigator expect techniques to have at least one of these platforms.
        # Without one, the technique will not render in the Navigator.
        x_mitre_platforms = 'Windows', 'Linux', 'Mac'

        technique_id = find_technique_id(stix_ids, technique_id_str)

        description = f"{t['summary']}" if 'summary' in t.index else ''

        if technique_id:
            technique = AttackPattern(
                id=technique_id,
                name=f"{t['name']}",
                description=description,
                external_references=external_references,
                object_marking_refs=marking_id,
                created_by_ref=identity_id,
                kill_chain_phases=kill_chain_phases,
                custom_properties={
                    'x_mitre_platforms': x_mitre_platforms,
                    'x_mitre_version': "2.1",
                    'x_mitre_is_subtechnique': x_mitre_is_subtechnique
                }
            )
        else:
            technique = AttackPattern(
                name=f"{t['name']}",
                description=description,
                external_references=external_references,
                object_marking_refs=marking_id,
                created_by_ref=identity_id,
                kill_chain_phases=kill_chain_phases,
                custom_properties={
                    'x_mitre_platforms': x_mitre_platforms,
                    'x_mitre_version': "2.1",
                    'x_mitre_is_subtechnique': x_mitre_is_subtechnique
                }
            )

        techniques.append(technique)
    return techniques
