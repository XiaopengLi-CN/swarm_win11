@echo off
echo ============================================================
echo Java版本BIPOP-CMA-ES基准测试项目 - 简化运行脚本
echo ============================================================

echo.
echo 检查Java环境...

:: 检查Java是否可用
java -version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo 错误：Java未安装或不在PATH中
    echo 请安装Java JDK 21并配置环境变量
    echo 下载地址：https://www.oracle.com/java/technologies/downloads/
    pause
    exit /b 1
)

echo Java环境检查通过！

echo.
echo 创建输出目录...
if not exist "Data\Baselines" mkdir "Data\Baselines"
if not exist "logs" mkdir "logs"

echo.
echo 编译Java源文件...
javac -cp "src\main\java" -d "target\classes" src\main\java\com\HSE\Li\swarm\eval\*.java

if %ERRORLEVEL% neq 0 (
    echo 编译失败！请检查Java代码
    pause
    exit /b 1
)

echo 编译成功！

echo.
echo 运行简单测试...
java -cp "target\classes" com.hse.li.swarm.eval.SimpleTest

if %ERRORLEVEL% neq 0 (
    echo 测试失败！
    pause
    exit /b 1
)

echo.
echo 简单测试通过！
echo.
echo 是否运行完整基准测试？(y/n)
set /p choice="请输入选择: "

if /i "%choice%"=="y" (
    echo.
    echo 开始运行完整基准测试...
    echo 注意：这将运行250个任务，可能需要较长时间
    java -cp "target\classes" com.hse.li.swarm.eval.Main
) else (
    echo 跳过完整基准测试
)

echo.
echo ============================================================
echo 运行完成！
echo 结果保存在: Data\Baselines\
echo 日志文件: logs\benchmark.log
echo ============================================================
pause

