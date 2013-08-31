from json import JSONEncoder
import datetime
from bson.objectid import ObjectId

class MyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)

