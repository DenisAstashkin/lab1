import numpy as np
from PIL import Image

def spin(coord, alpha, beta, gama, tx, ty, tz):
    R = np.matmul(np.array([[1, 0, 0], 
             [0, np.cos(alpha), np.sin(alpha)], 
             [0, -np.sin(alpha), np.cos(alpha)]]),
    np.array([[np.cos(beta), 0, np.sin(beta)], 
             [0, 1, 0], 
             [-np.sin(beta), 0, np.cos(beta)]]),
    np.array([[np.cos(gama), np.sin(gama), 0], 
             [-np.sin(gama), np.cos(gama), 0], 
             [0, 0, 1]]))
    ress = []
    for i in coord:
        c = np.matmul(np.array([i[0] - tx, i[1] - ty, i[2]]), R) + np.array([0, 0, tz])
        ress.append([float(c[0]), float(c[1]), float(c[2])])
    return ress

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

def calculate_model_bounds(vertices):
    if not vertices:
        return 0, 0, 0, 0
    
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    
    return min(xs), max(xs), min(ys), max(ys)

def draw_picture(vertices, faces, output_path, image_size=1000):
    H = W = image_size
    
    image_array = np.zeros((H, W, 3), dtype=np.uint8)
    
    min_x, max_x, min_y, max_y = calculate_model_bounds(vertices)
    model_width = max_x - min_x
    model_height = max_y - min_y
    
    scale_x = (W * 0.5) / max(model_width, 0.001)
    scale_y = (H * 0.5) / max(model_height, 0.001)
    
    scale = min(scale_x, scale_y) * 0.1
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    offset_x = W // 2 
    offset_y = H // 2 
    z_buf = np.full((H, W), 1000000, dtype=np.float32)
    
    vertices = spin(vertices, 0, 90, 0, center_x, center_y, 0.1)
    
    for face in faces:
        
        
        v1_idx = face[0]
        v2_idx = face[1]
        v3_idx = face[2]
        
        x1, y1, z1 = vertices[v1_idx]
        x2, y2, z2 = vertices[v2_idx]
        x3, y3, z3 = vertices[v3_idx]
        
        c = scalar(normal((x1, y1, z1), (x2, y2, z2), (x3, y3, z3)))
        
        if(c >= 0): continue
        
        img_x1 = x1 * scale / z1 + offset_x
        img_y1 = y1 * scale / z1 + offset_y
        img_x2 = x2 * scale / z2 + offset_x
        img_y2 = y2 * scale / z2 + offset_y
        img_x3 = x3 * scale / z3 + offset_x
        img_y3 = y3 * scale / z3 + offset_y
        
        x_min = min(img_x1, img_x2, img_x3)
        y_min = min(img_y1, img_y2, img_y3)
        x_max = max(img_x1, img_x2, img_x3)
        y_max = max(img_y1, img_y2, img_y3)
        
        color = (-255 * c, -255 * c, -255 * c)        
        
        for x in range(int(np.floor(x_min)), int(np.ceil(x_max))):
            for y in range(int(np.floor(y_min)), int(np.ceil(y_max))):
                cord = bar(x, y, (img_x1, img_y1), (img_x2, img_y2), (img_x3, img_y3))
                if(cord[0] >= 0 and cord[1] >= 0 and cord[2] >= 0): 
                    z = cord[0] * z1 + cord[1] * z2 + cord[2] * z3
                    try:
                        if (z < z_buf[H - y, x]):
                            image_array[H - y, x] = color
                            z_buf[H - y, x] = z
                    except:
                        continue
        
      
    
    image = Image.fromarray(image_array, 'RGB')
    image.save(output_path)


def main():
    obj_path = './obj/model_1.obj'
    vertices, faces = parse_obj_complete(obj_path)

    draw_picture(vertices, faces, './assets/rab2.png')
    

if __name__ == "__main__":
    main()