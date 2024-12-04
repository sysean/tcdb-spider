# 读取 s3://irida/tcdb_embedding_20241203/ 下所有 json 文件，遍历它

# 每一个json文件里面是一个json数组，遍历该数组，数组的每一个对象如下所示:

# {"image_name": "251191-15544088Fr.jpg", "embedding": ""}

# 拿到 image_name, 截取 251191-15544088 部分，前面拼上 Football_ 作为 card_v2表的id，查询 card_v2 表，拿到数据之后，将数据和原先的 json 对象进行 merge

# 重新生成一个新的 json 数组，并且写入到 s3://irida/tcdb_embedding_20241204/ 下，文件名和原先一样

import boto3
import json

from save_db import query_card_list

s3 = boto3.client('s3')

is_after = False
# 读取 s3://irida/tcdb_embedding_20241203/ 下所有 json 文件，遍历它
response = s3.list_objects_v2(Bucket='irida', Prefix='tcdb_embedding_20241203/')
for content in response['Contents']:
    if content['Key'].endswith('.json'):
        if not is_after and content['Key'] != 'tcdb_embedding_20241203/335000.json':
            continue

        is_after = True

        print(content['Key'])

        # 读取 json 文件到内存为list对象
        obj = s3.get_object(Bucket='irida', Key=content['Key'])
        json_data = json.loads(obj['Body'].read().decode('utf-8'))

        json_data_dict = {}

        # 遍历 json 数组
        card_id_list = []
        for item in json_data:
            image_name = item['image_name'][:-6]
            card_id = 'Football_' + image_name
            card_id_list.append(card_id)
            json_data_dict[card_id] = item

        # 查询 card_v2 表
        card_data_list = query_card_list(card_id_list)

        new_json_data = [{
            "id": card_data.id,
            "dataset_id": card_data.dataset_id,
            "index": card_data.index,
            "name": card_data.name,
            "team": card_data.team,
            "card_num": card_data.card_num,
            "sub_set": card_data.sub_set,
            "player_url": card_data.player_url,
            "front_img": card_data.front_img,
            "back_img": card_data.back_img,
            "front_submitted_time": card_data.front_submitted_time,
            "back_submitted_time": card_data.back_submitted_time,
            "price": card_data.price,
            "image_name": json_data_dict[card_data.id]['image_name'],
            "embedding": json_data_dict[card_data.id]['embedding']
        } for card_data in card_data_list]

        # 重新生成一个新的 json 数组，并且写入到 s3://irida/tcdb_embedding_20241204/ 下，文件名和原先一样
        new_json_str = json.dumps(new_json_data)
        new_key = content['Key'].replace('tcdb_embedding_20241203', 'tcdb_embedding_20241204')
        s3.put_object(Bucket='irida', Key=new_key, Body=new_json_str)
