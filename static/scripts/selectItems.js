function setCurrentField(field_selected, field_name) {
    const field_list = ['image-field', 'icon-field', 'audio-field', 'video-field', 'gif-field'];
    const choices = ['image', 'video', 'audio'];

    for (let i=0; i<field_list.length; i++) {
        if (field_list[i] == field_selected)
            document.getElementById(field_list[i]).style.display = 'block';
        else
            document.getElementById(field_list[i]).style.display = 'none';
    }
    
    for (let i=0; i<choices.length; i++) {
        if (choices[i] == field_name)
            document.getElementById(choices[i]).required = true;
        else
            document.getElementById(choices[i]).required = false;
    }
}

function unsetFields() {
    const field_list = ['image-field', 'icon-field', 'audio-field', 'video-field', 'gif-field'];

    for (let i=0; i<field_list.length; i++) {
        document.getElementById(field_list[i]).style.display = 'none';
    }
}

function selectFormatsOption() {
    const field_show = document.getElementById("mode").value;
    
    if (field_show === 'Image') {
        setCurrentField('image-field', 'image');
        if (document.getElementById('image').value === 'ico')
            document.getElementById('icon-field').style.display = 'block';
        else
            document.getElementById('icon-field').style.display = 'none';
    }
    else if (field_show === 'Audio') {
        setCurrentField('audio-field', 'audio');
    }
    else if (field_show === 'Video') {
        setCurrentField('video-field', 'video');
        if (document.getElementById('video').value === 'gif')
            document.getElementById('gif-field').style.display = 'block';
        else
            document.getElementById('gif-field').style.display = 'none';
    }
    else {
        unsetFields();
    }
}