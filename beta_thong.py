import json

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
thong_value_package = []
for row in range(131):
    line = f"{row:02}"
    thong_data = []
    thong_value_data = []
    count = 0
    if row > 99:
        for step in range(1200):
            thong_data.append(None)
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
    thong_value_package.append(thong_value_data)

# Convert to thong data file old
thong_old_data = []
for thong in range(1200):
    thong_data = []
    for row in range(131):
        value = thong_package[row][thong]
        thong_data.append(value)
    thong_old_data.append(thong_data)

# Export data to JSON file
output_data = {
    "thong_package": thong_package,
    "thong_value_package": thong_value_package,
    "thong": thong_old_data,
}

with open("data-test.json", "w") as json_file:
    json.dump(output_data, json_file)
