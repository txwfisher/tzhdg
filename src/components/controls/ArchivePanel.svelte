<script lang="ts">
import { onMount } from "svelte";

import I18nKey from "@/i18n/i18nKey";
import { i18n } from "@/i18n/translation";
import { getPostUrlBySlug } from "@/utils/url-utils";

export let tags: string[] = [];
export let categories: string[] = [];
export let archiveList: ArchiveItem[] = [];

const params = new URLSearchParams(window.location.search);
tags = params.has("tag") ? params.getAll("tag") : [];
categories = params.has("category") ? params.getAll("category") : [];
const uncategorized = params.get("uncategorized");

interface ArchiveItem {
	id: string;
	type: "post" | "moment" | "bangumi" | "life";
	data: {
		title: string;
		tags: string[];
		category?: string | null;
		published: Date;
		link?: string;
	};
}

interface Group {
	year: number;
	items: ArchiveItem[];
}

let groups: Group[] = [];

function formatDate(date: Date) {
	const month = (date.getMonth() + 1).toString().padStart(2, "0");
	const day = date.getDate().toString().padStart(2, "0");
	return `${month}-${day}`;
}

function formatTag(tagList: string[]) {
	return tagList.map((t) => `#${t}`).join(" ");
}

function getItemUrl(item: ArchiveItem) {
	if (item.type === "post") {
		return getPostUrlBySlug(item.id);
	}
	if (item.type === "moment") {
		return `/moments/#${item.id}`;
	}
	if (item.type === "life") {
		return item.data.link || "/life/";
	}
	// bangumi 类型
	return item.data.link || "/bangumi/";
}

onMount(async () => {
	let filteredItems: ArchiveItem[] = archiveList;

	if (tags.length > 0) {
		filteredItems = filteredItems.filter(
			(item) =>
				Array.isArray(item.data.tags) &&
				item.data.tags.some((tag) => tags.includes(tag)),
		);
	}

	if (categories.length > 0) {
		filteredItems = filteredItems.filter(
			(item) => item.data.category && categories.includes(item.data.category),
		);
	}

	if (uncategorized) {
		filteredItems = filteredItems.filter((item) => !item.data.category);
	}

	// 按发布时间倒序排序
	filteredItems = filteredItems
		.slice()
		.sort((a, b) => b.data.published.getTime() - a.data.published.getTime());

	const grouped = filteredItems.reduce(
		(acc, item) => {
			const year = item.data.published.getFullYear();
			if (!acc[year]) {
				acc[year] = [];
			}
			acc[year].push(item);
			return acc;
		},
		{} as Record<number, ArchiveItem[]>,
	);

	const groupedItemsArray = Object.keys(grouped).map((yearStr) => ({
		year: Number.parseInt(yearStr, 10),
		items: grouped[Number.parseInt(yearStr, 10)],
	}));

	groupedItemsArray.sort((a, b) => b.year - a.year);

	groups = groupedItemsArray;
});
</script>

<div class="card-base px-8 py-6">
    {#each groups as group}
        <div>
            <div class="flex flex-row w-full items-center h-15">
                <div class="w-[15%] md:w-[10%] transition text-2xl font-bold text-right text-75">
                    {group.year}
                </div>
                <div class="w-[15%] md:w-[10%]">
                    <div
                            class="h-3 w-3 bg-none rounded-full outline outline-(--primary) mx-auto
                  -outline-offset-2 z-50 outline-3"
                    ></div>
                </div>
                <div class="w-[70%] md:w-[80%] transition text-left text-50">
                    {group.items.length} {i18n(group.items.length === 1 ? I18nKey.postCount : I18nKey.postsCount)}
                </div>
            </div>

            {#each group.items as item}
                <a
                        href={getItemUrl(item)}
                        aria-label={item.data.title}
                        class="group btn-plain block! h-10 w-full rounded-lg hover:text-[initial]"
                >
                    <div class="flex flex-row justify-start items-center h-full">
                        <!-- date -->
                        <div class="w-[15%] md:w-[10%] transition text-sm text-right text-50">
                            {formatDate(item.data.published)}
                        </div>

                        <!-- dot and line -->
                        <div class="w-[15%] md:w-[10%] relative dash-line h-full flex items-center">
                            <div
                                    class="transition-all mx-auto w-1 h-1 rounded group-hover:h-5
                       bg-[oklch(0.5_0.05_var(--hue))] group-hover:bg-(--primary)
                       outline outline-4 z-50
                       outline-(--card-bg)
                       group-hover:outline-(--btn-plain-bg-hover)
                       group-active:outline-(--btn-plain-bg-active)"
                            ></div>
                        </div>

                        <!-- item title -->
                        <div
                                class="w-[70%] md:max-w-[65%] md:w-[65%] text-left font-bold
                     group-hover:translate-x-1 transition-all group-hover:text-(--primary)
                     text-75 pr-8 whitespace-nowrap text-ellipsis overflow-hidden flex items-center gap-2"
                        >
                            {#if item.type === 'post'}
                                <span class="px-1.5 py-0.5 text-[10px] bg-amber-500 text-white rounded-md shrink-0 uppercase tracking-wider opacity-80 font-normal">
                                    文章
                                </span>
                            {:else if item.type === 'moment'}
                                <span class="px-1.5 py-0.5 text-[10px] bg-(--primary) text-white rounded-md shrink-0 uppercase tracking-wider opacity-80 font-normal">
                                    {i18n(I18nKey.moments) || 'Moment'}
                                </span>
                            {:else if item.type === 'bangumi'}
                                <span class="px-1.5 py-0.5 text-[10px] bg-red-500 text-white rounded-md shrink-0 uppercase tracking-wider opacity-80 font-normal">
                                    {i18n(I18nKey.bangumi) || 'Record'}
                                </span>
                            {:else if item.type === 'life'}
                                <span class="px-1.5 py-0.5 text-[10px] bg-emerald-600 text-white rounded-md shrink-0 uppercase tracking-wider opacity-80 font-normal">
                                    生活
                                </span>
                            {/if}
                            {item.data.title}
                        </div>

                        <!-- tag list -->
                        <div
                                class="hidden md:block md:w-[15%] text-left text-sm transition
                     whitespace-nowrap text-ellipsis overflow-hidden text-30"
                        >
                            {formatTag(item.data.tags)}
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/each}
</div>