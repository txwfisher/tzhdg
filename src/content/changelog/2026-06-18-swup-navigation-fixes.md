---
version: "v1.7.1"
date: 2026-06-18
time: "17:30"
type: fix
description: 修复 Swup 导航相关的多个问题：后台样式丢失、Gist 数据首次加载失败、标签不可点击、页面切换闪烁
---

## Swup 导航修复

- 修复后台管理页面之间切换时布局样式瞬间丢失、只显示文字的问题
- 原因：后台页面使用 `data-swup-ignore`（Swup v3 属性），而 Swup v4 实际识别的是 `data-no-swup`
- 将 `src/pages/admin/` 下 3 个文件共 9 处 `data-swup-ignore` 替换为 `data-no-swup`

## Gist 数据首次加载失败修复

修复多个页面首次访问时 Gist 数据不显示、需要刷新才能加载的问题。根本原因相同：脚本被放在 `<MainGridLayout>` 组件标签外部，Astro 将其渲染到 `</body></html>` 之后，导致 Swup 导航时脚本无法被正确执行。

- **置顶说说页面** (`/moments/pinned/`)：将脚本移入 `<MainGridLayout>` 内部
- **笔记本索引页面** (`/life/notebooks/[slug]`)：将远程笔记加载脚本移入 `<MainGridLayout>` 内部
- **云端笔记页面** (`/life/notebooks/remote-entry/`)：将笔记内容加载脚本移入 `<MainGridLayout>` 内部

## 说说页面标签不可点击修复

- 修复说说页面外部 Gist 数据的标签点击后无反应的问题
- 原因：`MainGridLayout.astro` 中 `createCard()` 函数创建标签时使用 `<span>` 元素而非 `<a>` 链接
- 改为创建 `<a href="/archive/?tag=...">` 元素，与置顶页面和 MomentCard 组件行为一致

## 说说页面切换闪烁优化

- 优化从置顶页面返回说说页面时的样式闪烁问题
- 原因：两个页面各自有 `<style is:global>` 块定义卡片样式，Swup 的 `updateHead` 在切换时先移除旧样式再添加新样式，导致短暂无样式状态
- 将共享的卡片样式提取到 `src/styles/features/moments.css` 持久 CSS 文件中，通过 `main.css` 加载
- 从 `moments.astro` 和 `pinned.astro` 中移除重复的 `<style is:global>` 块
