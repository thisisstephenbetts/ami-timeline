import json

from n4j_ami_timeline import N4JAMITimeline


n4j = N4JAMITimeline()
n4j.clear_data()

ami_notes = json.load(open('./ami-catalog-notes_2017-12-07.json'))

notes_identifiers = {note['uuid']: {'mms_id': note['mms_id'], 'bnumber': note['bnumber']} for note in ami_notes}

with open('./1-events.ndjson') as reader:

    prev_uuid = None
    seq_id = 0

    for line in reader:
        event = json.loads(line)

        idents = notes_identifiers[event['uuid']]

        if prev_uuid != event['uuid']:
            n4j.create_nypl_item(idents['bnumber'], event['uuid'], idents['mms_id'])

            seq_id = 0
            prev_uuid = event['uuid']

        try:
            n4j.create_event(idents['bnumber'], event, seq_id)
        except Exception as e:
            print(event, e)
            # import pdb; pdb.set_trace()

        seq_id += 1

# clear_data()
# create_nypl_item('b12164540', 'da762390-0b50-0135-7237-0c51b7f7421d', 5230613)
# create_event('da762390-0b50-0135-7237-0c51b7f7421d', 'Acquired', 'This is a description', '2017-12-07', 0)
