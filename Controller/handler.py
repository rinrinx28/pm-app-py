import os
import json
from Pages.components.path import Path
import secrets
import glob
from datetime import datetime
import re


# TODO Handler Data
def changeNumber_old(number, value):
    if number == 1:
        if value != 0 and value != 1 and value != 2 and value != 3 and value != 4:
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
        if value != 0 and value != 2 and value != 4 and value != 6 and value != 8:
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
        if value != 1 and value != 3 and value != 5 and value != 7 and value != 9:
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
        if value != 5 and value != 6 and value != 7 and value != 8 and value != 9:
            if value == 0:
                return 5
            elif value == 1:
                return 7
            elif value == 2:
                return 8
            elif value == 3:
                return 9
            elif value == 4:
                return 6
            else:
                return value
        return value
    elif number == 5:
        if value != 1 and value != 2 and value != 3 and value != 4 and value != 0:
            if value == 5:
                return 1
            elif value == 6:
                return 2
            elif value == 7:
                return 3
            elif value == 8:
                return 4
            elif value == 9:
                return 0
            else:
                return value
        return value
    elif number == 6:
        if value != 0 and value != 1 and value != 2 and value != 3 and value != 4:
            if value == 5:
                return 3
            elif value == 6:
                return 4
            elif value == 7:
                return 0
            elif value == 8:
                return 1
            elif value == 9:
                return 2
            else:
                return value
        return value
    elif number == 7:
        if value != 5 and value != 6 and value != 7 and value != 8 and value != 9:
            if value == 0:
                return 7
            elif value == 1:
                return 8
            elif value == 2:
                return 6
            elif value == 3:
                return 5
            elif value == 4:
                return 9
            else:
                return value
        return value
    elif number == 8:
        if value != 0 and value != 1 and value != 2 and value != 3 and value != 9:
            if value == 4:
                return 2
            elif value == 5:
                return 3
            elif value == 6:
                return 9
            elif value == 7:
                return 0
            elif value == 8:
                return 1
            else:
                return value
        return value
    elif number == 9:
        if value != 0 and value != 1 and value != 7 and value != 8 and value != 9:
            if value == 2:
                return 0
            elif value == 3:
                return 1
            elif value == 4:
                return 7
            elif value == 5:
                return 8
            elif value == 6:
                return 9
            else:
                return value
        return value
    elif number == 10:
        if value != 2 and value != 3 and value != 4 and value != 6 and value != 7:
            if value == 0:
                return 2
            elif value == 1:
                return 3
            elif value == 5:
                return 4
            elif value == 8:
                return 7
            elif value == 9:
                return 6
            else:
                return value
        return value
    else:
        return value


def changeNumber(number, value):
    if number == 1:
        if value != 0 and value != 1 and value != 2 and value != 3 and value != 4:
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
        if value != 0 and value != 2 and value != 4 and value != 6 and value != 8:
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
        if value != 1 and value != 3 and value != 5 and value != 7 and value != 9:
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
        if value != 5 and value != 6 and value != 7 and value != 8 and value != 9:
            if value == 0:
                return 5
            elif value == 1:
                return 7
            elif value == 2:
                return 8
            elif value == 3:
                return 9
            elif value == 4:
                return 6
            else:
                return value
        return value
    elif number == 5:
        if value != 1 and value != 2 and value != 3 and value != 4 and value != 0:
            if value == 5:
                return 1
            elif value == 6:
                return 2
            elif value == 7:
                return 3
            elif value == 8:
                return 4
            elif value == 9:
                return 0
            else:
                return value
        return value
    elif number == 6:
        if value != 0 and value != 1 and value != 2 and value != 3 and value != 4:
            if value == 5:
                return 3
            elif value == 6:
                return 4
            elif value == 7:
                return 0
            elif value == 8:
                return 1
            elif value == 9:
                return 2
            else:
                return value
        return value
    elif number == 7:
        if value != 5 and value != 6 and value != 7 and value != 8 and value != 9:
            if value == 0:
                return 7
            elif value == 1:
                return 8
            elif value == 2:
                return 6
            elif value == 3:
                return 5
            elif value == 4:
                return 9
            else:
                return value
        return value
    elif number == 8:
        if value != 0 and value != 1 and value != 2 and value != 3 and value != 9:
            if value == 4:
                return 2
            elif value == 5:
                return 3
            elif value == 6:
                return 9
            elif value == 7:
                return 0
            elif value == 8:
                return 1
            else:
                return value
        return value
    elif number == 9:
        if value != 0 and value != 1 and value != 7 and value != 8 and value != 9:
            if value == 2:
                return 0
            elif value == 3:
                return 1
            elif value == 4:
                return 7
            elif value == 5:
                return 8
            elif value == 6:
                return 9
            else:
                return value
        return value
    elif number == 10:
        if value != 2 and value != 3 and value != 4 and value != 6 and value != 7:
            if value == 0:
                return 2
            elif value == 1:
                return 3
            elif value == 5:
                return 4
            elif value == 8:
                return 7
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
    joined_string = "".join(list(chuSo))
    return joined_string


