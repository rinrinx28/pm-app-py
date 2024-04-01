import os
from Pages.components.path import Path
import secrets
import json
import shutil

def changeNumber(number, value):
    if number == 1:
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
        if value != 3 and value != 4 and value != 5 and value != 6 and value !=7:
            if value == 0:
                return 3
            elif value == 1:
                return 4
            elif value == 2:
                return 5
            elif value == 8:
                return 6
            elif value == 9:
                return 7
            else:
                return value
        return value
    elif number == 5:
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
    return joined_string

def createThong(data, path):
    os.makedirs(path, exist_ok=True)
    thong_path = path
    row = 131
    col_custom = 3
    value = data.get('value')
    col = value
    id = Generate_Id()
    type_count = data.get('type_count')

    thong_file = []
    step = 0
    #/ Create Thong
    for i in range(0,col,60):
        if i == 0:
            for k in range(60):
                thong_data = []
                for j in range(row):
                    line = f'{j + 1:02}'
                    if j > 99:
                        thong_data.append('')
                    else:
                        if type_count == 1:
                            if k == 0:
                                thong_data.append(
                                    (int(line[0])) % 10
                                )
                            elif k == 1:
                                thong_data.append(
                                    (int(line[1])) % 10
                                )
                            else:
                                thong_data.append(0)
                        elif type_count == 2:
                            if k == 0:
                                thong_data.append(f'{line}')
                            else:
                                thong_data.append(0)
                        else:
                            thong_data.append('')
                thong_file.append(thong_data)
        else:
            for k in range(60):
                thong_data = []
                for j in range(row):
                    if j > 99:
                        thong_data.append('')
                    else:
                        if type_count == 1:
                            if k == 0:
                                thong_data.append(
                                    (int(thong_file[(step - 1) * 60][j]) + 1) % 10
                                )
                            elif k == 1:
                                thong_data.append(
                                    (int(thong_file[(step - 1) * 60 + 1][j]) + 1) % 10
                                )
                            else:
                                thong_data.append(0)
                        elif type_count == 2:
                            if k == 0:
                                first = thong_file[(step - 1 ) * 60][j]
                                second = f'{(int(first[0]) + 1) % 10}{(int(first[1]) + 1) % 10}'
                                thong_data.append(f'{second}')
                            else:
                                thong_data.append(0)
                        else:
                            thong_data.append('')
                thong_file.append(thong_data)
        step+=1
        
    if type_count == 1:
        for j in range(row):
            if j > 99:
                break
            for i in range(0,col,60):
                for k in range(60):
                    if k > 1:
                        first = thong_file[i + k - 2][j]
                        second = thong_file[i + k - 1][j]
                        sum = (first + second) % 10
                        thong_file[i + k][j] = sum
    if type_count == 2:
        for j in range(row):
            if j > 99:
                break
            for i in range(0,col,60):
                for k in range(60):
                    if k > 0:
                        first = thong_file[i + k - 1][j]
                        c = (int(first[0]) + int(first[1])) % 10
                        d = (int(first[1]) + c) % 10
                        thong_file[i + k][j] = f'{c}{d}'

    #/ Make fisrt file Thong
    with open(os.path.join(thong_path, f'thong_{id}_backup.json'),'w') as file:
        json.dump(thong_file, file)

    #/ Make Chuyen Doi
    for i in range(6):
        if i == 0:
            with open(os.path.join(thong_path, f'thong_{id}_{i}.json'),'w') as file:
                json.dump(thong_file, file)
        else:
            number_change = list(map(
                    lambda item: list(map(
                        lambda x: TachVaGhep(i, x), item
                    )), thong_file 
                ))
            with open(os.path.join(thong_path, f'thong_{id}_{i}.json'),'w') as file:
                json.dump(number_change, file)
    
    #/ Make Data Custom for thong data
    data_custon = []
    for i in range(col_custom):
        data_item = []
        for j in range(row):
            data_item.append('')
        data_custon.append(data_item)

    #/ Make Data STT for thong data
    stt_data = []
    for i in range(6):
        stt_col = []
        for j in range(row):
            value = f'{j:02}'
            stt_col.append(value)
        stt_data.append(stt_col)
        
    #/ Make new Data thong
    data['data'] = data_custon
    data['stt'] = stt_data
    data['id'] = id
    data['number'] = 0
    data['change'] = []
    data['type_thong'] = type_count
    # data['index'] = 
    with open(os.path.join(thong_path, 'thongs.json'), 'w') as file:
        json.dump(data, file)
    return data

def Generate_Id():
    #/ Generate 2 bytes of random data and ID
    random_bytes = secrets.token_bytes(8)
    id = random_bytes.hex()
    return id

def createDB(thong, name, path):
    thongId = thong['id']
    thongName = thong['name']
    id = Generate_Id()
    data = {
            "name": name,
            "password": "0",
            "col": 10,
            "thong": { "name": thongName, "value": 180, "id": thongId },
            "meta": {
                "notice": { "count": [0, 0], "color": [0, 0], "color2": [0, 0] },
                "features": { "N:2": True, "N=1": { "status": False, "value": 0 } },
                "setting": { "col_e": [2, 120] },
                "number": 0,
                "maxRow": 200,
                "buttons": [True, False]
            },
            "data": [],
            "id": id
        }
    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, 'index.json'), 'w') as file:
        json.dump(data, file)

def copy_files_into_folders(source_folder, destination_folder):
    try:
        # Walk through the directory tree
        for root, dirs, files in os.walk(source_folder):
            # Copy files into corresponding folders
            for file in files:
                source_file = os.path.join(root, file)
                destination_dir = os.path.join(destination_folder, os.path.relpath(root, source_folder))
                os.makedirs(destination_dir, exist_ok=True)
                destination_file = os.path.join(destination_dir, file)
                shutil.copy2(source_file, destination_file)  # shutil.copy2 ensures metadata preservation
                
        print("Files copied into folders successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create():
    current_dir = r'C:\data'
    default_dir = r'C:\data\1'
    arr_folder = ['image', 'number']

    for i in range(1, 31):
        for folder in arr_folder:
            prev_dir = os.path.join(current_dir, str(i), folder)
            next_dir = os.path.join(default_dir, folder)
            copy_files_into_folders(next_dir, prev_dir)

    for i in range(1, 31):
        thong_dir = os.path.join(current_dir, str(i), 'thong')
        db_dir = os.path.join(current_dir, str(i), 'db')
        if i < 11:
            dataThong = createThong({
                "value": 300,
                "type_count": 1,
                "name": f'Bảng 1 Số'
            }, thong_dir)
            createDB(dataThong, f'B{i}', db_dir)
        elif i > 10 and i < 21:
            dataThong = createThong({
                "value": 300,
                "type_count": 2,
                "name": f'Bảng 2 Số'
            }, thong_dir)
            createDB(dataThong, f'B{i}', db_dir)
        else:
            dataThong = createThong({
                "value": 300,
                "type_count": 0,
                "name": f'Bảng Trắng'
            }, thong_dir)
            createDB(dataThong, f'B{i}', db_dir)

# Example usage
create()
