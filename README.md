# 🚀 Ollama Web Summary AI 

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/1803053530/OllamaWebSummaryAI/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Open Issues](https://img.shields.io/github/issues/1803053530/OllamaWebSummaryAI)](https://github.com/1803053530/OllamaWebSummaryAI/issues)

✨ 基于Ollama的智能网页摘要系统，集成多线程进度监控

## 📌 功能特性
- 🚀 异步网页内容处理架构
- 📈 实时可视化进度条展示
- 🤖 灵活对接Ollama API服务
- 🛡️ 完善的错误重试机制
- ⚡ 支持批量URL自动处理

![处理流程演示](demo.gif) *（实际运行效果演示）*

## 🚦 快速入门
### 环境要求
- Python 3.8+
- 可访问的Ollama API服务

### 三步部署
```bash
# 1. 克隆仓库
git clone https://github.com/1803053530/OllamaWebSummaryAI.git

# 2. 安装依赖
pip install -r requirements.txt
```

```bash
# 3. 配置环境变量
#Linux:
export OLLAMA_API="您的API端点"

#Windows(Powershell):
$env:OLLAMA_API="您的API端点"
```


## 🛠️ 使用方法
### 基础配置
1. 编辑 `main.py` 添加目标URL：
```python
urls_to_process = [
    "https://news.example.com/article1",
    "https://blog.example.com/post2"
]
```

2. 启动处理流程：
```bash
python main.py
```

### 高级配置
| 功能 | 配置文件 | 说明 |
|------|----------|------|
| 模型选择 | `OllamaApiRequest.py` | 修改models字典适配您的Ollama模型 |
| 进度样式 | `ProcessingLine.py` | 调整update()参数定制进度动画 |
| 超时策略 | `OllamaApiRequest.py` | 设置timeout控制请求时限 |

## ⚠️ 注意事项
1. **API配置**：必须正确设置OLLAMA_API环境变量
2. **URL验证**：确保输入有效的http/https地址
3. **网络稳定**：需要保持API服务的稳定连接（*本地部署除外*）
4. **结果缓存**：建议自行实现结果存储逻辑

## ❓ 常见问题
### Q1: 进度条卡住不动？
> 检查网络连接并确认API服务可用，尝试：
> ```bash
> export OLLAMA_API_DEBUG=1 && python main.py
> ```

### Q2: 如何处理大量URL？
```python
# 使用文件导入模式
with open("urls.txt") as f:
    urls_to_process = [line.strip() for line in f]
```

### Q3: 如何切换模型？
```python
# 在OllamaApiRequest.py中修改模型标识符
models = {
    "MyModel": "your_model_name"  # 根据您需要使用的模型进行修改
}

try:
    url = os.environ.get("OLLAMA_API")
    payload = {
        "model": models["DeepseekR1"],  # 本次请求调用的模型
        "prompt": prompt,
        "stream": False
    }
```

## 👥 关于我们
### 核心组件
| 模块 | 说明 | 负责人 |
|------|------|------|
| 流程控制 | 主线程调度与任务分发 | @Takanashi|
| API集成 | Ollama接口封装与异常处理 | @Takanashi|
| 进度显示 | 多线程动画渲染引擎 | @Takanashi|

### 贡献指南
欢迎通过以下方式参与改进：
1. 提交Issue报告问题
2. 发起Pull Request贡献代码
3. 完善项目文档

## 📜 许可证
本项目采用 [MIT License](LICENSE)
 
项目完全开源，切勿用于违法用途，欢迎大家使用并提出反馈