# TODO Handler Data Bang
def createBan(data):
    path_db = Path().path_db()
    id = Generate_Id()
    data["id"] = id
    with open(path_db, "r") as file:
        data_db = json.load(file)

    data_find = [item for item in data_db if item["name"] == data["name"]]
    if len(data_find) > 0:
        return "Tên bảng đã được tạo, xin vui lòng kiểm tra lại!"
    data_filter = [
        item for item in data_db if item["id"] != id and item["name"] != data["name"]
    ]
    data_filter.append(data)
    with open(path_db, "w") as file:
        json.dump(data_filter, file)
    return data_filter


def updateBanInsert(data):
    path_db = Path().path_db()
    with open(path_db, "r") as file:
        data_db = json.load(file)
    data["insert"]["isDeleted"] = False
    insert = data["insert"]
    update = data["update"]
    maxRow = data_db["meta"]["maxRow"]

    # Lọc ra tất cả các phần tử chưa bị xóa
    notIsDeleted = [item for item in data_db["data"] if not item["isDeleted"]]

    # Nếu số phần tử chưa bị xóa vượt quá maxRow
    if len(notIsDeleted) >= maxRow:
        # Đếm số lượng phần tử cần đánh dấu là đã xóa
        excess_count = len(notIsDeleted) - (maxRow - 1)

        # Duyệt qua mảng gốc và đánh dấu các phần tử cũ nhất là đã xóa
        for item in data_db["data"]:
            if not item["isDeleted"]:
                if excess_count > 0:
                    item["isDeleted"] = True  # Đánh dấu phần tử là đã xóa
                    excess_count -= 1  # Giảm số lượng phần tử cần xóa
                else:
                    break  # Dừng khi đã đánh dấu đủ số lượng
    data_db["data"].append(insert)

    # / Update meta features
    data_db["meta"]["features"] = update

    # / Write File JSON
    with open(path_db, "w") as file:
        json.dump(data_db, file)

    return {"status": True, "msg": "Đã nhập liệu thành công!", "data": data_db}


def enableTables(data):
    path_db = Path().path_db()
    with open(path_db, "r") as file:
        data_db = json.load(file)
    data_db["meta"]["tables"] = data

    # / Write File JSON
    with open(path_db, "w") as file:
        json.dump(data_db, file)

    return {"status": True, "msg": "Đã cật nhập cài đặt thành công!", "data": data_db}


def updateThongInsert(data):
    path_db = Path().path_db()
    with open(path_db, "r") as file:
        data_db = json.load(file)
    update = data["thong"]
    # / Save insert date
    len_data = len(data_db["data"])
    data_db["data"][len_data - 1] = update
    # / Write File JSON
    with open(path_db, "w") as file:
        json.dump(data_db, file)
    return {"status": True, "msg": "Đã nhập thông thành công!", "data": data_db}


def updateColorInsert(data):
    path_db = Path().path_db()
    with open(path_db, "r") as file:
        data_db = json.load(file)
    update = data["notice"]
    col_e = data["col_e"]
    col_e2 = data["col_e2"]
    col_e3 = data["col_e3"]
    col_e4 = data["col_e4"]
    col_e5 = data["col_e5"]
    col_e6 = data["col_e6"]
    col_e7 = data["col_e7"]
    col_e8 = data["col_e8"]
    col_e9 = data["col_e9"]
    col_e10 = data["col_e10"]
    number = data["number"]
    col = data["col"]
    thong = data["thong"]
    maxRow = data["maxRow"]
    buttons = data["buttons"]
    tables = data["tables"]
    size = data["size"]
    # / Save insert date
    data_db["meta"]["notice"] = update
    data_db["meta"]["setting"]["col_e"] = col_e
    data_db["meta"]["setting"]["col_e2"] = col_e2
    data_db["meta"]["setting"]["col_e3"] = col_e3
    data_db["meta"]["setting"]["col_e4"] = col_e4
    data_db["meta"]["setting"]["col_e5"] = col_e5
    data_db["meta"]["setting"]["col_e6"] = col_e6
    data_db["meta"]["setting"]["col_e7"] = col_e7
    data_db["meta"]["setting"]["col_e8"] = col_e8
    data_db["meta"]["setting"]["col_e9"] = col_e9
    data_db["meta"]["setting"]["col_e10"] = col_e10
    data_db["meta"]["number"] = number
    data_db["col"] = col
    data_db["thong"] = thong
    data_db["meta"]["maxRow"] = maxRow
    data_db["meta"]["buttons"] = buttons
    data_db["meta"]["tables"] = tables
    data_db["size"] = size
    # / Write File JSON
    with open(path_db, "w") as file:
        json.dump(data_db, file)

    return {"status": True, "msg": "Đã cật nhập cài đặt thành công!", "data": data_db}


