import os
import json
from Pages.components.path import Path
import secrets
import glob
from datetime import datetime

# TODO Handler Data
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
    return joined_string

# TODO Handler Data Bang
def createBan(data):
    path_db = Path().path_db()
    id = Generate_Id()
    data['id'] = id
    with open(path_db, 'r') as file:
        data_db = json.load(file)
    
    data_find = [item for item in data_db if item['name'] == data['name']]
    if len(data_find) > 0:
        return 'Tên bảng đã được tạo, xin vui lòng kiểm tra lại!'
    data_filter = [item for item in data_db if item['id'] != id and item['name'] != data['name']]
    data_filter.append(data)
    with open(path_db, 'w') as file:
        json.dump(data_filter, file)
    return data_filter

def updateBanInsert(data):
    path_db = Path().path_db()
    with open(path_db, 'r') as file:
        data_db = json.load(file)
    insert = data['insert']
    update = data['update']
    maxRow  = data_db['meta']['maxRow']
    #/ Insert
    #/ Check Max Row
    if len(data_db['data']) + 1 >= maxRow:
        data_db['data'] = data_db['data'][1:]
    data_db['data'].append(insert)
    
    #/ Update meta features
    data_db['meta']['features'] = update

    #/ Write File JSON
    with open(path_db, 'w') as file:
        json.dump(data_db, file)
    
    return {"status": True, "msg":'Đã nhập liệu thành công!', "data": data_db}

def updateThongInsert(data):
    path_db = Path().path_db()
    with open(path_db, 'r') as file:
        data_db = json.load(file)
    update = data['thong']
     #/ Save insert date
    data_db['data'][-1] = update
    #/ Write File JSON
    with open(path_db, 'w') as file:
        json.dump(data_db, file)
    return {"status": True, "msg":'Đã nhập thông thành công!', "data": data_db}

def updateColorInsert(data):
    path_db = Path().path_db()
    with open(path_db, 'r') as file:
        data_db = json.load(file)
    update = data['notice']
    col_e = data['col_e']
    number = data['number']
    col = data['col']
    thong = data['thong']
    maxRow = data['maxRow']
    buttons = data['buttons']
    #/ Save insert date
    data_db['meta']['notice'] = update
    data_db['meta']['setting']['col_e'] = col_e
    data_db['meta']['number'] = number
    data_db['col'] = col
    data_db['thong'] = thong
    data_db['meta']['maxRow'] = maxRow
    data_db['meta']['buttons'] = buttons
    #/ Write File JSON
    with open(path_db, 'w') as file:
        json.dump(data_db, file)
    
    return {"status": True, "msg":'Đã cật nhập cài đặt thành công!', "data": data_db}

def deleteRowBan(data):
    path_db = Path().path_db()
    with open(path_db, 'r') as file:
        data_db = json.load(file)
    update = data['update']
    #/ Save insert date
    data_db['data'] = update
    #/ Save data find
    with open(path_db, 'w') as file:
        json.dump(data_db, file)
    
    return 'Đã đã xóa dòng mới thành công!'

def deleteFromToBan(fromdate,todate, id):
    path_db = Path().path_db()
    with open(path_db, 'r') as file:
        data_db = json.load(file)

    data = data_db['data']
    start_date = fromdate
    end_date = todate

    # Convert dates to comparable format
    start_date = datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y/%m/%d")
    end_date = datetime.strptime(end_date, "%d/%m/%Y").strftime("%Y/%m/%d")

    # Filter out entries with dates falling within the specified range
    filtered_data = [entry for entry in data if start_date <= datetime.strptime(entry["date"], "%d/%m/%Y").strftime("%Y/%m/%d") <= end_date]

    # Remove the filtered entries from the original data list
    data = [entry for entry in data if entry not in filtered_data]
    data_db['data'] = data

    #/ Save data find
    with open(path_db, 'w') as file:
        json.dump(data_db, file)
    
    return {'status': True, 'data':data_db, "msg": 'Đã xóa dữ liệu thành công!'}

# TODO Handler Data Thong
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
    col_custom = 4
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
                    line = f'{j}' if j > 9 else f'0{j}'
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
                        thong_data.append(0)
                thong_file.append(thong_data)
        else:
            for k in range(60):
                thong_data = []
                for j in range(row):
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
                        thong_data.append(0)
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
            value = f'{j}' if j > 9 else f'0{j}'
            stt_col.append(value)
        stt_data.append(stt_col)
        
    #/ Make new Data thong
    data['data'] = data_custon
    data['stt'] = stt_data
    data['id'] = id
    data['number'] = 0
    with open(os.path.join(thong_path, 'thongs.json'), 'w') as file:
        json.dump(data, file)
    return data

