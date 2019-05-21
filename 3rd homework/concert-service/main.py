# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
from flask import Flask
import requests, json

def html(text):
	return '<html><body>'+text+'</body></html>'

def parse_json(data, index):
	title = data['events'][index]['title']
	datetime_local = data['events'][index]['datetime_local']
	addr = data['events'][index]['venue']['name']
	price = str(data['events'][index]['stats']['average_price'])
	return '<tr><td>'+title+'</td><td>'+datetime_local+'</td><td>'+addr+'</td><td>'+price+'</td></tr>'

def create_table(data,n_entries):
	events_table = '<table style="width:100%"><tr><th>Title</th><th>Date</th> <th>Address</th><th>Price</th></tr>'
	for i in range(0,n_entries):
		events_table += parse_json(data,i)
	events_table += '</table>'
	return events_table

app = Flask(__name__)

@app.route('/')
def hello():
	return 'Concert location microservice'

@app.route('/<q>')
def query(q):
    response = requests.get("https://api.seatgeek.com/2/events/",
    params=[("client_id", 'MTY2OTg4MjF8MTU1ODI4NjEzNS4xOA'),("q",q)]
    )
    data = response.json()
    maxnum = data['meta']['total'];
    if(maxnum == 0):
    	return html('<h1>No queries found.</h1>')
    elif(maxnum < 10):
    	return html(create_table(data,maxnum))
    else:
    	return html(create_table(data,10))


@app.route('/photo/<q>')
def photo(q):
    response = requests.get("https://api.seatgeek.com/2/performers/",
    params=[("client_id", 'MTY2OTg4MjF8MTU1ODI4NjEzNS4xOA'),("q",q)]
    )
    data = response.json()
    image_link = data['performers'][0]['image'];
    return html('<img src="' + image_link + '"/>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
# [END app]
