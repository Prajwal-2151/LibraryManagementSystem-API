from rest_framework import serializers
from Book.models import Book, Borrowrecord

class BookSerializer(serializers.ModelSerializer):
          class Meta:
                    model = Book
                    fields = '__all__'

          def validate_isbn(self, value):
                    if len(value) != 13 or not value.isdigit():
                              raise serializers.ValidationError("ISBN must be a 13-digit number.")
                    return value

class RecordSerializer(serializers.ModelSerializer):
          class Meta:
                    model = Borrowrecord
                    fields = '__all__'
