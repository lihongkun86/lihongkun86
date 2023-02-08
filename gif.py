# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:11:08 2023

@author: lihongkun
"""

from moviepy.editor import VideoFileClip

videoClip = VideoFileClip("my-life.mp4")

videoClip.write_gif("my-life.gif")