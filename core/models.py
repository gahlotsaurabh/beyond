from django.db import models


class BaseContent(models.Model):
    """
        Captures BaseContent as created On and modified On and active field.
        common field accessed for the following classes.
    """

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.id
