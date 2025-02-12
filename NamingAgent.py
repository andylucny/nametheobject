import numpy as np
import cv2
from agentspace import space, Agent
import time
import os

from clip import image_clip, text_clip, cosine_similarity, clip
from sk import putText

def loadNames(fname):
    with open(fname,'rt',encoding='utf-8') as f:
        return [ line.strip() for line in f.readlines() ]

class NamingAgent(Agent):

    def __init__(self, nameFeatures, nameSpeak, clip_threshold=0.2, judgement_threshold=0.5):
        self.nameFeatures = nameFeatures
        self.nameSpeak = nameSpeak
        self.clip_threshold = clip_threshold
        self.judgement_threshold = judgement_threshold*10
        self.drawing_announced = False
        super().__init__()
    
    def init(self):
        self.sk = loadNames('sk.txt')
        self.en = loadNames('en.txt')
        wipeout_path = 'wipeout.npy'
        if os.path.exists(wipeout_path):
            print('loading wipeout, please wait')
            self.wipeout = np.load(wipeout_path)
            print('wipeout loaded')
        else:
            print('calculating wipeout, please wait')
            self.wipeout = text_clip(self.en)
            np.save(wipeout_path,self.wipeout)
            print('wipeout ready')
        self.judgement = {} # index : -10..10
        self.last_index = -1
        space.attach_trigger(self.nameFeatures,self)

    def speak(self, text):
        space(validity=0.1)[self.nameSpeak] = text

    #def dontLook(self):
    #    space['dontLook'] = True
    #
    #def lookAround(self):
    #    space['dontLook'] = False
        
    def nameIt(self, query):
        top = 3
        probabilities = cosine_similarity(query, self.wipeout)
        indices_above_threshold = np.where(probabilities >= self.clip_threshold)[0]
        filtered_probabilities = probabilities[indices_above_threshold]
        top_filtered_indices = np.argsort(filtered_probabilities)[-top:][::-1]
        top_indices = indices_above_threshold[top_filtered_indices]
        
        for i in top_indices:
            if i not in self.judgement:
                self.judgement[i] = 0

        remove_indices = []
        for i in self.judgement:
            self.judgement[i] = self.judgement[i] * 0.9 + 1 if i in top_indices else -1
            if self.judgement[i] <= -self.judgement_threshold:
                remove_indices.append(i)
                
        for i in remove_indices:
            del self.judgement[i]
        
        promissing = {i:self.judgement[i] for i in top_indices if i in self.judgement}
        index = max(promissing, key=promissing.get, default=-1)
        return index, probabilities[index] if index != -1 else 0.0

    def senseSelectAct(self):
        query = space[self.nameFeatures]
        if query is None:
            return
        
        index, confidence = self.nameIt(query)

        seeing_picture = False
        just_drawing = space['trajectories'] is not None
        if not just_drawing:
            self.drawing_announced = False

        image = space['robotEye']
        if image is not None:
            image = cv2.flip(image,1)
            y = 40
            for choice in self.judgement:
                score = self.judgement[choice]
                if score > 0:
                    color = (0,0,255) if score > self.judgement_threshold else (0,255,255)
                    if space['language'] != 'sk':
                        cv2.putText(image,f'{self.en[choice]} ... {score:.2f}',(10,y),0,1.0,color,2)
                    else:
                        putText(image,f'{self.sk[choice]} ... {score:.2f}',(10,y),0,1.0,color,2)
                    y += 40
            cv2.imshow('Naming',image)
            cv2.waitKey(1)
        
        if index != -1 and index in self.judgement:
            if self.judgement[index] > self.judgement_threshold or seeing_picture:
                if (self.last_index != index or seeing_picture) and \
                    self.en[index] != 'Desk' and self.en[index] != 'Tablet' and self.en[index] != 'laptop' and \
                    self.en[index] != 'Laptop' and self.en[index] != 'Blackboard' and self.en[index] != 'Whiteboard' and \
                    self.en[index] != 'Computer Box' and self.en[index] != 'Storage box' and \
                    self.en[index] != 'Coffee Table': # Desk and others are in the front of the robot

                    print(self.en[index],f'{confidence:.3f} {self.judgement[index]:.2f}')
                    if space(default='en')['language'] == 'sk':
                        text = f'Toto je asi {self.sk[index]}.'
                    else:
                        text = f'Perhaps, this is a{"n" if self.en[index][0] in ["a","e","i","o","u"] else ""} {self.en[index]}.'

                    self.speak(text)
                    self.last_index = index
                    
                    for t in [5,54,543,5432,54321]:
                        if image is not None:
                            cv2.putText(image,f'taking rest {t}',(10,y),0,1.0,color,2)
                            cv2.imshow('Naming',image)
                            cv2.waitKey(1)
                        time.sleep(1)
