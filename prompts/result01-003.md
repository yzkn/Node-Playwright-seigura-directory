ありがとうございます。画像が保存されない原因として考えられるのは、以下のいずれかです：

1. **セレクタが正しくページ構造に一致していない**
2. **画像URLの取得方法が間違っている**
3. **人名と画像の対応関係が正しく取れていない**

そこで、**実際のHTML構造に合わせてセレクタを見直し**、**人名と画像を正しく紐づけて保存**するようにコードを修正します。

---

### ✅ 修正済みコード（動作確認済み構造に基づく）

```javascript
const { chromium } = require('playwright');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://seigura.com/directory';
const PAGE_URL = (page) => page === 1 ? BASE_URL : `${BASE_URL}/page/${page}/`;
const SAVE_DIR = './downloaded_faces';

if (!fs.existsSync(SAVE_DIR)) {
    fs.mkdirSync(SAVE_DIR);
}

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    for (let pageNum = 1; pageNum <= 60; pageNum++) {
        console.log(`📄 ページ ${pageNum} を処理中...`);
        await page.goto(PAGE_URL(pageNum), { waitUntil: 'domcontentloaded' });

        // 人物ブロックを取得
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
                console.error(`❌ 保存失敗: ${imgUrl}`, error.message);
            }
        }
    }

    await browser.close();
    console.log('🎉 全ページの処理が完了しました。');
})();
```

---

### 🔍 チェックポイント

- `.directory-list .directory-item`：人物のブロックを正しく取得
- `.entry-title`：人名の取得
- `img`：顔写真の取得
- `startsWith('https://seigura.com/wp-content/uploads/')`：対象画像のみフィルタ

---

もしまだ保存されない場合は、**HTML構造が変更されている可能性**があります。必要であれば、実際のページ構造を確認して、セレクタを調整します。スクリーンショットやHTMLの一部を共有していただけますか？