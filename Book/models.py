import random
from django.db import models
from Author.models import Author

# Create your models here.
class Book(models.Model):
          b_id = models.AutoField(primary_key=True)
          b_title = models.CharField(max_length=255, blank=True, null=True)
          author = models.ForeignKey(Author, models.DO_NOTHING, db_column='author', blank=True, null=True)
          isbn = models.CharField(unique=True, max_length=13, blank=True, null=True)
          available_copies = models.IntegerField(blank=True, null=True)

          class Meta:
                    db_table = 'book'

          def save(self, *args, **kwargs):
                    if not self.isbn:
                              self.isbn = self.generate_isbn()
                    super().save(*args, **kwargs)

          @staticmethod
          def generate_isbn():
                    prefix = "978"  # Standard prefix for books
                    core_digits = ''.join(str(random.randint(0, 9)) for _ in range(9))
                    check_digit = Book.calculate_check_digit(f"{prefix}{core_digits}")
                    return f"{prefix}{core_digits}{check_digit}"

          @staticmethod
          def calculate_check_digit(isbn_without_check):
                    """Calculate the check digit for an ISBN-13."""
                    total = sum(int(digit) * (3 if i % 2 else 1) for i, digit in enumerate(isbn_without_check))
                    check_digit = (10 - (total % 10)) % 10
                    return str(check_digit)

class Borrowrecord(models.Model):
          r_id = models.AutoField(primary_key=True)
          book = models.ForeignKey(Book, models.DO_NOTHING, db_column='Book', blank=True,
                                   null=True)  # Field name made lowercase.
          borrowed_by = models.CharField(max_length=255, blank=True, null=True)
          borrow_date = models.DateField(blank=True, null=True)
          return_date = models.DateField(blank=True, null=True)

          class Meta:
                    db_table = 'borrowrecord'
