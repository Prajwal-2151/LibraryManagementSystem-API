from django.db import models

# Create your models here.
class Author(models.Model):
          a_id = models.AutoField(primary_key=True)
          a_name = models.CharField(max_length=255, blank=True, null=True)
          a_address = models.CharField(max_length=255, blank=True, null=True)
          a_contact = models.CharField(max_length=50, blank=True, null=True)

          class Meta:
                    db_table = 'author'
