const fs = require('fs');
const path = require('path');
const https = require('https');
const { chromium } = require('playwright');

const BASE_URL = 'https://seigura.com/directory';
const PAGE_URL = (page) => page === 1 ? BASE_URL : `${BASE_URL}/page/${page}/`;
const IMAGE_DIR = path.join(__dirname, 'images');

if (!fs.existsSync(IMAGE_DIR)) {
    fs.mkdirSync(IMAGE_DIR);
}

async function downloadImage(url, filename) {
    const filePath = path.join(IMAGE_DIR, filename);
    const file = fs.createWriteStream(filePath);
    https.get(url, (response) => {
        response.pipe(file);
    });
}

async function processPage(page, pageNumber) {
    await page.goto(PAGE_URL(pageNumber), { waitUntil: 'networkidle' });

    // ページ内のすべての顔写真要素をスクロールして読み込ませる
    await page.evaluate(() => {
        const items = document.querySelectorAll('.archive-list-item');
        items.forEach(item => item.scrollIntoView());
    });

    // 少し待機して画像の遅延読み込みを完了させる
    await page.waitForTimeout(2000);

    const entries = await page.$$eval('.archive-list-item', items => {
        return items.map(item => {
            const name = item.querySelector('.entry-title a')?.textContent?.trim();
            const imgTag = item.querySelector('img');
            const img = imgTag?.getAttribute('data-src') || imgTag?.getAttribute('src');
            return { name, img };
        }).filter(entry => entry.name && entry.img && entry.img.includes('wp-content/uploads'));
    });

    for (const entry of entries) {
        const imgName = entry.img.split('/').pop();
        const fileName = `${entry.name.replace(/\s+/g, ' ')}_${imgName}`;
        console.log(`Downloading: ${fileName}`);
        await downloadImage(entry.img, fileName);
    }
}

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    for (let i = 1; i <= 60; i++) {
        console.log(`Processing page ${i}...`);
        await processPage(page, i);
    }

    await browser.close();
    console.log('All images downloaded.');
})();
