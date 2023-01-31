function selectFormatsOption() {
    const field_show = document.getElementById("mode").value;
    const image_show = document.getElementById('image').value;
    const audio_show = document.getElementById('audio').value;

    if (field_show === 'Image') {
        document.getElementById('image-field').style.display = 'block';
        document.getElementById('audio-field').style.display = 'none';
        document.getElementById('video-field').style.display = 'none';
        document.getElementById('gif-field').style.display = 'none';
        document.getElementById('image').required = true;
        document.getElementById('audio').required = false;
        document.getElementById('video').required = false;

        if (document.getElementById('image').value === 'ico')
            document.getElementById('icon-field').style.display = 'block';
        else
            document.getElementById('icon-field').style.display = 'none';
    }
    else if (field_show === 'Audio') {
        document.getElementById('image-field').style.display = 'none';
        document.getElementById('icon-field').style.display = 'none';
        document.getElementById('audio-field').style.display = 'block';
        document.getElementById('video-field').style.display = 'none';
        document.getElementById('gif-field').style.display = 'none';
        document.getElementById('image').required = false;
        document.getElementById('audio').required = true;
        document.getElementById('video').required = false;
    }
    else if (field_show === 'Video') {
        document.getElementById('image-field').style.display = 'none';
        document.getElementById('icon-field').style.display = 'none';
        document.getElementById('audio-field').style.display = 'none';
        document.getElementById('video-field').style.display = 'block';
        document.getElementById('image').required = false;
        document.getElementById('audio').required = false;
        document.getElementById('video').required = true;

        if (document.getElementById('video').value === 'gif')
            document.getElementById('gif-field').style.display = 'block';
        else
            document.getElementById('gif-field').style.display = 'none';
    }
    else {
        document.getElementById('image-field').style.display = 'none';
        document.getElementById('icon-field').style.display = 'none';
        document.getElementById('audio-field').style.display = 'none';
        document.getElementById('video-field').style.display = 'none';
        document.getElementById('gif-field').style.display = 'none';
    }
}