import type { CoverImageConfig } from "../types/config";

/**
 * 文章封面图配置
 *
 * enableInPost - 是否在文章详情页显示封面图
 *
 * 随机封面图使用说明：
 * 1. 在文章的 Frontmatter 中添加 image: "api" 即可使用随机图功能
 * 2. 系统会依次尝试所有配置的 API，全部失败后使用备用图片
 *
 * // 文章 Frontmatter 示例：
 * ---
 * title: 文章标题
 * image: "api"
 * ---
 */
export const coverImageConfig: CoverImageConfig = {
	// 是否在文章详情页显示封面图
	enableInPost: false,

	randomCoverImage: {
		// 随机封面图功能开关
		enable: true,
		// 封面图API列表
		apis: [
			"https://re.tsh520.cn/img/zdy/1.webp",
			"https://re.tsh520.cn/img/zdy/2.webp",
			"https://re.tsh520.cn/img/zdy/3.webp",
			"https://re.tsh520.cn/img/zdy/4.webp",
			"https://re.tsh520.cn/img/zdy/5.webp",
			"https://re.tsh520.cn/img/zdy/6.webp",
			"https://re.tsh520.cn/img/zdy/7.webp",
			"https://re.tsh520.cn/img/zdy/8.webp",
			"https://re.tsh520.cn/img/zdy/9.webp",
			"https://re.tsh520.cn/img/zdy/10.webp",
			"https://re.tsh520.cn/img/zdy/11.webp",
			"https://re.tsh520.cn/img/zdy/12.webp",
			"https://re.tsh520.cn/img/zdy/13.webp",
			"https://re.tsh520.cn/img/zdy/14.webp",
			"https://re.tsh520.cn/img/zdy/15.webp",
			"https://re.tsh520.cn/img/zdy/16.webp",
			"https://re.tsh520.cn/img/zdy/17.webp",
			"https://re.tsh520.cn/img/zdy/18.webp",
			"https://re.tsh520.cn/img/zdy/19.webp",
			"https://re.tsh520.cn/img/zdy/20.webp",
			"https://re.tsh520.cn/img/zdy/21.webp",
			"https://re.tsh520.cn/img/zdy/22.webp",
			"https://re.tsh520.cn/img/zdy/23.webp",
			"https://re.tsh520.cn/img/zdy/24.webp",
			"https://re.tsh520.cn/img/zdy/25.webp",
			"https://re.tsh520.cn/img/zdy/26.webp",
			"https://re.tsh520.cn/img/zdy/27.webp",
			"https://re.tsh520.cn/img/zdy/28.webp",
			"https://re.tsh520.cn/img/zdy/29.webp",
			"https://re.tsh520.cn/img/zdy/30.webp",
			"https://re.tsh520.cn/img/zdy/31.webp",
			"https://re.tsh520.cn/img/zdy/32.webp",
			"https://re.tsh520.cn/img/zdy/33.webp",
			"https://re.tsh520.cn/img/zdy/34.webp",
			"https://re.tsh520.cn/img/zdy/35.webp",
			"https://re.tsh520.cn/img/zdy/36.webp",
			"https://re.tsh520.cn/img/zdy/37.webp",
			"https://re.tsh520.cn/img/zdy/38.webp",
			"https://re.tsh520.cn/img/zdy/39.webp",
			"https://re.tsh520.cn/img/zdy/40.webp",
			"https://re.tsh520.cn/img/zdy/41.webp",
			"https://re.tsh520.cn/img/zdy/42.webp",
			"https://re.tsh520.cn/img/zdy/43.webp",
			"https://re.tsh520.cn/img/zdy/44.webp",
			"https://re.tsh520.cn/img/zdy/45.webp",
			"https://re.tsh520.cn/img/zdy/46.webp",
			"https://re.tsh520.cn/img/zdy/47.webp",
			"https://re.tsh520.cn/img/zdy/48.webp",
			"https://re.tsh520.cn/img/zdy/49.webp",
			"https://re.tsh520.cn/img/zdy/50.webp",
			"https://re.tsh520.cn/img/zdy/51.webp",
			"https://re.tsh520.cn/img/zdy/52.webp",
			"https://re.tsh520.cn/img/zdy/53.webp",
			"https://re.tsh520.cn/img/zdy/54.webp",
			"https://re.tsh520.cn/img/zdy/55.webp",
			"https://re.tsh520.cn/img/zdy/56.webp",
			"https://re.tsh520.cn/img/zdy/57.webp",
			"https://re.tsh520.cn/img/zdy/58.webp",
			"https://re.tsh520.cn/img/zdy/59.webp",
			"https://re.tsh520.cn/img/zdy/60.webp",
			"https://re.tsh520.cn/img/zdy/61.webp",
			"https://re.tsh520.cn/img/zdy/62.webp",
			"https://re.tsh520.cn/img/zdy/63.webp",
			"https://re.tsh520.cn/img/zdy/64.webp",
			"https://re.tsh520.cn/img/zdy/65.webp",
			"https://re.tsh520.cn/img/zdy/66.webp",
			"https://re.tsh520.cn/img/zdy/67.webp",
			"https://re.tsh520.cn/img/zdy/68.webp",
			"https://re.tsh520.cn/img/zdy/69.webp",
			"https://re.tsh520.cn/img/zdy/70.webp",
			"https://re.tsh520.cn/img/zdy/71.webp",
			"https://re.tsh520.cn/img/zdy/72.webp",
			"https://re.tsh520.cn/img/zdy/73.webp",
			"https://re.tsh520.cn/img/zdy/74.webp",
			"https://re.tsh520.cn/img/zdy/75.webp",
			"https://re.tsh520.cn/img/zdy/76.webp",
			"https://re.tsh520.cn/img/zdy/77.webp",
			"https://re.tsh520.cn/img/zdy/78.webp",
			"https://re.tsh520.cn/img/zdy/79.webp",
			"https://re.tsh520.cn/img/zdy/80.webp",
			"https://re.tsh520.cn/img/zdy/81.webp",
			"https://re.tsh520.cn/img/zdy/82.webp",
			"https://re.tsh520.cn/img/zdy/83.webp",
			"https://re.tsh520.cn/img/zdy/84.webp",
			"https://re.tsh520.cn/img/zdy/85.webp",
			"https://re.tsh520.cn/img/zdy/86.webp",
			"https://re.tsh520.cn/img/zdy/87.webp",
			"https://re.tsh520.cn/img/zdy/88.webp",
			"https://re.tsh520.cn/img/zdy/89.webp",
			"https://re.tsh520.cn/img/zdy/90.webp",
			"https://re.tsh520.cn/img/zdy/91.webp",
			"https://re.tsh520.cn/img/zdy/92.webp",
			"https://re.tsh520.cn/img/zdy/93.webp",
			"https://re.tsh520.cn/img/zdy/94.webp",
			"https://re.tsh520.cn/img/zdy/95.webp",
			"https://re.tsh520.cn/img/zdy/96.webp",
		],
		// API失败时的回退图片路径（相对于src目录或以/开头的public目录路径）
		fallback: "assets/images/cover.avif",
		// 是否显示加载动画
		showLoading: false,
	},
};
