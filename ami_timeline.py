from collections import defaultdict

from flask import Flask

from n4j_ami_timeline import N4JAMITimeline


app = Flask(__name__)

@app.route('/item/<bnumber>')
def show_user_profile(bnumber):

    n4j_wrapper = N4JAMITimeline()

    records = n4j_wrapper.find_timeline_events(bnumber)

    results = ''
    for r in records:
        event = r['event']
        results += f"{event['event_type']}: {event['event']} ({event['event_start']})<br>"

    return f'data for {bnumber}: <br>{results}'


@app.route('/')
def hello_world():
    return 'Hello, World!'
