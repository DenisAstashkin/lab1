import numpy as np
from PIL import Image
import math

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
    
    drawer = BresenhamDrawer()
    
    edge_color = (255, 255, 255)
    
    for face in faces:
        
        for i in range(len(face)):
            v1_idx = face[i]
            v2_idx = face[(i + 1) % len(face)]
            
            x1, y1, z1 = vertices[v1_idx]
            x2, y2, z2 = vertices[v2_idx]
            
            img_x1 = x1 * scale + offset_x
            img_y1 = y1 * scale + offset_y
            img_x2 = x2 * scale + offset_x
            img_y2 = y2 * scale + offset_y
            
            drawer.bresenham_line(image_array, img_x1, W - img_y1, img_x2, W - img_y2, edge_color)
    
    
    
    image = Image.fromarray(image_array, 'RGB')
    image.save(output_path)


def main():
    obj_path = './obj/model_1.obj'
    vertices, faces = parse_obj_complete(obj_path)

    draw_all_edges_bresenham(vertices, faces, './assets/rab2.png')
    

if __name__ == "__main__":
    main()