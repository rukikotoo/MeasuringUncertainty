% -------------------------------------------------------------------------
% Load raw data and generate cleaned data used for analysis
% -------------------------------------------------------------------------

% Load data
clear; clc;
cd('D:\files\uncertainty\mec_test2\mec_test2')
country = '英国';  % 临时硬编码测试，为什么参数传不进去？？？？？？
fileDir = fullfile('对齐数据(处理)');  % 使用fullfile处理路径
filename = fullfile(fileDir, [country '_s.xlsx']);
[mdata, mtxt] = xlsread(filename);
mdata = mdata';  % 转置后：每列对应一个变量，首行是vartype

% 提取元数据
names = mtxt(2:end, 1)';     % 第一列变量名转行向量
vartype = mdata(1, :);       % 关键修改：直接从数值矩阵首行获取vartype
time_series = mdata(2:end,:);% 实际时间序列数据

% 数据预处理
[yt, a, b, c] = prepare(time_series, names, vartype);

% 截取有效数据段（保留第3行到最后）
data = yt(3:end, :);

% ==================== 数据清洗 ====================
valid_cols = ~any(isnan(data), 1);  % 有效列掩码
data = data(:, valid_cols);          % T×N_clean
names = names(:, valid_cols);        % 同步变量名
vartype = vartype(:, valid_cols);    % 同步变量类型
data(data == 0) = eps;               % 零值替换为极小值

% ==================== 时间序列对齐 ====================
T = size(data, 1);  % 基于清洗后数据获取时间长度
date = readtable(filename, 'ReadVariableNames', false); % 读取文件，不需要变量名

excelDate = date{1, end}; % 提取最后一列第一行的数据

% 将 Excel 日期转换为 MATLAB 日期格式
dateValue = datetime(excelDate, 'ConvertFrom', 'excel', 'Format', 'yyyy/MM/dd HH:mm:ss');

% 提取年份和月份
year = year(dateValue);
month = month(dateValue);

% 显示结果
fprintf('Year: %d, Month: %d\n', year, month);
dates = 1900 + (59:1/12:(year-1900)+1/12.*month)';  % 原时间生成逻辑
dates = dates(end-T+1:end);          % 截取对应长度
save testdata data dates names vartype year month 
save country country