def deleteRowBan(data):
    path_db = Path().path_db()
    with open(path_db, "r") as file:
        data_db = json.load(file)
    update = data["update"]
    # / Save insert date
    data_db["data"] = update
    # / Save data find
    with open(path_db, "w") as file:
        json.dump(data_db, file)

    return "Đã đã xóa dòng mới thành công!"


def deleteFromToBan(fromdate, todate, id, isChecked):
    path_db = Path().path_db()
    with open(path_db, "r") as file:
        data_db = json.load(file)

    data = data_db["data"]
    start_date = fromdate
    end_date = todate

    # Convert dates to comparable format
    current_date = datetime.strptime(data[-1]["date"], "%d/%m/%Y").strftime("%Y/%m/%d")
    start_date = datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y/%m/%d")
    end_date = datetime.strptime(end_date, "%d/%m/%Y").strftime("%Y/%m/%d")
    if end_date == current_date:
        filtered_data = []
        for i in range(len(data)):
            entry = data[i]
            entry_date = datetime.strptime(entry["date"], "%d/%m/%Y").strftime(
                "%Y/%m/%d"
            )
            if not (start_date <= entry_date <= end_date):
                filtered_data.append(entry)
        data = filtered_data
    else:
        # Remove the filtered entries from the original data list
        for i in range(len(data)):
            entry = data[i]
            if (
                start_date
                <= datetime.strptime(entry["date"], "%d/%m/%Y").strftime("%Y/%m/%d")
                <= end_date
            ):
                data[i]["isDeleted"] = True

    if isChecked:
        data_db["data"] = []
    else:
        data_db["data"] = data

    # / Save data find
    data_db["lastDelete"] = [fromdate, todate]
    with open(path_db, "w") as file:
        json.dump(data_db, file)

    return {"status": True, "data": data_db, "msg": "Đã xóa dữ liệu thành công!"}

# TODO Handler Data Thong
def CreateNumber():
    path = Path()
    path_number = path.path_number()
    number_backup = os.path.join(path_number, "number_backup.json")
    with open(number_backup, "r") as file:
        data = json.load(file)

    for i in range(6):
        new_data = [[TachVaGhep(i, y) for y in x] for x in data]
        number = os.path.join(path_number, f"number_{i}.json")
        with open(number, "w") as file:
            json.dump(new_data, file)


def createThong(data):
    thong_path = Path().path_thong()
    row = 121
    col_custom = 4
    value = data.get("value")
    col = value
    id = Generate_Id()
    type_count = data.get("type_count")

    thong_file = []
    step = 0
    # / Create Thong
    for i in range(0, col, 60):
        if i == 0:
            for k in range(60):
                thong_data = []
                for j in range(row):
                    line = f"{j}" if j > 9 else f"0{j}"
                    if type_count == 1:
                        if k == 0:
                            thong_data.append((int(line[0])) % 10)
                        elif k == 1:
                            thong_data.append((int(line[1])) % 10)
                        else:
                            thong_data.append(0)
                    elif type_count == 2:
                        if k == 0:
                            thong_data.append(f"{line}")
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
                            first = thong_file[(step - 1) * 60][j]
                            second = (
                                f"{(int(first[0]) + 1) % 10}{(int(first[1]) + 1) % 10}"
                            )
                            thong_data.append(f"{second}")
                        else:
                            thong_data.append(0)
                    else:
                        thong_data.append(0)
                thong_file.append(thong_data)
        step += 1

    if type_count == 1:
        for j in range(row):
            if j > 99:
                break
            for i in range(0, col, 60):
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
            for i in range(0, col, 60):
                for k in range(60):
                    if k > 0:
                        first = thong_file[i + k - 1][j]
                        c = (int(first[0]) + int(first[1])) % 10
                        d = (int(first[1]) + c) % 10
                        thong_file[i + k][j] = f"{c}{d}"

    # / Make fisrt file Thong
    with open(os.path.join(thong_path, f"thong_{id}_backup.json"), "w") as file:
        json.dump(thong_file, file)

    # / Make Chuyen Doi
    for i in range(6):
        if i == 0:
            with open(os.path.join(thong_path, f"thong_{id}_{i}.json"), "w") as file:
                json.dump(thong_file, file)
        else:
            number_change = list(
                map(
                    lambda item: list(map(lambda x: TachVaGhep(i, x), item)), thong_file
                )
            )
            with open(os.path.join(thong_path, f"thong_{id}_{i}.json"), "w") as file:
                json.dump(number_change, file)

    # / Make Data Custom for thong data
    data_custon = []
    for i in range(col_custom):
        data_item = []
        for j in range(row):
            data_item.append("")
        data_custon.append(data_item)

    # / Make Data STT for thong data
    stt_data = []
    for i in range(6):
        stt_col = []
        for j in range(row):
            value = f"{j}" if j > 9 else f"0{j}"
            stt_col.append(value)
        stt_data.append(stt_col)

    # / Make new Data thong
    data["data"] = data_custon
    data["stt"] = stt_data
    data["id"] = id
    data["number"] = 0
    with open(os.path.join(thong_path, "thongs.json"), "w") as file:
        json.dump(data, file)
    return data


