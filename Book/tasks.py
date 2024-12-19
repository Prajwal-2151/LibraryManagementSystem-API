import json
import os
from datetime import datetime
from loguru import logger
from celery import shared_task
from django.conf import settings
from .models import Author, Book, Borrowrecord

@shared_task()
def generate_report():
          logger.info("Starting report generation task...")

          try:
                    # Calculate required data
                    total_authors = Author.objects.count()
                    total_books = Book.objects.count()
                    total_borrowed_books = Borrowrecord.objects.filter(return_date=None).count()
                    logger.info("Data fetched: Total Authors: {}, Total Books: {}, Total Borrowed Books: {}",
                                total_authors, total_books, total_borrowed_books)

                    report_data = {
                              'total_authors': total_authors,
                              'total_books': total_books,
                              'total_borrowed_books': total_borrowed_books,
                              'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    }

                    # Use the REPORTS_DIR from settings
                    reports_dir = settings.REPORTS_DIR

                    # Ensure reports directory exists
                    if not os.path.exists(reports_dir):
                              os.makedirs(reports_dir, exist_ok=True)
                    logger.info(f"Reports directory ensured at: {reports_dir}")

                    # Generate the report file name based on the current date
                    file_path = os.path.join(reports_dir, f'report_{datetime.now().strftime("%Y%m%d")}.json')

                    # Save the report to the file
                    with open(file_path, 'w') as f:
                              json.dump(report_data, f, indent=4)
                    logger.info(f"Report saved successfully at: {file_path}")

                    return f'Report generated successfully at: {file_path}'
          except Exception as e:
                    logger.error("Error during report generation: {}", str(e))
                    raise e
