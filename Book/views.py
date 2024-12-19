import json
import os
from datetime import date, datetime
from loguru import logger
from django.conf import settings
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Author.models import Author
from Book.models import Book, Borrowrecord
from Book.serializers import BookSerializer, RecordSerializer
from Book.tasks import generate_report

# Create your views here.
class BookAPI(ModelViewSet):
          queryset = Book.objects.all()
          serializer_class = BookSerializer

          def list(self, request, *args, **kwargs):
                    try:
                              book = Book.objects.all()
                              serializer = self.get_serializer(book, many=True)
                              api_response = {
                                        'status': 'success',
                                        'code': status.HTTP_200_OK,
                                        'message': 'All books',
                                        'all_books': serializer.data,
                              }
                              return Response(api_response)
                    except Exception as e:
                              error_message = 'An error occurred while fetching book: {}'.format(str(e))
                    error_response = {
                              'status': 'error',
                              'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                              'message': error_message
                    }
                    return Response(error_response)

          def retrieve(self, request, *args, **kwargs):
                    try:
                              instance = self.get_object()
                              serializer = self.get_serializer(instance)
                              api_response = {
                                        'status': 'success',
                                        'code': status.HTTP_200_OK,
                                        'message': 'Book fetched successfully',
                                        'book_details': serializer.data,
                              }
                              return Response(api_response)
                    except Exception as e:
                              error_message = 'An error occurred while fetching book: {}'.format(str(e))
                              error_response = {
                                        'status': 'error',
                                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        'message': error_message
                              }
                    return Response(error_response)

          def create(self, request, *args, **kwargs):
                    try:
                              data = request.data.copy()

                              # Check if ISBN is valid or generate a new one
                              if 'isbn' not in data or len(data['isbn']) != 13 or not data['isbn'].isdigit():
                                        data[
                                                  'isbn'] = Book.generate_isbn()  # Use the model's method to generate a valid ISBN

                              serializer = self.serializer_class(data=data)
                              serializer.is_valid(raise_exception=True)
                              serializer.save()

                              api_response = {
                                        'status': 'success',
                                        'code': status.HTTP_201_CREATED,
                                        'message': 'Book added successfully',
                                        'new_book': serializer.data,
                              }
                              return Response(api_response)
                    except Exception as e:
                              error_message = 'Failed to add book: {}'.format(str(e))
                              error_response = {
                                        'status': 'error',
                                        'code': status.HTTP_400_BAD_REQUEST,
                                        'message': error_message
                              }
                              return Response(error_response)

          def update(self, request, *args, **kwargs):
                    try:
                              instance = self.get_object()
                              serializer = self.get_serializer(instance, data=request.data)
                              serializer.is_valid(raise_exception=True)
                              serializer.save()

                              api_response = {
                                        'status': 'success',
                                        'code': status.HTTP_200_OK,
                                        'message': 'Book updated successfully',
                                        'updated_book': serializer.data,
                              }
                              return Response(api_response)
                    except Exception as e:
                              error_message = 'Failed to update book:{}'.format(str(e))
                              error_response = {
                                        'status': 'error',
                                        'code': status.HTTP_400_BAD_REQUEST,
                                        'message': error_message
                              }
                              return Response(error_response)

          def partial_update(self, request, *args, **kwargs):
                    try:
                              instance = self.get_object()
                              serializer = self.get_serializer(instance, data=request.data, partial=True)
                              serializer.is_valid(raise_exception=True)
                              serializer.save()

                              api_response = {
                                        'status': 'success',
                                        'code': status.HTTP_200_OK,
                                        'message': 'Book updated successfully',
                                        'updated_book': serializer.data,
                              }
                              return Response(api_response)
                    except Exception as e:
                              error_message = 'Failed to partially update book:{}'.format(str(e))
                              error_response = {
                                        'status': 'error',
                                        'code': status.HTTP_400_BAD_REQUEST,
                                        'message': error_message
                              }
                              return Response(error_response)

          def search(self, request, *args, **kwargs):
                    try:
                              search_term = request.query_params.get('search_term')
                              if not search_term:
                                        return Response({"message": "Please provide a search term"},
                                                        status=status.HTTP_400_BAD_REQUEST)

                              # Perform case-insensitive search by fieldname
                              search_results = Book.objects.filter(
                                        Q(b_title__icontains=search_term))

                              serializer = self.get_serializer(search_results, many=True)

                              api_response = {
                                        "status": "success",
                                        "code": status.HTTP_200_OK,
                                        "message": f"Search results for '{search_term}'",
                                        "total_records": search_results.count(),
                                        "data": serializer.data,
                              }
                              return Response(api_response)
                    except Exception as e:
                              error_message = "An error occurred while searching book: {}".format(str(e))
                              error_response = {
                                        "status": "error",
                                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                        "message": error_message,
                              }
                              return Response(error_response)

          def destroy(self, request, *args, **kwargs):
                    try:
                              instance = self.get_object()
                              instance.delete()

                              api_response = {
                                        'status': 'success',
                                        'code': status.HTTP_200_OK,
                                        'message': 'Book deleted successfully',
                              }
                              return Response(api_response)
                    except Exception as e:
                              error_message = 'Failed to delete book:{}'.format(str(e))
                              error_response = {
                                        'status': 'error',
                                        'code': status.HTTP_400_BAD_REQUEST,
                                        'message': error_message
                              }
                    return Response(error_response)

