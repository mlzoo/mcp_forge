# MCP Server 通用开发框架

## 项目简介

这是一个专为开发企业级 Model Context Protocol (MCP) 工具而设计的通用开发框架，旨在标准化 MCP server 的开发流程，帮助开发者快速构建高质量的 AI 工具。通过集成 FastAPI 和 FastAPI-MCP，本框架实现了从传统 API 到 AI 工具的无缝转换。

### 核心特色

- **MCP工具标准化**：将传统FastAPI接口自动转换为AI模型可调用的MCP工具
- **抽象与实现分离**：支持接口定义与实现分离，方便模拟测试和生产环境切换
- **依赖注入设计**：基于FastAPI依赖注入机制，实现服务组件的灵活组合与解耦
- **完整开发链路**：提供从开发、测试到部署的完整工具链支持
- **示例即文档**：通过实际示例演示最佳实践，加速上手过程

本框架特别适合：
- AI工具开发团队
- 需要将现有API转换为AI工具的开发者
- 希望实施标准化微服务架构的组织

## 架构设计

### 核心架构

```
┌─────────────┐      ┌───────────────┐      ┌─────────────────┐
│  API 路由层  │ ─→   │  服务接口层     │ ─→   │  服务实现层      │
└─────────────┘      └───────────────┘      └─────────────────┘
       ↓                                            
┌─────────────┐                                     
│  MCP 端点    │ ←── FastAPI-MCP 自动转换            
└─────────────┘                                     
```

### 关键组件

- **FastAPI 应用**：提供HTTP API服务的基础框架
- **FastAPI-MCP**：将API端点自动转换为MCP工具
- **服务接口层**：通过抽象基类定义服务契约
- **依赖注入提供者**：管理服务实例的创建与注入
- **实现类**：包括Mock实现和真实实现，支持环境切换

## 技术栈

- **Python 3.10+**：利用最新的语言特性和类型注解
- **FastAPI**：高性能异步Web框架
- **FastAPI-MCP**：自动化暴露FastAPI端点作为MCP tool
- **开发工具链**：包含代码质量检查与测试工具

## 快速开始

### 环境准备

