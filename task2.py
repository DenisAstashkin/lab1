import numpy as np
import math
from PIL import Image

class LineDrawer:
    def __init__(self):
        pass
    def dotted_line1(self, image, x0, y0, x1, y1, count, color):
        step = 1.0 / count
        for t in np.arange(0, 1, step):
            x = round ((1.0 - t)*x0 + t*x1)
            y = round ((1.0 - t)*y0 + t*y1)
            image[y,x] = color

    def dotted_line2(self, image, x0, y0, x1, y1, color):
        count = math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
        step = 1.0/count
        for t in np.arange(0, 1, step):
            x = round ((1.0 - t)*x0 + t*x1)
            y = round ((1.0 - t)*y0 + t*y1)
            image[y,x] = color

    def x_loop_line(self, image, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        for x in range(x0, x1):
            t = (x - x0)/(x1 - x0)
            y = round((1.0 - t)*y0 + t*y1)
            image[y,x] = color

    def x_loop_line_h1(self, image, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        if(x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        for x in range (x0, x1):
            t = (x - x0)/(x1 - x0)
            y = round((1.0 - t)*y0 + t*y1)
            image[y,x] = color      

    def x_loop_line_h2(self, image, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        if(x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        xchange = False
        if(abs(x0 - x1) < abs(y0 - y1)):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            xchange = True
        for x in range (x0, x1):
            t = (x - x0)/(x1 - x0)
            y = round((1.0 - t)*y0 + t*y1)
            if(xchange):
                image[x,y] = color
            else:
                image[y,x] = color

    def x_loop_line2(self, image, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        if(x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        xchange = False
        if(abs(x0 - x1) < abs(y0 - y1)):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            xchange = True
        y = y0
        dy = abs(y1 - y0)/(x1 - x0)
        derror = 0.0
        y_update = 1 if y1 > y0 else -1
        for x in range (x0, x1):
            if(xchange):
                image[x,y] = color
            else:
                image[y,x] = color
            derror += dy
            if(derror > 0.5):
                derror -= 1.0
                y += y_update

    def x_loop_line2m(self, image, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        if(x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        xchange = False
        if(abs(x0 - x1) < abs(y0 - y1)):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            xchange = True
        y = y0
        dy = 2.0*(x1 - x0)*abs(y1 - y0)/(x1 - x0)
        derror = 0.0
        y_update = 1 if y1 > y0 else -1
        for x in range (x0, x1):
            if(xchange):
                image[x,y] = color
            else:
                image[y,x] = color
            derror += dy
            if(derror > 2.0*(x1 - x0)*0.5):
                derror -= 2.0*(x1 - x0)*1.0
                y += y_update      

    def bresenham_line(self, image, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        if(x0 > x1):
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        xchange = False
        if(abs(x0 - x1) < abs(y0 - y1)):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            xchange = True
        y = y0
        dy = 2*abs(y1 - y0)
        derror = 0
        y_update = 1 if y1 > y0 else -1
        for x in range (x0, x1):
            if(xchange):
                image[x,y] = color
            else:
                image[y,x] = color
            derror += dy
            if(derror > (x1 - x0)):
                derror -= 2*(x1 - x0)
                y += y_update           
                
def main():
    W, H = 200, 200
    image_array = np.zeros((H, W, 3), dtype=np.uint8)
    
    
    drawer = LineDrawer()
    
    blue = (0, 0, 255)
    for i in range(0, 12):
        drawer.dotted_line1(image_array, 100, 100, (100 + 95 * np.cos(2 * np.pi * i / 13)),
                                                    100 + 95 * np.sin(2 * np.pi * i / 13), 200, blue)
    
    gradient_image = Image.fromarray(image_array, mode='RGB')
    gradient_image.save('./assets/star1.png')
    for i in range(0, 12):
        drawer.dotted_line2(image_array, 100, 100, (100 + 95 * np.cos(2 * np.pi * i / 13)),
                                                    100 + 95 * np.sin(2 * np.pi * i / 13), blue)
    
    gradient_image = Image.fromarray(image_array, mode='RGB')
    gradient_image.save('./assets/star2.png')
    for i in range(0, 12):
        drawer.x_loop_line(image_array, 100, 100, (100 + 95 * np.cos(2 * np.pi * i / 13)),
                                                    100 + 95 * np.sin(2 * np.pi * i / 13), blue)
    
    gradient_image = Image.fromarray(image_array, mode='RGB')
    gradient_image.save('./assets/star3.png')
    for i in range(0, 12):
        drawer.x_loop_line_h1(image_array, 100, 100, (100 + 95 * np.cos(2 * np.pi * i / 13)),
                                                    100 + 95 * np.sin(2 * np.pi * i / 13), blue)
    
    gradient_image = Image.fromarray(image_array, mode='RGB')
    gradient_image.save('./assets/star4.png')
    for i in range(0, 12):
        drawer.x_loop_line_h2(image_array, 100, 100, (100 + 95 * np.cos(2 * np.pi * i / 13)),
                                                    100 + 95 * np.sin(2 * np.pi * i / 13), blue)
    
    gradient_image = Image.fromarray(image_array, mode='RGB')
    gradient_image.save('./assets/star5.png')
    for i in range(0, 12):
        drawer.x_loop_line2(image_array, 100, 100, (100 + 95 * np.cos(2 * np.pi * i / 13)),
                                                    100 + 95 * np.sin(2 * np.pi * i / 13), blue)
    
    gradient_image = Image.fromarray(image_array, mode='RGB')
    gradient_image.save('./assets/star6.png')
    for i in range(0, 12):
        drawer.x_loop_line2m(image_array, 100, 100, (100 + 95 * np.cos(2 * np.pi * i / 13)),
                                                    100 + 95 * np.sin(2 * np.pi * i / 13), blue)
    
    gradient_image = Image.fromarray(image_array, mode='RGB')
    gradient_image.save('./assets/star7.png')
    for i in range(0, 12):
        drawer.bresenham_line(image_array, 100, 100, (100 + 95 * np.cos(2 * np.pi * i / 13)),
                                                    100 + 95 * np.sin(2 * np.pi * i / 13), blue)

    
    gradient_image = Image.fromarray(image_array, mode='RGB')
    gradient_image.save('./assets/star8.png')
    
    
if __name__ == '__main__':
    main()