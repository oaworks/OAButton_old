from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    # TODO: we can use geo-django later if we move to pgsql, just get
    # this up and running for now
    coords_lat = models.DecimalField(max_digits=19, decimal_places=10)
    coords_lng = models.DecimalField(max_digits=19, decimal_places=10)

    last_accessed = models.DateTimeField(auto_now=True)

    pub_date = models.DateTimeField(auto_now=True)

    doi = models.CharField(max_length=255)
    url = models.URLField()
    story = models.TextField()
    email = models.EmailField()
