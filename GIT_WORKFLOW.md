# Git工作流程指南

## 日常开发流程

### 1. 开始新功能开发前
```bash
# 确保在最新版本上
git pull origin main

# 创建新分支（可选）
git checkout -b feature/新功能名称
```

### 2. 修改代码后提交
```bash
# 查看修改状态
git status

# 添加修改的文件
git add .  # 添加所有修改
# 或者 git add 文件名  # 添加特定文件

# 提交修改
git commit -m "描述你的修改内容"

# 推送到远程仓库
git push origin main  # 如果在main分支
# 或者 git push origin feature/新功能名称  # 如果在功能分支
```

### 3. 查看历史记录
```bash
# 查看提交历史
git log --oneline

# 查看特定文件的修改历史
git log --oneline 文件名

# 查看最近一次提交的详细信息
git show
```

### 4. 回滚修改
```bash
# 撤销工作区的修改（未提交）
git checkout -- 文件名

# 撤销已提交的修改
git revert 提交ID

# 回滚到特定版本
git reset --hard 提交ID
```

### 5. 分支管理
```bash
# 查看所有分支
git branch -a

# 切换分支
git checkout 分支名

# 删除分支
git branch -d 分支名
```

## 提交信息规范
建议使用以下格式：
- `feat: 添加新功能`
- `fix: 修复bug`
- `docs: 更新文档`
- `style: 代码格式调整`
- `refactor: 重构代码`
- `test: 添加测试`
- `chore: 构建过程或辅助工具的变动`

## 注意事项
1. 每次修改前先拉取最新代码：`git pull`
2. 提交前检查状态：`git status`
3. 写清晰的提交信息
4. 定期推送代码到远程仓库
5. 重要修改前创建备份分支
