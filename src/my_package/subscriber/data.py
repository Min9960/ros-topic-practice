# file: lidar_to_mysql.py
import os
import json
import mysql.connector
from datetime import datetime

# MySQL 연결 설정
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",     # 실제 MySQL root 비밀번호
    database="lidar"     # 미리 생성한 DB 이름
)
cursor = conn.cursor()

json_dir = "lidar_json"  # 퍼블리셔에서 생성한 폴더

for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(json_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            scan = json.load(f)

        # MySQL 컬럼에 맞춰 변환
        ranges_json = json.dumps(scan["ranges"])
        action = scan["meta"]["pattern"]

        query = """
        INSERT INTO lidardata (ranges, `when`, action)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (ranges_json, datetime.now(), action))
        conn.commit()

        print(f"Inserted {filename} -> action={action}")

cursor.close()
conn.close()