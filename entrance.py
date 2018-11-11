
class Entrance():
    def __init__(self, x1, x2, y1, y2, next_map, x3, y3):
        """交互点"""
        self.check_point = x1, x2, y1, y2
        """下一个地图"""
        self.next_map = next_map
        """到下一个地图的坐标"""
        self.to_point = x3, y3