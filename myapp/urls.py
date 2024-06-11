from django.urls import path
from . import views

urlpatterns = [
    path('' , view=views.clipboard_list_page, name='home'),
    path('write/', view=views.write_notes, name='write')
]
