import sys
import uuid
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.append(str(Path(__file__).parent))

from fastapi import Depends, FastAPI
from fastapi_mcp import add_mcp_server
from pydantic import BaseModel, Field

from services.parking_service import ParkingService, get_parking_service

app = FastAPI()



class NearbyParkingRequest(BaseModel):
    """附近停车场请求模型"""
    address: str = Field(..., description="搜索地址")
    radius: float = Field(1.0, description="搜索半径（公里）")


class ParkingLotInfoRequest(BaseModel):
    """停车场详情请求模型"""
    parking_lot_id: str = Field(..., description="停车场ID")



@app.post("/parking/nearby", operation_id="find_nearby_parking")
async def find_nearby(
    request: NearbyParkingRequest,
    parking_service: ParkingService = Depends(get_parking_service)  # noqa: B008
):
    """查找附近停车场接口"""
    run_id = str(uuid.uuid4())
    print("run_id:", run_id)

    result = parking_service.find_nearby_parking_lots(
        request.address,
        request.radius
    )

    return {
        "status": "success",
        "parking_lots": result["data"]["parking_lots"],
        "message": f"已為您找到{len(result['data']['parking_lots'])}個停車場，搜尋範圍：{request.radius}公里"
    }


@app.post("/parking/info", operation_id="get_parking_info")
async def get_info(
    request: ParkingLotInfoRequest,
    parking_service: ParkingService = Depends(get_parking_service)  # noqa: B008
):
    """获取停车场详情接口"""
    run_id = str(uuid.uuid4())
    print("run_id:", run_id)

    result = parking_service.parking_lot_details(request.parking_lot_id)

    return {
        "status": "success",
        "parking_lot_info": result["data"],
        "message": f"已獲取停車場 {request.parking_lot_id} 的詳細資訊"
    }


# 添加 MCP 服务器
add_mcp_server(
    app,
    mount_path="/mcp",
    name="parking",
    base_url="http://localhost:8002",
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)  # noqa: S104
