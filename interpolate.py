import pandas as pd
file="D:\\files\\uncertainty\\mec_test2\\mec_test2\\对齐数据(处理)\\日本_s.xlsx"
# 读取Excel并保留原始列名
df = pd.read_excel(file, engine='openpyxl')

# 分离文本区域与数据区域
text_columns = df.iloc[:, :2]  # 前二列全部保留
#name vartype 频率
data_region = df.iloc[1:, 2:]  # 从第二行开始，第2列之后的数据

# 执行行向插值（axis=1）
filled_data = data_region.interpolate(axis=1, method='linear', limit_direction='both')#关键是按行插值

# 重新组合数据框
final_df = pd.concat([
    text_columns.iloc[1:].reset_index(drop=True),  # 文本列（排除标题行）
    filled_data.reset_index(drop=True)
], axis=1)

# 还原列标题
final_df.columns = df.columns

# 保存结果
final_df.to_excel(file, index=False)