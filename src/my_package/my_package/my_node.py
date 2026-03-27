# file: lidar_publisher.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import json
import math
import random
import os

NUM_POINTS = 360
RANGE_MIN = 0.12
RANGE_MAX = 3.5
AVAILABLE_PATTERNS = ["front_wall", "left_wall", "right_wall"]

def create_empty_scan():
    return {
        "angle_min": math.radians(0),
        "angle_max": math.radians(359),
        "angle_increment": math.radians(1),
        "range_min": RANGE_MIN,
        "range_max": RANGE_MAX,
        "ranges": [float(RANGE_MAX) for _ in range(NUM_POINTS)],
        "intensities": [100.0 for _ in range(NUM_POINTS)],
    }

def make_the_wall(ranges, center_deg, width_deg):
    half_width = width_deg // 2
    for offset in range(-half_width, half_width + 1):
        idx = (center_deg + offset) % NUM_POINTS
        ranges[idx] = 0.4

def pattern_front_wall(scan):
    make_the_wall(scan["ranges"], 0, 40)

def pattern_left_wall(scan):
    make_the_wall(scan["ranges"], 90, 30)

def pattern_right_wall(scan):
    make_the_wall(scan["ranges"], 270, 30)

def generate_single_scan(pattern_name):
    scan = create_empty_scan()
    if pattern_name == "front_wall":
        pattern_front_wall(scan)
    elif pattern_name == "left_wall":
        pattern_left_wall(scan)
    elif pattern_name == "right_wall":
        pattern_right_wall(scan)
    return scan

class ScanPublisher(Node):
    def __init__(self):
        super().__init__('scan_publisher')
        self.publisher_ = self.create_publisher(LaserScan, '/scan', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def convert_to_ros_scan(self, scan_dict):
        msg = LaserScan()
        msg.angle_min = scan_dict["angle_min"]
        msg.angle_max = scan_dict["angle_max"]
        msg.angle_increment = scan_dict["angle_increment"]
        msg.range_min = scan_dict["range_min"]
        msg.range_max = scan_dict["range_max"]
        msg.ranges = list(map(float, scan_dict["ranges"]))
        msg.intensities = list(map(float, scan_dict["intensities"]))
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "laser_frame"
        return msg

    def timer_callback(self):
        pattern = random.choice(AVAILABLE_PATTERNS)
        scan_dict = generate_single_scan(pattern)
        msg = self.convert_to_ros_scan(scan_dict)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing scan ({pattern})')

def main(args=None):
    rclpy.init(args=args)
    node = ScanPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()