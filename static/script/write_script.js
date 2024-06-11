const fontStylesIndex = {
    '--primary-font': "1",
    '--secondary-font': "2",
    '--comic-san': "3",
    '--arial-rounded': "4",
    '--lucida-writing': "5",
    '--bradley-hand': "6",
    '--chalkboard-se': "7",
    '--dakota': "8",
    '--permanent-marker': "9",
    '--indie-flower': "10"
};

const noteColor = {
    "1" : "#f9f485",
    "2" : "#F3BCCF",
    "3" : "#A1FF6C",
    "4" : "#DCCAFF",
    "5" : "#87CDFF",
    "6" : "#F37750",
}

const textColor = {
    "black" : "1",
    "red" : "2",
    "blue" : "3"
}


function getCurrentDateFormatted() {
    const date = new Date();
    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    const month = monthNames[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();
    return `${month} ${day}, ${year}`;
}


function changeTemplate(url) {
    window.location.href = url;
}


function isFillUp(){
    // Get the form value
    let nickname = document.getElementById('nickname').value;
    let content = document.getElementById('content').value;
    
    if (!nickname || !content){
        return false;
    }
    return true;
}

function validateInput(input) {
    const regex = /^[ -~]*$/; // Regular expression to match ASCII characters
    if (!regex.test(input.value)) {
        // If input contains non-ASCII characters, remove them
        input.value = input.value.replace(/[^\x20-\x7E]/g, '');
    }
}

function changeNicknameColor(selected_color){
    const sticky_nickname = document.getElementsByClassName('nickname')[0];
    sticky_nickname.style.color = selected_color;

    const sticky_note = document.getElementById("stickynote");
    sticky_note.setAttribute('nickname_color' , textColor[selected_color]);
};

function updateNickname(){
    
    var form_nickname = document.getElementById('nickname');
    validateInput(form_nickname);

    const sticky_nickname = document.getElementsByClassName('nickname')[0];
    sticky_nickname.textContent = form_nickname.value;

    const sticky_note = document.getElementById("stickynote");
    sticky_note.setAttribute('nickname', form_nickname.value);
}

function changeNicknameFont(font_used){
    const font_index = fontStylesIndex[font_used];
    const selected_font = getComputedStyle(document.documentElement).getPropertyValue(font_used);
    const sticky_nickname = document.getElementsByClassName('nickname')[0];
    sticky_nickname.style.fontFamily = selected_font;

    
    const sticky_note = document.getElementById("stickynote");
    sticky_note.setAttribute('nickname_font', font_index);
}

function updateContent(){
    
    var form_content = document.getElementById('content');
    validateInput(form_content);

    const sticky_content_parent = document.getElementsByClassName('sticky-note-content')[0]
    const content = sticky_content_parent.getElementsByTagName('p')[0];
    content.textContent = form_content.value;

    
    const sticky_note = document.getElementById("stickynote");
    sticky_note.setAttribute('content', form_content.value);
}

function changeContentFont(font_used){
    const selected_font = getComputedStyle(document.documentElement).getPropertyValue(font_used);
    const sticky_content_parent = document.getElementsByClassName('sticky-note-content')[0]
    const content = sticky_content_parent.getElementsByTagName('p')[0];
    content.style.fontFamily = selected_font;

    
    const sticky_note = document.getElementById("stickynote");
    sticky_note.setAttribute('content_font' , fontStylesIndex[font_used]);
}

function changeContentColor(selected_color){
    const sticky_content_parent = document.getElementsByClassName('sticky-note-content')[0]
    const content = sticky_content_parent.getElementsByTagName('p')[0];
    content.style.color = selected_color;

    const sticky_note = document.getElementById("stickynote");
    sticky_note.setAttribute('content_color', textColor[selected_color]);
};

function changeNoteColor(selected_color){
    const sticky_note = document.getElementsByClassName('sticky-note')[0];
    sticky_note.style.backgroundColor = noteColor[selected_color];
    sticky_note.setAttribute('note_color', selected_color);
}

function changeEmoji(emoji){
    const preview_emoji = document.getElementsByClassName('emoji')[0];
    preview_emoji.textContent = emoji;

    const sticky_note = document.getElementById("stickynote");
    sticky_note.setAttribute('emoji', emoji);
}

function clearAll(){
    const preview_emoji = document.getElementsByClassName('emoji')[0];
    preview_emoji.textContent = '🥰';

    const sticky_content_parent = document.getElementsByClassName('sticky-note-content')[0]
    const content = sticky_content_parent.getElementsByTagName('p')[0];
    content.textContent = '';

    const sticky_nickname = document.getElementsByClassName('nickname')[0];
    sticky_nickname.textContent = "";

    
    document.getElementById('nickname').value = "";
    document.getElementById('content').value = "";
}
