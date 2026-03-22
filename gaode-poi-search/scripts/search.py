#!/usr/bin/env python3
"""
高德地图关键字搜索 POI 脚本

使用高德地图 Web 服务 API 的关键字搜索接口（/v3/place/text），
根据关键词查询特定城市或全国范围内的兴趣点（POI）。

使用方法:
    python search.py --key <AMAP_KEY> --keywords "北京大学" [--city "北京"] [--page 1] [--offset 20] [--extensions all]

环境变量:
    AMAP_KEY: 高德地图 Web 服务 API Key（也可通过 --key 参数传入）
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


AMAP_API_BASE = "https://restapi.amap.com/v3/place/text"


def search_poi(
    key: str,
    keywords: str,
    city: str = "",
    types: str = "",
    citylimit: bool = False,
    children: int = 0,
    offset: int = 20,
    page: int = 1,
    extensions: str = "all",
) -> dict:
    """
    调用高德地图关键字搜索 POI 接口。

    Args:
        key: 高德地图 API Key
        keywords: 搜索关键词
        city: 查询城市（可选，默认全国）
        types: POI 类型编码（可选）
        citylimit: 是否限制在指定城市搜索（默认 False）
        children: 是否返回子 POI 数据（1=返回，0=不返回）
        offset: 每页返回数量（1-25，默认 20）
        page: 当前页码（默认 1）
        extensions: 返回信息控制（base=基础信息，all=详细信息）

    Returns:
        dict: API 返回的 JSON 数据
    """
    params = {
        "key": key,
        "keywords": keywords,
        "city": city,
        "types": types,
        "citylimit": "true" if citylimit else "false",
        "children": str(children),
        "offset": str(min(max(offset, 1), 25)),
        "page": str(max(page, 1)),
        "extensions": extensions,
        "output": "JSON",
    }

    url = f"{AMAP_API_BASE}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GaodePOISearch/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        return {"status": "0", "info": f"HTTP Error: {e.code}", "pois": []}
    except urllib.error.URLError as e:
        return {"status": "0", "info": f"URL Error: {e.reason}", "pois": []}
    except Exception as e:
        return {"status": "0", "info": f"Error: {str(e)}", "pois": []}


def format_results(data: dict) -> str:
    """
    格式化搜索结果为可读的 Markdown 格式。

    Args:
        data: API 返回的 JSON 数据

    Returns:
        str: Markdown 格式的搜索结果
    """
    if data.get("status") != "1":
        return f"❌ 搜索失败: {data.get('info', '未知错误')}"

    pois = data.get("pois", [])
    count = data.get("count", "0")

    if not pois:
        return "🔍 未找到相关结果。"

    lines = []
    lines.append(f"🔍 共找到 **{count}** 条结果，当前展示 {len(pois)} 条：\n")

    for i, poi in enumerate(pois, 1):
        name = poi.get("name", "未知")
        address = poi.get("address", "暂无地址")
        if isinstance(address, list):
            address = "、".join(address) if address else "暂无地址"

        poi_type = poi.get("type", "未知类型")
        location = poi.get("location", "")
        tel = poi.get("tel", "")
        if isinstance(tel, list):
            tel = "、".join(tel) if tel else ""

        pname = poi.get("pname", "")
        cityname = poi.get("cityname", "")
        adname = poi.get("adname", "")
        region = f"{pname}{cityname}{adname}".strip()

        business_area = poi.get("business_area", "")
        if isinstance(business_area, list):
            business_area = "、".join(business_area) if business_area else ""

        poi_id = poi.get("id", "")

        lines.append(f"### {i}. {name}")
        lines.append("")

        lines.append(f"| 属性 | 信息 |")
        lines.append(f"|------|------|")
        lines.append(f"| 📍 地址 | {address} |")
        if region:
            lines.append(f"| 🏙️ 区域 | {region} |")
        lines.append(f"| 📂 类型 | {poi_type} |")
        if tel:
            lines.append(f"| 📞 电话 | {tel} |")
        if business_area:
            lines.append(f"| 🏪 商圈 | {business_area} |")
        if location:
            lng, lat = location.split(",") if "," in location else (location, "")
            lines.append(f"| 🗺️ 坐标 | 经度 {lng}, 纬度 {lat} |")
        if poi_id:
            lines.append(f"| 🆔 POI ID | {poi_id} |")

        # 子 POI 信息
        children_pois = poi.get("children", [])
        if children_pois and isinstance(children_pois, list):
            lines.append("")
            lines.append(f"<details><summary>📎 附属设施 ({len(children_pois)} 个)</summary>\n")
            for child in children_pois:
                child_name = child.get("name", "").strip()
                child_addr = child.get("address", "").strip()
                child_type = child.get("subtype", "")
                if child_name:
                    lines.append(f"- **{child_name}**")
                    if child_type:
                        lines.append(f"  - 类型: {child_type}")
                    if child_addr:
                        lines.append(f"  - 地址: {child_addr}")
            lines.append("\n</details>")

        lines.append("")

    # 建议信息
    suggestion = data.get("suggestion", {})
    sug_cities = suggestion.get("cities", [])
    if sug_cities and isinstance(sug_cities, list):
        city_names = []
        for c in sug_cities:
            if isinstance(c, dict):
                city_names.append(c.get("name", ""))
            elif isinstance(c, str):
                city_names.append(c)
        city_names = [c for c in city_names if c]
        if city_names:
            lines.append(f"💡 **其他城市建议**: {', '.join(city_names)}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="高德地图关键字搜索 POI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python search.py --key YOUR_KEY --keywords "北京大学"
  python search.py --key YOUR_KEY --keywords "火锅" --city "成都"
  python search.py --key YOUR_KEY --keywords "咖啡" --city "上海" --offset 10 --page 1
  python search.py --key YOUR_KEY --keywords "医院" --city "广州" --types "090100"
  python search.py --key YOUR_KEY --keywords "停车场" --city "深圳" --children 1
        """,
    )

    parser.add_argument(
        "--key",
        type=str,
        default=os.environ.get("AMAP_KEY", ""),
        help="高德地图 API Key（也可通过 AMAP_KEY 环境变量设置）",
    )
    parser.add_argument("--keywords", type=str, required=True, help="搜索关键词")
    parser.add_argument("--city", type=str, default="", help="查询城市（可选，默认全国）")
    parser.add_argument("--types", type=str, default="", help="POI 类型编码（可选）")
    parser.add_argument(
        "--citylimit", action="store_true", help="是否仅在指定城市搜索"
    )
    parser.add_argument(
        "--children", type=int, default=0, choices=[0, 1], help="是否返回子POI（0/1）"
    )
    parser.add_argument(
        "--offset", type=int, default=20, help="每页返回数量（1-25，默认 20）"
    )
    parser.add_argument("--page", type=int, default=1, help="当前页码（默认 1）")
    parser.add_argument(
        "--extensions",
        type=str,
        default="all",
        choices=["base", "all"],
        help="返回信息控制（base/all，默认 all）",
    )
    parser.add_argument(
        "--raw", action="store_true", help="输出原始 JSON 数据"
    )

    args = parser.parse_args()

    if not args.key:
        print("❌ 错误: 缺少高德地图 API Key。")
        print("   请通过 --key 参数传入，或设置 AMAP_KEY 环境变量。")
        print("   获取方式: https://console.amap.com/")
        sys.exit(1)

    data = search_poi(
        key=args.key,
        keywords=args.keywords,
        city=args.city,
        types=args.types,
        citylimit=args.citylimit,
        children=args.children,
        offset=args.offset,
        page=args.page,
        extensions=args.extensions,
    )

    if args.raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_results(data))


if __name__ == "__main__":
    main()
