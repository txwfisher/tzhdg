# Scripts 工具箱

所有脚本通过统一入口 `cli.js` 调用，只需记住一个命令：

```bash
pnpm cli
```

## 可用命令

| 命令 | 说明 | 脚本 |
|------|------|------|
| `sync` | 同步 Obsidian 笔记到博客 | `sync.js` |
| `new` | 创建新文章 | `new-post.js` |
| `media` | 下载影视封面 + 生成 md（TMDB） | `fetch-media.py` |
| `music` | 下载音乐 + 歌词 + 封面（Meting API） | `fetch-lrc.py` |
| `lrc` | 从本地 M4A 提取歌词/封面 | `extract-lrc.py` |
| `desc` | AI 批量生成文章摘要（千问 API） | `fill-descriptions.ts` |
| `dev` | 启动本地开发服务器 | `pnpm dev` |
| `build` | 构建生产站点 | `pnpm build` |

## 使用方式

```bash
# 交互菜单（推荐）
pnpm cli

# 子命令直达
pnpm cli sync [-a] [-f] [-s skip|incremental|force]
pnpm cli new "文章名"
pnpm cli media "片名" [--type=movie|tv] [-y]
pnpm cli music "歌名" --md
pnpm cli lrc <文件或目录>
pnpm cli desc
pnpm cli dev
pnpm cli build
```

所有子命令的额外参数会原样转发给对应的脚本。

## 各脚本详情

### sync.js — Obsidian 笔记同步

将 Obsidian 笔记库同步到博客 content 目录。支持三种策略：
- **skip**（默认）: 跳过已存在的文件
- **incremental**: 仅当源文件较新时更新
- **force**: 强制覆盖

配置：复制 `sync.config.example.js` 为 `sync.config.js`，填写 `obsidianVaultPath` 等字段。

### fetch-media.py — 影视封面下载

从 TMDB 搜索影视并生成 bangumi md 文件。封面输出到 `scripts/img-anime/`，md 输出到 `src/content/bangumi/anime/`。

### fetch-lrc.py — 音乐下载

从 Meting API 搜索下载音乐（含歌词/封面），生成 bangumi music md 文件。

### extract-lrc.py — 歌词提取

从本地 M4A/AAC/MP4 音频文件中提取内嵌歌词和封面。

### fill-descriptions.ts — 文章摘要生成

调用千问 API 批量为缺少 description 的文章自动生成摘要。
