import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 基础路径和日期文件
file = 'D:\\files\\uncertainty\\mec_test2\\mec_test2\\output（对齐）\\中国'
dates_df = pd.read_excel(os.path.join(file, 'dates.xlsx'))
dates = dates_df.iloc[:, 0]
folder_name = os.path.basename(file)

# 需要处理的 Excel 文件列表
excel_files = ['utpca.xlsx', 'utcsa.xlsx']

for excel_file in excel_files:
    file_path = os.path.join(file, excel_file)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，跳过处理")
        continue
    
    # 读取数据
    df = pd.read_excel(file_path)
    month = df.iloc[:, 0]
    season = df.iloc[:, 2]
    year = df.iloc[:, 11]
    
    # 生成后缀（从文件名提取 pca/csa）
    suffix = excel_file[2:-5]  # 移除 "ut" 前缀和 ".xlsx" 后缀
    
    # 创建画布
    plt.figure(figsize=(10, 6))
    plt.plot(dates, month, label='月度')
    plt.plot(dates, season, label='季度')
    plt.plot(dates, year, label='年度')
    
    # 添加元信息
    plt.title(f"{folder_name}_{suffix}") 
    plt.xlabel('日期')
    plt.ylabel('数值')
    plt.legend()
    
    # 保存并清理
    output_path = os.path.join(file, f"{folder_name}_{suffix}.png")
    plt.savefig(output_path)
    plt.close()  # 关闭当前图表，避免内存泄漏
    print(f"已生成图片: {output_path}")

print("所有文件处理完成")