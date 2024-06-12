from django.db import models
import typing as tp

# Create your models here.
REACTIONS = ('loves', 'angries', 'cries', 'wows')
REACTION_INCREMENT = 1

class StickyNote(models.Model):
    
    note_color = models.PositiveSmallIntegerField(default=None)
    
    nickname = models.CharField(max_length=13)
    nickname_color = models.PositiveSmallIntegerField()
    nickname_font = models.PositiveSmallIntegerField()
    
    content = models.CharField(max_length=230)
    content_color = models.PositiveSmallIntegerField()
    content_font = models.PositiveSmallIntegerField()
    
    emoji = models.CharField(max_length=255, default='')
    
    posted_date = models.DateTimeField( auto_now_add=True)
    
    loves = models.PositiveBigIntegerField(default=0)
    angries = models.PositiveBigIntegerField(default=0)
    cries = models.PositiveBigIntegerField(default=0)
    wows = models.PositiveBigIntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.posted_date.date()} - {self.nickname}"
    
    def get_my_data(self):
        print(self.replies)
        # data = {
        #     'note_color' : self.note_color,
        #     'nickname' : self.nickname,
        #     'nickname_color' : self.nickname_color,
        #     'nickname_font' : self.nickname_font,
        #     'content' : self.content,
        #     'content_color' : self.content_color,
        #     'content_font' : self.content_font,
        #     'emoji' : self.emoji,
        #     'time' : self.posted_date.time().__str__,
        #     'loves' : self.loves,
        #     'angries' : self.angries,
        #     'cries' : self.cries,
        #     'wows' : self.wows,
        #     'replies' : [
        #         reply.get_data() for reply in self.replies.objects.all()
        #     ]
        # }
        
        # return data
    
    @classmethod
    def next_page(cls, start_id : int, number_to_display : int) -> tp.List['StickyNote'] :
        sticky_notes = cls.objects.filter(id__lt=start_id).order_by('-id')[:number_to_display]
        return sticky_notes

    @classmethod
    def previous_page(cls, start_id : int, number_to_display : int) -> tp.List['StickyNote'] :
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
    
    

class Replies(models.Model):
    sticky_note = models.ForeignKey(StickyNote, on_delete=models.CASCADE, related_name='replies', default=None)
    nickname = models.CharField(max_length=13)
    content = models.TextField()
    
    def get_data(self) -> tuple[str, str]:
        return ( self.nickname.__str__, self.content.__str__)
    
    @classmethod
    def getData(cls) -> tuple[str, str]:
        return ( cls.nickname.__str__, cls.content.__str__ )
    
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