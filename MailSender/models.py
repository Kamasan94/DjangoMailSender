from django.db import models

class MailAddress(models.Model):
    address = models.CharField(max_length=320)

    def __str__(self):
        return self.address


