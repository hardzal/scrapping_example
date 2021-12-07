const axios = require('axios'); 
const playwright = require('playwright'); 
const cheerio = require('cheerio'); 
 
const url = 'https://scrapeme.live/shop/page/1/'; 
const useHeadless = false; // "true" to use playwright 
const maxVisits = 30; // Arbitrary number for the maximum of links visited 
const visited = new Set(); 
const allProducts = []; 
 
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms)); 
 
const getHtmlPlaywright = async url => { 
	const browser = await playwright.chromium.launch(); 
	const context = await browser.newContext(); 
	const page = await context.newPage(); 
	await page.goto(url); 
	const html = await page.content(); 
	await browser.close(); 
 
	return html; 
}; 
 
const getHtmlAxios = async url => { 
	const { data } = await axios.get(url); 
 
	return data; 
}; 
 
const getHtml = async url => { 
	return useHeadless ? await getHtmlPlaywright(url) : await getHtmlAxios(url); 
}; 
 
const extractContent = $ => 
	$('.product') 
		.map((_, product) => { 
			const $product = $(product); 
 
			return { 
				id: $product.find('a[data-product_id]').attr('data-product_id'), 
				title: $product.find('h2').text(), 
				price: $product.find('.price').text(), 
			}; 
		}) 
		.toArray(); 
 
const extractLinks = $ => [ 
	...new Set( 
		$('.page-numbers a') 
			.map((_, a) => $(a).attr('href')) 
			.toArray() 
	), 
]; 
 
const crawl = async url => { 
	visited.add(url); 
	console.log('Crawl: ', url); 
	const html = await getHtml(url); 
	const $ = cheerio.load(html); 
	const content = extractContent($); 
	const links = extractLinks($); 
	links 
		.filter(link => !visited.has(link)) 
		.forEach(link => { 
			q.enqueue(crawlTask, link); 
		}); 
	allProducts.push(...content); 
 
	// We can see how the list grows. Gotta catch 'em all! 
	console.log(allProducts.length); 
}; 
 
// Change the default concurrency or pass it as param 
const queue = (concurrency = 4) => { 
	let running = 0; 
	const tasks = []; 
 
	return { 
		enqueue: async (task, ...params) => { 
			tasks.push({ task, params }); 
			if (running >= concurrency) { 
				return; 
			} 
 
			++running; 
			while (tasks.length) { 
				const { task, params } = tasks.shift(); 
				await task(...params); 
			} 
			--running; 
		}, 
	}; 
}; 
 
const crawlTask = async url => { 
	if (visited.size >= maxVisits) { 
		console.log('Over Max Visits, exiting'); 
		return; 
	} 
 
	if (visited.has(url)) { 
		return; 
	} 
 
	await crawl(url); 
}; 
 
const q = queue(); 
q.enqueue(crawlTask, url);