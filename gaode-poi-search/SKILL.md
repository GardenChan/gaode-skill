---
name: gaode-poi-search
description: "This skill should be used when the user wants to search for places, locations, points of interest (POI), shops, restaurants, hotels, attractions, or any geographic entities using Gaode (AMap) Maps. Trigger phrases include: '搜索地点', '查找位置', '附近的', '找一下', 'POI搜索', '高德搜索', '地图搜索', 'search place', 'find location', 'nearby', 'POI search', or any request involving searching for specific places, addresses, or businesses in China."
---

# 高德地图关键字搜索 POI

## 概述

此 Skill 提供高德地图关键字搜索 POI（兴趣点）的能力，通过调用高德地图 Web 服务 API 的 `/v3/place/text` 接口，根据关键词搜索全国或指定城市的地点信息，包括地址、坐标、电话、商圈等详细信息。

## 前提条件

使用此 Skill 需要高德地图 Web 服务 API Key：

1. 访问 [高德开放平台控制台](https://console.amap.com/)
2. 注册/登录高德开发者账号
3. 进入「应用管理」→ 创建新应用
4. 为应用添加 Key，服务平台选择 **Web服务**
5. 获得 API Key

API Key 可以通过以下方式提供：
- 命令行参数 `--key YOUR_KEY`
- 环境变量 `AMAP_KEY`

如果用户未提供 Key，提示用户按照以上步骤获取。

## 工作流程

### 1. 确认搜索参数

从用户请求中提取以下信息：

| 参数 | 必填 | 说明 |
|------|------|------|
| keywords | ✅ | 搜索关键词（如"火锅"、"北京大学"） |
| city | 可选 | 限定城市范围（如"北京"、"上海"） |
| types | 可选 | POI 类型编码过滤 |
| page | 可选 | 页码（默认1） |
| offset | 可选 | 每页数量（默认20，最大25） |

如果用户没有明确指定城市，默认搜索全国。

### 2. 执行搜索

使用 `scripts/search.py` 脚本执行搜索：

```bash
# 基本搜索
python scripts/search.py --key <AMAP_KEY> --keywords "关键词"

# 指定城市搜索
python scripts/search.py --key <AMAP_KEY> --keywords "关键词" --city "城市名"

# 获取子POI信息（如停车场等附属设施）
python scripts/search.py --key <AMAP_KEY> --keywords "关键词" --city "城市" --children 1

# 限定城市范围（不扩展到其他城市）
python scripts/search.py --key <AMAP_KEY> --keywords "关键词" --city "城市" --citylimit

# 获取原始 JSON 数据
python scripts/search.py --key <AMAP_KEY> --keywords "关键词" --raw
```

脚本将自动格式化输出为 Markdown，直接展示给用户即可。

### 3. 结果展示格式

搜索结果按照以下 Markdown 格式展示：

```markdown
🔍 共找到 **N** 条结果，当前展示 M 条：

### 1. 地点名称

| 属性 | 信息 |
|------|------|
| 📍 地址 | 具体地址 |
| 🏙️ 区域 | 省份/城市/区县 |
| 📂 类型 | POI 类型 |
| 📞 电话 | 联系电话 |
| 🏪 商圈 | 所属商圈 |
| 🗺️ 坐标 | 经度 xxx, 纬度 xxx |
| 🆔 POI ID | B000XXXXXX |
```

### 4. 错误处理

- **Key 缺失**: 提示用户前往 https://console.amap.com/ 获取
- **Key 无效 (10001)**: 提示用户检查 Key 是否正确或已过期
- **超出配额 (10003)**: 提示用户日访问量已达上限
- **频率限制 (10004)**: 提示用户稍后重试
- **无结果**: 建议用户调整关键词或扩大城市范围

## 常用搜索示例

| 用户请求 | 转换为命令 |
|----------|-----------|
| "帮我搜一下北京的火锅店" | `--keywords "火锅" --city "北京"` |
| "上海附近有什么医院" | `--keywords "医院" --city "上海"` |
| "找一下成都的咖啡馆" | `--keywords "咖啡馆" --city "成都"` |
| "搜索北京大学" | `--keywords "北京大学"` |
| "深圳有哪些停车场" | `--keywords "停车场" --city "深圳" --children 1` |

## 资源

### scripts/search.py

核心搜索脚本。调用高德地图 `/v3/place/text` 接口进行关键字搜索，支持格式化 Markdown 输出和原始 JSON 输出。无需额外依赖，仅使用 Python 标准库。

执行方式：直接运行脚本，参数通过命令行传入。

### references/api_reference.md

高德地图关键字搜索 API 的完整参考文档，包含请求参数、返回字段、错误码、常用 POI 类型编码等详细信息。在需要查阅特定字段含义或类型编码时读取此文件。
