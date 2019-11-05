import cv2
from os import listdir, remove
import time

def init_cam(camera_device_str = "0"):
    if len(camera_device_str) <= 3:
        camera_device_str = int(camera_device_str)
    try:
        cam = cv2.VideoCapture(camera_device_str)
    except Exception as e :
        cam = None
        print(e)
    return cam

def release_cam(cam):
    cam.release()

def capture(cam, display_enabled = False, capture_count = 5, capture_delay = 0.5):
    
    if len(listdir("captured/")) > 0:
        t = input("Captured directory is not empty. Use that or capture new? [Y/n]: ")
        if t=='y' or t=='Y' or t=='':
            for f in listdir("captured/"):
                remove("captured/"+f)
        else:
            return
    if display_enabled:
        cv2.namedWindow("test")
        cv2.resizeWindow("test", 200, 200)
    c = 0
    if not display_enabled:
        print("Starting to auto capture " + str(capture_count) + " images with " + str(capture_delay) + " sec delay")
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        if display_enabled:
            cv2.imshow("test", frame)
            k = cv2.waitKey(1)
            if k%256 == 27:
                print("Escape pressed, closing...")
                break
            elif k%256 == 32:
                cv2.imwrite("captured/cap"+str(c)+".jpg", frame)
                print("captured/cap"+str(c)+".jpg saved..")
                c += 1
        else:
            cv2.imwrite("captured/cap"+str(c)+".jpg", frame)
            print("captured/cap"+str(c)+".jpg saved..")
            c += 1
            time.sleep(capture_delay)
            if c >= capture_count:
                break

    cv2.destroyAllWindows()
        
if __name__ == "__main__":
    capture(init_cam(), display_enabled = True)