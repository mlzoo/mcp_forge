import random
import time
from abc import ABC, abstractmethod
from typing import Any, Dict


class ParkingService(ABC):
    """停车场服务抽象基类"""

    @abstractmethod
    def find_nearby_parking_lots(self, address: str, radius: float = 1.0) -> Dict[str, Any]:
        """查找附近停车场"""
        pass

    @abstractmethod
    def parking_lot_details(self, parking_lot_id: str) -> Dict[str, Any]:
        """获取停车场详情"""
        pass


class ParkingServiceMockImpl(ParkingService):
    """停车场服务Mock实现类"""

    def find_nearby_parking_lots(self, address: str, radius: float = 1.0) -> Dict[str, Any]:
        """查找附近停车场的Mock实现"""
        time.sleep(0.1)  # 模拟API延迟

        # 模拟停车场数据
        parking_lots = [
            {
                "parking_lot_id": "P001",
                "parking_lot_name": "MYSPACE富邦金融中心停車場",
                "address": "台北市信義區松仁路100號B2-B5",
                "distance": round(random.uniform(0.1, radius), 2),  # noqa: S311
                "available_spaces": random.randint(0, 100),  # noqa: S311
                "total_spaces": 200,
                "hourly_rate": 60,
                "coordinates": {"latitude": 25.0330, "longitude": 121.5654},
            },
            {
                "parking_lot_id": "P002",
                "parking_lot_name": "信義威秀停車場",
                "address": "台北市信義區松壽路18號B1-B4",
                "distance": round(random.uniform(0.1, radius), 2),  # noqa: S311
                "available_spaces": random.randint(0, 150),  # noqa: S311
                "total_spaces": 300,
                "hourly_rate": 50,
                "coordinates": {"latitude": 25.0359, "longitude": 121.5672},
            },
            {
                "parking_lot_id": "P003",
                "parking_lot_name": "台北101購物中心停車場",
                "address": "台北市信義區信義路五段7號B1-B4",
                "distance": round(random.uniform(0.1, radius), 2),  # noqa: S311
                "available_spaces": random.randint(0, 200),  # noqa: S311
                "total_spaces": 400,
                "hourly_rate": 70,
                "coordinates": {"latitude": 25.0338, "longitude": 121.5645},
            },
            {
                "parking_lot_id": "P004",
                "parking_lot_name": "遠東百貨寶慶停車場",
                "address": "台北市萬華區寶慶路32號B1-B3",
                "distance": round(random.uniform(0.1, radius), 2),  # noqa: S311
                "available_spaces": random.randint(0, 80),  # noqa: S311
                "total_spaces": 150,
                "hourly_rate": 45,
                "coordinates": {"latitude": 25.0421, "longitude": 121.5067},
            },
            {
                "parking_lot_id": "P005",
                "parking_lot_name": "微風廣場停車場",
                "address": "台北市松山區復興南路一段39號B1-B3",
                "distance": round(random.uniform(0.1, radius), 2),  # noqa: S311
                "available_spaces": random.randint(0, 120),  # noqa: S311
                "total_spaces": 250,
                "hourly_rate": 55,
                "coordinates": {"latitude": 25.0468, "longitude": 121.5443},
            },
        ]

        # 按距离排序
        sorted_lots = sorted(parking_lots, key=lambda x: x["distance"])

        return {
            "code": 200,
            "message": "success",
            "data": {
                "search_address": address,
                "radius": radius,
                "parking_lots": sorted_lots,
                "total": len(sorted_lots),
            },
        }

    def parking_lot_details(self, parking_lot_id: str) -> Dict[str, Any]:
        """获取停车场详情的Mock实现"""
        time.sleep(0.1)  # 模拟API延迟

        # 模拟停车场详细信息
        details = {
            "P001": {
                "parking_lot_id": "P001",
                "parking_lot_name": "MYSPACE富邦金融中心停車場",
                "address": "台北市信義區松仁路100號B2-B5",
                "available_spaces": random.randint(0, 200),  # noqa: S311
                "total_spaces": 200,
                "hourly_rate": 60,
                "business_hours": "00:00-24:00",
                "features": ["室內停車場", "電梯", "無障礙設施", "充電樁"],
                "payment_methods": ["現金", "信用卡", "行動支付"],
                "contact": {"phone": "02-2345-6789", "email": "service@mysbase-parking.com"},
                "real_time_info": {"is_open": True, "congestion_level": "中等", "estimated_wait_time": "5分鐘"},
            }
        }

        return {
            "code": 200,
            "message": "success",
            "data": details.get(parking_lot_id, {"error": "找不到該停車場資訊", "parking_lot_id": parking_lot_id}),
        }


# FastAPI 依赖注入函数
def get_parking_service() -> ParkingService:
    """获取停车场服务实例"""
    return ParkingServiceMockImpl()


class ParkingServiceImpl(ParkingService):
    """停车场服务真实实现类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def find_nearby_parking_lots(self, address: str, radius: float = 1.0) -> Dict[str, Any]:
        raise NotImplementedError

    def parking_lot_details(self, parking_lot_id: str) -> Dict[str, Any]:
        raise NotImplementedError
