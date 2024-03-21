import os
import json
from Pages.components.path import Path
import secrets
import glob

def changeNumber_old(number, value):
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

def CreateNumber():
    path = Path()
    path_number = path.path_number()
    number_backup = os.path.join(path_number, 'number_backup.json')
    with open(number_backup, 'r') as file:
        data = json.load(file)
    
    for i in range(6):
        new_data = [[TachVaGhep(i, y) for y in x] for x in data]
        number = os.path.join(path_number, f'number_{i}.json')
        with open(number, 'w') as file:
            json.dump(new_data, file)

def createThong(data):
    thong_path = Path().path_thong()
    row = 121
    col_custom = 3
    value = data.get('value')
    col = int(value)
    #/ Generate 2 bytes of random data and ID
    random_bytes = secrets.token_bytes(8)
    # Convert the random bytes to hexadecimal
    id = random_bytes.hex()

    thong_file = []
    #/ Create Thong
    for i in range(col):
        thong_data = []
        for j in range(row):
            thong_data.append('')
        thong_file.append(thong_data)

    #/ Make fisrt file Thong
    with open(os.path.join(thong_path, f'thong_{id}_backup.json'),'w') as file:
        json.dump(thong_file, file)
    
    #/ Add Data thong into Thong DB
    with open(os.path.join(thong_path, 'thongs.json'),'r') as file:
        thong_db = json.load(file)
    
    filter_thong  = [item for item in thong_db if item['id'] != id and item['name'] != data.get('name')]
    
    #/ Make Data Custom for thong data
    data_custon = []
    for i in range(col_custom):
        data_item = []
        for j in range(row):
            data_item.append('')
        data_custon.append(data_item)

    #/ Make new Data thong
    data['data'] = data_custon
    data['id'] = id
    filter_thong.append(data)
    with open(os.path.join(thong_path, 'thongs.json'), 'w') as file:
        json.dump(filter_thong, file)
    return data

def find_files_by_pattern(directory, pattern):
    # Construct the search pattern
    search_pattern = os.path.join(directory, pattern)
    
    # Use glob to find files matching the pattern
    matching_files = glob.glob(search_pattern)
    
    # Extract filenames from file paths
    matching_filenames = [os.path.basename(file_path) for file_path in matching_files]
    
    return matching_filenames

def getFileWithOutBackUp(files):
    file = [file for file in files if not 'backup' in file]
    if len(file) == 0:
        return files
    else:
        return file