def saveThong(data):
    thong_path = Path().path_thong()
    update = data["update"]
    custom = data["custom"]
    id = data["id"]
    number = data["number"]
    stt = data["stt"]
    change = data["change"]
    setting = data["setting"]
    # / Load File thong db
    with open(os.path.join(thong_path, "thongs.json"), "r") as file:
        thong_db = json.load(file)

    thong_db["data"] = custom
    thong_db["stt"] = stt
    thong_db["change"] = change
    thong_db["setting"] = setting

    # / Save Thong DB
    with open(os.path.join(thong_path, "thongs.json"), "w") as file:
        json.dump(thong_db, file)

    # / Save thong data
    with open(os.path.join(thong_path, f"thong_{id}_{number}.json"), "w") as file:
        json.dump(update, file)

    return "Đã Lưu Thành Công!"


def backupThong(data):
    thong_path = Path().path_thong()
    number = data["number"]
    id = data["id"]

    # / Load File thong db
    with open(os.path.join(thong_path, "thongs.json"), "r") as file:
        thong_db = json.load(file)

    stt_data_number = thong_db["stt"]
    for j in range(131):
        value = f"{j:02}"
        stt_data_number[number][j] = value

    thong_db["stt"] = stt_data_number
    thong_db["change"] = [
        item for item in thong_db["change"] if item["number"] != number
    ]

    # / Save Thong DB
    with open(os.path.join(thong_path, "thongs.json"), "w") as file:
        json.dump(thong_db, file)

    # / Load Backup thong
    with open(os.path.join(thong_path, f"thong_{id}_backup.json"), "r") as file:
        thong_backup = json.load(file)

    number_change = list(
        map(lambda item: list(map(lambda x: TachVaGhep(number, x), item)), thong_backup)
    )
    # / Save backup Thong Number
    with open(os.path.join(thong_path, f"thong_{id}_{number}.json"), "w") as file:
        json.dump(number_change, file)

    return {"thong_info": thong_db, "thong_data": number_change}


def saveBackupThong(data):
    thong_path = Path().path_thong()
    id = data["id"]
    thong_data = data["thong_data"]
    custom = data["custom"]
    thong_sp = data["thong_sp"]
    # / Load File thong db
    with open(os.path.join(thong_path, "thongs.json"), "r") as file:
        thong_db = json.load(file)

    # / Make Data STT for thong data
    stt_data = []
    for i in range(11):
        stt_col = []
        for j in range(131):
            value = f"{j:02}"
            stt_col.append(value)
        stt_data.append(stt_col)

    thong_db["stt"] = stt_data
    thong_db["change"] = []
    thong_db["data"] = custom

    # / Save Thong DB
    with open(os.path.join(thong_path, "thongs.json"), "w") as file:
        json.dump(thong_db, file)

    # / Save new backup thong
    with open(os.path.join(thong_path, f"thong_{id}_backup.json"), "w") as file:
        json.dump(thong_data, file)
    
    # / Save data thong sp
    # isThong_one = True if thong_db['type_count'] in [1,3] else False
    # if isThong_one:
    #     with open(os.path.join(thong_path, f"thong_sp_{id}.json"), "w") as file:
    #         json.dump(thong_sp, file)
    with open(os.path.join(thong_path, f"thong_sp_{id}.json"), "w") as file:
        json.dump(thong_sp, file)

    # / re-render all bo chuyen doi
    for i in range(11):
        if i == 0:
            with open(os.path.join(thong_path, f"thong_{id}_{i}.json"), "w") as file:
                json.dump(thong_data, file)
        else:
            number_change = list(
                map(
                    lambda item: list(map(lambda x: TachVaGhep(i, x), item)), thong_data
                )
            )
            with open(os.path.join(thong_path, f"thong_{id}_{i}.json"), "w") as file:
                json.dump(number_change, file)

    return {"thong_info": thong_db, "thong_data": thong_data}


