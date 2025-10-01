import numpy as np
from PIL import Image

H = 400
W = 600

def zero_pic():
    matrix = np.zeros((H, W), dtype=np.uint8)
    black_image = Image.fromarray(matrix, mode='L')
    black_image.save('./assets/black_image.png')
    
def white_pic():
    matrix = np.full((H, W), 255, dtype=np.uint8)
    white_image = Image.fromarray(matrix, mode='L')
    white_image.save('./assets/white_image.png')

def red_pic():
    matrix = np.full((H, W, 3), (255, 0, 0), dtype=np.uint8)
    red_image = Image.fromarray(matrix, mode='RGB')
    red_image.save('./assets/red_image.png')

def grad_pic():
    x_c = np.arange(W)
    y_c = np.arange(H)
    X, Y = np.meshgrid(x_c, y_c)
    
    grad_v = (X + Y) / (W + H) * 256 # (X + Y) % 256 - делает резкие переходы градиента 
    
    gradient_matrix = np.zeros((H, W, 3), dtype=np.uint8)
    
    gradient_matrix[:, :, 0] = (X + Y) / (W + H) * 144
    gradient_matrix[:, :, 1] = (0.1 * X + Y) / (W + H) * 155
    gradient_matrix[:, :, 2] = (0.9 * X + Y) / (W + H) * 256
        
    gradient_image = Image.fromarray(gradient_matrix, mode='RGB')
    gradient_image.save('./assets/gradient_image.png')

def main():
    zero_pic()
    white_pic()
    red_pic()
    grad_pic()
    

if __name__ == '__main__':
    main()