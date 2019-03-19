from django.db import models


class Direction(models.Model):
    direction = models.CharField(max_length=4)	

    def __str__(self):
        return self.direction