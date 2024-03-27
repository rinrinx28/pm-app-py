import os
from Pages.components.path import Path
import json

def createSTTNumber():
    path = Path()
    path_number = path.path_number()

    stt = []
    for i in range(6):
        stt_data= []
        for j in range(31):
            value = f'{j + 1}' if j >= 9 else f'0{j + 1}'
            stt_data.append(value)
        stt.append(stt_data)
    
    with open(os.path.join(path_number, 'number.json'), 'w') as file:
        json.dump(stt, file)

createSTTNumber()