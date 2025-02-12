import numpy as np
import cv2

def similarImages(img1, img2, binarize=False):
    if len(img1.shape) > 2:
        img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    if len(img2.shape) > 2:
        img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    
    if binarize:
        _, img1 = cv2.threshold(img1,1,255,cv2.THRESH_BINARY)
        _, img2 = cv2.threshold(img2,1,255,cv2.THRESH_BINARY)
        
    if img1.shape[0] != img2.shape[0] or img1.shape[1] != img2.shape[1]:
        height, width = max(img1.shape[0],img2.shape[0]), max(img1.shape[1],img2.shape[1])
        imge1 = ~np.zeros((height,width),np.uint8)
        imge1[:img1.shape[0],:img1.shape[1]] = img1
        imge2 = ~np.zeros((height,width),np.uint8)
        imge2[:img2.shape[0],:img2.shape[1]] = img2
        img1 = imge1
        img2 = imge2
    
    if binarize:
        ksize = 5
        img1 = cv2.dilate(img1,cv2.getStructuringElement(cv2.MORPH_RECT,(2*ksize+1,2*ksize+1)))
        img2 = cv2.dilate(img2,cv2.getStructuringElement(cv2.MORPH_RECT,(2*ksize+1,2*ksize+1)))
    else:
        ksize = 5
        img1 = cv2.erode(img1,cv2.getStructuringElement(cv2.MORPH_RECT,(2*ksize+1,2*ksize+1)))
        img2 = cv2.erode(img2,cv2.getStructuringElement(cv2.MORPH_RECT,(2*ksize+1,2*ksize+1)))

    # Convert images to floating-point for phase correlation
    img1_f = np.float32(img1)
    img2_f = np.float32(img2)
    img1_f /= 255.0
    img2_f /= 255.0
    if not binarize:
        # Apply Hanning window to avoid edge effects in DFT
        hann_window = cv2.createHanningWindow((img1.shape[1],img1.shape[0]), cv2.CV_64F)
        img1_f = img1 * hann_window
        img2_f = img2 * hann_window

    # Perform phase correlation
    shift, response = cv2.phaseCorrelate(img1_f, img2_f)
    
    return response
    
if __name__ == '__main__':
    img1 = np.zeros((190,200,3),np.uint8)
    cv2.circle(img1,(100,100),50,(255,255,255),5)
    img2 = np.zeros((200,190,3),np.uint8)
    cv2.circle(img2,(120,120),50,(255,255,255),5)
    img3 = np.zeros((200,200,3),np.uint8)
    cv2.rectangle(img3,(80,80,40,40),(255,255,255),5)
    print(similarImages(img1,img1,binarize=True))
    print(similarImages(img1,img2,binarize=True))
    print(similarImages(img1,img3,binarize=True))
    print(similarImages(img2,img3,binarize=True))
    
    """
    img1 = cv2.imread('img1.png')
    img2 = cv2.imread('img2.png')
    print(similarImages(img1,img2))
    print(similarImages(img1,img1))
    img2[:,:,:]=255
    print(similarImages(img1,img2))
    img2[:,:,:]=0
    print(similarImages(img1,img2))
    """
    
    """
    from drawingExtraction import extract_trajectories, visualize_trajectories
    img1 = cv2.imread('img1.png')
    img2 = cv2.imread('img2.png')
    trajectories1 = extract_trajectories(img1)
    trajectories2 = extract_trajectories(img2)
    visual1 = visualize_trajectories(trajectories1,img1.shape)
    visual2 = visualize_trajectories(trajectories2,img2.shape)
    print(similarImages(visual1,visual2,binarize=True))
    """