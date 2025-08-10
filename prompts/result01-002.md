以下は、**Playwright + JavaScript** を使って、顔写真を保存する際に `<div class="entry-title">` に表示されている人名を画像ファイル名の先頭に追加するように修正したコードです。

---

### ✅ 修正ポイント
- 各人物の画像と名前をセットで取得
- ファイル名は `人名_画像ファイル名.jpg` の形式で保存

---

### 💻 修正済みコード

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

        // 各人物の画像と名前を取得
        const entries = await page.$$eval('.directory-list .directory-item', items => {
            return items.map(item => {
                const nameElement = item.querySelector('.entry-title');
                const imgElement = item.querySelector('img');
                const name = nameElement ? nameElement.textContent.trim().replace(/[\\/:*?"<>|]/g, '') : 'unknown';
                const imgUrl = imgElement ? imgElement.src : null;
                return { name, imgUrl };
            }).filter(entry => entry.imgUrl && entry.imgUrl.startsWith('https://seigura.com/wp-content/uploads/'));
        });

        console.log(`🔍 発見人物数: ${entries.length}`);

        for (const { name, imgUrl } of entries) {
            try {
                const filename = `${name}_${path.basename(imgUrl.split('?')[0])}`;
                const filepath = path.join(SAVE_DIR, filename);

                const response = await axios.get(imgUrl, { responseType: 'arraybuffer' });
                fs.writeFileSync(filepath, response.data);
                console.log(`✅ 保存: ${filename}`);
            } catch (error) {
                console.error(`❌ エラー: ${imgUrl}`, error.message);
            }
        }
    }

    await browser.close();
    console.log('🎉 全ページの処理が完了しました。');
})();
```

---

### 🔧 補足
- `replace(/[\\/:*?"<>|]/g, '')` はファイル名に使えない文字を除去するための処理です。
- `.directory-item` や `.entry-title` のセレクタは、サイト構造に依存します。もし構造が異なる場合は、調整が必要です。

---

さらに、**重複画像のスキップ**や**進捗バー表示**などの機能も追加できます。ご希望ですか？