def saveAllThong(data):
    type_count = data["type_count"]
    update = data["update"]
    custom = data["custom"]
    number = data["number"]
    name = data["name"]
    change = data["change"]
    stt = data["stt"]
    pm = data["pm"]
    
    # isThong_one = True if type_count in [1,3] else False
    # if isThong_one:
    #     thong_sp = data["thong_sp"]
    thong_sp = data["thong_sp"]
    index = extract_index(name)

    current_path = rf"C:\data"

    # Xác định phạm vi index dựa trên type_count
    if pm == 1:
        range_tuple = get_range_by_index(index, 0)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 2:
        range_tuple = get_range_by_index(index, 30)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 3:
        range_tuple = get_range_by_index(index, 60)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 4:
        range_tuple = get_range_by_index(index, 90)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 5:
        range_tuple = get_range_by_index(index, 120)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 6:
        range_tuple = get_range_by_index(index, 150)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    else:
        return "Type count không hợp lệ"

    range_start, range_end = range_tuple

    # / re-render all bo chuyen doi
    data_async = []
    for k in range(11):
        if k == 0:
            data_async.append(update)
        else:
            number_change = list(
                map(
                    lambda item: list(map(lambda x: TachVaGhep(k, x), item)), update
                )
            )
            data_async.append(number_change)

    for i in range(range_start - 1, range_end):  # Chuyển đổi sang chỉ số 0
        file_type = i + 1
        thong_path = os.path.join(current_path, f"{file_type}", "thong")

        with open(os.path.join(thong_path, "thongs.json"), "r") as file:
            thong_db = json.load(file)

        thong_id = thong_db["id"]
        thong_db["stt"] = stt
        thong_db["data"] = custom
        thong_db["change"] = change

        # / Save Thong DB
        with open(os.path.join(thong_path, "thongs.json"), "w") as file:
            json.dump(thong_db, file)

        # / Save thong data
        with open(
            os.path.join(thong_path, f"thong_{thong_id}_{number}.json"), "w"
        ) as file:
            json.dump(update, file)
        
        # / Save new backup thong
        with open(os.path.join(thong_path, f"thong_{thong_id}_backup.json"), "w") as file:
            json.dump(update, file)
        
        # if type_count in [1,3]:
        #     with open(os.path.join(thong_path, f"thong_sp_{thong_id}.json"), "w") as file:
        #         json.dump(thong_sp, file)
        with open(os.path.join(thong_path, f"thong_sp_{thong_id}.json"), "w") as file:
            json.dump(thong_sp, file)

        for k, data_arr_async in enumerate(data_async):
            with open(os.path.join(thong_path, f"thong_{thong_id}_{k}.json"), "w") as file:
                json.dump(data_arr_async, file)
        
        print(f"Done {i + 1}")

    # type_count_label = (
    #     "1a Số"
    #     if type_count == 1
    #     else ("2 Số" if type_count == 2 else "trắng" if type_count == 0 else "1b Số")
    # )

    return f"Đã đồng bộ dữ liệu"


