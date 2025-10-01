import numpy as np
from PIL import Image

def parse_obj_vertices(path):
    coords = []
    with open(path, 'r') as file:
        for line in file:
            line = line.split()
            if len(line) == 0:
                continue
            if line[0] == 'v':
                coords.append([float(line[1]), float(line[2])])
    return coords

def draw_vertices_with_auto_scaling(vertices, output_path):
    H = W = 1000
    
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    model_width = max_x - min_x
    model_height = max_y - min_y
    
    scale_x = (W * 0.8) / max(model_width, 0.001)
    scale_y = (H * 0.8) / max(model_height, 0.001)
    scale = min(scale_x, scale_y)
    
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    
    offset_x = W // 2 - center_x * scale
    offset_y = H // 2 - center_y * scale
    
    image_array = np.zeros((H, W, 3), dtype=np.uint8)
    color = (255, 255, 255)
    
    for x, y in vertices:
        img_x = int(x * scale + offset_x)
        img_y = int(y * scale + offset_y)
        
        image_array[H - img_y, img_x] = color
    
    image = Image.fromarray(image_array, 'RGB')
    image.save(output_path)

def main():
    vertices = parse_obj_vertices('./obj/model_1.obj')
    
    draw_vertices_with_auto_scaling(vertices, './assets/rab1.png')


if __name__ == "__main__":
    main()
    