以下は、PlaywrightとJavaScriptを使って、指定されたWebサイトから顔写真をすべてダウンロードするためのサンプルコードです。ページを1から60まで順番に処理し、各ページにある画像をローカルに保存します。

### ✅ 前提条件
- Node.jsがインストールされていること
- `playwright`と`axios`と`fs`モジュールがインストールされていること

```bash
npm install playwright axios
```

---

### 💻 JavaScriptコード（Node.js）

```javascript
const { chromium } = require('playwright');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://seigura.com/directory';
const PAGE_URL = (page) => page === 1 ? BASE_URL : `${BASE_URL}/page/${page}/`;
const IMAGE_BASE = 'https://seigura.com/wp-content/uploads/';
const SAVE_DIR = './downloaded_faces';

if (!fs.existsSync(SAVE_DIR)) {
    fs.mkdirSync(SAVE_DIR);
}

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    for (let pageNum = 1; pageNum <= 60; pageNum++) {
        console.log(`📄 処理中: ページ ${pageNum}`);
        await page.goto(PAGE_URL(pageNum), { waitUntil: 'domcontentloaded' });

        // 画像URLを抽出
        const imageUrls = await page.$$eval('img', imgs =>
            imgs.map(img => img.src).filter(src => src.startsWith('https://seigura.com/wp-content/uploads/'))
        );

        console.log(`🔍 発見画像数: ${imageUrls.length}`);

        for (const url of imageUrls) {
            try {
                const filename = path.basename(url.split('?')[0]); // クエリ除去
                const filepath = path.join(SAVE_DIR, filename);

                const response = await axios.get(url, { responseType: 'arraybuffer' });
                fs.writeFileSync(filepath, response.data);
                console.log(`✅ 保存: ${filename}`);
            } catch (error) {
                console.error(`❌ エラー: ${url}`, error.message);
            }
        }
    }

    await browser.close();
    console.log('🎉 全ページの処理が完了しました。');
})();
```

---

### 📁 保存先
- 画像は `./downloaded_faces` フォルダに保存されます。

---

### 🛡️ 注意点
- サイトの利用規約に従ってください。
- 大量アクセスによるサーバー負荷に注意し、必要に応じてリクエスト間に待機時間を入れることをおすすめします。

---

ご希望であれば、**TypeScript版**や**画像の重複チェック機能付き**なども提供できます。どうしますか？