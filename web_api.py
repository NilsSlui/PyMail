import cherrypy
import json

class HelloWorld(object):
    @cherrypy.expose
    def index(self, **params):
        return "Hello World!"
        print(params)

def object_to_json(object):
    # converts everything it doesn't know to strings. stackoverflow.com/questions/11875770/
    j = json.dumps([ob.__dict__ for ob in object], indent=4, sort_keys=True, default=str)
    return j

cherrypy.quickstart(HelloWorld())