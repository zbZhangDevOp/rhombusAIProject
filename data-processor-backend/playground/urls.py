from django.urls import path
from playground.views import upload_and_process_file

# URL Configuration for the playground app
urlpatterns = [
    path('upload/', upload_and_process_file, name='upload_and_process_file'),
]