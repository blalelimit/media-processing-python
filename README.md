# media-processing-python
A python project that processes image, audio, and video files using [Pillow](https://pillow.readthedocs.io/en/stable/) and [FFmpeg](https://ffmpeg.org/). The [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) wrapper was used for the project.

# Overview
* File Format Converter for image, audio, video files.
* Includes audio/video processing features such as merging audio and video codecs, etc.
* Conversion of pdf to image formats is also included.
* The FFmpeg executable must first be installed and added to PATH, if video processing is needed.

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
* notebooks/main.ipynb -> Jupyter Notebook with same functionality as the scripts.
* notebooks/probe.ipynb -> Jupyter Notebook for audio and video probing.


# Scripts
* image_to_image.py -> Image formats converter.
* media_to_media.py -> Convert audio to audio or video to video.
* media_combine.py -> Combines audio and video codecs. Can also be used to replace audio.
* media_process.py -> Processing features for audio and video, such as trimming, concatenation, adding text, or thumbnail generation from video.