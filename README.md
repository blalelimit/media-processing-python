# MediaFormatProcessing
A python project that processes image, audio, and video files using [Pillow](https://pillow.readthedocs.io/en/stable/) and [FFmpeg](https://ffmpeg.org/). The [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) wrapper was used for the project.

# Overview
* File Format Converter for image, audio, and video files.
* Audio/video processing features such as merging audio and video codecs, etc.
* The FFmpeg executable must first be installed and added to PATH.

# Requirements
* Python 3
* FFmpeg executable from the official website.
* Flask, Pillow, ffmpeg-python, and other libraries (for webapp).
* You can install the packages in the requirements.txt file.
```sh
  python -m pip install -r requirements.txt
```
* If you wish to use the webapp, the packages can be installed through the requirements_webapp.txt file.
```sh
  python -m pip install -r requirements_webapp.txt
```

# Features
* webapp.py -> Webapp deployed using Flask framework
* media_convert.py -> Main method to convert file formats
* processing -> Folder containing python files for audio/video editing.

# Convert
* image_to_image -> Image formats converter.
* media_to_image -> Convert audio to audio or video to video.

# Processing folder
* audio_speed -> Speed up audio, re-encodes with aac codec.
* media_merge.py -> Merges audio and video codecs. Can also be used to replace audio.
* video_flip.py -> Filter to flip the video horizontally or vertically.
* video_quality.py -> Re-encode video with libx265 codec, can be used to reduce video size.
* video_speed.py -> Speed up video, includes audio, re-encodes with libx264 and aac codec.
* video_thumbnail.py -> Generate thumbnail from video (jpg).