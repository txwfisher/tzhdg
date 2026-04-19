# 同步脚本使用说明

## 功能

将 Obsidian 笔记库中的笔记同步到博客项目的 content 文件夹中。

### 新增：增量同步支持

脚本现在支持三种同步策略，可以根据需要选择合适的同步方式：

- **skip**（默认）: 跳过已存在的文件
- **incremental**: 仅当源文件较新时更新目标文件
- **force**: 强制覆盖所有文件

## 配置

1. 复制 `sync.config.example.js` 为 `sync.config.js`
2. 修改配置文件中的路径：
   - `obsidianVaultPath`: 你的 Obsidian 笔记库路径
   - `projectContentPath`: 博客项目的 content 文件夹路径（通常是 `src/content`）
   - `syncStrategy`: 默认同步策略（可选：`skip` | `incremental` | `force`）

## 使用方法

### 交互模式（默认）

```bash
# 进入 scripts 目录
cd scripts

# 运行同步脚本（使用默认 skip 策略）
node sync.js
```

### 命令行参数模式

```bash
# 增量同步（仅更新较新的文件）
node sync.js --strategy incremental

# 强制覆盖所有文件
node sync.js --strategy force

# 指定同步类型
node sync.js --type 文章

# 指定多个同步类型
node sync.js --type 文章 --type 动态

# 同步全部类型
node sync.js --all

# 组合使用
node sync.js --all --strategy incremental
```

### 快捷参数

```bash
# -s: 指定策略
node sync.js -s incremental

# -t: 指定类型
node sync.js -t 文章

# -a: 同步全部
node sync.js -a

# -f: 强制覆盖（等同于 --strategy force）
node sync.js -f

# -h: 显示帮助
node sync.js -h
```

## 同步选项

交互模式下提供以下同步选项：
1. **同步文章** - 同步到 `posts/` 文件夹
2. **同步动态** - 同步到 `moments/` 文件夹
3. **同步记录** - 同步到 `bangumi/` 文件夹
4. **同步生活** - 同步到 `life/` 文件夹
5. **同步全部** - 同步所有类型的内容
6. **退出**

## 文件命名规则

脚本会根据 frontmatter 中的 `published` 字段自动重命名文件：
- moments: `YYYY-MM-DD.md`
- posts: 保留原文件名或使用 title 生成

## 注意事项

- 确保 Obsidian 笔记包含正确的 frontmatter 元数据
- moments 类型的笔记需要 `published` 字段（日期格式：YYYY-MM-DD）
- 命令行参数会覆盖配置文件中的默认策略
- 增量同步基于文件修改时间判断，建议在 Obsidian 中编辑后执行
