import os
import json
from os import path
from save_db import insert_year_dataset_output_batch

config_dir_path = path.join('data', 'Football')

year_set_files = [f for f in os.listdir(config_dir_path) if path.isfile(path.join(config_dir_path, f))]

year_set_files.sort(key=lambda x: int(x[6:-5]), reverse=True)

print(year_set_files)

for f in year_set_files:
    data = json.load(open(path.join(config_dir_path, f), 'r', encoding='utf-8'))

    year = int(f[6:-5])

    batch_data = []
    for set_msg in data:
        batch_data.append({
            "category": "Football",
            "year": year,
            "sid": set_msg['sid'],
            "set_name": set_msg['name'],
        })

    insert_year_dataset_output_batch(batch_data)