def saveThong(data):
    thong_path = Path().path_thong()
    update = data['update']
    custom = data['custom']
    id = data['id']
    number = data['number']
    stt = data['stt']
    change = data['change']
    setting = data['setting']
    #/ Load File thong db
    with open(os.path.join(thong_path, 'thongs.json'), 'r') as file:
        thong_db = json.load(file)

    thong_db['data'] = custom
    thong_db['stt'] = stt
    thong_db['change'] = change
    thong_db['setting'] = setting

    #/ Save Thong DB
    with open(os.path.join(thong_path, 'thongs.json'), 'w') as file:
        json.dump(thong_db, file)

    #/ Save thong data
    with open(os.path.join(thong_path, f'thong_{id}_{number}.json'), 'w') as file:
        json.dump(update, file)
    
    return 'Đã Lưu Thành Công!'

def backupThong(data):
    thong_path = Path().path_thong()
    number = data['number']
    id = data['id']
    #/ Load File thong db
    with open(os.path.join(thong_path, 'thongs.json'), 'r') as file:
        thong_db = json.load(file)

    stt_data_number = thong_db['stt']
    for j in range(131):
        value = f'{j:02}'
        stt_data_number[number][j] = value

    thong_db['stt'] = stt_data_number
    thong_db['change'] = [item for item in thong_db['change']
                          if item['number'] !=number]

    #/ Save Thong DB
    with open(os.path.join(thong_path, 'thongs.json'), 'w') as file:
        json.dump(thong_db, file)

    #/ Load Backup thong
    with open(os.path.join(thong_path, f'thong_{id}_backup.json'), 'r') as file:
        thong_backup = json.load(file)
    
    number_change = list(map(
                    lambda item: list(map(
                        lambda x: TachVaGhep(number, x), item
                    )), thong_backup 
                ))
    #/ Save backup Thong Number
    with open(os.path.join(thong_path, f'thong_{id}_{number}.json'), 'w') as file:
        json.dump(number_change, file)
    
    return {'thong_info': thong_db, "thong_data": number_change}

def saveAllThong(data):
    type_count = data['type_count']
    update = data['update']
    custom = data['custom']
    number = data['number']
    change = data['change']
    stt = data['stt']

    current_path = fr'C:\data'

    if type_count == 1:
        for i in range(10):
            file_type = i + 1
            thong_path = os.path.join(current_path, f'{file_type}','thong')
            with open(os.path.join(thong_path, 'thongs.json'), 'r') as file:
                thong_db = json.load(file)

            thong_id = thong_db['id']
            thong_db['stt'] = stt
            thong_db['data'] = custom
            thong_db['change'] = change

            #/ Save Thong DB
            with open(os.path.join(thong_path, 'thongs.json'), 'w') as file:
                json.dump(thong_db, file)

            #/ Save thong data
            with open(os.path.join(thong_path, f'thong_{thong_id}_{number}.json'), 'w') as file:
                json.dump(update, file)
    elif type_count == 2:
        for i in range(10,20):
            file_type = i + 1
            thong_path = os.path.join(current_path, f'{file_type}','thong')
            with open(os.path.join(thong_path, 'thongs.json'), 'r') as file:
                thong_db = json.load(file)

            thong_id = thong_db['id']
            thong_db['stt'] = stt
            thong_db['data'] = custom
            thong_db['change'] = change

            #/ Save Thong DB
            with open(os.path.join(thong_path, 'thongs.json'), 'w') as file:
                json.dump(thong_db, file)

            #/ Save thong data
            with open(os.path.join(thong_path, f'thong_{thong_id}_{number}.json'), 'w') as file:
                json.dump(update, file)
    else:
        for i in range(20,30):
            file_type = i + 1
            thong_path = os.path.join(current_path, f'{file_type}','thong')
            with open(os.path.join(thong_path, 'thongs.json'), 'r') as file:
                thong_db = json.load(file)

            thong_id = thong_db['id']
            thong_db['stt'] = stt
            thong_db['data'] = custom
            thong_db['change'] = change

            #/ Save Thong DB
            with open(os.path.join(thong_path, 'thongs.json'), 'w') as file:
                json.dump(thong_db, file)

            #/ Save thong data
            with open(os.path.join(thong_path, f'thong_{thong_id}_{number}.json'), 'w') as file:
                json.dump(update, file)

    value_type = f'{type_count} số' if type_count >= 1 else f'Trắng'
    return f'Đã đồng bộ dữ liệu bộ {value_type}'

