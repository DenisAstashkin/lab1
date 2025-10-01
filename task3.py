def parser_obj(path):
    coords = []
    with open(path, 'r') as file:
        for i in file:
            i = i.split()
            if(i[0] == 'v'):
                coords.append([float(i[1]), float(i[2]), float(i[3])])
    return coords
            

def main():
    print(parser_obj('./obj/model_1.obj'))
    
if __name__ == '__main__':
    main()