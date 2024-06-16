
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

function getStartId(direction){
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

function configuringPageButton(isDatabaseHasData, direction ){
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

function displayNote(note , notesList , urlFromTemplate){
    notesList.append(
        `
        <div>
            
            <div class="clip">
                <p id="replies-text-${note.note_id}" onclick="changeTemplate('${urlFromTemplate}')">REPLIES</p>
                <svg fill="#B76767" height="200px" width="200px" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <g> <path d="M487.458,271.701C501.632,267.546,512,254.43,512,238.933c0-18.825-15.309-34.133-34.133-34.133H316.083l-7.808-45.662 c20.198-10.906,33.058-28.075,33.058-47.787c0-33.724-37.478-60.151-85.333-60.151c-47.846,0-85.333,26.428-85.333,60.151 c0,19.712,12.868,36.881,33.067,47.787l-7.808,45.662H34.133C15.317,204.8,0,220.109,0,238.933 c0,15.497,10.377,28.612,24.55,32.768L2.722,431.744c-0.998,7.322,1.22,14.72,6.084,20.301c4.855,5.564,11.887,8.755,19.277,8.755 h91.383c4.719,0,8.533-3.814,8.533-8.533c0-18.825,15.317-34.133,34.133-34.133c18.825,0,34.133,15.309,34.133,34.133 c0,4.719,3.823,8.533,8.533,8.533h102.4c4.719,0,8.533-3.814,8.533-8.533c0-18.825,15.317-34.133,34.133-34.133 c18.825,0,34.133,15.309,34.133,34.133c0,4.719,3.823,8.533,8.533,8.533h91.383c7.398,0,14.43-3.191,19.285-8.764 c4.864-5.581,7.083-12.971,6.084-20.292L487.458,271.701z M213.24,204.8l6.639-38.827c10.931,3.516,23.117,5.53,36.122,5.53 c13.005,0,25.199-2.014,36.13-5.53l6.639,38.827H213.24z"></path> </g> </g> </g></svg>
            </div>
            
            <div class="sticky-note"id="sticky-note-${note.note_id}" note_id="${ note.note_id }">

                <div class="note-header">
                    <p class="nickname" id="nickname-${note.note_id}" >${ note.nickname }</p>
                    <p class="emoji">${ note.emoji }</p>
                    <span class="pin" id="pin-${note.note_id}"></span>
                </div>

                <div class="sticky-note-content">
                    <p id="content-${note.note_id}">${ note.content }</p>
                </div>

            </div>

            <div class="reactions">
                <div class="react react-${note.note_id}" onclick="clickReact(this)" >
                    <p>😻</p>
                    <i id="love-num-${note.note_id}" note-id="${note.note_id}" react="1" total="${note.loves}"></i>
                </div>
                <div class="react react-${note.note_id}" onclick="clickReact(this)" >
                    <p>😾</p>
                    <i id="angry-num-${note.note_id}" note-id="${note.note_id}" react="2" total="${note.angries}"></i>
                </div>
                <div class="react react-${note.note_id}" onclick="clickReact(this)" >
                    <p>😿</p>
                    <i id="cry-num-${note.note_id}" note-id="${note.note_id}" react="3" total="${note.cries}"></i>
                </div>
                <div class="react react-${note.note_id}" onclick="clickReact(this)" >
                    <p>🙀</p>
                    <i id="wow-num-${note.note_id}" note-id="${note.note_id}" react="4" total="${note.wows}"></i>
                </div>
            </div>

            <div class="note-date" id="note-date-${note.note_id}">
                ${note.time}
            </div>

        </div>
        `
    )
    
    onetimeChange(
        note.note_id, note.note_color,note.nickname_font, 
        note.nickname_color, note.content_font, note.content_color,
        note.gender
    );
    
}

function updatePageNumberAndMove(direction){
    const pageNum = document.getElementById("page-number");
    if (direction == "down"){
        pageNum.innerHTML = `${parseInt(pageNum.innerHTML, 10 ) - 1}`;
    } else {
        pageNum.innerHTML = `${parseInt(pageNum.innerHTML, 10 ) + 1}`;
    }

    const headBarLoc = document.getElementById('headbar-location');
    headBarLoc.scrollIntoView({behavior:'smooth'});
}
