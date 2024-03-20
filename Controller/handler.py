import os
import json

def changeNumber(number, value):
        if number == 1:
            if value != 3 and value != 4 and value != 5 and value != 6 and value !=7:
                if value == 0:
                    return 3
                elif value == 1:
                    return 4
                elif value == 2:
                    return 5
                elif value == 8:
                    return 6
                elif value == 7:
                    return 9
                else:
                    return value
            return value
        elif number == 2:
            if value != 0 and value != 2 and value != 4 and value != 6 and value !=8:
                if value == 1:
                    return 0
                elif value == 3:
                    return 2
                elif value == 5:
                    return 4
                elif value == 7:
                    return 6
                elif value == 9:
                    return 8
                else:
                    return value
            return value
        elif number == 3:
            if value != 1 and value != 3 and value != 5 and value != 7 and value !=9:
                if value == 2:
                    return 1
                elif value == 4:
                    return 3
                elif value == 6:
                    return 5
                elif value == 8:
                    return 7
                elif value == 0:
                    return 9
                else:
                    return value
            return value
        elif number == 4:
            if value != 5 and value != 6 and value != 7 and value != 8 and value !=9:
                if value == 1:
                    return 5
                elif value == 2:
                    return 6
                elif value == 3:
                    return 7
                elif value == 4:
                    return 8
                elif value == 0:
                    return 9
                else:
                    return value
            return value
        elif number == 5:
            if value != 0 and value != 1 and value != 2 and value != 3 and value !=4:
                if value == 5:
                    return 0
                elif value == 6:
                    return 1
                elif value == 7:
                    return 2
                elif value == 8:
                    return 3
                elif value == 9:
                    return 4
                else:
                    return value
            return value
        elif number == 6:
            if value != 0 and value != 1 and value != 2 and value != 3 and value !=5:
                if value == 4:
                    return 3
                elif value == 6:
                    return 0
                elif value == 7:
                    return 1
                elif value == 8:
                    return 2
                elif value == 9:
                    return 5
                else:
                    return value
            return value
        elif number == 7:
            if value != 1 and value != 2 and value != 3 and value != 4 and value != 5:
                if value == 0:
                    return 4
                elif value == 6:
                    return 5
                elif value == 7:
                    return 1
                elif value == 8:
                    return 2
                elif value == 9:
                    return 3
                else:
                    return value
            return value
        elif number == 8:
            if value != 4 and value != 5 and value != 6 and value != 7 and value != 9:
                if value == 1:
                    return 5
                elif value == 2:
                    return 6
                elif value == 3:
                    return 9
                elif value == 8:
                    return 7
                elif value == 0:
                    return 4
                else:
                    return value
            return value
        elif number == 9:
            if value != 2 and value != 3 and value != 4 and value != 5 and value !=7:
                if value == 0:
                    return 2
                elif value == 1:
                    return 3
                elif value == 6:
                    return 4
                elif value == 8:
                    return 5
                elif value == 9:
                    return 7
                else:
                    return value
            return value
        elif number == 10:
            if value != 1 and value != 2 and value != 3 and value != 4 and value != 6:
                if value == 0:
                    return 1
                elif value == 5:
                    return 2
                elif value == 7:
                    return 3
                elif value == 8:
                    return 4
                elif value == 9:
                    return 6
                else:
                    return value
            return value
        else:
            return value
        
def TachVaGhep(number, value):
    chuoiso = str(value)
    mangso = list(chuoiso)
    chuSo = map(lambda i: str(changeNumber(number, int(i))), mangso)
    joined_string = ''.join(list(chuSo))
    result_int = int(joined_string)
    return result_int

def createBan(data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..','Pages','data','database','index.json')
    with open(file_path,'r') as file:
        old_data = json.load(file)

    old_data.append(data)

    with open(file_path,'w') as file:
        json.dump(old_data, file)
    return
