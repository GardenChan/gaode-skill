# 🗺️ 高德地图关键字搜索 POI Skill

一个用于 [CodeBuddy](https://www.codebuddy.ai/) 的 Skill 插件，通过高德地图 Web 服务 API 实现关键字搜索 POI（兴趣点）功能。

> 💬 对 CodeBuddy 说「帮我搜一下北京的火锅店」即可触发搜索。

## ✨ 功能特性

- 🔍 **关键字搜索** — 按关键词搜索全国或指定城市的兴趣点
- 🏙️ **城市过滤** — 限定搜索范围到指定城市
- 📂 **类型过滤** — 按 POI 类型编码精确筛选（餐饮、医疗、景点等）
- 📄 **分页支持** — 支持翻页查看更多结果
- 🏗️ **子 POI** — 查看附属设施（如停车场、出入口等）
- 📊 **格式化输出** — 搜索结果自动以 Markdown 表格展示

## 📁 项目结构

```
gaode-poi-search/
├── SKILL.md                        # Skill 定义文件（触发条件、工作流程、输出格式）
├── scripts/
│   └── search.py                   # 核心搜索脚本（纯 Python 标准库，零依赖）
└── references/
    └── api_reference.md            # 高德 API 参考文档（参数、字段、错误码）
```

## 🔑 前提条件：获取高德 API Key

使用前需要获取一个**高德地图 Web 服务 API Key**：

1. 访问 [高德开放平台控制台](https://console.amap.com/)
2. 注册 / 登录高德开发者账号
3. 进入「应用管理」→ 点击「创建新应用」
4. 为应用「添加 Key」，服务平台选择 **Web服务**
5. 复制生成的 API Key

## 🚀 安装 Skill

### 方式一：zip 安装

1. 下载 [Releases](https://github.com/GardenChan/gaode-skill/releases) 中的 `gaode-poi-search.zip`
2. 在 CodeBuddy 中导入 Skill zip 包即可

### 方式二：手动安装

将 `gaode-poi-search/` 目录复制到 CodeBuddy 的 Skills 目录下：

```bash
cp -r gaode-poi-search/ ~/.codebuddy/skills/gaode-poi-search
```

## 💬 使用方式

在 CodeBuddy 对话中直接用自然语言描述你想搜索的地点：

| 你说的话 | Skill 会做什么 |
|---------|--------------|
| 帮我搜一下北京的火锅店 | 搜索关键词「火锅」，城市限定「北京」 |
| 上海附近有什么医院 | 搜索关键词「医院」，城市限定「上海」 |
| 找一下成都的咖啡馆 | 搜索关键词「咖啡馆」，城市限定「成都」 |
| 搜索北京大学 | 搜索关键词「北京大学」，全国范围 |
| 深圳有哪些停车场 | 搜索关键词「停车场」，城市限定「深圳」，包含子 POI |

## 📋 输出示例

```
🔍 共找到 899 条结果，当前展示 20 条：

### 1. 北京大学

| 属性 | 信息 |
|------|------|
| 📍 地址 | 颐和园路5号 |
| 🏙️ 区域 | 北京市海淀区 |
| 📂 类型 | 科教文化服务;学校;高等院校 |
| 🏪 商圈 | 西苑 |
| 🗺️ 坐标 | 经度 116.310905, 纬度 39.992806 |
| 🆔 POI ID | B000A816R6 |
```

## ⚙️ 脚本独立使用

`search.py` 也可以作为独立命令行工具使用，无需任何第三方依赖：

```bash
# 基本搜索
python gaode-poi-search/scripts/search.py --key YOUR_KEY --keywords "北京大学"

# 指定城市
python gaode-poi-search/scripts/search.py --key YOUR_KEY --keywords "火锅" --city "成都"

# 使用环境变量提供 Key
export AMAP_KEY="your_api_key_here"
python gaode-poi-search/scripts/search.py --keywords "咖啡" --city "上海"

# 限定城市范围（不扩展搜索）
python gaode-poi-search/scripts/search.py --key YOUR_KEY --keywords "酒店" --city "杭州" --citylimit

# 获取子 POI（附属设施）
python gaode-poi-search/scripts/search.py --key YOUR_KEY --keywords "停车场" --city "深圳" --children 1

# 输出原始 JSON
python gaode-poi-search/scripts/search.py --key YOUR_KEY --keywords "北京大学" --raw
```

### 完整参数列表

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--key` | 是* | `$AMAP_KEY` | 高德 API Key（可用环境变量代替） |
| `--keywords` | 是 | — | 搜索关键词 |
| `--city` | 否 | 全国 | 查询城市 |
| `--types` | 否 | — | POI 类型编码 |
| `--citylimit` | 否 | `false` | 仅在指定城市搜索 |
| `--children` | 否 | `0` | 是否返回子 POI（0/1） |
| `--offset` | 否 | `20` | 每页数量（1-25） |
| `--page` | 否 | `1` | 页码 |
| `--extensions` | 否 | `all` | 返回信息详细程度（base/all） |
| `--raw` | 否 | — | 输出原始 JSON |

## 📚 参考

- [高德地图关键字搜索 API 文档](https://amap.apifox.cn/api-14633570)
- [高德开放平台控制台](https://console.amap.com/)
- [CodeBuddy 官方文档](https://www.codebuddy.ai/)

## 📄 License

MIT
