from collections import defaultdict

from flask import Flask, Response
import requests

from n4j_ami_timeline import N4JAMITimeline


app = Flask(__name__)

@app.route('/item/<bnumber>')
def events_for_bnumber(bnumber):
    resp = Response(events_html(bnumber))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def events_html(bnumber):

    n4j_wrapper = N4JAMITimeline()

    records = n4j_wrapper.find_timeline_events(bnumber)

    results = '<ul>'
    for r in records:
        event = r['event']
        results += f"<li><strong>{event['event_type']} on {event['event_start']}:</strong> <br>&nbsp;&nbsp;{event['full_event']}</li>"

    results += '</ul>'
    return f'<div style="margin-top: 2em">{results}</div>'


@app.route('/')
def hello_world():
    return 'Hello, World!'
