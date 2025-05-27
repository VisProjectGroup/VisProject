import csv
import json
import os

def process_consumption(input_file, output_dir):
    city_data = {}  # 数据结构：{城市名: {年份: 能耗值}}

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过首行标题

        for row in reader:
            if len(row) < 9:  # 确保数据完整性
                continue

            city = row[0].strip()
            year = row[1].strip()
            consumption = row[8].strip()  # 第9列数据（索引8）

            # 跳过无效城市名
            if not city:
                continue

            # 转换年份
            try:
                year_int = int(year)
                if not (2006 <= year_int <= 2021):  # 验证年份范围
                    continue
            except ValueError:
                continue

            # 转换能耗值
            try:
                # 处理可能存在的千分位逗号（如"1,234.56"）
                consumption_clean = consumption.replace(',', '')
                consumption_val = float(consumption_clean)
            except (ValueError, AttributeError):
                consumption_val = None

            # 组织数据结构
            if city not in city_data:
                city_data[city] = {}
            
            # 保留最新数据（如果同一年份有多个记录）
            city_data[city][year_int] = consumption_val

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 生成JSON文件
    for city, year_dict in city_data.items():
        # 转换为排序后的列表
        sorted_data = sorted(
            [{"year": year, "consumption": val} for year, val in year_dict.items()],
            key=lambda x: x["year"]
        )
        
        # 生成安全文件名
        safe_city = city.replace('/', '_').replace('\\', '_')
        filename = f"{safe_city}.json"
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    process_consumption(
        input_file='consumption.csv',
        output_dir='energy_consumption'
    )