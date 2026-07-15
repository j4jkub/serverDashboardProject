import requests
import psutil
import redis
import json

class Collector:
    def __init__(self, config):
        self.config = config

        self.url = config["url"]
        
        self.cpu_usage = []
        self.cpu_usage_max = 0.0
        self.cpu_usage_min = 99999.0

        self.ram_usage = []
        self.ram_usage_max = 0.0
        self.ram_usage_min = 99999.0

        self.disk_used = 0 #in bytes

        self.current_metrics = {}

        self.measurement_interval = 10 # in seconds

        self.redis_client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

    def collect(self):
        
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        
        self.cpu_usage.append(cpu_usage)
        self.ram_usage.append(ram_usage)
        
        self.current_metrics = {
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "disk_used": psutil.disk_usage('/').used
        }
        self.redis_client.set("latest_metrics", json.dumps(self.current_metrics, separators=(',', ':')))


        if cpu_usage > self.cpu_usage_max:
            self.cpu_usage_max = cpu_usage

        if cpu_usage < self.cpu_usage_min:
            self.cpu_usage_min = cpu_usage
        
        if ram_usage > self.ram_usage_max:
            self.ram_usage_max = ram_usage

        if ram_usage < self.ram_usage_min:
            self.ram_usage_min = ram_usage

    def process(self):
        for i in range(self.measurement_interval):
            self.collect()
        self.save()
    
    def clear_data(self):
        self.data = {}
        self.cpu_usage = []
        self.cpu_usage_max = 0.0
        self.cpu_usage_min = 99999.0

        self.ram_usage = []
        self.ram_usage_max = 0.0
        self.ram_usage_min = 99999.0

        self.disk_used = 0 #in bytes

    def save(self):
        self.data = {
            "cpu_usage_avg": sum(self.cpu_usage) / len(self.cpu_usage) if self.cpu_usage else 0.0,
            "cpu_usage_min": self.cpu_usage_min,
            "cpu_usage_max": self.cpu_usage_max,
            "ram_usage_avg": sum(self.ram_usage) / len(self.ram_usage) if self.ram_usage else 0.0,
            "ram_usage_min": self.ram_usage_min,
            "ram_usage_max": self.ram_usage_max,
            "disk_used": psutil.disk_usage('/').used
        }

        try:
            response = requests.post(self.url, json=self.data)
            response.raise_for_status()
            print(f"Data sent successfully: {self.data}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")


        self.clear_data()

    def run(self):
        while True:
            self.process()

collector = Collector(config={"url": "http://localhost:8000/api/metrics/"})
collector.run()