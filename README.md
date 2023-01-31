# MediaFormatProcessing
A python project that processes image, audio, and video files using [Pillow](https://pillow.readthedocs.io/en/stable/) and [FFmpeg](https://ffmpeg.org/). The [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) wrapper was used for the project.

# Overview:
* File Format Converter for image, audio, and video files.
* Audio/video processing features such as merging audio and video codecs, etc.
* The FFmpeg executable must first be installed and added to PATH.

# Requirements:
* Python 3
* FFmpeg executable from the official website.
* Flask, Pillow, and ffmpeg-python libraries.

# Features:
* webapp.py -> Webapp deployed using Flask framework
* media_convert.py -> Main method to convert file formats
* processing -> Folder containing python files for audio/video editing.

# Processing folder:
* media_merge.py -> Merges audio and video codecs. Can also be used to replace audio.
* video_flip.py -> Filter to flip the video horizontally or vertically.
* video_quality.py -> Re-encode video with libx265 codec, can be used to reduce video size.
* video_speed.py -> Speed up video.
* video_thumbnail.py -> Generate thumbnail from video (jpg).