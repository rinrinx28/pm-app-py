import os
from Pages.components.path import Path
import secrets
import json
import shutil


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


def createThong(data, path):
    os.makedirs(path, exist_ok=True)
    thong_path = path
    row = 131
    value = data.get("value")
    col = value
    id = Generate_Id()
    type_count = data.get("type_count")

    thong_file = []
    thong_file_sp = []
    step = 0
    # / Create Thong
    if type_count == 1:
        # Define steps
        steps = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 0, 1, 2, 3],
            [3, 4, 5, 6, 7, 8, 9, 0, 1, 2],
            [7, 8, 9, 0, 1, 2, 3, 4, 5, 6],
        ]

        # Initialize modifications for array a in each step
        modifications_a = [0, 8, 4, 2]

        # Process data in steps
        step_size = 1200 // 4
        thong_package = []
        for row in range(131):
            line = f"{row:02}"
            thong_data = []
            thong_value_data = []
            count = 0
            if row > 99:
                for step in range(1200):
                    thong_data.append("")
                    for luot in range(step, step + step_size, 30):
                        thong_value_data.append(["", ""])
            else:
                for step in range(0, 1200, step_size):
                    count_h = 0
                    for luot in range(step, step + step_size, 30):
                        e = (int(line[0]) + modifications_a[count]) % 10
                        h = (int(line[1]) + steps[count][count_h]) % 10
                        for thong in range(luot, luot + 30):
                            if thong == luot:
                                thong_data.append((e + h) % 10)
                            elif thong == luot + 1:
                                thong_data.append((h + thong_data[thong - 1]) % 10)
                            else:
                                thong_data.append(
                                    (thong_data[thong - 2] + thong_data[thong - 1]) % 10
                                )
                        thong_value_data.append([e, h])
                        count_h += 1
                    count += 1
            thong_package.append(thong_data)
            thong_file_sp.append(thong_value_data)

        # Convert to thong data file old
        for thong in range(1200):
            thong_data = []
            for row in range(131):
                value = thong_package[row][thong]
                thong_data.append(value)
            thong_file.append(thong_data)

    if type_count == 3:
        # Define steps
        steps = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 0, 1, 2, 3],
            [3, 4, 5, 6, 7, 8, 9, 0, 1, 2],
            [7, 8, 9, 0, 1, 2, 3, 4, 5, 6],
        ]

        # Initialize modifications for array a in each step
        modifications_a = [0, 8, 4, 2]

        # Process data in steps
        step_size = 1200 // 4
        thong_package = []
        for row in range(131):
            line = f"{row:02}"
            thong_data = []
            thong_value_data = []
            count = 0
            if row > 99:
                for step in range(1200):
                    thong_data.append("")
                    for luot in range(step, step + step_size, 30):
                        thong_value_data.append(["", ""])
            else:
                for step in range(0, 1200, step_size):
                    count_h = 0
                    for luot in range(step, step + step_size, 30):
                        e = (int(line[0]) + modifications_a[count]) % 10
                        h = (int(line[1]) + steps[count][count_h]) % 10
                        for thong in range(luot, luot + 30):
                            if thong == luot:
                                thong_data.append((e + h) % 10)
                            elif thong == luot + 1:
                                thong_data.append((h + thong_data[thong - 1]) % 10)
                            else:
                                thong_data.append(
                                    (thong_data[thong - 2] + thong_data[thong - 1]) % 10
                                )
                        thong_value_data.append([e, h])
                        count_h += 1
                    count += 1
            thong_package.append(thong_data)
            thong_file_sp.append(thong_value_data)

        # Convert to thong data file old
        for thong in range(1200):
            thong_data = []
            for row in range(131):
                value = thong_package[row][thong]
                thong_data.append(value)
            thong_file.append(thong_data)

    if type_count == 2:

        # Populate thong_file based on row and column values
        for i in range(0, col, 100):
            for k in range(i, i + 100, 10):
                for l in range(10):
                    thong_data = []
                    for j in range(row):
                        line = f"{j:02}"  # Format j as a two-digit string
                        if j > 99:
                            thong_data.append("")  # Append empty string if j exceeds 99
                        else:
                            if l == 0:
                                thong_data.append(
                                    f"{line}"
                                )  # Append formatted line for the first column
                            else:
                                thong_data.append(0)  # Default value for other columns
                    thong_file.append(thong_data)  # Append the constructed thong_data

        # Process and calculate values for thong_file
        for j in range(row):
            if j > 99:
                break  # Exit if j exceeds 99
            for i in range(0, col, 100):
                for k in range(i, i + 100, 10):
                    for l in range(10):
                        if i == 0:
                            if k == 0:
                                if l > 0:
                                    first = thong_file[k + l - 1][
                                        j
                                    ]  # Get previous value
                                    c = (
                                        int(first[0]) + int(first[1])
                                    ) % 10  # Calculate first digit
                                    d = (
                                        int(first[1]) + c
                                    ) % 10  # Calculate second digit
                                    thong_file[k + l][
                                        j
                                    ] = f"{c}{d}"  # Update thong_file
                            else:
                                if l == 0:
                                    first = thong_file[k + l - 10][
                                        j
                                    ]  # Reference a different row
                                    c = f"{(int(first[0]) + 1) % 10}{(int(first[1]) + 1) % 10}"
                                    thong_file[k + l][j] = f"{c}"  # Update first column
                                else:
                                    first = thong_file[k + l - 1][
                                        j
                                    ]  # Get previous value
                                    c = (
                                        int(first[0]) + int(first[1])
                                    ) % 10  # Calculate first digit
                                    d = (
                                        int(first[1]) + c
                                    ) % 10  # Calculate second digit
                                    thong_file[k + l][
                                        j
                                    ] = f"{c}{d}"  # Update thong_file

                        else:
                            if k == 100:
                                if l == 0:
                                    first = thong_file[98][
                                        j
                                    ]  # Reference the penultimate row
                                    second = thong_file[99][j]  # Reference the last row
                                    thong_file[100][
                                        j
                                    ] = f"{first[1]}{second[0]}"  # Update based on previous rows
                                else:
                                    first = thong_file[k + l - 1][
                                        j
                                    ]  # Get previous value
                                    c = (
                                        int(first[0]) + int(first[1])
                                    ) % 10  # Calculate first digit
                                    d = (
                                        int(first[1]) + c
                                    ) % 10  # Calculate second digit
                                    thong_file[k + l][
                                        j
                                    ] = f"{c}{d}"  # Update thong_file
                            else:
                                if l == 0:
                                    first = thong_file[k + l - 10][
                                        j
                                    ]  # Reference a different row
                                    c = f"{(int(first[0]) + 1) % 10}{(int(first[1]) + 1) % 10}"
                                    thong_file[k + l][j] = f"{c}"  # Update first column
                                else:
                                    first = thong_file[k + l - 1][
                                        j
                                    ]  # Get previous value
                                    c = (
                                        int(first[0]) + int(first[1])
                                    ) % 10  # Calculate first digit
                                    d = (
                                        int(first[1]) + c
                                    ) % 10  # Calculate second digit
                                    thong_file[k + l][
                                        j
                                    ] = f"{c}{d}"  # Update thong_file

    if type_count == 0:
        for i in range(col):
            thong_data = []
            for j in range(row):
                thong_data.append("")
            thong_file.append(thong_data)

    # / Make fisrt file Thong
    with open(os.path.join(thong_path, f"thong_{id}_backup.json"), "w") as file:
        json.dump(thong_file, file)

    if type_count == 1 or type_count == 3:
        with open(os.path.join(thong_path, f"thong_sp_{id}.json"), "w") as file:
            json.dump(thong_file_sp, file)

    # / Make Chuyen Doi
    for i in range(11):
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
    data_custon = [
        [
            "77902",
            "2345",
            "4562",
            "8906",
            "3456",
            "8712",
            "2389",
            "7623",
            "7823",
            "0921",
            "6721",
            "9853",
            "4509",
            "0732",
            "1231",
            "1250",
            "4587",
            "4589",
            "7894",
            "9856",
            "6542",
            "4125",
            "6352",
            "4562",
            "7845",
            "6523",
            "7896",
            "4589",
            "5632",
            "1235",
            "0214",
            "4563",
            "1234",
            "5687",
            "2135",
            "5896",
            "7896",
            "1478",
            "8524",
            "9635",
            "77894",
            "1234",
            "9865",
            "7894",
            "7896",
            "1478",
            "8529",
            "2589",
            "7897",
            "0145",
            "2589",
            "3214",
            "7456",
            "3210",
            "6875",
            "7532",
            "1598",
            "7530",
            "9876",
            "7896",
            "4589",
            "7896",
            "3258",
            "9654",
            "4568",
            "7896",
            "7532",
            "0236",
            "8657",
            "3210",
            "7418",
            "0147",
            "5468",
            "7896",
            "6547",
            "8521",
            "3654",
            "3257",
            "9804",
            "4178",
            "8963",
            "4578",
            "3214",
            "7896",
            "7441",
            "7896",
            "4561",
            "2147",
            "3210",
            "0147",
            "2314",
            "5698",
            "2145",
            "3578",
            "9514",
            "7536",
            "9578",
            "9510",
            "3257",
            "4568",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
        [
            "8024",
            "7032",
            "4784",
            "1346",
            "8928",
            "5780",
            "2342",
            "9234",
            "6236",
            "3168",
            "5297",
            "2789",
            "9251",
            "6213",
            "3795",
            "0137",
            "7809",
            "4601",
            "1563",
            "8025",
            "0124",
            "7896",
            "4678",
            "1680",
            "8152",
            "5374",
            "2346",
            "9028",
            "6930",
            "3452",
            "5671",
            "2453",
            "9025",
            "6897",
            "3569",
            "0231",
            "7983",
            "4785",
            "1097",
            "8039",
            "0568",
            "7890",
            "4312",
            "1234",
            "8906",
            "5238",
            "2450",
            "9132",
            "6794",
            "3126",
            "5885",
            "2357",
            "9889",
            "6231",
            "3673",
            "0345",
            "7987",
            "4569",
            "1231",
            "8903",
            "0342",
            "7984",
            "4896",
            "1678",
            "8790",
            "5342",
            "2354",
            "9056",
            "6708",
            "3450",
            "5789",
            "2341",
            "9023",
            "6345",
            "3457",
            "0679",
            "7021",
            "4563",
            "1345",
            "8567",
            "0346",
            "7098",
            "4560",
            "1032",
            "8234",
            "5346",
            "2348",
            "9230",
            "6782",
            "3564",
            "5463",
            "2345",
            "9087",
            "6789",
            "3451",
            "0123",
            "7895",
            "4567",
            "1239",
            "8231",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
        [
            "2345",
            "1478",
            "7410",
            "4789",
            "7417",
            "8975",
            "9630",
            "7536",
            "9510",
            "7532",
            "9512",
            "7531",
            "7536",
            "9874",
            "1478",
            "7412",
            "8521",
            "7475",
            "7531",
            "9547",
            "4580",
            "4567",
            "9864",
            "4678",
            "1270",
            "0532",
            "5690",
            "3491",
            "8931",
            "2367",
            "0945",
            "0934",
            "2345",
            "9854",
            "4567",
            "0934",
            "2345",
            "7521",
            "2980",
            "4567",
            "9801",
            "4567",
            "2345",
            "5678",
            "7642",
            "2439",
            "2312",
            "5632",
            "1743",
            "8932",
            "2367",
            "2315",
            "8439",
            "6557",
            "4567",
            "7490",
            "2145",
            "7390",
            "4513",
            "6577",
            "2341",
            "6789",
            "2345",
            "1234",
            "6789",
            "6543",
            "1232",
            "3456",
            "7891",
            "3456",
            "2345",
            "9087",
            "4357",
            "1234",
            "8901",
            "3456",
            "3456",
            "5678",
            "6789",
            "6789",
            "5679",
            "4567",
            "3457",
            "0987",
            "5673",
            "2347",
            "5670",
            "0852",
            "2345",
            "1234",
            "0961",
            "0986",
            "3456",
            "6780",
            "5421",
            "6709",
            "4568",
            "1268",
            "2345",
            "4567",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
        [
            "2345",
            "1478",
            "7410",
            "4789",
            "7417",
            "8975",
            "9630",
            "7536",
            "9510",
            "7532",
            "9512",
            "7531",
            "7536",
            "9874",
            "1478",
            "7412",
            "8521",
            "7475",
            "7531",
            "9547",
            "4580",
            "4567",
            "9864",
            "4678",
            "1270",
            "0532",
            "5690",
            "3491",
            "8931",
            "2367",
            "0945",
            "0934",
            "2345",
            "9854",
            "4567",
            "0934",
            "2345",
            "7521",
            "2980",
            "4567",
            "9801",
            "4567",
            "2345",
            "5678",
            "7642",
            "2439",
            "2312",
            "5632",
            "1743",
            "8932",
            "2367",
            "2315",
            "8439",
            "6557",
            "4567",
            "7490",
            "2145",
            "7390",
            "4513",
            "6577",
            "2341",
            "6789",
            "2345",
            "1234",
            "6789",
            "6543",
            "1232",
            "3456",
            "7891",
            "3456",
            "2345",
            "9087",
            "4357",
            "1234",
            "8901",
            "3456",
            "3456",
            "5678",
            "6789",
            "6789",
            "5679",
            "4567",
            "3457",
            "0987",
            "5673",
            "2347",
            "5670",
            "0852",
            "2345",
            "1234",
            "0961",
            "0986",
            "3456",
            "6780",
            "5421",
            "6709",
            "4568",
            "1268",
            "2345",
            "4567",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
    ]

    # / Make Data STT for thong data
    stt_data = []
    for i in range(11):
        stt_col = []
        for j in range(row):
            value = f"{j:02}"
            stt_col.append(value)
        stt_data.append(stt_col)

    # / Make new Data thong
    data["data"] = data_custon
    data["stt"] = stt_data
    data["id"] = id
    data["number"] = 0
    data["change"] = []
    data["type_thong"] = type_count
    data["setting"] = 0
    with open(os.path.join(thong_path, "thongs.json"), "w") as file:
        json.dump(data, file)
    return data


def Generate_Id():
    # / Generate 2 bytes of random data and ID
    random_bytes = secrets.token_bytes(8)
    id = random_bytes.hex()
    return id


def createDB(thong, name, path):
    thongId = thong["id"]
    thongName = thong["name"]
    id = Generate_Id()

    # Render number of col D of Tables Color
    col_d = []
    number_tables = 10
    number_of_col_d = 1
    total_col_d_of_table = 120
    for i in range(number_tables):
        total_col_d_table = []
        for j in range(total_col_d_of_table):
            total_col_d_table.append(number_of_col_d)
        col_d.append(total_col_d_table)

    data = {
        "name": name,
        "password": "0",
        "col": [1, 10],
        "thong": {"name": thongName, "value": [1, 10], "id": thongId},
        "meta": {
            "notice": {
                "count": [1, 1],
                "color": [1, 1],
                "color2": [1, 1],
                "colorM2": [1, 1],
                "colorM3": [1, 1],
                "colorM4": [1, 1],
                "colorM5": [1, 1],
                "colorM6": [1, 1],
                "colorM7": [1, 1],
                "colorM8": [1, 1],
                "colorM9": [1, 1],
                "colorM10": [1, 1],
            },
            "features": {"N:2": False, "N=1": {"status": False, "value": 0}},
            "setting": {
                "col_e": [2, 5],
                "col_e2": [2, 5],
                "col_e3": [2, 5],
                "col_e4": [1, 5],
                "col_e5": [1, 5],
                "col_e6": [1, 5],
                "col_e7": [1, 5],
                "col_e8": [1, 5],
                "col_e9": [1, 5],
                "col_e10": [1, 5],
            },
            "tables": [
                {
                    "enable": True,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
                {
                    "enable": True,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
                {
                    "enable": False,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
                {
                    "enable": False,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
                {
                    "enable": False,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
                {
                    "enable": False,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
                {
                    "enable": False,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
                {
                    "enable": False,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
                {
                    "enable": False,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
                {
                    "enable": False,
                    "col_d": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                    ],
                },
            ],
            "number": 0,
            "maxRow": 100,
            "buttons": [True, False],
        },
        "data": [],
        "id": id,
    }
    os.makedirs(path, exist_ok=True)

    stay = {"thong": 0, "ngang": 0}

    with open(os.path.join(path, "index.json"), "w") as file:
        json.dump(data, file)

    with open(os.path.join(path, "stay.json"), "w") as file:
        json.dump(stay, file)


def copy_files_into_folders(source_folder, destination_folder):
    try:
        # Walk through the directory tree
        for root, dirs, files in os.walk(source_folder):
            # Copy files into corresponding folders
            for file in files:
                source_file = os.path.join(root, file)
                destination_dir = os.path.join(
                    destination_folder, os.path.relpath(root, source_folder)
                )
                os.makedirs(destination_dir, exist_ok=True)
                destination_file = os.path.join(destination_dir, file)
                shutil.copy2(
                    source_file, destination_file
                )  # shutil.copy2 ensures metadata preservation

        print("Files copied into folders successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create():
    current_dir = r"C:\data"
    default_dir = r"C:\data\1"
    arr_folder = ["image", "number"]

    for i in range(2, 121):
        for folder in arr_folder:
            prev_dir = os.path.join(current_dir, str(i), folder)
            next_dir = os.path.join(default_dir, folder)
            copy_files_into_folders(next_dir, prev_dir)

    for i in range(1, 121):
        thong_dir = os.path.join(current_dir, str(i), "thong")
        db_dir = os.path.join(current_dir, str(i), "db")
        if i < 31:
            dataThong = createThong(
                {"value": 1200, "type_count": 1, "name": f"Bản 1a.{i}"}, thong_dir
            )
            createDB(dataThong, f"B{i}", db_dir)
        elif i > 30 and i < 61:
            dataThong = createThong(
                {"value": 600, "type_count": 2, "name": f"Bản 2.{i - 30}"}, thong_dir
            )
            createDB(dataThong, f"B{i}", db_dir)
        elif i > 60 and i < 91:
            dataThong = createThong(
                {"value": 1200, "type_count": 3, "name": f"Bản 1b.{i - 60}"}, thong_dir
            )
            createDB(dataThong, f"B{i}", db_dir)
        else:
            dataThong = createThong(
                {"value": 600, "type_count": 0, "name": f"Bản 0.{i - 90}"}, thong_dir
            )
            createDB(dataThong, f"B{i}", db_dir)


def create_ngang_file():
    default_dir = r"C:\data\1\number"
    with open(default_dir + "/number_backup.json", "r") as file:
        backup = json.load(file)
    for i in range(11):
        if i == 0:
            with open(default_dir + "/number_0.json", "w") as file:
                json.dump(backup, file)
        else:
            number_change = list(
                map(lambda item: list(map(lambda x: TachVaGhep(i, x), item)), backup)
            )
            with open(default_dir + f"/number_{i}.json", "w") as file:
                json.dump(number_change, file)


# Example usage
create()
# create_ngang_file()
