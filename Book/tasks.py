import json
import os
from datetime import datetime

from celery import shared_task
from django.conf import settings
from .models import Author, Book, Borrowrecord

import logging

logger = logging.getLogger(__name__)

@shared_task()
def generate_report():
          # Calculate required data
          total_authors = Author.objects.count()
          total_books = Book.objects.count()
          total_borrowed_books = Borrowrecord.objects.filter(return_date=None).count()

          report_data = {
                    'total_authors': total_authors,
                    'total_books': total_books,
                    'total_borrowed_books': total_borrowed_books,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          }

          # Ensure reports directory exists
          reports_dir = os.path.join(settings.BASE_DIR, 'reports')
          os.makedirs(reports_dir, exist_ok=True)

          file_path = os.path.join(reports_dir, f'report_{datetime.now().strftime("%Y%m%d")}.json')

          # Save the report
          with open(file_path, 'w') as f:
                    json.dump(report_data, f, indent=4)

          logger.info(f'Report generated successfully at: {file_path}')
          return f'Report generated successfully at: {file_path}'
