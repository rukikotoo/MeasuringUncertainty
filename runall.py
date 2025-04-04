import subprocess
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os
# 配置区------------------------------------------------------------------
SCRIPTS = [
    r"D:\files\uncertainty\mec_test2\mec_test2\generate_jlndata.m",
    r"D:\files\uncertainty\mec_test2\mec_test2\generate_testferrors.m",
    r"D:\files\uncertainty\mec_test2\mec_test2\generate_svfdraws_para.r",
    r"D:\files\uncertainty\mec_test2\mec_test2\generate_svydraws_para.r",
    r"D:\files\uncertainty\mec_test2\mec_test2\generate_testut.m",
    r"D:\files\uncertainty\mec_test2\mec_test2\generate_aggu.m"
]

WORKING_DIR = r"D:\files\uncertainty\mec_test2\mec_test2"  # 所有脚本的工作目录
country="英国"
output_dir = os.path.join(WORKING_DIR, "output（对齐）")  # 更安全的路径拼接方式
target_dir = os.path.join(output_dir, country)  # 完整的目标路径

# 创建目录（如果不存在）
os.makedirs(target_dir, exist_ok=True)  # exist_ok=True 表示目录存在时不报错
# ------------------------------------------------------------------------

def execute_script(script_path):
    """执行单个脚本的通用函数"""
    script = Path(script_path)
    
    # 自动识别脚本类型
    if script.suffix == '.m':
        cmd = [
    'matlab',
    '-batch',
    f"run('{script.name}');"
]
        print(f"\n▶ 正在执行MATLAB脚本: {script.name}")
    elif script.suffix in ('.r', '.R'):
        cmd = [
    'Rscript', 
    '--vanilla',          # 独立参数
    '--slave', 
    '--no-save', 
    '--silent', #试了半天，这个命令太重要了
    '--no-restore', 
    '--encoding=UTF-8',   # 编码参数
    script.name           # 脚本名称
]
        print(f"\n▶ 正在执行R脚本: {script.name}")
    else:
        raise ValueError(f"不支持的脚本类型: {script.suffix}")

    try:
        # 在指定工作目录下执行命令
        subprocess.run(
            cmd,                    # 直接传递命令列表
            shell=False,            # 禁用shell模式
            check=True, 
            cwd=script.parent, 
            stdout=subprocess.DEVNULL,  # 丢弃输出
            stderr=subprocess.DEVNULL   # 丢弃错误输出
        )
        print(f"✅ 成功执行: {script.name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 执行失败: {script.name}")
        print(f"命令: {' '.join(cmd)}")
        print(f"工作目录: {script.parent}")
        exit(1)

if __name__ == "__main__":
    
    print(f"🚀 开始执行工作流，共 {len(SCRIPTS)} 个脚本")
    print(f"工作目录: {WORKING_DIR}\n{'='*50}")
    
    for idx, script in enumerate(SCRIPTS, 1):
        print(f"\n[{idx}/{len(SCRIPTS)}] ", end='')
        execute_script(script)
    
    print("\n" + "="*50)
    print("🎉 所有脚本执行完成！")


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 基础路径和日期文件
file = 'D:\\files\\uncertainty\\mec_test2\\mec_test2\\output（对齐）\\'+country
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