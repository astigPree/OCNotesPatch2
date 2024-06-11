from django.db import models

# Create your models here.

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
    
    replies = models.PositiveBigIntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.posted_date} - {self.nickname}"
    

class Replies(models.Model):
    
    nickname = models.CharField(max_length=13)
    content = models.TextField()
    replied_note_in = models.PositiveBigIntegerField()
    

class UserSuggestion(models.Model):

    nickname = models.CharField(max_length=13)
    subject = models.CharField(max_length=50)
    content = models.TextField()
    
    def __str__(self) -> str:
        return self.subject