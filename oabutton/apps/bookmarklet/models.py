from django.db import models


class OAEvent(models.Model):
    location = models.CharField(max_length=200, null=True, blank=True)

    coords_lat = models.FloatField()
    coords_lng = models.FloatField()

    def _get_coords(self):
        return {'lat': self.coords_lat, 'lng': self.coords_lng}

    def _set_coords(self, value):
        self.coords_lat = value['lat']
        self.coords_lng = value['lng']

    coords = property(_get_coords, _set_coords)

    accessed = models.DateTimeField()
    doi = models.TextField()
    url = models.URLField(max_length=400)
    story = models.TextField(null=True, blank=True)
    description = models.TextField()

    # This is a lookup to the user object
    user_slug = models.CharField(max_length=40, db_index=True)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=200)
    user_profession = models.CharField(max_length=200)


class OAUser(models.Model):
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(db_index=True, null=False)

    profession = models.CharField(max_length=200)
    mailinglist = models.BooleanField()

    slug = models.CharField(unique=True, max_length=40)

    def get_bookmarklet_url(self):
        # generate a boilerplate URL for each user
        from django.conf import settings
        return "%s/api/bookmarklet/%s.js" % (settings.HOSTNAME, self.slug)

class OASession(models.Model):
    key = models.CharField(max_length=40)
    data = models.TextField()
    expire = models.FloatField()

