import cv2
import os.listdir, os.remove

def init_cam():
    ip_l = input("Last of webcam ip: ")
    cam = cv2.VideoCapture("http://192.168.12."+ip_l+":4747/video")
    return cam

def release_cam(cam):
    cam.release()

def capture(cam):
    
    if len(os.listdir("captured/")) > 0:
        t = input("Captured directory is not empty. Use that or capture new? [Y/n]: ")
        if t=='y' or t=='Y' or t=='':
            for f in os.listdir("captured/"):
                os.remove("captured/"+f)
        else:
            return
    
    cv2.namedWindow("test")
    cv2.resizeWindow("test", 200, 200)
    c = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k%256 == 27:
            print("Escape pressed, closing...")
            break
        elif k%256 == 32:
            cv2.imwrite("captured/cap"+str(c)+".jpg", frame)
            print("captured/cap"+str(c)+".jpg saved..")
            c += 1

    cv2.destroyAllWindows()
        
if __name__ == "__main__":
    capture(init_cam())