def typeWithRecipe(data):
    row = data["row"]
    setting = data["setting"]
    value = data["value"]
    thong_sp = data["thong_sp"]
    update = data["update"]
    col = value
    # / Create new Rowstep = 0
    if setting == 1:
        # Initialize data
        steps = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 0, 1, 2, 3],
            [3, 4, 5, 6, 7, 8, 9, 0, 1, 2],
            [7, 8, 9, 0, 1, 2, 3, 4, 5, 6],
            [8, 9, 0, 1, 2, 3, 4, 5, 6, 7],
            [2, 3, 4, 5, 6, 7, 8, 9, 0, 1],
            [5, 6, 7, 8, 9, 0, 1, 2, 3, 4],
            [9, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
        ]

        # Initialize modifications for array a in each step
        modifications_a = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        ]

        # Initialize result containers
        current_thong_data = [0] * 1500
        thong_value_data = []

        # Process data for each tap and luot
        for count in range(10):  # 8 tập
            for count_h in range(10):  # Mỗi tập 10 lượt
                # Calculate E and H
                e = (int(thong_sp[row][0][0]) + modifications_a[count][count_h]) % 10
                h = (int(thong_sp[row][0][1]) + steps[count][count_h]) % 10

                # Determine starting index for thong in current_thong_data
                thong_start_index = (count * 10 + count_h) * 15  # Tính chỉ số dựa trên tập và lượt

                # Generate 15 thong values for this luot
                for thong_index in range(15):
                    thong = thong_index + thong_start_index
                    if thong_index == 0:
                        current_thong_data[thong] = (e + h) % 10
                    elif thong_index == 1:
                        current_thong_data[thong] = (
                            h + current_thong_data[thong - 1]
                        ) % 10
                    else:
                        current_thong_data[thong] = (
                            current_thong_data[thong - 2]
                            + current_thong_data[thong - 1]
                        ) % 10

                # Append E and H values to thong_value_data
                thong_value_data.append([e, h])

        # Save processed thong_sp for the current row
        thong_sp[row] = thong_value_data

        # Update thong_data matrix
        for thong_index, value in enumerate(current_thong_data):
            update[thong_index][row] = value

    if setting == 2:
        for i in range(0, col, 100):
            if i == 0:
                for k in range(i, i + 100, 10):
                    for l in range(10):
                        if k == 0:
                            update[k + l][row] = update[k + l][row]
                        else:
                            update[k + l][row] = 0
            else:
                for k in range(i, i + 100, 10):
                    for l in range(10):
                        update[k + l][row] = 0

        for i in range(0, col, 100):
            for k in range(i, i + 100, 10):
                for l in range(10):
                    if i == 0:
                        if k == 0:
                            if l > 0:
                                first = update[k + l - 1][row]
                                c = (int(first[0]) + int(first[1])) % 10
                                d = (int(first[1]) + c) % 10
                                update[k + l][row] = f"{c}{d}"
                        else:
                            if l == 0:
                                first = update[k + l - 10][row]
                                c = f"{(int(first[0]) + 1) % 10}{(int(first[1]) + 1) % 10}"
                                update[k + l][row] = f"{c}"
                            else:
                                first = update[k + l - 1][row]
                                c = (int(first[0]) + int(first[1])) % 10
                                d = (int(first[1]) + c) % 10
                                update[k + l][row] = f"{c}{d}"

                    else:
                        if k == 100:
                            if l == 0:
                                first = update[98][row]
                                second = update[99][row]
                                update[100][row] = f"{first[1]}{second[0]}"
                            else:
                                first = update[k + l - 1][row]
                                c = (int(first[0]) + int(first[1])) % 10
                                d = (int(first[1]) + c) % 10
                                update[k + l][row] = f"{c}{d}"

                        else:
                            if l == 0:
                                first = update[k + l - 10][row]
                                c = f"{(int(first[0]) + 1) % 10}{(int(first[1]) + 1) % 10}"
                                update[k + l][row] = f"{c}"
                            else:
                                first = update[k + l - 1][row]
                                c = (int(first[0]) + int(first[1])) % 10
                                d = (int(first[1]) + c) % 10
                                update[k + l][row] = f"{c}{d}"

    return data


# TODO Handler Data Ngang


def saveNgang(data):
    ngang_path = Path().path_number()
    update = data["update"]
    number = data["number"]
    stt = data["stt"]
    change = data["change"]

    # / Save STT
    with open(os.path.join(ngang_path, "number.json"), "r") as file:
        ngang_data = json.load(file)

    ngang_data["stt"] = stt
    ngang_data["change"] = change
    with open(os.path.join(ngang_path, "number.json"), "w") as file:
        json.dump(ngang_data, file)

    # / Save Data Ngang
    with open(os.path.join(ngang_path, f"number_{number}.json"), "w") as file:
        json.dump(update, file)

    return


def backUpNgang(data):
    ngang_path = Path().path_number()
    number = data["number"]

    # / Render STT Ngang
    stt = []
    for j in range(41):
        value = f"{j + 1:02}"
        stt.append(value)

    # / Load and Save STT Ngang
    with open(os.path.join(ngang_path, "number.json"), "r") as file:
        stt_ngang = json.load(file)

    stt_ngang["stt"][number] = stt
    stt_ngang["change"] = [
        item for item in stt_ngang["change"] if item["number"] != number
    ]

    with open(os.path.join(ngang_path, "number.json"), "w") as file:
        json.dump(stt_ngang, file)

    # / Load and save Ngang Data
    with open(os.path.join(ngang_path, f"number_backup.json"), "r") as file:
        ngang_data = json.load(file)

    number_change = list(
        map(lambda item: list(map(lambda x: TachVaGhep(number, x), item)), ngang_data)
    )
    with open(os.path.join(ngang_path, f"number_{number}.json"), "w") as file:
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
    file = [file for file in files if not "backup" in file]
    if len(file) == 0:
        return files
    else:
        return file


def Generate_Id():
    # / Generate 2 bytes of random data and ID
    random_bytes = secrets.token_bytes(8)
    id = random_bytes.hex()
    return id


def get_range_by_index(index, skip):
    """Xác định phạm vi dựa trên index."""
    if 1 <= index <= 10:
        return 1 + skip, 10 + skip
    elif 11 <= index <= 20:
        return 11 + skip, 20 + skip
    elif 21 <= index <= 30:
        return 21 + skip, 30 + skip
    else:
        return None  # Trả về None nếu index không hợp lệ


def extract_index(s):
    # Tách chuỗi tại dấu chấm
    parts = s.split(".")

    # Lấy phần đầu tiên và chuyển đổi sang số nguyên
    if parts:
        index = parts[1]  # Phần trước dấu chấm
        return int(index)  # Chuyển đổi sang số nguyên
    return None  # Nếu không tìm thấy


