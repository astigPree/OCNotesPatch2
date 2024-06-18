from django.db import models
import typing as tp
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import pytz

# Define the Masbate City timezone
manila_tz = pytz.timezone('Asia/Manila')

# Create your models here.
REACTIONS = ('loves', 'angries', 'cries', 'wows')
REACTION_INCREMENT = 1

class StickyNote(models.Model):
    
    note_color = models.PositiveSmallIntegerField(default=None)
    
    nickname = models.CharField(max_length=13)
    nickname_color = models.PositiveSmallIntegerField()
    nickname_font = models.PositiveSmallIntegerField()
    
    content = models.CharField(max_length=240)
    content_color = models.PositiveSmallIntegerField()
    content_font = models.PositiveSmallIntegerField()
    
    emoji = models.CharField(max_length=255, default='')
    
    posted_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    
    loves = models.PositiveBigIntegerField(default=0)
    angries = models.PositiveBigIntegerField(default=0)
    cries = models.PositiveBigIntegerField(default=0)
    wows = models.PositiveBigIntegerField(default=0)
    
    gender = models.CharField(max_length=1, default='')
    
    def __str__(self) -> str:
        return f"{self.posted_date} - {self.nickname}"
    
    def get_my_data_without_reply(self) -> dict:
        data = {
            'note_id' : self.id,
            'note_color' : self.note_color,
            'nickname' : self.nickname,
            'nickname_color' : self.nickname_color,
            'nickname_font' : self.nickname_font,
            'content' : self.content,
            'content_color' : self.content_color,
            'content_font' : self.content_font,
            'emoji' : self.emoji,
            'time' : self.posted_date.strftime("%B %d").upper(),
            'loves' : self.loves,
            'angries' : self.angries,
            'cries' : self.cries,
            'wows' : self.wows,
            'gender' : self.gender,
            'total_replies' : self.replies.count()
        }
        # data = {
        #     'note_id' : self.id,
        #     'note_color' : self.note_color,
        #     'nickname' : self.nickname,
        #     'nickname_color' : self.nickname_color,
        #     'nickname_font' : self.nickname_font,
        #     'content' : self.content,
        #     'content_color' : self.content_color,
        #     'content_font' : self.content_font,
        #     'emoji' : self.emoji,
        #     'time' : self.posted_date.strftime("%b / %I:%M %p").lower(),
        #     'loves' : self.loves,
        #     'angries' : self.angries,
        #     'cries' : self.cries,
        #     'wows' : self.wows,
        #     'gender' : self.gender,
        #     'total_replies' : self.replies.count()
        # }
        
        return data
    
    def get_my_data(self) -> dict:
        data = {
            'note_id' : self.id,
            'note_color' : self.note_color,
            'nickname' : self.nickname,
            'nickname_color' : self.nickname_color,
            'nickname_font' : self.nickname_font,
            'content' : self.content,
            'content_color' : self.content_color,
            'content_font' : self.content_font,
            'emoji' : self.emoji,
            'time' : self.posted_date.strftime("%B %d").upper(),
            'loves' : self.loves,
            'angries' : self.angries,
            'cries' : self.cries,
            'wows' : self.wows,
            'gender' : self.gender,
            'total_replies' : self.replies.count(),
            'replies' : [
                reply.get_data() for reply in self.replies.all()[::-1]
            ]
        }
        
        return data
    
    @classmethod
    def next_page(cls, start_id : int, number_to_display : int) -> tp.Union[tp.List['StickyNote'], None] :
        """Get the next page

        Args:
            start_id (int): The starting ID of the selected StickyNote

        Returns:
            Queryset[StickyNote, ...] : return the sticky notes needed 
        """
        sticky_notes = cls.objects.filter(id__lt=start_id).order_by('-id')[:number_to_display]
        return sticky_notes
    
    @classmethod
    def next_page_remaining(cls, start_id: int = None, number_to_display: int = 10) -> int:
        queryset = cls.objects.order_by('-id')
        
        paginator = Paginator(queryset, number_to_display)

        if start_id is None:
            # Start from the first page
            start_page = paginator.page(1)
            
        else:
            # Get the page based on the start_id
            start_page = paginator.get_page(start_id // number_to_display + 1)
        
        print("page next number ", paginator.get_page(start_page.next_page_number()) )

        # Get the remaining objects after the start_page
        remaining_objects = paginator.object_list[start_page.end_index():]

        return len(remaining_objects)
    
    @classmethod
    def previous_page(cls, start_id : int, number_to_display : int) -> tp.Tuple[ tp.Union[ tp.List['StickyNote'], None] , int ] :
        """Get the prev page

        Args:
            start_id (int): The starting ID of the selected StickyNote

        Returns:
            tuple[ Queryset[StickyNote, ...] , remaining notes ]: return the sticky notes needed and the remaining notes
        """
        sticky_notes = cls.objects.filter(id__gt=start_id).order_by('id')[:number_to_display:-1]
        remaining = len(cls.objects.filter(id__gt=start_id).order_by('-id')) - number_to_display
        if remaining < 0:
            remaining = 0
        return sticky_notes, remaining
    
    @classmethod
    def prev_page_remaining(cls, start_id : int , number_to_display : int) -> int:
        remaining = len(cls.objects.filter(id__gt=start_id).order_by('-id')) - number_to_display
        if remaining < 0:
            remaining = 0
        return remaining
    
    @classmethod
    def isWhiteBoardIsFull(cls, note_id ) -> bool:
        sticky_note = cls.objects.filter(id=note_id).first()
        if sticky_note is None:
            return True
        
        total_replies = sticky_note.replies.count()
        if total_replies == 30:
            return True
        return False
    
    @classmethod
    def getTheReplies(cls , note_id)-> tp.Sequence['Replies']:
        """
        Get all replies associated with a specific StickyNote.

        Args:
            note_id (int): ID of the StickyNote.

        Returns:
            QuerySet[Replies] or None: A queryset of related Replies or None if the StickyNote doesn't exist.
        """
        sticky_note = cls.objects.get(id=note_id)
        if sticky_note is None:
            return None
        return sticky_note.replies.all()

    @classmethod
    def addUserReaction(cls, note_id : int, react_type : str) -> bool:
        sticky_note = StickyNote.objects.filter(id=note_id).first()
        if sticky_note is None:
            return False
        if (react_type == REACTIONS[0]):
            sticky_note.loves += REACTION_INCREMENT
        if (react_type == REACTIONS[1]):
            sticky_note.angries += REACTION_INCREMENT
        if (react_type == REACTIONS[2]):
            sticky_note.cries += REACTION_INCREMENT
        if (react_type == REACTIONS[3]):
            sticky_note.wows += REACTION_INCREMENT
        sticky_note.save()
        return True
    
    @classmethod
    def getStickyNote(cls , note_id : int) -> tp.Union[None , object]:
        sticky_note = cls.objects.filter(id=note_id).first()
        return sticky_note
    
    @classmethod
    def get_top_stats(cls):
        contain_notes = cls.objects.all().exists()
        # print("contain" , contain_notes)
        if (contain_notes):
            top_5_loves = [ top_5.get_my_data_without_reply() for top_5 in cls.objects.order_by('-loves')[:5] ]
            top_5_angries = [ top_5.get_my_data_without_reply() for top_5 in cls.objects.order_by('-angries')[:5] ]
            top_5_cries = [ top_5.get_my_data_without_reply() for top_5 in cls.objects.order_by('-cries')[:5] ] 
            top_5_wows = [ top_5.get_my_data_without_reply() for top_5 in cls.objects.order_by('-wows')[:5] ]

            top_stats = {
                'top_overall':[ ],
                'top_5_loves': top_5_loves,
                'top_5_angries': top_5_angries,
                'top_5_cries': top_5_cries,
                'top_5_wows': top_5_wows
            }
            
            top_love = cls.objects.order_by('-loves').first()
            top_love_data = top_love.get_my_data_without_reply()
            top_stats['top_overall'].append(top_love_data)
            
            top_angry = cls.objects.order_by('-angries').first()
            top_angry_data = top_angry.get_my_data_without_reply()
            if top_angry_data not in top_stats['top_overall']:
                top_stats['top_overall'].append(top_angry_data)
            
            top_cry = cls.objects.order_by('-cries').first()
            top_cry_data = top_cry.get_my_data_without_reply()
            if top_cry_data not in top_stats['top_overall']:
                top_stats['top_overall'].append(top_cry_data)
                
            top_wow = cls.objects.order_by('-wows').first()
            top_wow_data = top_wow.get_my_data_without_reply()
            if top_wow_data not in top_stats['top_overall']:
                top_stats['top_overall'].append(top_wow_data)
            
            return top_stats

        else:
            top_stats = {
                'top_overall':[],
                'top_5_loves': [],
                'top_5_angries': [],
                'top_5_cries': [],
                'top_5_wows': []
            }
            return top_stats
            
    
    @classmethod
    def get_previous_objects(cls, start_id: int = None, number_to_display: int = 10, isRetriving : bool = False) -> tuple[list, int]:
        try:
            if start_id is None:
                start_object = cls.objects.order_by('-id').first()
                start_id = start_object.id if start_object else None
                queryset = cls.objects.filter(id__gt=start_id).order_by('-id')
            else:
                start_object = cls.objects.get(id=start_id)
                if isRetriving:
                    queryset = cls.objects.filter(id__gt=start_id).order_by('-id')
                    print("happen Retrive", start_id)
                else :
                    queryset = cls.objects.filter(id__gte=start_id).order_by('-id')
                    print("happen Read" , start_id)
                    
                
            
            
            print("-----------------------------------")
            for n , q in enumerate(queryset):
                print(f"{n}: {q.id} - {q}")
    
            paginator = Paginator(queryset, number_to_display)
            print("total page : ", paginator.num_pages)
            start_page = paginator.page( paginator.num_pages)
            remaining_objects = paginator.object_list[start_page.start_index():]
            print(remaining_objects)
            
            print("-----------------------------------")
            for n , q in enumerate(paginator.object_list):
                print(f"{n}: {q.id} - {q}")

            
            
            
            print("-----------------------------------")
            for n , q in enumerate(start_page):
                print(f"{n}: {q.id} - {q}")
            
            # print("-----------------------------------")
            # print("Query Len " , len(queryset))
            # print( "Page list" , len(paginator.object_list))
            # print( "Getted Page" , len(start_page.object_list))
            # print( "List Remaining : ", len(remaining_objects) )
            remaining = len(paginator.object_list) - len(start_page.object_list) if isRetriving else len(paginator.object_list)
            return list(start_page.object_list),  remaining
        except ObjectDoesNotExist:
            return [], 0
    
        
    @classmethod
    def get_next_objects(cls, start_id: int = None, number_to_display: int = 10, isRetriving : bool = False) -> tuple[list, int]:
        try:
            if start_id is None:
                start_object = cls.objects.order_by('-id').first()
                start_id = start_object.id if start_object else None
                queryset = cls.objects.filter(id__lte=start_id).order_by('-id')
            else:
                start_object = cls.objects.get(id=start_id)
                if isRetriving:
                    queryset = cls.objects.filter(id__lt=start_id).order_by('-id')
                    print("happen Retrive", start_id)
                else :
                    queryset = cls.objects.filter(id__lte=start_id).order_by('-id')
                    print("happen Read" , start_id)

            paginator = Paginator(queryset, number_to_display)
            start_page = paginator.page(1)
            
            # print(" Query Len " , len(queryset))
            # print( "Page list" , len(paginator.object_list))
            # print( "Getted Page" , len(start_page.object_list))
            remaining = len(paginator.object_list)  - len(start_page.object_list) if isRetriving else len(paginator.object_list)
            return list(start_page.object_list), remaining
        except ObjectDoesNotExist:
            return [], 0
        
        
    
class Replies(models.Model):
    sticky_note = models.ForeignKey(StickyNote, on_delete=models.CASCADE, related_name='replies', default=None)
    nickname = models.CharField(max_length=13)
    content = models.TextField()
    replies_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.sticky_note.posted_date.date()} - {self.sticky_note.nickname}"
    
    def get_data(self) -> tuple[str, str]:
        return ( self.nickname, self.content , self.replies_date.strftime("%B %d").upper())
        # return ( self.nickname, self.content , self.replies_date.strftime("%I:%M%p").lower())
    
    @classmethod
    def getData(cls) -> tuple[str, str]:
        return ( cls.nickname, cls.content, cls.replies_date.strftime("%B %d").upper())
        # return ( cls.nickname, cls.content, cls.replies_date.strftime("%I:%M%p").lower() )
    
    @classmethod
    def addNewReplies(cls, note_id : int , nickname : str , content : str) -> bool:
        """Create new replies based on the note id passed

        Args:
            note_id (int): ID of the StickyNote

        Returns:
            bool: if the replies saved or not
        """
        sticky_note = StickyNote.objects.filter(id=note_id).first()
        if sticky_note is None:
            return False
        
        reply = cls.objects.create(sticky_note=sticky_note, nickname=nickname, content=content)
        reply.replies_date = timezone.now().astimezone(manila_tz)
        reply.save()
        return True
         
    
class UserSuggestion(models.Model):

    nickname = models.CharField(max_length=13)
    subject = models.CharField(max_length=50)
    content = models.TextField()
    
    def __str__(self) -> str:
        return self.subject