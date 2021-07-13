import numpy as np
import cv2
import time
from directkeys import ReleaseKey, PressKey, W, A, S, D
from draw_lanes import draw_lanes
from grabscreen import grab_screen

def roi(img, vertices):
    # blank mask
    mask = np.zeros_like(img)

    # filling pixels inside the polygon defined by "vertices" with the fill color 
    cv2.fillPoly(mask, vertices, 255)

    # returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_img(image):
    original_image = image

    # convert to gray
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # edge detection
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    vertices = np.array([[10,500],[10,300],[300,200],[500,200],[800,300],[800,500],
                         ], np.int32)
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
    processed_img = roi(processed_img, [vertices])

    # Find edges of street
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 100, 5)

    m1 = 0
    m2 = 0
    try:
        l1, l2, m1, m2 = draw_lanes(lines)
        cv2.line(original_image, (l1[0], l1[1]), (l1[2], l1[3]), [0,255,0], 30)
        cv2.line(original_image, (l2[0], l2[1]), (l2[2], l2[3]), [0,255,0], 30)
    except Exception as e:
        print(str(e))
        pass

    try:
        for coords in lines:
            coords = coords[0]
            try:
                cv2.line(processed_img, (coords[0], coords[1]), (coords[2], coords[3]), [255,0,0], 3)
            except Exception as e:
                print(str(e))
    except Exception as e:
        pass

    return processed_img, original_image, m1, m2

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    ReleaseKey(A)

def right():
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def slow_ya_roll():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def main():
    for i in reversed(range(0, 4)):
        print(i + 1)
        time.sleep(1)

    last_time = time.time()
    while True:
        # 800x600 windowed mode 
        screen =  grab_screen(region=(0, 40, 800, 640))

        # print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()

        new_screen, original_image, m1, m2 = process_img(screen)
        cv2.imshow("window", new_screen)
        cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))

        if m1 < 0 and m2 < 0:
            right()
        elif m1 > 0 and m2 > 0:
            left()
        straight()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()