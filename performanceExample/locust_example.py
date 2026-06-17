"""
Locust 负载测试示例

用于模拟大量并发用户访问系统，测试系统的性能和稳定性
"""

from locust import HttpUser, task, between, LoadTestShape


class WebsiteUser(HttpUser):
    """定义单个用户的行为"""
    
    # 用户行为之间的等待时间（1-3秒）
    wait_time = between(1, 3)
    
    def on_start(self):
        """用户开始时执行的初始化操作"""
        # 模拟用户登录
        self.client.post(
            "/login",
            {
                "username": "testuser",
                "password": "password123"
            }
        )
    
    @task(3)  # 权重为3，执行频率更高
    def view_rooms(self):
        """浏览房间列表"""
        self.client.get("/rooms")
    
    @task(2)
    def view_single_room(self):
        """查看单个房间详情"""
        # 随机选择房间ID
        self.client.get("/rooms/1")
    
    @task(1)
    def search_rooms(self):
        """搜索房间"""
        self.client.get("/rooms?search=Beijing")
    
    @task(1)
    def view_profile(self):
        """查看个人资料"""
        self.client.get("/profile")


class StagesShape(LoadTestShape):
    """定义负载测试阶段"""
    
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 1},   # 1分钟内达到10用户
        {"duration": 120, "users": 50, "spawn_rate": 2},  # 2分钟内达到50用户
        {"duration": 180, "users": 100, "spawn_rate": 3}, # 3分钟内达到100用户
        {"duration": 240, "users": 150, "spawn_rate": 2}, # 4分钟内达到150用户
        {"duration": 300, "users": 200, "spawn_rate": 2}, # 5分钟内达到200用户
    ]
    
    def tick(self):
        run_time = self.get_run_time()
        
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
        
        return None


if __name__ == "__main__":
    import os
    os.system("locust -f locust_example.py --host=https://fangdong.fun")
