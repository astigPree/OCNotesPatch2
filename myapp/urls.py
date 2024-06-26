from django.urls import path
from . import views

urlpatterns = [
    path('' , view=views.clipboard_list_page, name='home'),
    path('write/', view=views.write_notes, name='write'),
    path('stickynotes/', view=views.sticky_notes_view, name='stickynotes'),
    path('suggestion/', view=views.suggestion_page , name="suggestion"),
    path('whiteboard/<str:pk>', view=views.whiteboard_page, name="whiteboard"),
    path('reacted/', view=views.reacted, name="reacted"),
    path('reactionboards/', view=views.reactionboards, name="reactionboards" ),
    path('reply/' , view=views.reply_in_whiteboard, name="reply")
]
