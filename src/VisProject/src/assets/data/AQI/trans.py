import csv
import json
import os
from pathlib import Path

def split_csv_to_city_json(csv_path, output_dir="cities_json"):
    """
    将AQI CSV文件拆分为每个城市单独的JSON文件
    
    参数:
    - csv_path: 输入CSV文件路径
    - output_dir: 输出目录，默认为"cities_json"
    """
    try:
        # 创建输出目录（如果不存在）
        os.makedirs(output_dir, exist_ok=True)
        
        # 读取CSV文件
        with open(csv_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # 获取表头
            
            # 提取城市名称（从第三列开始）
            cities = headers[2:]
            
            # 为每个城市创建一个字典，用于存储其数据
            city_data = {city: [] for city in cities}
            
            # 解析每一行数据
            for row in reader:
                if not row:  # 跳过空行
                    continue
                
                # 提取日期（第一列）
                date = row[0]
                
                # 提取每个城市的AQI值
                for i, city in enumerate(cities):
                    # 城市AQI值在第i+2列（因为索引从0开始，且跳过前两列）
                    aqi_index = i + 2
                    if aqi_index < len(row):
                        aqi_value = row[aqi_index].strip()
                        if aqi_value:  # 确保有值
                            try:
                                aqi = float(aqi_value)
                                city_data[city].append({
                                    'date': date,
                                    'aqi': aqi
                                })
                            except ValueError:
                                print(f"警告: 城市 '{city}' 在日期 '{date}' 的AQI值 '{aqi_value}' 无法转换为数字")
        
        # 为每个城市写入单独的JSON文件
        for city, records in city_data.items():
            if records:  # 只处理有数据的城市
                city_file = os.path.join(output_dir, f"{city}.json")
                with open(city_file, 'w', encoding='utf-8') as jsonfile:
                    json.dump(records, jsonfile, ensure_ascii=False, indent=2)
                print(f"已生成 {city}.json，包含 {len(records)} 条记录")
        
        print(f"\n所有城市数据已拆分并保存到 '{output_dir}' 目录")
            
    except Exception as e:
        print(f"处理失败: {str(e)}")
        return None

if __name__ == "__main__":
    # 示例用法
    csv_file = "AQI.csv"  # 替换为你的CSV文件路径
    output_directory = "cities_json"  # 替换为你想要的输出目录
    
    split_csv_to_city_json(csv_file, output_directory)