from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import cgi
import json

#read the json
#from now on data means the db
with open('db.json') as f:
    data = json.load(f)

#BaseHTTPRequestHandler is a python class that does the com transfer http
#by re-writing do_GET, do_POST, etc., we decide what that action does
class RestHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #self.path always is the current request parameters 
        req_params = urlparse.parse_qs(self.path[2:])
        print("request params")
        print(req_params)
        
        if bool(req_params) == False:
            #params are empty, we GET all the json entries
            self.send_response(200) #OK
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data))
        else:
            #params are not empty, GET the requested id
            #the id param is actually list of ids
            id_list = req_params.get('id');
            #get the first id of the list [0], then convert it to int
            my_id = int(id_list[0])

            #find the id in the json data
            #i = index in json array
            #obj = basically data[i]
            for i, obj in enumerate(data):
                if obj['id'] == my_id :
                    self.send_response(200) #OK
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(obj))
                    return
            #if the for ends and we haven't found the id, we respond with error
            self.send_response(404) #NOT FOUND
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("ID not found.") 
        return
 
    def do_PUT(self):
        
        #First we determine the max id used till now
        last_index = len(data) - 1
        new_id = int(data[last_index]['id']) + 1 ;

        #the request has 2 params, brand and model
        req_params = urlparse.parse_qs(self.path[2:])
        
        if bool(req_params) == False:
            #handling the 0 params case
            #params are empty, we 400
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("Incorrect params.") 
            return
        else:
            #get the params
            brand = req_params.get('brand')
            model = req_params.get('model')
            
            #only continue if they are not empty
            if bool(brand) and bool (model):
                brand = brand[0]
                model = model[0]
                #ready to update db here
                #first we write the json string
                new_guitar = {'id': new_id, 'brand': brand, 'model':model}
                #then we append it to the json object
                data.append(new_guitar)
                #then we write the new json file to disk
                with open('db.json', 'w') as outfile:  
                    json.dump(data, outfile)
                    
                #then we send response with the our entry
                self.send_response(201) #new entry code
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(new_guitar))     
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write("Brand or model param left empty.") 
                return
        return
    
    def do_POST(self):
        #POST updates an entry
        #the request has 3 params, the id to find the entry
        #and brand and model to modify    
        req_params = urlparse.parse_qs(self.path[2:])
        
        if bool(req_params) == False:
            #handling the 0 params case
            #params are empty, we 400
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("Incorrect params.") 
            return
        else:
            #get the params
            my_id = req_params.get('id')
            brand = req_params.get('brand')
            model = req_params.get('model')

            #check if we have the brand param in the req
            #else make it 0 so we know not to update it later
            if bool(brand):
                brand = brand[0]
            else:
                brand = 0
                
            #check if we have the model param
            if bool(model):
                model = model[0]
            else:
                model = 0

                
            #first check that the id is not empty
            if bool(my_id) == False:
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write("Empty id")
                return

            #then find the entry with that id
            my_id = int(my_id[0])

            for i, obj in enumerate(data):
                if obj['id'] == my_id :
                    #found the entry here, ready to update it.
                    if model != 0:
                        data[i]['model'] = model
                    if brand != 0:
                        data[i]['brand'] = brand
                        
                    #then we write the new json file to disk
                    with open('db.json', 'w') as outfile:  
                        json.dump(data, outfile)
                        
                    #then we send response with the our updated entry
                    self.send_response(200) #OK
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(data[i]))              
                    return
            #if the for ends and we haven't found the id, we respond with error
            self.send_response(404) #NOT FOUND
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("ID not found.") 
        return

    def do_DELETE(self):
        #DELETE deletes an entry
        #the request has 1 param, the id to find the entry   
        req_params = urlparse.parse_qs(self.path[2:])
        
        if bool(req_params) == False:
            #handling the 0 params case
            #params are empty, we 400
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("Incorrect params.") 
            return
        else:
            #get the param
            my_id = req_params.get('id')

            #first check that the id is not empty
            if bool(my_id) == False:
                self.send_response(400)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write("Empty id")
                return

            #then find the entry with that id
            my_id = int(my_id[0])
            for i, obj in enumerate(data):
                if obj['id'] == my_id :
                    #found the entry here, ready to delete it.
                    deleted_data = data.pop(i)
                    
                    #then we write the new json file to disk
                    with open('db.json', 'w') as outfile:  
                        json.dump(data, outfile)
                        
                    #then we send response with the our updated entry
                    self.send_response(200) #OK
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(deleted_data))              
                    return
            #if the for ends and we haven't found the id, we respond with error
            self.send_response(404) #NOT FOUND
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write("ID not found.") 
        return
    
httpd = HTTPServer(('127.0.0.1', 8000), RestHTTPRequestHandler)
while True:
    httpd.handle_request()
