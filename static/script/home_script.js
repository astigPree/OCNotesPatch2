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

function homePrePageLoad() {
        
    // Remove any buttons if no sticky notes display
    var note_list = document.getElementsByClassName('sticky-notes-container')[0].getElementsByClassName('sticky-note');
    if (note_list.length < 1){
        const nextPageBut = document.getElementById('next-page-button');
        if (nextPageBut.onclick){
            nextPageBut.onclick = null;
            nextPageBut.style.opacity = 0;
        }
        const prevPageBut = document.getElementById('prev-page-button');
        if (prevPageBut.onclick){
            prevPageBut.onclick = null;
            prevPageBut.style.opacity = 0;
        }
    }

    // Get the current date and display it in the p tag
    const currentDateElement = document.getElementById('currentDate');
    currentDateElement.textContent = getCurrentDateFormatted();
}

function changeTemplate(url) {
    window.location.href = url;
}

function onetimeChangeOnTheMainScript(nickname_font, content_font, note_id) {
    const selected_font = getComputedStyle(document.documentElement).getPropertyValue(nickname_font);
    const sticky_nickname = document.getElementById(`nickname-${note_id}`);
    sticky_nickname.style.fontFamily = selected_font;
    const selected_content_font = getComputedStyle(document.documentElement).getPropertyValue(content_font);
    const sticky_content_parent = document.getElementById(`content-${note_id}`)
    const content = sticky_content_parent.getElementsByTagName('p')[0];
    content.style.fontFamily = selected_content_font;

}

function getStartId(){
    var note_list = document.getElementsByClassName('sticky-notes-container')[0].getElementsByClassName('sticky-note');
        
    // reverse because the reading is the upper Id to lower id
    if (direction === "down"){
        var startId = note_list[0].getAttribute('note_id');
    } else {
        if (1 < note_list.length){
            startId = note_list[note_list.length - 1].getAttribute('note_id');
        } else {
            startId = note_list[0].getAttribute('note_id');
        }
    }

    return startId
}

function configuringPageButton(isDatabaseHasData ){
    // Removing a function on the buttons in next page and previus page
    if ( isDatabaseHasData ){
        const nextPageBut = document.getElementById('next-page-button');
        if (!nextPageBut.onclick){
            nextPageBut.setAttribute('onclick' , "fetchStickyNotes('up')");
            nextPageBut.style.opacity = 1;
        }
        const prevPageBut = document.getElementById('prev-page-button');
        if (!prevPageBut.onclick){
            prevPageBut.setAttribute('onclick' , "fetchStickyNotes('down')");
            prevPageBut.style.opacity = 1;
        }
        
    } else {
        if (direction == "up" ){
            const nextPageBut = document.getElementById('next-page-button');
            if (nextPageBut.onclick){
                nextPageBut.onclick = null;
                nextPageBut.style.opacity = 0;
            }
        } else {
            const prevPageBut = document.getElementById('prev-page-button');
            if (prevPageBut.onclick){
                prevPageBut.onclick = null;
                prevPageBut.style.opacity = 0;
            }
        }
    } 
}


function displayNote(note , notesList){
    notesList.append(
        `<div class="sticky-note" note_id="${ note.note_id }" >

            <div class="note-header">
                <p class="nickname" id="nickname-${note.note_id}" style="color: ${note.nickname_color};" >
                    ${ note.nickname }
                </p>
                <p class="emoji">${ note.emoji }</p>
                <span class="pin"></span>
            </div>

            <div class="sticky-note-content" id="content-${note.note_id}">
                <p style="color:${ note.content_color };">
                    ${ note.content }
                </p>
            </div>
        </div>
        `
    );

    onetimeChangeOnTheMainScript(note.nickname_font , note.content_font, note.note_id);
    
}

function updatePageNumberAndMove(){
    const pageNum = document.getElementById("page-number");
    if (direction == "down"){
        pageNum.innerHTML = `${parseInt(pageNum.innerHTML, 10 ) - 1}`;
    } else {
        pageNum.innerHTML = `${parseInt(pageNum.innerHTML, 10 ) + 1}`;
    }

    const headBarLoc = document.getElementById('headbar-location');
    headBarLoc.scrollIntoView({behavior:'smooth'});
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
    sticky_nickname.setAttribute('nickname_color' , selected_color);
};

function updateNickname(){
    
    var form_nickname = document.getElementById('nickname');
    validateInput(form_nickname);

    const sticky_nickname = document.getElementsByClassName('nickname')[0];
    sticky_nickname.textContent = form_nickname.value;
}

function changeNicknameFont(font_used){
    const font_index = fontStylesIndex[font_used];
    const selected_font = getComputedStyle(document.documentElement).getPropertyValue(font_used);
    const sticky_nickname = document.getElementsByClassName('nickname')[0];
    sticky_nickname.style.fontFamily = selected_font;
    sticky_nickname.setAttribute('nickname_font', font_index);
}

function updateContent(){
    
    var form_content = document.getElementById('content');
    validateInput(form_content);

    const sticky_content_parent = document.getElementsByClassName('sticky-note-content')[0]
    const content = sticky_content_parent.getElementsByTagName('p')[0];
    content.textContent = form_content.value;
}

function changeContentFont(font_used){
    const selected_font = getComputedStyle(document.documentElement).getPropertyValue(font_used);
    const sticky_content_parent = document.getElementsByClassName('sticky-note-content')[0]
    const content = sticky_content_parent.getElementsByTagName('p')[0];
    content.style.fontFamily = selected_font;
    content.setAttribute('content_font' , fontStylesIndex[font_used]);
}

function changeContentColor(selected_color){
    const sticky_content_parent = document.getElementsByClassName('sticky-note-content')[0]
    const content = sticky_content_parent.getElementsByTagName('p')[0];
    content.style.color = selected_color;
    content.setAttribute('content_color', selected_color);
};

function changeNoteColor(selected_color){
    const sticky_note = document.getElementsByClassName('sticky-note')[0];
    sticky_note.style.backgroundColor = noteColor[selected_color];
    sticky_note.setAttribute('note_color', selected_color);
    console.log(selected_color);
}

function changeEmoji(emoji){
    const preview_emoji = document.getElementsByClassName('emoji')[0];
    preview_emoji.textContent = emoji;
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