class BooksByAuthor(APIView):
          def get(self, request, a_id, *args, **kwargs):
                    if not a_id:
                              return Response({
                                        'status': 'error',
                                        'message': 'author_id parameter is required'
                              }, status=status.HTTP_400_BAD_REQUEST)

                    # Retrieve author instance
                    try:
                              author = Author.objects.get(a_id=a_id)
                    except Author.DoesNotExist:
                              return Response({
                                        'status': 'error',
                                        'message': f'Author with ID {a_id} not found'
                              }, status=status.HTTP_404_NOT_FOUND)

                    # Filter books by the specified author
                    books = Book.objects.filter(author=author)
                    book_count = books.count()

                    if book_count == 0:
                              return Response({
                                        'status': 'success',
                                        'message': f'No books found for author {author.a_name}',
                                        'total_books': 0,
                                        'books': []
                              }, status=status.HTTP_200_OK)

                    serializer = BookSerializer(books, many=True)

                    return Response({
                              'status': 'success',
                              'message': f'Books by author {author.a_name}',
                              'total_books': book_count,
                              'books': serializer.data
                    }, status=status.HTTP_200_OK)

class RecordAPI(ModelViewSet):
          queryset = Borrowrecord.objects.all()
          serializer_class = RecordSerializer

          def create(self, request, *args, **kwargs):
                    try:
                              book_id = request.data.get('book')
                              try:
                                        book = Book.objects.get(b_id=book_id)
                                        if book.available_copies and book.available_copies > 0:
                                                  available_before = book.available_copies

                                                  serializer = self.serializer_class(data=request.data)
                                                  serializer.is_valid(raise_exception=True)
                                                  serializer.save()

                                                  book.available_copies -= 1
                                                  book.save()

                                                  api_response = {
                                                            'status': 'success',
                                                            'code': status.HTTP_201_CREATED,
                                                            'message': 'Borrow record added successfully',
                                                            'new_record': serializer.data,
                                                            'book': book.b_title,
                                                            'available_copies_before': available_before,
                                                            'available_copies_after': book.available_copies,
                                                  }
                                                  return Response(api_response)
                                        else:
                                                  return Response({
                                                            'status': 'error',
                                                            'code': status.HTTP_400_BAD_REQUEST,
                                                            'message': 'No copies left.'
                                                  })
                              except Book.DoesNotExist:
                                        return Response({
                                                  'status': 'error',
                                                  'code': status.HTTP_404_NOT_FOUND,
                                                  'message': 'Book not found.'
                                        })
                    except Exception as e:
                              error_message = f'Failed to add borrow record: {str(e)}'
                              error_response = {
                                        'status': 'error',
                                        'code': status.HTTP_400_BAD_REQUEST,
                                        'message': error_message
                              }
                              return Response(error_response)

          def update(self, request, *args, **kwargs):
                    try:
                              r_id = kwargs.get('pk')  # Retrieve r_id from URL parameters (not request data)
                              try:
                                        record = Borrowrecord.objects.get(r_id=r_id)
                                        book = record.book  # Assuming there's a ForeignKey to Book in Borrowrecord

                                        # Increase the available copies for the book
                                        book.available_copies += 1
                                        book.save()

                                        # Update the return_date to today's date
                                        record.return_date = date.today()
                                        record.save()

                                        api_response = {
                                                  'status': 'success',
                                                  'code': status.HTTP_200_OK,
                                                  'message': 'Borrow record updated successfully',
                                                  'updated_record': RecordSerializer(record).data,
                                                  'available_copies_after': book.available_copies,
                                                  'return_date': record.return_date
                                        }
                                        return Response(api_response)
                              except Borrowrecord.DoesNotExist:
                                        return Response({
                                                  'status': 'error',
                                                  'code': status.HTTP_404_NOT_FOUND,
                                                  'message': 'Borrow record not found.'
                                        })
                    except Exception as e:
                              error_message = f'Failed to update borrow record: {str(e)}'
                              error_response = {
                                        'status': 'error',
                                        'code': status.HTTP_400_BAD_REQUEST,
                                        'message': error_message
                              }
                              return Response(error_response)

