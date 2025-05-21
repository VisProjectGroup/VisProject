# import csv
# import json
# import random
# from pathlib import Path

# def read_csv_to_mappings(csv_file_path):
#     """读取 CSV 文件并创建市到省的映射和省列表"""
#     city_to_province = {}
#     provinces = set()
    
#     with open(csv_file_path, 'r', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if len(row) >= 2:
#                 province, city = row[0].strip(), row[1].strip()
#                 city_to_province[city] = province
#                 provinces.add(province)
    
#     return city_to_province, sorted(provinces)

# def generate_color_map(provinces):
#     """为每个省份生成一个唯一的颜色"""
#     # 生成随机颜色，确保有足够的对比度
#     def random_color():
#         return f"#{random.randint(50, 200):02x}{random.randint(50, 200):02x}{random.randint(50, 200):02x}"
    
#     return {province: random_color() for province in provinces}

# def write_to_json(data, output_file_path):
#     """将数据写入 JSON 文件"""
#     with open(output_file_path, 'w', encoding='utf-8') as file:
#         json.dump(data, file, ensure_ascii=False, indent=2)

# def main():
#     # 设置文件路径
#     csv_file = Path('city.csv')  # 替换为你的 CSV 文件路径
#     city_to_province_file = Path('city_to_province.json')
#     province_to_color_file = Path('province_to_color.json')
    
#     try:
#         # 读取 CSV 文件并创建映射
#         city_to_province, provinces = read_csv_to_mappings(csv_file)
        
#         # 生成省到颜色的映射
#         province_to_color = generate_color_map(provinces)
        
#         # 写入 JSON 文件
#         write_to_json(city_to_province, city_to_province_file)
#         write_to_json(province_to_color, province_to_color_file)
        
#         print(f"成功生成 {city_to_province_file} 和 {province_to_color_file}")
        
#     except FileNotFoundError:
#         print(f"错误：找不到 CSV 文件 '{csv_file}'")
#     except Exception as e:
#         print(f"发生错误：{e}")

# if __name__ == "__main__":
#     main()   



import csv
import json
import sys
from pathlib import Path

def build_city_to_province_mapping(csv_file_path):
    """
    从 CSV 文件构建市到省的映射关系
    
    参数:
    csv_file_path (str): CSV 文件路径
    
    返回:
    dict: 市到省的映射字典
    """
    city_to_province = {}
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                # 跳过空行
                if not row:
                    continue
                
                # 处理不同长度的行
                if len(row) == 2:
                    # 省级别数据 (如: 110000,北京市)
                    province_code, province_name = row
                    current_province = province_name
                elif len(row) == 3:
                    # 市级别数据 (如: 130100,河北省,石家庄市)
                    code, province_name, city_name = row
                    # 检查省名称是否与当前省一致
                    if province_name == current_province:
                        # 提取市名称 (处理可能的后缀)
                        city_key = city_name
                        # # 处理常见的市后缀
                        # if city_key.endswith('市'):
                        #     city_key = city_key[:-1]
                        city_to_province[city_key] = province_name
    
    except FileNotFoundError:
        print(f"错误: 文件 '{csv_file_path}' 不存在")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 处理文件时发生异常: {e}")
        sys.exit(1)
    
    return city_to_province

def save_to_json(data, output_file_path):
    """
    将数据保存为 JSON 文件
    
    参数:
    data (dict): 要保存的数据
    output_file_path (str): 输出 JSON 文件路径
    """
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"成功保存映射关系到 '{output_file_path}'")
    except Exception as e:
        print(f"错误: 保存 JSON 文件时发生异常: {e}")
        sys.exit(1)

def main():
    # 默认文件路径
    default_csv_path = 'example.csv'
    default_json_path = 'city_to_province1.json'
    
    # 获取命令行参数
    csv_path = sys.argv[1] if len(sys.argv) > 1 else default_csv_path
    json_path = sys.argv[2] if len(sys.argv) > 2 else default_json_path
    
    print(f"正在处理: {csv_path}")
    
    # 构建映射
    mapping = build_city_to_province_mapping(csv_path)
    
    # 保存到 JSON
    save_to_json(mapping, json_path)
    
    # 输出统计信息
    print(f"已处理 {len(mapping)} 个市到省的映射关系")

if __name__ == "__main__":
    main()    