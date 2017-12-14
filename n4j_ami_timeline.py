import uuid

from neo4j.v1 import GraphDatabase


class N4JAMITimeline:

    def __init__(self):
        uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

    def clear_data(self):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run("MATCH (n) DETACH DELETE n")

    def create_nypl_item(self, bnumber, uuid, mms_id):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run(f"CREATE (:NYPLItem {{bnumber: '{bnumber}', uuid: '{uuid}', mms_id: {mms_id}}})")

    def create_event(self, bnumber, event, sequence=0):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                try:
                    # if bnumber == 'b12170486':
                    #     import pdb; pdb.set_trace()

                    event_uuid = uuid.uuid4()

                    for property in 'event', 'full_event', 'full_note', 'media':
                        if event[property] is not None:
                            event[property] = event[property].replace('"', '\\"').replace("'", "\\'")

                    tx.run(f"""
                            MATCH (item:NYPLItem {{bnumber: '{bnumber}'}})
                            MERGE (item)-[:EVENTS]->(e:TimelineEvent {{
                                uuid: '{event_uuid}',
                                event_type: '{event['event_type']}',
                                event_start: '{event['event_start']}',
                                event_end: '{event['event_end']}',
                                event: '{event['event']}',
                                full_event: '{event['full_event']}',
                                media: '{event['media']}',
                                full_note: '{event['full_note']}',
                                sequence: '{sequence}'
                            }})
                            """)
                except Exception as e:
                    print(bnumber, event, sequence, e)
                    raise(e)

    def find_timeline_events(self, bnumber):

        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                return tx.run(f"MATCH (item:NYPLItem {{bnumber: '{bnumber}'}})-[:EVENTS]->(event:TimelineEvent) RETURN event order by event.event_start").records()