def save_ngang_backup(data):
    ngang_path = Path().path_number()
    ngang_data = data["ngang_data"]
    # / Load File ngang db
    with open(os.path.join(ngang_path, "number.json"), "r") as file:
        ngang_db = json.load(file)

    # / Make Data STT for ngang data
    stt_data = []
    for i in range(11):
        stt_col = []
        for j in range(131):
            value = f"{j:02}"
            stt_col.append(value)
        stt_data.append(stt_col)

    ngang_db["stt"] = stt_data
    ngang_db["change"] = []

    # / Save ngang DB
    with open(os.path.join(ngang_path, "number.json"), "w") as file:
        json.dump(ngang_db, file)

    # / Save new backup ngang
    with open(os.path.join(ngang_path, f"number_backup.json"), "w") as file:
        json.dump(ngang_data, file)

    # / re-render all bo chuyen doi
    for i in range(11):
        if i == 0:
            with open(os.path.join(ngang_path, f"ngang_{i}.json"), "w") as file:
                json.dump(ngang_data, file)
        else:
            number_change = list(
                map(
                    lambda item: list(map(lambda x: TachVaGhep(i, x), item)), ngang_data
                )
            )
            with open(os.path.join(ngang_path, f"ngang_{i}.json"), "w") as file:
                json.dump(number_change, file)

    return {"ngang_info": ngang_db, "ngang_data": ngang_data}


def sync_ngang(data):
    update = data["update"]
    number = data["number"]
    name = data["name"]
    stt = data["stt"]
    pm = data["pm"]
    current_path = rf"C:\data"
    index = extract_index(name)

    # Xác định phạm vi index dựa trên pm
    if pm == 1:
        range_tuple = get_range_by_index(index, 0)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 2:
        range_tuple = get_range_by_index(index, 30)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 3:
        range_tuple = get_range_by_index(index, 60)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 4:
        range_tuple = get_range_by_index(index, 90)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 5:
        range_tuple = get_range_by_index(index, 120)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 6:
        range_tuple = get_range_by_index(index, 150)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    else:
        return "Type count không hợp lệ"

    range_start, range_end = range_tuple

    for i in range(range_start - 1, range_end):  # Chuyển đổi sang chỉ số 0
        file_type = i + 1
        ngang_path = os.path.join(current_path, f"{file_type}", "number")
        with open(os.path.join(ngang_path, "number.json"), "r") as file:
            ngang_db = json.load(file)

        ngang_db["stt"] = stt
        ngang_db["change"] = []

        # / Save Thong DB
        with open(os.path.join(ngang_path, "number.json"), "w") as file:
            json.dump(ngang_db, file)

        # / Save thong data
        with open(os.path.join(ngang_path, f"number_{number}.json"), "w") as file:
            json.dump(update, file)

    return f"Đã đồng bộ dữ liệu"


def convert_string_format(input_string):
    # Match the pattern "Bản Xb.Y" where X and Y are numbers
    _, suffix = input_string.split(" ", 1)
    bo, app = suffix.split(".")

    type_count = "Trắng" if bo == "0" else bo
    # Assuming Tập is the same as App in this context
    type_app = "Tập 1" if int(app) < 11 else "Tập 2" if int(app) < 21 else "Tập 3"

    # Format the new string
    return f"A{app} - {type_app} - Bộ {type_count}"


def convert_string_format_type(input_string):
    # Match the pattern "Bản Xb.Y" where X and Y are numbers
    _, suffix = input_string.split(" ", 1)
    bo, app = suffix.split(".")

    type_count = "Trắng" if bo == "0" else bo
    # Assuming Tập is the same as App in this context
    type_app = "Tập 1" if int(app) < 11 else "Tập 2" if int(app) < 21 else "Tập 3"

    # Format the new string
    return f"Bộ {type_count} - {type_app}"

def convert_string_format_type_pm(input_string):
    # Match the pattern "Bản Xb.Y" where X and Y are numbers
    _, suffix = input_string.split(" ", 1)
    bo, app = suffix.split(".")

    type_count = "Trắng" if bo.startswith("0") else bo

    # Format the new string
    return f"Bộ {type_count}"


def convert_string_to_type_count(input_string):
    # Match the pattern "Bản Xb.Y" where X and Y are numbers
    _, suffix = input_string.split(" ", 1)
    bo, app = suffix.split(".")

    type_count = 0 if bo.startswith("0") else bo

    # Format the new string
    return type_count


