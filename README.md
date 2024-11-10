# FastAPI 项目模板

## 项目简介

这是一个基于 FastAPI 框架的项目模板，提供了基础的项目结构和配置。

## 项目结构

my_fastapi_app/
├── app/
│   ├── __init__.py
│   ├── main.py # 主程序入口
│   ├── api/ # API路由模块
│   ├── core/ # 核心配置
│   ├── db/ # 数据库相关
│   └── models/ # 数据模型
├── requirements.txt # 项目依赖
└── README.md # 项目文档

## 安装步骤

1. 克隆项目：
   ```bash
   git clone <项目地址>
   cd my_fastapi_app
   ```

2. 创建虚拟环境：
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 启动应用：
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --reload
   ```
5. API文档访问
启动项目后，可以通过以下地址访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API根路径: http://localhost:8000/

现在 README.md 文件已经包含了完整的文档内容，包括：
- 清晰的项目结构说明
- 详细的安装步骤
- 配置说明
- 开发指南
- 常见问题解答等


