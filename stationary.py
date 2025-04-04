import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

# 定义特殊经济变量白名单（可根据需要扩展）
SPECIAL_CASES = {
    'CPI': 5,        # 通胀指标强制使用对数差分
    'GDP': 5,        # GDP常用对数增长率
    'InterestRate': 1, # 利率通常保持原始形式
    'UnemploymentRate': 2 # 失业率常用一阶差分
}

def determine_processing_method(time_series, name):
    """
    改进后的处理方法选择逻辑：
    1. 优先考虑经济学意义
    2. 禁用二阶差分
    3. 分层选择策略
    """
    # 异常值处理增强
    try:
        time_series = pd.to_numeric(time_series, errors="coerce").dropna()
        if len(time_series) < 5:  # 最少需要5个观测值
            print(f"{name} 数据不足（有效长度{len(time_series)}<5）")
            return 1, None
    except Exception as e:
        print(f"时间序列: {name} 解析错误: {e}")
        return 1, None

    # 特殊变量优先处理
    if name in SPECIAL_CASES:
        method = SPECIAL_CASES[name]
        print(f"特殊变量 {name} 强制使用方法 {method}")
        return method, None

    # 全同值处理
    if time_series.nunique() == 1:
        print(f"{name} 序列值相同")
        return 1, None

    # ADF检验函数（增加长度检查）
    def adf_test(series):
        if len(series) < 5:  # statsmodels要求最小长度
            return np.inf, None
        try:
            result = adfuller(series, autolag="AIC")
            return result[1], result
        except:
            return np.inf, None

    p_values = {k:np.inf for k in range(1,7)}  # 初始化所有方法为无穷大
    
    # 原始序列 (方法1)
    p_values[1], res1 = adf_test(time_series)

    # 一阶差分 (方法2)
    if len(time_series) > 1:  # 差分可行性检查
        diff1 = time_series.diff().dropna()
        p_values[2], res2 = adf_test(diff1)

    # 禁用二阶差分 (方法3)
    p_values[3] = np.inf

    # 对数处理条件放宽（允许0值）
    has_zeros = (time_series == 0).any()
    has_negatives = (time_series < 0).any()
    
    # 允许包含0但不含负值的序列取对数（加1处理）
    if not has_negatives:
        offset = 1 if has_zeros else 0  # 包含0值时加1处理
        log_series = np.log(time_series + offset)
        
        # 方法4：对数序列
        p_values[4], res4 = adf_test(log_series)
        
        # 方法5：对数一阶差分
        if len(log_series) > 1:
            log_diff1 = log_series.diff().dropna()
            p_values[5], res5 = adf_test(log_diff1)
        
        # 启用对数二阶差分 (方法6)
        if len(log_diff1) > 2:
            log_diff2 = log_diff1.diff().dropna()
            p_values[6], res6 = adf_test(log_diff2)

    # 分层选择策略
    def select_method(pvals):
        # 找出所有小于0.05的p值
        significant_methods = [k for k, v in pvals.items() if v < 0.05]
        if significant_methods:
            return min(significant_methods)
        # 如果没有小于0.05的p值，返回最小的p值
        return min(pvals, key=pvals.get)

    best_method = select_method(p_values)
    
    # 结果打印优化
    print(f"序列: {name} 方法: {best_method} (p={p_values[best_method]:.3f})")
    return best_method, p_values[best_method]

# 文件路径处理增强
input_path = "D:\\files\\uncertainty\\mec_test2\\mec_test2\\对齐数据(处理)\\中国.xlsx"
output_path = "D:\\files\\uncertainty\\mec_test2\\mec_test2\\对齐数据(处理)\\中国_s.xlsx"

if __name__ == "__main__":
    try:
        df = pd.read_excel(input_path)
        
        # 添加新的处理方法列
        if '处理方法' not in df.columns:
            df.insert(1, '处理方法', None)
        
        for index, row in df.iterrows():
            # 使用iloc按位置访问
            name_cell = row.iloc[0]  # 第一列
            time_series = row.iloc[1:].astype(float).dropna()  # 从第二列开始
            
            # 名称清洗逻辑增强
            try:
                clean_name = str(name_cell).split('：')[-1].strip()  # 处理中文冒号
            except:
                clean_name = str(name_cell).split(':')[-1].strip()  # 处理英文冒号
            
            method, p_value = determine_processing_method(time_series, clean_name)
            if p_value >= 0.05:  # 如果处理后仍不平稳，删除该行
                print(f"删除序列: {clean_name} (p={p_value:.3f})")
                df.drop(index, inplace=True)
            else:
                df.iloc[index, df.columns.get_loc('处理方法')] = method  # 明确按列名定位
        
        df.to_excel(output_path, index=False)
        print(f"处理完成，保存至: {output_path}")
        
    except Exception as e:
        print(f"运行时错误: {str(e)}")