# //TODO ———————————————[Setting Async]———————————————
def async_setting_number_pm(data):
    current_path = rf"C:\data"
    pm = data.get("pm")
    name = data.get("name")

    # Xác định phạm vi index dựa trên type_count
    if pm == 1:
        range_tuple = 0,30
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 2:
        range_tuple = 31,60
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 3:
        range_tuple = 61,90
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 4:
        range_tuple = 91,120
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 5:
        range_tuple = 121, 150
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 6:
        range_tuple = 151,180
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    else:
        return "Type count không hợp lệ"
    
    range_start, range_end = range_tuple
    step = 0
    for i in range(range_start - 1, range_end):  # Chuyển đổi sang chỉ số 0
        step += 1
        file_type = i + 1
        db_path = os.path.join(current_path, f"{file_type}", "db")

        with open(os.path.join(db_path, 'index.json') , 'r') as file:
            db = json.load(file)

        db['meta']['number'] = step
        
        with open(os.path.join(db_path, 'index.json') , 'w') as file:
            json.dump(db, file)
        if step == 10:
            step = 0

    name_pm = convert_string_format_type_pm(name)

    return f"Đã đặt bộ chuyển đổi cho {name_pm}, xin vui lòng thoát Bảng Tính"

def async_setting_range_thong(data):
    current_path = rf"C:\data"
    name = data['name']
    range_thong = data['thong']['value']
    pm = data.get("pm")

    index = extract_index(name)

    # Xác định phạm vi index dựa trên pm
    if pm == 1:
        range_tuple = get_range_by_index(index, 0)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 2:
        range_tuple = get_range_by_index(index, 30)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 3:
        range_tuple = get_range_by_index(index, 60)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 4:
        range_tuple = get_range_by_index(index, 90)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 5:
        range_tuple = get_range_by_index(index, 120)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 6:
        range_tuple = get_range_by_index(index, 150)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    else:
        return "Type count không hợp lệ"
    
    range_start, range_end = range_tuple
    for i in range(range_start - 1, range_end):  # Chuyển đổi sang chỉ số 0
        file_type = i + 1
        db_path = os.path.join(current_path, f"{file_type}", "db")

        with open(os.path.join(db_path, 'index.json') , 'r') as file:
            db = json.load(file)

        db['thong']['value'] = range_thong
        
        with open(os.path.join(db_path, 'index.json') , 'w') as file:
            json.dump(db,file)

    name_pm = convert_string_format_type_pm(name)

    return f"Đã đồng bộ khoảng thông cho {name_pm}, xin vui lòng thoát Bảng Tính"

def save_setting_tables(data):
    col = data["col"]
    name = data["thong"]["name"]
    meta = data["meta"]
    index = extract_index(name)

    path_thong = Path().path_thong()
    with open(os.path.join(path_thong, "thongs.json"), "r") as file:
        thong_db = json.load(file)

    pm = thong_db["pm"]
    current_path = rf"C:\data"

    # Xác định phạm vi index dựa trên pm
    index = extract_index(name)

    # Xác định phạm vi index dựa trên type_count
    if pm == 1:
        range_tuple = get_range_by_index(index, 0)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 2:
        range_tuple = get_range_by_index(index, 30)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 3:
        range_tuple = get_range_by_index(index, 60)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 4:
        range_tuple = get_range_by_index(index, 90)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 5:
        range_tuple = get_range_by_index(index, 120)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    elif pm == 6:
        range_tuple = get_range_by_index(index, 150)
        if range_tuple is None:
            return "Index không nằm trong phạm vi hợp lệ"
    else:
        return "Type count không hợp lệ"

    range_start, range_end = range_tuple

    # Tiến hành đồng bộ dữ liệu cho các index trong phạm vi xác định
    for i in range(range_start - 1, range_end):  # Chuyển đổi sang chỉ số 0
        file_type = i + 1
        db_path = os.path.join(current_path, f"{file_type}", "db")

        # Đọc dữ liệu từ index.json
        with open(os.path.join(db_path, "index.json"), "r") as file:
            db_index = json.load(file)

        # Cập nhật thông tin trong db_index
        db_index["col"] = col
        # db_index["thong"]["value"] = value
        db_index["meta"]["notice"] = meta["notice"]
        db_index["meta"]["features"] = meta["features"]
        db_index["meta"]["setting"] = meta["setting"]
        db_index["meta"]["tables"] = meta["tables"]
        # db_index["meta"]["number"] = meta["number"]
        db_index["meta"]["maxRow"] = meta["maxRow"]
        db_index["meta"]["buttons"] = meta["buttons"]

        # Ghi lại dữ liệu vào index.json
        with open(os.path.join(db_path, "index.json"), "w") as file:
            json.dump(db_index, file)

    # type_count_label = (
    #     "1a Số"
    #     if type_count == 1
    #     else ("2 Số" if type_count == 2 else "trắng" if type_count == 0 else "1b Số")
    # )

    return f"Đã đồng bộ dữ liệu"


