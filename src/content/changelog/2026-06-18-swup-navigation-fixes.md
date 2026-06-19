---
version: "v1.7.1"
date: 2026-06-18
time: "17:30"
type: fix
description: 修复后台页面切换时样式丢失 + 置顶说说页面首次访问不显示 Gist 数据
---

## Swup 导航修复

- 修复后台管理页面之间切换时布局样式瞬间丢失、只显示文字的问题
- 原因：后台页面使用 `data-swup-ignore`（Swup v3 属性），而 Swup v4 实际识别的是 `data-no-swup`
- 将 `src/pages/admin/` 下 3 个文件共 9 处 `data-swup-ignore` 替换为 `data-no-swup`

## 置顶说说 Gist 数据加载修复

- 修复首次访问 `/moments/pinned/` 页面时外部 Gist 置顶数据不显示、需要刷新才能加载的问题
- 原因：脚本被放在 `<MainGridLayout>` 组件标签外部，Astro 将其渲染到 `</body></html>` 之后，导致 Swup 导航时脚本无法被正确管理和重新执行
- 将脚本移入 `<MainGridLayout>` 内部，使 Swup ScriptsPlugin 能在每次导航时自动重新执行
- 优化闭包变量为函数参数，避免 DOM 引用过期
- 添加 `setTimeout` + `try/catch` 防御性编程
