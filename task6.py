import numpy as np
from PIL import Image
import random as rnd

def normal(c0: tuple, c1: tuple, c2: tuple):
    x_n = (c1[1] - c2[1]) * (c1[2] - c0[2]) - (c1[1] - c0[1]) * (c1[2] - c2[2])
    y_n = (c1[2] - c2[2]) * (c1[0] - c0[0]) - (c1[0] - c2[0]) * (c1[2] - c0[2])
    z_n = (c1[0] - c2[0]) * (c1[1] - c0[1]) - (c1[1] - c2[1]) * (c1[0] - c0[0])
    
    return (x_n, y_n, z_n)

def scalar(c_n: tuple):
    return c_n[2] / (np.sqrt(c_n[0] ** 2  + c_n[1] ** 2 + c_n[2] ** 2))
    

def bar(x: float, y: float, c0: tuple, c1: tuple, c2: tuple):
    lambda0 = ((x - c2[0]) * (c1[1] - c2[1]) - (c1[0] - c2[0]) * (y - c2[1])) / ((c0[0] - c2[0]) * (c1[1] - c2[1]) - (c1[0] - c2[0]) * (c0[1] - c2[1]))
    lambda1 = ((c0[0] - c2[0]) * (y - c2[1]) - (x - c2[0]) * (c0[1] - c2[1])) / ((c0[0] - c2[0]) * (c1[1] - c2[1]) - (c1[0] - c2[0]) * (c0[1] - c2[1]))
    lambda2 = 1.0 - lambda0 - lambda1
    
    return (lambda0, lambda1, lambda2)


def parse_obj_complete(path):
    vertices = []
    faces = []
    
    with open(path, 'r') as file:
        for line in file:
            line = line.split()
            if len(line) == 0:
                continue
            if line[0] == 'v':
                vertices.append([float(line[1]), float(line[2]), float(line[3])])
            elif line[0] == 'f': 
                face_vertices = []
                for item in line[1:]:
                    vertex_index = int(item.split('/')[0]) - 1 
                    face_vertices.append(vertex_index)
                faces.append(face_vertices)
    
    return vertices, faces

class BresenhamDrawer:
    def __init__(self):
        pass
    
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

def calculate_model_bounds(vertices):
    if not vertices:
        return 0, 0, 0, 0
    
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    
    return min(xs), max(xs), min(ys), max(ys)

def draw_all_edges_bresenham(vertices, faces, output_path, image_size=1000):
    H = W = image_size
    
    image_array = np.zeros((H, W, 3), dtype=np.uint8)
    
    min_x, max_x, min_y, max_y = calculate_model_bounds(vertices)
    model_width = max_x - min_x
    model_height = max_y - min_y
    
    scale_x = (W * 0.9) / max(model_width, 0.001)
    scale_y = (H * 0.9) / max(model_height, 0.001)
    scale = min(scale_x, scale_y)
    
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    offset_x = W // 2 - center_x * scale
    offset_y = H // 2 - center_y * scale
    z_buf = np.full((H, W), 1000000, dtype=np.float32)
    
    for face in faces:
        
        
        v1_idx = face[0]
        v2_idx = face[1]
        v3_idx = face[2]
        
        x1, y1, z1 = vertices[v1_idx]
        x2, y2, z2 = vertices[v2_idx]
        x3, y3, z3 = vertices[v3_idx]
        
        c = scalar(normal((x1, y1, z1), (x2, y2, z2), (x3, y3, z3)))
        
        if(c >= 0): continue
        
        img_x1 = x1 * scale + offset_x
        img_y1 = y1 * scale + offset_y
        img_x2 = x2 * scale + offset_x
        img_y2 = y2 * scale + offset_y
        img_x3 = x3 * scale + offset_x
        img_y3 = y3 * scale + offset_y
        
        x_min = min(img_x1, img_x2, img_x3)
        y_min = min(img_y1, img_y2, img_y3)
        x_max = max(img_x1, img_x2, img_x3)
        y_max = max(img_y1, img_y2, img_y3)
        
        #if(x_min <0):x_min = 0
        #if(y_min<0): y_min = 0
        color = (-255 * c, -255 * c, -255 * c)
        #color = (rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))
        
        
        for x in range(int(np.floor(x_min)), int(np.ceil(x_max))):
            for y in range(int(np.floor(y_min)), int(np.ceil(y_max))):
                cord = bar(x, y, (img_x1, img_y1), (img_x2, img_y2), (img_x3, img_y3))
                if(cord[0] >= 0 and cord[1] >= 0 and cord[2] >= 0): 
                    z = cord[0] * z1 + cord[1] * z2 + cord[2] * z3
                    if (z < z_buf[H - y, x]):
                        image_array[H - y, x] = color
                        z_buf[H - y, x] = z
        
      

    
    
    image = Image.fromarray(image_array, 'RGB')
    image.save(output_path)


def main():
    obj_path = './obj/model_1.obj'
    vertices, faces = parse_obj_complete(obj_path)

    draw_all_edges_bresenham(vertices, faces, './assets/rab2.png')
    

if __name__ == "__main__":
    main()