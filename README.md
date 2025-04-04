# MeasuringUncertainty

replication of Jurado(2015)  


运行参考runall.py。里面写的是绝对路径，肯定是运行不了的。但聪明的你研究一下runall.py就能知道项目的文件布局和整体逻辑，good luck。
输入文件格式第一行为时间，第一列为变量名。运行stationary.py整理数据后，第二列会插入平稳化处理方法，之后可以运行interpolate.py进行线性插值填补空缺数据，最后再运行runall.py。平稳化方法的选取参考原文appendix。注意，此时的平稳化方法只是通过ADF检验的最低条件，还需要根据经济意义进行人为调整。比如大部分宏观经济变量都是要取对数之后再差分的。


Run the script using runall.py as a reference. Since it uses absolute paths, it probably won’t run directly. But if you take a look at runall.py, you’ll figure out the project’s file structure and logic. Good luck!
The input file format has the first row as time and the first column as variable names. After running stationary.py to organize the data, the second column will include the stationarity method. Next, run interpolate.py to fill missing data through interpolation, and finally run runall.py.
The selection of stationarity methods should refer to the original appendix. Note that the stationarity methods here only meet the minimum condition of passing the ADF test and may require manual adjustments based on economic interpretation. For example, most macroeconomic variables typically need to be logged and differenced.
