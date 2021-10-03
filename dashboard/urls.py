from django.urls import path
from .views import *

urlpatterns = [
    # Home Url
    path('',home,name="home"),
    # Eslatmalar url
    path('notes/',notes,name="notes"),
    path('delete-notes/<int:pk>/',delete_note,name="delete_note"),
    path('notes-detail/<int:pk>/',NotesDeatilView.as_view(),name="note-detail"),
    # Uy vazifa url
    path('homework/',homework,name="homework"),
    path('update-homework/<int:pk>/',update_homework,name="update_homework"),
    path('delete-homework/<int:pk>/',delete_homework,name="delete_homework"),
    # You Tube Url
    path('youtube/',youtube,name="youtube"),
    # Todo Url
    path('todo/',todo,name="todo"),
    path('update-todo/<int:pk>/',update_todo,name="update_todo"),
    path('delete-todo/<int:pk>/',delete_todo,name="delete_todo"),
    # Books Url
    path('books/',books,name="books"),
    # Dictionary Url
    path('dictionary/',Dictionary,name="dictionary"),
    # Wikipediya Url
    path('wikipediya/',Wiki,name="wiki"),
    # Conversion Url
    path('conversion/',Conversion,name="conversion"),
    
]   