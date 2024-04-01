import os
import json
from Controller.handler import TachVaGhep

current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data') #/ File Data for Dev



def path_number():
    path = os.path.join(current_dir,'number')
    return path
def path_thong():
    path = os.path.join(current_dir, 'thong')
    return path

def createNewNumber():
    path = path_number()
    number_bk = os.path.join(path, 'number_backup.json')
    with open(number_bk, 'r') as file:
        number_data = json.load(file)
    #/ Add new 10 row and 600 col into by one
    row_add = 10
    col_add = 600
    for i in range(row_add):
        new_number_data = []
        for j in range(col_add):
            new_number_data.append('')
        number_data.append(new_number_data)
    #/ Save data backup!
    with open(number_bk, 'w') as file:
        json.dump(number_data, file)
    
    change = 6
    for i in range(change):
        #/ Convert Data change with Func
        number_change = list(map(
            lambda item: list(map(
                lambda x: TachVaGhep(i, x), item
            )), number_data
        ))
        #/ get path Number change
        number_path = os.path.join(path, f'number_{i}.json')
        #/ Save data change
        with open(number_path, 'w') as file:
            json.dump(number_change, file)

def createNewSttNumber():
    path = path_number()
    number_path = os.path.join(path, 'number.json')
    with open(number_path, 'r') as file:
        number_data = json.load(file)
    
    new_number_data = []
    for i in range(6):
        data = []
        for j in range(41):
            value = f'{j + 1:02}'
            data.append(value)
        new_number_data.append(data)
    
    # #/ Save new data stt
    number_data = {
        "stt": new_number_data,
        "number": 0,
        "change": []
    }
    print(number_data)
    #/ Save data
    with open(number_path, 'w') as file:
        json.dump(number_data, file)

createNewSttNumber()
createNewNumber()
