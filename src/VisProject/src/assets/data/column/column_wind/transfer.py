import csv
import json
import os

def format_date(date_str):
    """将8位数字日期转换为YYYY/M/D格式"""
    try:
        if len(date_str) != 8 or not date_str.isdigit():
            return None
        year = date_str[:4]
        month = str(int(date_str[4:6]))  # 去掉前导零
        day = str(int(date_str[6:8]))    # 去掉前导零
        return f"{year}/{month}/{day}"
    except:
        return None

def process_csv_files(input_files, output_dir):
    city_data = {}  # 键为city_code，值为城市数据和风速记录

    for file_path in input_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            dates = headers[6:]  # 日期列从第7个开始

            for row in reader:
                if len(row) < 6:  # 跳过不完整行
                    continue

                city_code = row[4]
                city_name = row[3]
                wind_speed_values = row[6:6+len(dates)]  # 风速数据列

                if city_code not in city_data:
                    city_data[city_code] = {
                        'city_name': city_name,
                        'data': []
                    }

                # 处理每个风速值
                for date_str, wind_speed in zip(dates, wind_speed_values):
                    formatted_date = format_date(date_str)
                    if not formatted_date:
                        continue

                    wind_speed = wind_speed.strip()
                    try:
                        speed_val = float(wind_speed) if wind_speed else None
                    except ValueError:
                        speed_val = None

                    city_data[city_code]['data'].append({
                        "date": formatted_date,
                        "wind_speed": speed_val  # 修改键名
                    })

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 写入JSON文件
    for city_code, info in city_data.items():
        safe_city_name = info['city_name'].replace('/', '_').replace(' ', '_')
        filename = f"{safe_city_name}.json"
        file_path = os.path.join(output_dir, filename)
        
        # 按日期排序（可选）
        sorted_data = sorted(info['data'], key=lambda x: x['date'])
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    input_files = [f'{year}.csv' for year in range(2015, 2022)]
    output_dir = 'wind_speed_data'  # 修改输出目录名
    process_csv_files(input_files, output_dir)