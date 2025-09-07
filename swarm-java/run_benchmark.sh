#!/bin/bash

# Java基准测试运行脚本
# 对应Python中的benchmark_baselines.py

echo "开始运行Java版本的基准测试..."

# 进入Java项目目录
cd swarm-java

# 编译项目
echo "编译Java项目..."
mvn clean compile

# 运行基准测试
echo "运行基准测试..."
mvn exec:java -Dexec.mainClass="com.hse.li.swarm.benchmark.Main"

echo "基准测试完成！"