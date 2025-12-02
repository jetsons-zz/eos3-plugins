"""
AQI Client - 空气质量数据客户端
使用 AQICN API 获取全球空气质量数据
需要免费 Token（demo token 仅支持上海）
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote


# AQICN API 配置
API_BASE = "https://api.waqi.info"

# 默认使用 demo token（仅支持上海测试）
# 生产环境请在 https://aqicn.org/data-platform/token/ 注册获取
DEFAULT_TOKEN = "demo"

# AQI 等级定义
AQI_LEVELS = {
    (0, 50): {
        "level": "优",
        "level_en": "Good",
        "color": "green",
        "emoji": "🟢",
        "health_implications": "空气质量令人满意，基本无空气污染",
        "cautionary_statement": "无需采取任何预防措施"
    },
    (51, 100): {
        "level": "良",
        "level_en": "Moderate",
        "color": "yellow",
        "emoji": "🟡",
        "health_implications": "空气质量可接受，某些污染物可能对极少数敏感人群有轻微影响",
        "cautionary_statement": "极少数敏感人群应减少户外活动"
    },
    (101, 150): {
        "level": "轻度污染",
        "level_en": "Unhealthy for Sensitive Groups",
        "color": "orange",
        "emoji": "🟠",
        "health_implications": "敏感人群可能出现健康影响，一般人群影响不大",
        "cautionary_statement": "儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间户外活动"
    },
    (151, 200): {
        "level": "中度污染",
        "level_en": "Unhealthy",
        "color": "red",
        "emoji": "🔴",
        "health_implications": "所有人群可能开始出现健康影响，敏感人群健康影响更为严重",
        "cautionary_statement": "儿童、老年人及心脏病、呼吸系统疾病患者应避免长时间户外活动，一般人群减少户外活动"
    },
    (201, 300): {
        "level": "重度污染",
        "level_en": "Very Unhealthy",
        "color": "purple",
        "emoji": "🟣",
        "health_implications": "健康警报：所有人群可能出现更严重的健康影响",
        "cautionary_statement": "儿童、老年人及心脏病、呼吸系统疾病患者应停止户外活动，一般人群避免户外活动"
    },
    (301, 500): {
        "level": "严重污染",
        "level_en": "Hazardous",
        "color": "maroon",
        "emoji": "🟤",
        "health_implications": "健康警报：所有人群都可能受到严重健康影响",
        "cautionary_statement": "所有人群应避免一切户外活动"
    }
}

# 主要污染物信息
POLLUTANT_INFO = {
    "pm25": {"name": "PM2.5", "unit": "μg/m³", "description": "细颗粒物，可深入肺部"},
    "pm10": {"name": "PM10", "unit": "μg/m³", "description": "可吸入颗粒物"},
    "o3": {"name": "臭氧", "unit": "μg/m³", "description": "地面臭氧，影响呼吸系统"},
    "no2": {"name": "二氧化氮", "unit": "μg/m³", "description": "来自机动车和工业排放"},
    "so2": {"name": "二氧化硫", "unit": "μg/m³", "description": "来自燃煤和工业排放"},
    "co": {"name": "一氧化碳", "unit": "mg/m³", "description": "来自不完全燃烧"}
}

# 热门城市映射
POPULAR_CITIES = {
    # 中国
    "北京": "beijing",
    "上海": "shanghai",
    "广州": "guangzhou",
    "深圳": "shenzhen",
    "杭州": "hangzhou",
    "成都": "chengdu",
    "重庆": "chongqing",
    "南京": "nanjing",
    "武汉": "wuhan",
    "西安": "xian",
    "天津": "tianjin",
    "苏州": "suzhou",
    # 国际城市
    "东京": "tokyo",
    "首尔": "seoul",
    "新加坡": "singapore",
    "香港": "hongkong",
    "台北": "taipei",
    "曼谷": "bangkok",
    "纽约": "new-york",
    "洛杉矶": "los-angeles",
    "伦敦": "london",
    "巴黎": "paris",
    "悉尼": "sydney",
    "迪拜": "dubai"
}


class AQIClient:
    """空气质量数据客户端"""

    def __init__(self, token: str = None):
        """
        初始化客户端

        Args:
            token: AQICN API token，如果不提供则使用 demo token
        """
        self.token = token or DEFAULT_TOKEN
        self._cache = {}
        self._cache_ttl = 300  # 缓存5分钟

    def _is_cache_valid(self, key: str) -> bool:
        """检查缓存是否有效"""
        if key not in self._cache:
            return False
        cached_time = self._cache[key].get('_cached_at', 0)
        return (datetime.now().timestamp() - cached_time) < self._cache_ttl

    def _get_aqi_level(self, aqi: int) -> Dict:
        """获取 AQI 等级信息"""
        for (low, high), info in AQI_LEVELS.items():
            if low <= aqi <= high:
                return info
        # 超出范围
        return AQI_LEVELS[(301, 500)]

    def get_city_aqi(self, city: str) -> Optional[Dict]:
        """
        获取城市空气质量

        Args:
            city: 城市名称（中文或英文）

        Returns:
            空气质量数据
        """
        # 中文城市转换
        city_query = POPULAR_CITIES.get(city, city)

        cache_key = f"city_{city_query}"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            url = f"{API_BASE}/feed/{quote(city_query)}/?token={self.token}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get('status') != 'ok':
                return {"error": data.get('data', 'Unknown error'), "city": city}

            aqi_data = data.get('data', {})
            aqi_value = aqi_data.get('aqi', 0)

            # 如果 AQI 是字符串 "-"，表示没有数据
            if isinstance(aqi_value, str):
                aqi_value = 0

            level_info = self._get_aqi_level(aqi_value)

            # 解析污染物数据
            iaqi = aqi_data.get('iaqi', {})
            pollutants = {}
            for key, info in POLLUTANT_INFO.items():
                if key in iaqi:
                    pollutants[key] = {
                        "value": iaqi[key].get('v', 0),
                        "name": info['name'],
                        "unit": info['unit']
                    }

            # 找出主要污染物
            dominant_pollutant = aqi_data.get('dominentpol', None)

            # 天气数据
            weather = {}
            if 't' in iaqi:
                weather['temperature'] = iaqi['t'].get('v')
            if 'h' in iaqi:
                weather['humidity'] = iaqi['h'].get('v')
            if 'p' in iaqi:
                weather['pressure'] = iaqi['p'].get('v')
            if 'w' in iaqi:
                weather['wind'] = iaqi['w'].get('v')

            # 预报数据
            forecast = aqi_data.get('forecast', {}).get('daily', {})

            result = {
                "city": aqi_data.get('city', {}).get('name', city),
                "aqi": aqi_value,
                "level": level_info['level'],
                "level_en": level_info['level_en'],
                "emoji": level_info['emoji'],
                "color": level_info['color'],
                "health_implications": level_info['health_implications'],
                "cautionary_statement": level_info['cautionary_statement'],
                "dominant_pollutant": dominant_pollutant,
                "pollutants": pollutants,
                "weather": weather,
                "forecast": forecast,
                "location": {
                    "lat": aqi_data.get('city', {}).get('geo', [None, None])[0],
                    "lon": aqi_data.get('city', {}).get('geo', [None, None])[1]
                },
                "updated_at": aqi_data.get('time', {}).get('s', ''),
                "_cached_at": datetime.now().timestamp()
            }

            self._cache[cache_key] = result
            return result

        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}", "city": city}
        except Exception as e:
            return {"error": str(e), "city": city}

    def get_aqi_by_location(self, lat: float, lon: float) -> Optional[Dict]:
        """
        根据坐标获取空气质量

        Args:
            lat: 纬度
            lon: 经度

        Returns:
            空气质量数据
        """
        cache_key = f"geo_{lat}_{lon}"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            url = f"{API_BASE}/feed/geo:{lat};{lon}/?token={self.token}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get('status') != 'ok':
                return {"error": data.get('data', 'Unknown error'), "lat": lat, "lon": lon}

            aqi_data = data.get('data', {})
            aqi_value = aqi_data.get('aqi', 0)

            if isinstance(aqi_value, str):
                aqi_value = 0

            level_info = self._get_aqi_level(aqi_value)

            result = {
                "city": aqi_data.get('city', {}).get('name', f"{lat}, {lon}"),
                "aqi": aqi_value,
                "level": level_info['level'],
                "level_en": level_info['level_en'],
                "emoji": level_info['emoji'],
                "health_implications": level_info['health_implications'],
                "location": {"lat": lat, "lon": lon},
                "updated_at": aqi_data.get('time', {}).get('s', ''),
                "_cached_at": datetime.now().timestamp()
            }

            self._cache[cache_key] = result
            return result

        except Exception as e:
            return {"error": str(e), "lat": lat, "lon": lon}

    def search_stations(self, keyword: str) -> List[Dict]:
        """
        搜索监测站

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的监测站列表
        """
        try:
            url = f"{API_BASE}/search/?keyword={quote(keyword)}&token={self.token}"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get('status') != 'ok':
                return []

            stations = []
            for item in data.get('data', []):
                stations.append({
                    "name": item.get('station', {}).get('name', ''),
                    "aqi": item.get('aqi', '-'),
                    "uid": item.get('uid'),
                    "time": item.get('time', {}).get('stime', '')
                })

            return stations

        except Exception as e:
            return []

    def get_multiple_cities(self, cities: List[str]) -> List[Dict]:
        """
        获取多个城市的空气质量

        Args:
            cities: 城市名称列表

        Returns:
            各城市空气质量数据
        """
        results = []
        for city in cities:
            data = self.get_city_aqi(city)
            if data and 'error' not in data:
                results.append(data)
        return results


def get_city_aqi(city: str, token: str = None) -> Optional[Dict]:
    """
    便捷函数：获取城市空气质量

    Args:
        city: 城市名称
        token: API token（可选）

    Returns:
        空气质量数据
    """
    client = AQIClient(token)
    return client.get_city_aqi(city)


def get_aqi_by_location(lat: float, lon: float, token: str = None) -> Optional[Dict]:
    """
    便捷函数：根据坐标获取空气质量

    Args:
        lat: 纬度
        lon: 经度
        token: API token（可选）

    Returns:
        空气质量数据
    """
    client = AQIClient(token)
    return client.get_aqi_by_location(lat, lon)


def get_popular_cities() -> List[str]:
    """获取支持的热门城市列表"""
    return list(POPULAR_CITIES.keys())