本框架采用`uv`作为包管理工具，提供更快的依赖解析和虚拟环境管理，安装方法可参考[uv官方文档](https://docs.astral.sh/uv/getting-started/installation/)。

```bash
# 安装依赖并设置开发环境
make install
```

### 启动示例服务

```bash
# 启动开发服务器
make dev
```

服务启动后，您可以：
- 访问 `http://localhost:5000/docs` 查看API文档
- 使用MCP客户端(如Cursor、Claude Desktop)连接 `http://localhost:5000/mcp` 端点

## 项目结构

```
.
├── main.py                    # 应用入口和路由定义
├── services/                  # 服务层实现
│   └── parking_service.py     # 示例服务（可替换为自定义服务）
├── pyproject.toml             # 项目配置和依赖定义
└── Makefile                   # 开发和构建任务
```

## MCP 工具开发指南

### 开发流程概览

1. **定义服务接口**：创建抽象基类定义服务契约
2. **实现服务**：根据需求实现Mock或真实服务
3. **创建API端点**：使用FastAPI开发API接口
4. **启用MCP服务**：通过FastAPI-MCP暴露为AI工具

### 服务接口与实现

```python
# 1. 服务接口定义
from abc import ABC, abstractmethod
from typing import Dict, Any

class DataService(ABC):
    @abstractmethod
    def get_data(self, id: str) -> Dict[str, Any]:
        """获取数据接口"""
        pass

# 2A. Mock实现 - 用于开发测试
class DataServiceMockImpl(DataService):
    def get_data(self, id: str) -> Dict[str, Any]:
        return {"id": id, "name": "测试数据", "mock": True}

# 2B. 真实实现 - 用于生产环境
class DataServiceImpl(DataService):
    def __init__(self, database_url: str):
        self.db = Database(database_url)
    
    def get_data(self, id: str) -> Dict[str, Any]:
        return self.db.query("SELECT * FROM data WHERE id = :id", {"id": id})

# 3. 依赖注入配置
def get_data_service() -> DataService:
    # 根据环境选择不同实现
    return DataServiceMockImpl() # 或 return DataServiceImpl(settings.DATABASE_URL)
```

### API与MCP工具定义

```python
from fastapi import FastAPI, Depends
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel, Field

app = FastAPI()

# 请求模型
class ItemRequest(BaseModel):
    query: str = Field(..., description="查询参数")
    limit: int = Field(10, description="返回结果数量限制")

# API端点 - 将自动转换为MCP工具
@app.post("/items/search", operation_id="search_items")
async def search_items(
    request: ItemRequest,
    service: DataService = Depends(get_data_service)
):
    result = service.search_items(request.query, request.limit)
    return {"items": result["items"], "total": len(result["items"])}

# 创建并挂载MCP服务
mcp = FastApiMCP(
    app, 
    name="example-service",
    description="示例MCP服务",
    base_url="http://localhost:5000",
    include_operations=["search_items"]
)

# 挂载MCP服务到指定路径
mcp.mount(mount_path="/mcp")
```

## 依赖注入详解

FastAPI 的依赖注入系统也是本框架考虑的的一部分，它提供了强大且灵活的依赖管理能力。

### 依赖注入基本原理

依赖注入是一种设计模式，它允许将依赖项（如服务、数据库连接等）注入到使用它们的组件中，而不是让组件自己创建和管理依赖项。在FastAPI中，依赖注入通过`Depends`函数实现。

```python
from fastapi import Depends

def get_db():
    """数据库连接提供者"""
    db = connect_to_db()
    try:
        yield db  # 使用 yield 可以实现依赖项的生命周期管理
    finally:
        db.close()

@app.get("/items/")
async def get_items(db = Depends(get_db)):
    return db.query(Item).all()
```

### 依赖类型

FastAPI支持多种类型的依赖注入：

1. **函数依赖**：如上例所示，使用函数作为依赖提供者
2. **类依赖**：使用类作为依赖，支持更复杂的依赖管理

```python
class DatabaseDependency:
    def __init__(self, settings = Depends(get_settings)):
        self.settings = settings
    
    def __call__(self):
        db = connect_to_db(self.settings.db_url)
        try:
            yield db
        finally:
            db.close()

@app.get("/users/")
async def get_users(db = Depends(DatabaseDependency())):
    return db.query(User).all()
```

3. **嵌套依赖**：依赖项可以依赖于其他依赖项，形成依赖树

### 在MCP工具开发中的应用

在本框架中，依赖注入主要用于：

1. **服务实例管理**：将服务实现注入到API端点
2. **环境适配**：根据运行环境选择不同服务实现
3. **资源生命周期**：管理数据库连接等资源的创建和释放

## FastAPI-MCP 功能详解

### MCP工具自动生成

FastAPI-MCP能够自动将FastAPI端点转换为MCP工具：

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()

# 定义普通FastAPI端点
@app.post("/predict", operation_id="predict_sentiment")
async def predict_sentiment(text: str):
    return {"sentiment": "positive", "confidence": 0.92}

# 创建并挂载MCP服务 - 自动转换上述端点为MCP工具
mcp = FastApiMCP(
    app,
    name="sentiment-analysis",
    description="情感分析服务",
    base_url="http://localhost:5000",
    include_operations=["predict_sentiment"]
)

# 挂载MCP服务到指定路径
mcp.mount(mount_path="/mcp")
```

### 工具命名最佳实践

MCP工具名称默认使用API端点的`operation_id`，建议遵循以下命名规则：

- 使用清晰描述性的名称
- 采用动词_名词格式（如`predict_sentiment`、`find_nearby_parking`）
- 显式设置`operation_id`而非依赖自动生成

```python
# 推荐: 显式设置operation_id
@app.post("/parking/nearby", operation_id="find_nearby_parking")
async def find_nearby(request: NearbyRequest):
    # 实现逻辑...
    pass

# 不推荐: 依赖自动生成的operation_id (会生成如"find_nearby_parking_nearby_post")
@app.post("/parking/nearby")
async def find_nearby(request: NearbyRequest):
    # 实现逻辑...
    pass
```

## 测试与质量保证

本框架支持多层次测试策略：

```bash
# 运行代码质量检查
make check

# 运行测试套件
make test
```

### 测试策略

- **单元测试**：使用Mock服务实现测试独立组件
- **集成测试**：测试组件间交互
- **API测试**：验证HTTP接口行为
- **MCP工具测试**：验证AI工具功能

## 性能优化

为确保MCP工具的高性能，建议：

- **异步处理**：利用FastAPI的异步特性处理并发请求
- **缓存策略**：对频繁请求的数据实施缓存
- **批量处理**：设计支持批量操作的API减少调用次数

## 贡献指南

欢迎对本框架进行贡献：

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

[MIT License](LICENSE)

## 参考资料

- [FastAPI](https://fastapi.tiangolo.com/) - 高性能Web框架
- [FastAPI-MCP](https://github.com/tadata-org/fastapi_mcp) - MCP工具自动生成库
