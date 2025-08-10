以下は、PlaywrightとJavaScriptを使って、指定されたWebサイトからすべての顔写真をダウンロードするためのサンプルコードです。ページを1から60まで順に処理し、画像を人名付きのファイル名で保存します。

### ✅ 必要な準備
- Node.jsのインストール
- Playwrightのインストール（`npm install playwright`）
- `fs`と`path`モジュールを使用して画像を保存

---

### 💻 ソースコード（`download_faces.js`）

```javascript
const fs = require('fs');
const path = require('path');
const https = require('https');
const { chromium } = require('playwright');

const BASE_URL = 'https://seigura.com/directory';
const PAGE_URL = (page) => page === 1 ? BASE_URL : `${BASE_URL}/page/${page}/`;
const IMAGE_DIR = path.join(__dirname, 'images');

// 画像保存用ディレクトリ作成
if (!fs.existsSync(IMAGE_DIR)) {
    fs.mkdirSync(IMAGE_DIR);
}

// 画像をダウンロードして保存
async function downloadImage(url, filename) {
    const filePath = path.join(IMAGE_DIR, filename);
    const file = fs.createWriteStream(filePath);
    https.get(url, (response) => {
        response.pipe(file);
    });
}

// ページを処理
async function processPage(page, pageNumber) {
    await page.goto(PAGE_URL(pageNumber), { waitUntil: 'domcontentloaded' });

    const entries = await page.$$eval('.archive-list-item', items => {
        return items.map(item => {
            const name = item.querySelector('.entry-title a')?.textContent?.trim();
            const img = item.querySelector('img')?.getAttribute('src');
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

// メイン処理
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

### 📁 保存先
- 画像はスクリプトと同じディレクトリ内の `images` フォルダに保存されます。
- ファイル名は「人名_画像ファイル名.jpg」の形式になります。

---

### 🔒 注意点
- サイトの利用規約に従ってください。
- 大量アクセスによるサーバー負荷を避けるため、必要に応じて `setTimeout` などで間隔を空ける処理を追加してください。

---

ご希望に応じて、TypeScript版や画像の重複チェック機能なども追加できます。どうしますか？