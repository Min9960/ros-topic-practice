안냐세요 ros2를 활용한 가상 Lidar 센서 시뮬레이션 코드입니다.

ros2 토픽 발행을 우분투를 활용했고, 구독은 파이썬으로 했습니다.
토픽발행을 하면서 센서 데이터를 파일로 저장하고, 파이썬에서 불러들여 mysql 서버에 업로드합니다.

# 🚗 LIDAR Simulation & Data Logging (ROS2 + MySQL)

## 📌 Overview

이 프로젝트는 ROS 2 환경에서 LIDAR 데이터를 시뮬레이션하고,
해당 데이터를 실시간으로 MySQL 데이터베이스에 저장하는 시스템입니다.

* LIDAR 센서 없이도 테스트 가능
* 다양한 벽 패턴 시뮬레이션 지원
* JSON 형태로 데이터 저장

---

## 🛠 Tech Stack

* ROS 2 (rclpy)
* Python 3
* MySQL
* roslibpy

---

## 📂 Project Structure

```
lidar/
├── src/
│   ├── publisher/
│   │   └── lidar_publisher.py   # LIDAR 데이터 생성
│   ├── subscriber/
│   │   └── subscriber.py        # 데이터 수신 및 DB 저장
│
├── README.md
```

---

## ⚙️ How It Works

### 1️⃣ Publisher (LIDAR Simulator)

* 360도 스캔 데이터 생성
* 벽 패턴 랜덤 생성:

  * front_wall
  * left_wall
  * right_wall
* `/scan` 토픽으로 publish

### 2️⃣ Subscriber

* `/scan` 토픽 구독
* LaserScan 데이터를 JSON으로 변환
* MySQL에 저장

---

## 🗄 Database Setup

### 1. MySQL 접속

```bash
mysql -u root -p
```

### 2. 데이터베이스 생성

```sql
CREATE DATABASE lidar;
USE lidar;
```

### 3. 테이블 생성

```sql
CREATE TABLE lidardata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ranges JSON,
    created_at DATETIME,
    action VARCHAR(50)
);
```

---

## ▶️ How to Run

### 1️⃣ ROS2 실행

```bash
source /opt/ros/<your_ros2>/setup.bash
```

---

### 2️⃣ Publisher 실행

```bash
python3 lidar_publisher.py
```

---

### 3️⃣ Subscriber 실행

```bash
python3 subscriber.py
```

---

## 📊 Example Data

```json
{
  "ranges": [3.5, 3.5, 0.4, 0.4, ...],
  "created_at": "2026-03-27 12:00:00",
  "action": "front_wall"
}
```

---

## ⚠️ Troubleshooting

### ❗ Table doesn't exist

```
Table 'lidar.lidar' doesn't exist
```

👉 해결:

* 테이블 이름 확인 (`lidardata`)
* DB 선택 확인 (`USE lidar;`)

---

### ❗ PyCharm vs bash 데이터 불일치

👉 원인:

* 서로 다른 MySQL 서버 연결

👉 해결:

* host / port / database 동일하게 설정

---

## 💡 Future Improvements

* 실시간 시각화 (RViz)
* 데이터 분석 및 시각화
* 장애물 감지 알고리즘 추가

---

## 👨‍💻 Author

* Min

---

## 📄 License

MIT License
