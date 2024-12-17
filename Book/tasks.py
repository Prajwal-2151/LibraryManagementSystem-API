import json
import os
from datetime import datetime

from celery import shared_task

from .models import Author, Book, Borrowrecord

@shared_task()
def generate_report():
          # Calculate required data
          total_authors = Author.objects.count()
          total_books = Book.objects.count()
          total_borrowed_books = Borrowrecord.objects.filter(return_date=None).count()

          # Create report data
          report_data = {
                    'total_authors': total_authors,
                    'total_books': total_books,
                    'total_borrowed_books': total_borrowed_books,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          }

          # Ensure the reports directory exists
          os.makedirs('reports', exist_ok=True)

          # Create a file name with a timestamp
          file_name = f'reports/report_{datetime.now().strftime("%Y%m%d")}.json'
          file_path = os.path.join(file_name)

          # Save the data to a JSON file
          with open(file_path, 'w') as f:
                    json.dump(report_data, f, indent=4)

          return f'Report generated successfully at: {file_path}'
