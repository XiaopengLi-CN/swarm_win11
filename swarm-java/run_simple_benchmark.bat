@echo off
echo ============================================================
echo 简化版Java基准测试 - 无需Maven
echo ============================================================

echo.
echo 检查Java环境...
java -version
if %ERRORLEVEL% neq 0 (
    echo 错误：Java未安装或不在PATH中
    echo 请安装Java JDK并配置环境变量
    pause
    exit /b 1
)

echo.
echo 创建输出目录...
if not exist "Data\Baselines" mkdir "Data\Baselines"
if not exist "logs" mkdir "logs"

echo.
echo 编译Java源文件...
javac -d "target\classes" src\main\java\com\HSE\Li\swarm\eval\SimpleBenchmark.java src\main\java\com\HSE\Li\swarm\eval\OptimizationTask.java

if %ERRORLEVEL% neq 0 (
    echo 编译失败！请检查Java代码
    pause
    exit /b 1
)

echo 编译成功！

echo.
echo 运行简化版基准测试...
java -cp "target\classes" com.hse.li.swarm.eval.SimpleBenchmark

echo.
echo ============================================================
echo 运行完成！
echo 结果保存在: Data\Baselines\
echo ============================================================
pause

