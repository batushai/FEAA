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


app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Google maps microservice.'

@app.route('/get_map/<q>')
def get_map(q):
    google_link = 'https://www.google.com/maps/embed/v1/place?key=AIzaSyDhUnfHiAuYxvTXZCPI8mhIH6MKDl_iBRQ&q='+q
    iframe = '<iframe width="100%" height="100%" frameborder="0" style="border:0" scrolling="no" style="overflow:hidden;" src="'+google_link+'" allowfullscreen></iframe>'
    return iframe

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
# [END app]
