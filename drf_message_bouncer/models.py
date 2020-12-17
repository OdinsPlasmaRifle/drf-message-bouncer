import uuid
from logging import getLogger

from django.db import models, connection


logger = getLogger('django')


class MessageManager(models.Manager):
    def in_range(self, latitude, longitude, radius, results=100):
        unit = 6371 # Distance unit (kms)
        radius = float(radius) / 1000.0 # Distance radius convert m to km
        latitude = float(latitude) # Central point latitude
        longitude = float(longitude) # Central point longitude

        sql = """SELECT id FROM
                    (SELECT id, latitude, longitude, ({unit} * acos(CAST((cos(radians({latitude})) * cos(radians(latitude)) *
                                                     cos(radians(longitude) - radians({longitude})) +
                                                     sin(radians({latitude})) * sin(radians(latitude))) AS DECIMAL)))
                     AS distance
                     FROM drf_message_bouncer_message) AS distances
                 WHERE distance < {radius}
                 ORDER BY distance
                 OFFSET 0
                 LIMIT {results};""".format(unit=unit, latitude=latitude, longitude=longitude, radius=radius, results=results)

        cursor = connection.cursor()
        cursor.execute(sql)
        ids = [row[0] for row in cursor.fetchall()]

        return ids


class Message(models.Model):
    session = models.ForeignKey('drf_message_bouncer.Session', null=True, on_delete=models.SET_NULL)
    message = models.CharField(max_length=250)
    original = models.ForeignKey('self', null=True, related_name='original_children', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, related_name='parent_children', on_delete=models.CASCADE)
    latitude = models.DecimalField(decimal_places=15, max_digits=17)
    longitude = models.DecimalField(decimal_places=15, max_digits=17)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = MessageManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'original'], name='unique_session_original'
            )
        ]


class Session(models.Model):
    identifier = models.UUIDField(
        unique=True,
        db_index=True,
        default=uuid.uuid4
    )
    latitude = models.DecimalField(decimal_places=15, max_digits=17)
    longitude = models.DecimalField(decimal_places=15, max_digits=17)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
