from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from .models import UserSuggestion, Replies

from .tools import *


# Create your views here.
def clipboard_list_page(request):
    
    if request.method == "GET":
        # notes = StickyNote.objects.all().order_by('-id')[:NUMBER_OF_NOTES_TO_DISPLAY]
        notes = StickyNote.objects.order_by('-id')[:NUMBER_OF_NOTES_TO_DISPLAY]
        context = { "notes" : [ note.get_my_data() for note in notes ] }
        print(context)
        return render(request , 'clipboards_screens.html' , context=context)
    
def sticky_notes_view(request):
    if request.method == 'POST':
        direction = request.POST.get('direction')
        start_id = request.POST.get('start_id')
        
        start_id = int(request.POST.get('start_id'))

        if direction == 'up':
            sticky_notes = StickyNote.next_page(start_id=start_id, number_to_display=NUMBER_OF_NOTES_TO_DISPLAY)
        elif direction == 'down':
            sticky_notes = StickyNote.previous_page(start_id=start_id, number_to_display=NUMBER_OF_NOTES_TO_DISPLAY)
            
        else:
            return JsonResponse({'error': 'Invalid direction'}, status=400)
        
        if sticky_notes is None:
            return JsonResponse({'error': 'Invalid ID'}, status=400)

        isDatabaseHasData = len(sticky_notes) > NUMBER_OF_NOTES_TO_DISPLAY - 1
        notes_data = [
            note.get_my_data() for note in sticky_notes
        ]
        
        return JsonResponse(
            {
                'sticky_notes': notes_data ,
                'isDatabaseHasData' : isDatabaseHasData
            }
        )
    else:
        # If it's not a POST request, you can return an empty response or handle it accordingly
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def reacted(request):
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        react = request.POST.get('react')
        
        result = isReactionClickingCorrect(note_id, react)
        
        if not result:
            return JsonResponse({'error': 'Invalid direction'}, status=400)
            
        return JsonResponse({'message':''})
    else:
        # If it's not a POST request, you can return an empty response or handle it accordingly
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def reactionboards(request):
    notes = StickyNote.objects.order_by('-id')[:NUMBER_OF_NOTES_TO_DISPLAY]
    context = { "notes" : [ note.get_my_data() for note in notes ] }
    return render(request, 'reactionboard.html', context)


@csrf_exempt
def write_notes(request):
    if request.method == 'POST':
        
        result, data = isDataIncorrect(request)
        
        if not result:
            sticky_note = StickyNote(
            nickname=data[0], nickname_color=int(data[1]), nickname_font=int(data[2]),
            content=data[3], content_color=int(data[4]), content_font=int(data[5]),
            emoji=data[6] , note_color = int(data[7])
            )
            sticky_note.save()
            
        return JsonResponse(
            {
                'message': '',
                'incorrect_data' : result,
            }
        )
    elif request.method == 'GET':
        return render(request , 'write_notes_screens.html' )
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def suggestion_page(request):
    print(StickyNote.getStickyNote(7).get_my_data())
    
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        suggestion = UserSuggestion(nickname=nickname, subject=subject, content=content)
        suggestion.save()
        return JsonResponse({'message': ''})
    elif request.method == 'GET':
        return render(request, 'suggestions_screens.html')
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
def whiteboard_page(request):
    return render(request , 'whiteboard.html')