
from .models import StickyNote
from html.parser import HTMLParser
import re

NUMBER_OF_NOTES_TO_DISPLAY = 3
BAD_WORDS = (
    'puta', 'pota', 'tangina', 'gago' , 'bobo' , 'bubo' , 'bubu' , 'bobu' , 'gaga', 'patay', 'matay', 'natay', 'amp', 'nigga', 'yawa',
    'pisot' , 'bayag', 'buto', 'totoy', 'boto', 'letche', 'itot', 'lolo' , 'salsal', 'jabol', 'pusli', 'shabu', 'whana', 'bilat', 'belat',
    'puke', 'sex' , 'porn', 'dudu', 'dede', 'putay', 'kupal', 'kopal', 'bolbol', 'kantu', 'kasta', 'torjack', 'pisti', 'peste' , 'piste', 'pesti',
    'kant', 'yatis', 'ngina','shuta','nigger','negro','pampam','whore','slut','gagi','shole','hoe','shit','fuck','bitch','cock','pussy',
    'cunt','shat','shite','jaku','kanor','jako',
)
EMOJIS = (
    '🥰', '😂', '😏','🤪', '😑', '😴', '😢', '😡', '🤔', '😎', '😚',
    '🥵', '🤮', '😮', '😒', '😌'
)
NICKNAME_LENGTH = 13
CONTENT_LENGTH = 230
NICKNAME_CONTENT_COLORS = ( '1' , '2' , '3')
NICKNAME_FONTS = ('1' , '2', '3' , '4' , '5' , '6', '7', '8', '9', '10')
CONTENT_FONTS = ('3', '4' , '2' , '6' , '7' , '8' , '10')
NOTE_COLORS = ('1' , '2', '3' , '4', '5' , '6')
REACTIONS = { "1" : "loves", "2" : 'angries', "3" : 'cries', "4" : 'wows'}


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.contains_html = False

    def handle_starttag(self, tag, attrs):
        self.contains_html = True
        
def willMakeAHTMLObject(text: str) -> bool:
    parser = MyHTMLParser()
    parser.feed(text)
    return parser.contains_html

def isBadWords(sentence : str, word : str) -> bool:
    hasBadWord = sentence.lower().find(word)
    return True if hasBadWord > -1 else False

def updateSentence(sentence, start , end) -> str:
    for i in range(start , end + 1):
        sentence[i] = '*'
    return sentence

def hasBadWord(sentence : str) -> bool:
    for word in BAD_WORDS:
        if isBadWords(sentence , word):
            return True
    return False

def get_incremental_sticky_notes(start_id, count):
    sticky_notes = list(StickyNote.objects.filter(id__gte=start_id).order_by('id')[:count])
    sticky_notes.reverse()
    return sticky_notes

def next_page(start_id):
    sticky_notes = StickyNote.objects.filter(id__lt=start_id).order_by('-id')[:NUMBER_OF_NOTES_TO_DISPLAY]
    return sticky_notes

def previous_page(start_id):
    sticky_notes = StickyNote.objects.filter(id__gt=start_id).order_by('id')[:NUMBER_OF_NOTES_TO_DISPLAY:-1]
    return sticky_notes
    
def get_decremental_sticky_notes(start_id, count):
    sticky_notes = list(StickyNote.objects.filter(id__lte=start_id).order_by('-id')[:count])
    sticky_notes.reverse()
    return sticky_notes

def isCorrectTextFormat(text : str , text_len : int) -> bool:
    pattern = r'^[ -~]*$'
    
    # Check if the input string matches the pattern
    if re.match(pattern, text):
        if len(text) <= text_len:
            return True
    return False

def isDataIncorrect(request) -> tuple[bool, object] :
    """Check if the request data has anything might cause the system or database an error 

    Args:
        request (object): request in the web using POST

    Returns:
        bool: return if the data is not valid or valid
        object : return a collected data if all valid if not then None
    """
    nickname = request.POST.get('nickname')
    content = request.POST.get('content')
    
    # Check if has a badwords and Check if can be turn to html object        
    if ( hasBadWord(nickname) or hasBadWord(content) or willMakeAHTMLObject(nickname) or willMakeAHTMLObject(content) ):
        return True, None
    # Check if the text is in the right format
    if ( not isCorrectTextFormat(nickname, NICKNAME_LENGTH) or not isCorrectTextFormat(content , CONTENT_LENGTH) ):
        return True, None
    # Check if the colors is correct and the font is correct
    nickname_color = request.POST.get('nickname_color')
    content_color = request.POST.get('content_color')
    if (nickname_color not in NICKNAME_CONTENT_COLORS or content_color not in NICKNAME_CONTENT_COLORS):
        return True, None
    # Check if the content and nickname font is correct
    nickname_font = request.POST.get('nickname_font')
    content_font = request.POST.get('content_font')
    if (nickname_font not in NICKNAME_FONTS or content_font not in CONTENT_FONTS):
        return True, None
    # Check if the emoji exist
    emoji = request.POST.get('emoji')
    if (emoji not in EMOJIS):
        return True, None
    # Check if the sticky note colors exist
    note_color = request.POST.get('note_color')
    if (note_color not in NOTE_COLORS):
        return True, None

    
    # IF all is False then it is correct
    return False, ( nickname, nickname_color, nickname_font, content, content_color, content_font, emoji, note_color)

def isReactionClickingCorrect(note_id : str , react : str):
    if not note_id.isnumeric():
        return False
    stickynote = StickyNote.getStickyNote(int(note_id))
    if not stickynote or stickynote is None:
        return False
    if react not in REACTIONS:
        return False
    
    StickyNote.addUserReaction(int(note_id), REACTIONS[react])
    return True
    