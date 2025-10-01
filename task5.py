def parse_obj(path):
    coords = []
    with open(path, 'r') as file:
        for line in file:
            line = line.split()
            if line[0] == 'f':
                coords.append([int(line[1].split('/')[0]),
                               int(line[1].split('/')[1]),
                               int(line[1].split('/')[2])])
    return coords

print(parse_obj('./obj/model_1.obj'))