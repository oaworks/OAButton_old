from django.db import models

try:
    import simplejson as json
except:
    import json

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    # TODO: we can use geo-django later if we move to pgsql, just get
    # this up and running for now
    coords_lat = models.DecimalField(max_digits=19, decimal_places=10)
    coords_lng = models.DecimalField(max_digits=19, decimal_places=10)

    def set_coords(self, coords):
        """Expect a comma separated string of float """
        self.coords_lat, self.coords_lng = coords['lat'], coords['lng']

    def get_coords(self):
        """Return a comma separated string of floats"""
        return {'lat': str(self.coords_lat), 'lng': str(self.coords_lng)}

    coords = property(get_coords, set_coords)

    accessed = models.DateTimeField(auto_now=True)

    pub_date = models.DateTimeField(auto_now=True)

    doi = models.CharField(max_length=255)
    url = models.URLField()
    story = models.TextField()
    email = models.EmailField()

    def from_json(self, jdata):
        data = json.loads(jdata)

        self.id = data['id']
        self.name = data['name']
        self.profession = data['profession']
        self.location = data['location']
        self.coords = data['coords']
        self.accessed = data['accessed']
        self.pub_date = data['pub_date']
        self.doi = data['doi']
        self.url = data['url']
        self.story = data['story']
        self.email = data['email']

    def to_dict(self):
        doc = {'id': self.id,
               'name': self.name,
               'profession': self.profession,
               'location': self.location,
               'coords': self.coords,
               'accessed': self.accessed,
               'pub_date': self.pub_date,
               'doi': self.doi,
               'url': self.url,
               'story': self.story,
               'email': self.email, }
        return doc
