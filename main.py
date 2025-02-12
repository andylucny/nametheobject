import time
import os
import signal
import re
import numpy as np
import cv2 as cv
from agentspace import Agent, space, Trigger

from dino import dino_visualization
from clip import image_clip, text_clip, cosine_similarity, clip

def quit():
    os._exit(0)

def signal_handler(signal, frame): 
    quit()
    
signal.signal(signal.SIGINT, signal_handler)

from CameraAgent import CameraAgent
from PerceptionAgent import PerceptionAgent
from LookAroundAgent import LookAroundAgent
from SpeakerAgent import SpeakerAgent
from NamingAgent import NamingAgent
from lips import LipsAgent

CameraAgent('HD Pro Webcam C920',0,'robotEye',fps=10) 
time.sleep(1)
PerceptionAgent('robotEye','clipFeatures','dinoPoints')
time.sleep(1)
LookAroundAgent('dinoPoints','dontLook')
time.sleep(1)
LipsAgent('speaking')
time.sleep(1)
SpeakerAgent('tospeak')
time.sleep(1)
NamingAgent('clipFeatures','tospeak')
time.sleep(1)
