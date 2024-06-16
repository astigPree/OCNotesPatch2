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

function genderIcon(gender, iconColor){
    if (gender == "1"){
        return `<svg id="gender-icon" fill="${iconColor}" viewBox="-25.6 -25.6 307.20 307.20" id="Flat" xmlns="http://www.w3.org/2000/svg" stroke="#791717" transform="rotate(0)"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round" stroke="#CCCCCC" stroke-width="1.536"></g><g id="SVGRepo_iconCarrier"> <path d="M227.9978,39.95557q-.00219-.56984-.05749-1.13819c-.018-.18408-.05237-.36279-.07849-.54443-.02979-.20557-.05371-.41211-.09424-.61621-.04029-.20362-.09607-.40088-.14649-.60059-.04541-.18017-.08484-.36084-.13867-.53906-.05884-.19434-.13159-.38135-.19971-.57129-.06445-.17969-.12353-.36084-.19677-.5376-.07349-.17724-.15967-.34668-.24109-.51953-.08582-.18213-.16687-.36621-.26257-.54492-.088-.16455-.18824-.32031-.2837-.48047-.10534-.17627-.2052-.355-.32031-.52685-.11572-.17334-.24475-.33545-.369-.502-.11-.14746-.21252-.29834-.3302-.4414-.23462-.28614-.4834-.55957-.74316-.82227-.01782-.01807-.03247-.03809-.05054-.05615-.01953-.01953-.041-.03565-.06067-.05469-.26123-.25781-.53271-.50537-.81653-.73828-.14794-.12158-.30383-.22754-.45605-.34082-.16138-.12061-.31885-.24561-.48645-.35791-.17725-.11865-.36108-.22168-.54309-.33008-.15442-.0918-.30518-.189-.46411-.27392-.18311-.09815-.37134-.18116-.55811-.269-.16846-.07959-.334-.16357-.50659-.23486-.18042-.0752-.36475-.13525-.54785-.20068-.18652-.0669-.37073-.13868-.56152-.19629-.18189-.05518-.3667-.09571-.55066-.14161-.19568-.04931-.389-.10449-.58851-.144-.20935-.041-.42077-.06592-.63171-.09619-.17688-.02539-.351-.05908-.53027-.07666q-.56837-.05567-1.13953-.05762c-.01465,0-.02893-.002-.0437-.002H168a12,12,0,0,0,0,24h19.02905l-32.7334,32.7334a83.9988,83.9988,0,1,0,16.971,16.97021L204,68.9707V88a12,12,0,0,0,24,0V40C228,39.98486,227.9978,39.97021,227.9978,39.95557ZM146.42627,194.42676a59.97169,59.97169,0,1,1,0-84.85352A60.06666,60.06666,0,0,1,146.42627,194.42676Z"></path> </g></svg>`
    }
    if (gender == "2"){
        return `<svg id="gender-icon" fill="${iconColor}" viewBox="0 0 256 256" id="Flat" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M212,96a84,84,0,1,0-96,83.12891V196H88a12,12,0,0,0,0,24h28v20a12,12,0,0,0,24,0V220h28a12,12,0,0,0,0-24H140V179.12891A84.119,84.119,0,0,0,212,96ZM68,96a60,60,0,1,1,60,60A60.06812,60.06812,0,0,1,68,96Z"></path> </g></svg>`
    }
    return `<svg id="gender-icon" fill="${iconColor}" viewBox="0 0 256 256" id="Flat" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M219.9978,23.95557q-.00219-.56984-.05749-1.13819c-.018-.18408-.05237-.36279-.07849-.54443-.02979-.20557-.05371-.41211-.09424-.61621-.04029-.20362-.09607-.40088-.14649-.60059-.04541-.18017-.08484-.36084-.13867-.53906-.05884-.19434-.13159-.38135-.19971-.57129-.06445-.17969-.12353-.36084-.19677-.5376-.07349-.17724-.15967-.34668-.24109-.51953-.08582-.18213-.16687-.36621-.26257-.54492-.088-.16455-.18824-.32031-.2837-.48047-.10534-.17627-.2052-.355-.32031-.52685-.11572-.17334-.24475-.33545-.369-.502-.11-.14746-.21252-.29834-.3302-.4414-.23462-.28614-.4834-.55957-.74316-.82227-.01782-.01807-.03247-.03809-.05054-.05615-.01831-.01856-.03857-.0332-.05688-.05127q-.39441-.38966-.82227-.74317c-.13965-.11474-.28686-.21435-.43042-.32177-.16992-.127-.33606-.25879-.51269-.377-.16883-.11328-.34424-.21093-.51734-.31445-.16333-.09765-.32324-.20019-.49145-.29-.1731-.09277-.3512-.1709-.52759-.25439-.17871-.08448-.35462-.17383-.538-.24951-.16932-.07032-.34229-.12647-.514-.18848-.19751-.07129-.39307-.14649-.59534-.208-.16882-.05078-.34045-.08789-.51086-.13135-.20874-.05322-.41529-.11132-.62818-.15332-.19055-.03759-.383-.05957-.57507-.08789-.19544-.02881-.38831-.06494-.58679-.08447-.33252-.03271-.666-.04541-.99988-.05078C208.11853,12.0083,208.0603,12,208,12H172a12,12,0,0,0,0,24h7.0293l-15.051,15.05127A71.97526,71.97526,0,1,0,108,178.981V192H88a12,12,0,0,0,0,24h20v16a12,12,0,0,0,24,0V216h20a12,12,0,0,0,0-24H132V178.981A71.928,71.928,0,0,0,180.27783,68.69287L196,52.9707V60a12,12,0,0,0,24,0V24C220,23.98486,219.9978,23.97021,219.9978,23.95557ZM120,156a48,48,0,1,1,48-48A48.05468,48.05468,0,0,1,120,156Z"></path> </g></svg>`
}

function updateGenderIcon(gender){
    const sticky_note = document.getElementsByClassName('sticky-note')[0];
    sticky_note.setAttribute('gender', gender);

    const selected_color = sticky_note.getAttribute('note_color');

    const gender_tag = document.getElementById("pin-gender");
    gender_tag.innerHTML = genderIcon(gender, noteColor[selected_color]);
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
    
    const gender = document.getElementById("pin-gender");
    gender.innerHTML = genderIcon(sticky_note.getAttribute("gender"), noteColor[selected_color]);

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

    const gender = document.getElementById("pin-gender");
    gender.innerHTML = genderIcon("1", "#f9f485");

}
