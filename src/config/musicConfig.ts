import type { MusicPlayerConfig } from "../types/config";

export const musicPlayerConfig: MusicPlayerConfig = {
	showInNavbar: true,
	mode: "local",
	volume: 0.7,
	playMode: "list",
	showLyrics: true,

	meting: {
		api: "https://mu.tsh520.cn/api?server=:server&type=:type&id=:id",
		server: "netease",
		type: "song",
		id: "30254265974",
		auth: "",
		fallbackApis: ["https://mu.tsh520.cn/api?server=:server&type=:type&id=:id"],
	},

	local: {
		playlist: [
			{
				name: "知我",
				artist: "国风堂",
				url: "https://re.tsh520.cn/music/%E7%9F%A5%E6%88%91.mp3",
				cover: "https://re.0824.uk/zl/tx.webp",
				lrc: "https://re.tsh520.cn/music/%E7%9F%A5%E6%88%91.lrc",
			},
			{
				name: "女孩",
				artist: "韦礼安",
				url: "https://re.tsh520.cn/music/%E5%A5%B3%E5%AD%A9.mp3",
				cover: "https://re.0824.uk/zl/tx.webp",
				lrc: "https://re.tsh520.cn/music/%E5%A5%B3%E5%AD%A9.lrc",
			},
			{
				name: "爱得起",
				artist: "郑秀文",
				url: "https://re.tsh520.cn/music/%E7%88%B1%E5%BE%97%E8%B5%B7.mp3",
				cover: "https://re.0824.uk/zl/tx.webp",
				lrc: "https://re.tsh520.cn/music/%E7%88%B1%E5%BE%97%E8%B5%B7.lrc",
			},
		],
	},
};