class GenerateReport(APIView):
          def post(self, request, *args, **kwargs):
                    logger.info("Received request to generate report")
                    try:
                              # Call the Celery task to generate the report asynchronously
                              generate_report.delay()
                              logger.info("Report generation task triggered successfully")

                              return Response({
                                        'status': 'success',
                                        'message': 'Report generation in progress.',
                              }, status=status.HTTP_202_ACCEPTED)

                    except Exception as e:
                              logger.error("Error while triggering the report generation task: {}", str(e))
                              return Response({
                                        'status': 'error',
                                        'message': f'An error occurred while triggering the report: {str(e)}',
                              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LatestReport(APIView):
          def get(self, request, *args, **kwargs):
                    try:
                              # Define the path to the reports directory using settings
                              reports_dir = settings.REPORTS_DIR

                              logger.info(f"Reports directory path: {reports_dir}")

                              # Get the latest report file (assuming filenames are in the format 'report_YYYYMMDD.json')
                              report_files = [f for f in os.listdir(reports_dir) if
                                              f.startswith('report_') and f.endswith('.json')]

                              if not report_files:
                                        logger.warning(f"No report files found in directory: {reports_dir}")
                                        return Response({
                                                  'status': 'error',
                                                  'message': 'No reports found.',
                                        }, status=status.HTTP_404_NOT_FOUND)

                              # Sort reports by date (latest file first)
                              latest_report_file = max(report_files, key=lambda f: datetime.strptime(f[7:15], '%Y%m%d'))
                              file_path = os.path.join(reports_dir, latest_report_file)

                              # Return the latest report file as a JSON response
                              with open(file_path, 'r') as f:
                                        report_data = f.read()

                              return Response({
                                        'status': 'success',
                                        'message': 'Latest report retrieved successfully.',
                                        'report': json.loads(report_data)  # Returning the content of the report
                              }, status=status.HTTP_200_OK)

                    except Exception as e:
                              # Handle any exceptions that occur during the process
                              logger.error(f"Error occurred while fetching the latest report: {str(e)}")
                              return Response({
                                        'status': 'error',
                                        'message': f'An error occurred while fetching the latest report: {str(e)}',
                              }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
