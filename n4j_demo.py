import ast
import json
import uuid
from neo4j.v1 import GraphDatabase

def clear_data():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run("MATCH (n) DETACH DELETE n")


def create_nypl_item(bnumber, uuid, mms_id):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run(f"CREATE (:NYPLItem {{bnumber: '{bnumber}', uuid: '{uuid}', mms_id: {mms_id}}})")


def create_event(bnumber, type, description, date, sequence=0):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            # import pdb; pdb.set_trace()
            event_uuid = uuid.uuid4()
            tx.run(f"""
                    MATCH (item:NYPLItem {{bnumber: '{bnumber}'}})
                    MERGE (item)-[:EVENTS]->(e:TimelineEvent {{uuid: '{event_uuid}'}})
                    """)
            tx.run(f"""
                    MATCH (event:TimelineEvent {{uuid: '{event_uuid}'}})
                    MERGE (event)-[:OF_TYPE]->(:EventType {{name: '{type}'}})
                    """)
            escaped_desc = description.replace('"', '\\"').replace("'", "\\'")
            tx.run(f"""
                    MATCH (event:TimelineEvent {{uuid: '{event_uuid}'}})
                    MERGE (event)-[:DESCRIPTION]->(:EventDescription {{text: '{escaped_desc}'}})
                    """)
            tx.run(f"""
                    MATCH (event:TimelineEvent {{uuid: '{event_uuid}'}})
                    MERGE (event)-[:OCCURRED]->(:EventDate {{date: '{date}'}})
                    """)
            tx.run(f"""
                    MATCH (event:TimelineEvent {{uuid: '{event_uuid}'}})
                    MERGE (event)-[:SEQUENCE]->(:EventSequence {{ordinality: '{sequence}'}})
                    """)

def print_data(name):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run("MATCH (s:NYPLItem {uuid: 'da762390-0b50-0135-7237-0c51b7f7421d'}) RETURN s"):
                print(record['s'])


ami_notes = json.load(open('./ami-catalog-notes_2017-12-07.json'))

notes_identifiers = {note['uuid']: {'mms_id': note['mms_id'], 'bnumber': note['bnumber']} for note in ami_notes}

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

clear_data()
with open('./events-phase-1.ndjson') as reader:

    prev_uuid = None
    seq_id = 0

    for line in reader:
        event = ast.literal_eval(line)

        if prev_uuid != event['uuid']:
            seq_id = 0
        
        idents = notes_identifiers[event['uuid']]
        create_nypl_item(idents['bnumber'], event['uuid'], idents['mms_id'])

        create_event(idents['bnumber'], event['what'].split(' ')[0], event['what'], event['when'], seq_id)
        seq_id += 1

# clear_data()
# create_nypl_item('b12164540', 'da762390-0b50-0135-7237-0c51b7f7421d', 5230613)
# create_event('da762390-0b50-0135-7237-0c51b7f7421d', 'Acquired', 'This is a description', '2017-12-07', 0)
