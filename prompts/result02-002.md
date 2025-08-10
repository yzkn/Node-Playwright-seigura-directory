ありがとうございます！画像が6枚しか保存されない原因として、以下の可能性が考えられます：

1. **Playwrightが一部の要素しか読み込んでいない（遅延読み込み）**
2. **画像がJavaScriptによって後から読み込まれている**
3. **セレクタが一部の画像しか取得できていない**

これを解決するために、以下の修正を加えます：

- ページ遷移後に十分な待機時間を設ける
- `scrollIntoView` で全要素を表示させる
- 画像と人名の取得をより確実なセレクタで行う

---

### ✅ 修正済みコード

```javascript
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
```

---

### 🔧 主な修正点

- `scrollIntoView()` を使ってすべての画像要素を表示
- `data-src` 属性もチェックして遅延読み込み画像を取得
- `waitForTimeout(2000)` で読み込み完了を待機

---

これで各ページの最大30枚の画像がすべて保存されるはずです。もしまだ不足がある場合は、さらにスクロールや待機時間を調整できます。

試してみて、うまくいったか教えていただけますか？必要ならさらに調整します！