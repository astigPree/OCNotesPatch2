from django.db import models
from django.utils import timezone
import typing as tp

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
    
    posted_date = models.DateTimeField( auto_now_add=True)
    
    loves = models.PositiveBigIntegerField(default=0)
    angries = models.PositiveBigIntegerField(default=0)
    cries = models.PositiveBigIntegerField(default=0)
    wows = models.PositiveBigIntegerField(default=0)
    
    gender = models.CharField(max_length=1, default='')
    
    def __str__(self) -> str:
        return f"{self.posted_date.date()} - {self.nickname}"
    
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
            'time' : self.posted_date.strftime("%b / %I:%M %p").lower(),
            'loves' : self.loves,
            'angries' : self.angries,
            'cries' : self.cries,
            'wows' : self.wows,
            'gender' : self.gender
        }
        
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
            'time' : self.posted_date.strftime("%b / %I:%M %p").lower(),
            'loves' : self.loves,
            'angries' : self.angries,
            'cries' : self.cries,
            'wows' : self.wows,
            'gender' : self.gender,
            'replies' : [
                reply.get_data() for reply in self.replies.all()[::-1]
            ]
        }
        
        return data
    
    @classmethod
    def next_page(cls, start_id : int, number_to_display : int) -> tp.Union[tp.List['StickyNote'], None] :
        sticky_notes = cls.objects.filter(id__lt=start_id).order_by('-id')[:number_to_display]
        return sticky_notes
        
    @classmethod
    def previous_page(cls, start_id : int, number_to_display : int) -> tp.Union[ tp.List['StickyNote'], None] :
        sticky_notes = cls.objects.filter(id__gt=start_id).order_by('id')[:number_to_display:-1]
        return sticky_notes
    
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
        print("contain" , contain_notes)
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
            
    
    
class Replies(models.Model):
    sticky_note = models.ForeignKey(StickyNote, on_delete=models.CASCADE, related_name='replies', default=None)
    nickname = models.CharField(max_length=13)
    content = models.TextField()
    replies_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.sticky_note.posted_date.date()} - {self.sticky_note.nickname}"
    
    def get_data(self) -> tuple[str, str]:
        return ( self.nickname, self.content , self.replies_date.strftime("%I:%M%p").lower())
    
    @classmethod
    def getData(cls) -> tuple[str, str]:
        return ( cls.nickname, cls.content, cls.replies_date.strftime("%I:%M%p").lower() )
    
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
        
        cls.objects.create(sticky_note=sticky_note, nickname=nickname, content=content)
        return True
         
    
class UserSuggestion(models.Model):

    nickname = models.CharField(max_length=13)
    subject = models.CharField(max_length=50)
    content = models.TextField()
    
    def __str__(self) -> str:
        return self.subject