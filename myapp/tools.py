
from .models import StickyNote
from html.parser import HTMLParser
import re

NUMBER_OF_NOTES_TO_DISPLAY = 25
BAD_WORDS = (
    'puta', 'pota', 'tangina', 'gago' , 'bobo' , 'bubo' , 'bubu' , 'bobu', 'patay', 'matay', 'natay', 'amp', 'nigga', 'yawa',
    'pisot' , 'bayag', 'buto', 'totoy', 'boto', 'letche', 'itot' , 'salsal', 'jabol', 'pusli', 'shabu', 'whana', 'bilat', 'belat',
    'puke', 'sex' , 'porn', 'dede', 'putay', 'kupal', 'kopal', 'bolbol', 'kantu', 'kasta', 'torjack', 'pisti', 'peste' , 'piste', 'pesti',
    'kant', 'yatis', 'ngina','shuta','nigger','negro','pampam','whore','slut','gagi','shole','hoe','shit','fuck','bitch','cock','pussy',
    'cunt','shat','shite','jaku','kanor','jako',
)
EMOJIS = (
    '🥰', '😂', '😏','🤪', '😑', '😴', '😢', '😡', '🤔', '😎', '😚',
    '🥵', '🤮', '😮', '😒', '😌'
)
NICKNAME_LENGTH = 13
CONTENT_LENGTH = 240
REPLY_CONTENT_LENGTH = 347
NICKNAME_CONTENT_COLORS = ( '1' , '2' , '3')
NICKNAME_FONTS = ('1' , '2', '3' , '4' , '5' , '6', '7', '8', '9', '10')
CONTENT_FONTS = ('3', '4' , '2' , '6' , '7' , '8' , '10')
NOTE_COLORS = ('1' , '2', '3' , '4', '5' , '6')
REACTIONS = { "1" : "loves", "2" : 'angries', "3" : 'cries', "4" : 'wows'}
GENDER = {"1" : "MALE", "2" : "FEMALE", "3" : "NON-BINARY"}

ERROR_TYPE = {
    'html' : "May nilagay ka na pwede kamakasira sa website at ito ay {word}. Alisin o lagyan mo ng '*'",
    'bad' : "May salita ka na nilagay na hindi kaaya aya pwede mo to lagyan ng '*' at kung gusto mo palitan mo ito! Ang salitang yun ay ' {word} '",
    'hack' : "May ginawa ka na hindi kaaya aya at pwede makasira sa website! Sana naman ayusin mo ang pag gamit neto"
}

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.contains_html = False
        self.tag_positions = []

    def handle_starttag(self, tag, attrs):
        self.contains_html = True
        self.tag_positions.append((tag, self.getpos()))

    def get_tag_positions(self):
        return self.tag_positions
        
def willMakeAHTMLObject(text: str) -> bool:
    parser = MyHTMLParser()
    parser.feed(text)
    # print("Has html object" , parser.contains_html)
    return parser.contains_html

def getLocationOfTag(text: str) -> list:
    parser = MyHTMLParser()
    parser.feed(text)
    tags = parser.get_tag_positions()
    # print("Tag html object" , tags )
    return [ f'{tag[0]}' for tag in tags]

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

def getBadWords(sentence : str) -> str:
    for word in BAD_WORDS:
        if isBadWords(sentence , word):
            return word
    return ''

def get_incremental_sticky_notes(start_id, count):
    sticky_notes = list(StickyNote.objects.filter(id__gte=start_id).order_by('id')[:count])
    sticky_notes.reverse()
    return sticky_notes

def next_page(start_id) -> tuple[list[StickyNote], int ]:
    """Get the next page

    Args:
        start_id (int): The starting ID of the selected StickyNote

    Returns:
        tuple[ Queryset[StickyNote, ...] , remaining notes ]: return the sticky notes needed and the remaining notes
    """
    sticky_notes = StickyNote.objects.filter(id__lt=start_id).order_by('-id')[:NUMBER_OF_NOTES_TO_DISPLAY]
    return sticky_notes, len(StickyNote.objects.filter(id__lt=start_id).order_by('-id')[NUMBER_OF_NOTES_TO_DISPLAY::])

def previous_page(start_id):
    sticky_notes = StickyNote.objects.filter(id__gt=start_id).order_by('id')[:NUMBER_OF_NOTES_TO_DISPLAY:-1]
    return sticky_notes, len(StickyNote.objects.filter(id__lt=start_id).order_by('-id')[NUMBER_OF_NOTES_TO_DISPLAY::])
    
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
    
    # Check if can be turn to html object        
    if willMakeAHTMLObject(nickname):
        return True, None, ERROR_TYPE['html'].format(word=getLocationOfTag(nickname))
    if willMakeAHTMLObject(content) :
        return True, None, ERROR_TYPE['html'].format(word=getLocationOfTag(content))
    #  Check if has a badwords and 
    if hasBadWord(nickname):
        return True, None, ERROR_TYPE['bad'].format(word=getBadWords(nickname))
    if hasBadWord(content) :
        return True, None, ERROR_TYPE['bad'].format(word=getBadWords(content))
    
    # Check if the text is in the right format
    if ( not isCorrectTextFormat(nickname, NICKNAME_LENGTH) or not isCorrectTextFormat(content , CONTENT_LENGTH) ):
        return True, None, ERROR_TYPE['hack']
    
    # Check if the colors is correct and the font is correct
    nickname_color = request.POST.get('nickname_color')
    content_color = request.POST.get('content_color')
    if (nickname_color not in NICKNAME_CONTENT_COLORS or content_color not in NICKNAME_CONTENT_COLORS):
        return True, None, ERROR_TYPE['hack']
    # Check if the content and nickname font is correct
    
    nickname_font = request.POST.get('nickname_font')
    content_font = request.POST.get('content_font')
    if (nickname_font not in NICKNAME_FONTS or content_font not in CONTENT_FONTS):
        return True, None, ERROR_TYPE['hack']
    # Check if the emoji exist
    emoji = request.POST.get('emoji')
    if (emoji not in EMOJIS):
        return True, None, ERROR_TYPE['hack']
    # Check if the sticky note colors exist
    note_color = request.POST.get('note_color')
    if (note_color not in NOTE_COLORS):
        return True, None, ERROR_TYPE['hack']
    #Check if the gender exist
    gender = request.POST.get('gender')
    if (gender not in GENDER):
        return True, None, ERROR_TYPE['hack']
    
    # IF all is False then it is correct
    return ( False, ( 
        nickname, nickname_color, nickname_font, 
        content, content_color, content_font, 
        emoji, note_color, gender
    ), '' )

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

def isReplyCorrect(nickname : str, content : str):
    if len(nickname) > NICKNAME_LENGTH or len(content) > REPLY_CONTENT_LENGTH:
        return False , ERROR_TYPE['hack']
    if willMakeAHTMLObject(nickname):
        return False , ERROR_TYPE['html'].format(word=getLocationOfTag(nickname))
    if willMakeAHTMLObject(content) :
        return False , ERROR_TYPE['html'].format(word=getLocationOfTag(content))
    if hasBadWord(nickname):
        return False, ERROR_TYPE['bad'].format(word=getBadWords(nickname))
    if hasBadWord(content):
        return False, ERROR_TYPE['bad'].format(word=getBadWords(content))
    
    return True , None