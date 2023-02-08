# Referece: https://github.com/arpanneupane19/Flask-File-Uploads/blob/main/main.py
from os import path, remove
from flask import Flask, request, render_template, flash, session
from flask_uploads import UploadSet, IMAGES, AUDIO
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename, redirect
from wtforms.validators import InputRequired
from uuid import uuid4
from utils.convert import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/inputs'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

images = IMAGES + ('ico',)
audios = AUDIO + ('opus', 'm4a')
videos = ('mp4', 'mkv', 'avi', 'mov')
ALLOWED_EXTENSIONS = images + audios + videos
media = UploadSet('media', extensions=ALLOWED_EXTENSIONS, default_dest=None)


class UploadFileForm(FlaskForm):
    file = FileField("file", validators=[InputRequired()])
    submit = SubmitField("Upload File")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, random_uuid, input_filename):
    # Saves the file to static/outputs
    file.save(path.join(path.abspath(path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                           secure_filename(f'{random_uuid}.{input_filename[-1]}')))

def delete_file(filename):
    if path.exists(f'static/inputs/{filename}'):
       remove(f'static/inputs/{filename}')


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    return render_template('index.html')


@app.route('/upload', methods=['GET', "POST"])
def upload():
    # Extract form data
    forms = UploadFileForm()
    mode_form = request.form.get("mode")
    image_form = request.form.get("image")
    icon_form = request.form.get("icon")
    audio_form = request.form.get("audio")
    video_form = request.form.get("video")
    gif_form = request.form.get("gif")

    # Default output text
    output = 'Please input a file'

    if request.method == "POST":
        # Check if form is submitted
        if forms.validate_on_submit():
            file = forms.file.data

            # Check if file form does not have file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            # File does not exist
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            # File exists and extension is allowed
            if file and allowed_file(file.filename):
                input_filename = file.filename.split(".")
                random_uuid = uuid4()

                # Pass the data as session
                session['CURRENT_FILE'] = input_filename
                session['CURRENT_UUID'] = random_uuid

                # Get filenames
                input_filename = session.get('CURRENT_FILE', None)
                random_uuid = session.get('CURRENT_UUID', None)

                # Ask user for mode
                if mode_form == 'Image' and input_filename[-1] in list(images):
                    save_file(file, random_uuid, input_filename)
                    MediaConvert(random_uuid, input_filename, image_form).image_convert(icon_form)
                    output = f'Image file "{input_filename[0]}.{input_filename[-1]}" ' \
                             f'has been converted to ' \
                             f'"{input_filename[0]}.{image_form}"'
                    delete_file(f'{random_uuid}.{input_filename[-1]}')
                elif mode_form == 'Audio' and input_filename[-1] in list(audios):
                    save_file(file, random_uuid, input_filename)
                    MediaConvert(random_uuid, input_filename, audio_form).audio_convert()
                    output = f'Audio file "{input_filename[0]}.{input_filename[-1]}" ' \
                             f'has been converted to ' \
                             f'"{input_filename[0]}.{audio_form}"'
                    delete_file(f'{random_uuid}.{input_filename[-1]}')

                elif mode_form == 'Video' and input_filename[-1] in list(videos):
                    save_file(file, random_uuid, input_filename)
                    MediaConvert(random_uuid, input_filename, video_form).video_convert(gif_form)
                    output = f'Video file "{input_filename[0]}.{input_filename[-1]}" ' \
                             f'has been converted to ' \
                             f'"{input_filename[0]}.{video_form}"'
                    delete_file(f'{random_uuid}.{input_filename[-1]}')

                else:
                    output = 'Invalid selected mode'

            else:
                output = 'Invalid input file format'

    return render_template('upload.html', forms=forms,
                           image_text=images, audio_text=audios, video_text=videos, output=output)


if __name__ == '__main__':
    app.run(debug=True)
