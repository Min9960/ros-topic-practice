import roslibpy
import numpy as np
import mysql.connector
from datetime import datetime
import json
import time

# MySQL 연결 설정 (autocommit 활성화)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",
    database="lidar",
    autocommit=True
)
cursor = conn.cursor()

# ROSBridge 서버 연결
client = roslibpy.Ros(host='localhost', port=9090)
client.run()

# 연결 완료까지 대기
while not client.is_connected:
    time.sleep(0.1)

print('Connected to ROSBridge:', client.is_connected)

# LaserScan 토픽 구독
laser_sub = roslibpy.Topic(client, '/scan', 'sensor_msgs/LaserScan')

safe_dist = 0.5  # 안전거리 기준
RANGE_MAX = 3.5  # publisher와 동일하게 설정

# 유효한 값만 필터링 (NaN, inf 제거)
def clean_ranges(r):
    return r[np.isfinite(r)]

def callback(message):
    ranges = np.array(message['ranges'])

    # 데이터 길이 검증
    if len(ranges) != 360:
        print("Invalid scan size")
        return

    # 방향별 데이터 추출 + 정제
    front = clean_ranges(np.r_[ranges[350:360], ranges[0:10]])
    left  = clean_ranges(ranges[80:100])
    right = clean_ranges(ranges[260:280])

    # 평균 계산 (비어있으면 최대값 사용)
    front_dist = np.mean(front) if len(front) > 0 else RANGE_MAX
    left_dist  = np.mean(left)  if len(left) > 0 else RANGE_MAX
    right_dist = np.mean(right) if len(right) > 0 else RANGE_MAX

    # 액션 결정
    if front_dist < safe_dist:
        action = 'turn_left' if left_dist > right_dist else 'turn_right'
    else:
        action = 'go_forward'

    print(f'front: {front_dist:.2f}, left: {left_dist:.2f}, right: {right_dist:.2f}, action: {action}')

    # DB 저장
    ranges_json = ranges.tolist()
    query = """
    INSERT INTO lidar (ranges, `when`, action)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (json.dumps(ranges_json), datetime.now(), action))
    print("Saved to DB.")

# 구독 시작
laser_sub.subscribe(callback)

try:
    print('Listening to /scan topic... Press Ctrl+C to exit.')
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print('Shutting down...')

finally:
    laser_sub.unsubscribe()
    client.terminate()
    cursor.close()
    conn.close()