def typeWithRecipe(data):
    row = data['row']
    # number = data['number']
    setting = data['setting']
    # stt = data['stt']
    update = data['update']
    col = len(update[0])
    line = f'{row:02}'
    #/ Create new Rowstep = 0
    step = 0
    if setting == 1:
        for i in range(0,col,60):
            if i == 0:
                for k in range(60):
                    if k == 0:
                        update[k + i][row] = int(line[0]) % 10
                    elif k == 1:
                        update[k + i][row] = int(line[1]) % 10
                    else:
                        update[k + i][row] = 0
            else:
                for k in range(60):
                    if k == 0:
                        update[k + i][row] = (int(update[(step - 1) * 60][row]) + 1) % 10
                    elif k == 1:
                        update[k + i][row] = (int(update[(step - 1) * 60 + 1][row]) + 1) % 10
                    else:
                        update[k + i][row] = 0
            step+=1
    
        for i in range(0,col,60):
            for k in range(60):
                if k > 1:
                    first = update[i + k - 2][row]
                    second = update[i + k - 1][row]
                    sum = (first + second) % 10
                    update[i + k][row] = sum
                        
    if setting == 2:
        for i in range(0, col, 100):
            if i == 0:
                for k in range(i, i + 100, 10):
                    for l in range(10):
                        if k == 0:
                            update[k + l][row] = f'{row:02}'
                        else:
                            update[k + l][row] = 0
            else:
                for k in range(i, i + 100, 10):
                    for l in range(10):
                        update[k + l][row] = 0
                        
        for i in range(0,col,100):
            for k in range(i, i + 100, 10):
                for l in range(10):
                    if i == 0:
                        if k == 0:
                            if l > 0:
                                first = update[k + l - 1][row]
                                c = (int(first[0]) + int(first[1])) % 10
                                d = (int(first[1]) + c) % 10
                                update[k + l][row] = f'{c}{d}'
                        else:
                            if l == 0:
                                first = update[k + l - 10][row]
                                c = f'{(int(first[0]) + 1) % 10}{(int(first[1]) + 1) % 10}'
                                update[k + l][row] = f'{c}'
                            else:
                                first = update[k + l - 1][row]
                                c = (int(first[0]) + int(first[1])) % 10
                                d = (int(first[1]) + c) % 10
                                update[k + l][row] = f'{c}{d}'

                    else:
                        if k == 100:
                            if l == 0:
                                first = update[98][row]
                                second = update[99][row]
                                update[100][row] = f'{first[1]}{second[0]}'
                            else:
                                first = update[k + l - 1][row]
                                c = (int(first[0]) + int(first[1])) % 10
                                d = (int(first[1]) + c) % 10
                                update[k + l][row] = f'{c}{d}'

                        else:
                            if l == 0:
                                first = update[k + l - 10][row]
                                c = f'{(int(first[0]) + 1) % 10}{(int(first[1]) + 1) % 10}'
                                update[k + l][row] = f'{c}'
                            else:
                                first = update[k + l - 1][row]
                                c = (int(first[0]) + int(first[1])) % 10
                                d = (int(first[1]) + c) % 10
                                update[k + l][row] = f'{c}{d}'

    return data

# TODO Handler Data Ngang

def saveNgang(data):
    ngang_path = Path().path_number()
    update = data['update']
    number = data['number']
    stt = data['stt']
    change = data['change']

    #/ Save STT
    with open(os.path.join(ngang_path, 'number.json'), 'r') as file:
        ngang_data = json.load(file)

    ngang_data['stt'] = stt
    ngang_data['change'] = change
    with open(os.path.join(ngang_path, 'number.json'), 'w') as file:
        json.dump(ngang_data, file)

    #/ Save Data Ngang
    with open(os.path.join(ngang_path, f'number_{number}.json'), 'w') as file:
        json.dump(update, file)
    
    return

def backUpNgang(data):
    ngang_path = Path().path_number()
    number = data['number']

    #/ Render STT Ngang
    stt = []
    for j in range(41):
        value = f'{j + 1:02}'
        stt.append(value)

    #/ Load and Save STT Ngang
    with open(os.path.join(ngang_path, 'number.json'), 'r') as file:
        stt_ngang = json.load(file)
    
    stt_ngang['stt'][number] = stt
    stt_ngang['change'] = [item for item in stt_ngang['change']
                           if item['number'] != number]
 
    with open(os.path.join(ngang_path, 'number.json'), 'w') as file:
        json.dump(stt_ngang, file)

    #/ Load and save Ngang Data
    with open(os.path.join(ngang_path, f'number_backup.json'), 'r') as file:
        ngang_data = json.load(file)
    
    number_change = list(map(
                    lambda item: list(map(
                        lambda x: TachVaGhep(number, x), item
                    )), ngang_data 
                ))
    with open(os.path.join(ngang_path, f'number_{number}.json'), 'w') as file:
        json.dump(number_change, file)
    
    return {"stt": stt_ngang, "ngang_data": number_change}

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
    
def Generate_Id():
    #/ Generate 2 bytes of random data and ID
    random_bytes = secrets.token_bytes(8)
    id = random_bytes.hex()
    return id