PlaywrightとJavaScriptを用いて、以下のWebサイトからすべての顔写真をダウンロードするソースコードを提案してください。1ページ目に掲載されている顔写真を保存し終わったら2ページ目、2ページ目が終わったら3ページ目と、最後のページまで連続処理をしてください。

＜対象＞
1ページ目： https://seigura.com/directory/
2ページ目以降： https://seigura.com/directory/page/#PAGE#/ （#PAGE#は、2～60までの整数が入る）
各ページには、最大30枚の顔写真が掲載されている。https://seigura.com/wp-content/uploads/からはじまるURLに格納されている画像ファイルを、ローカルに保存する。

画像ファイルを保存する際には、entry-titleクラスをもつdivタグの中に表示されている人名を、画像ファイル名の先頭に_を挟んで追加するようにしてください。
例えば、2ページ目に含まれる以下のHTMLソースを例にすると、58cb9a44a89c30dd5e23d27a9b0cfa84.jpgを保存する際に、ファイル名を青山 吉能_58cb9a44a89c30dd5e23d27a9b0cfa84.jpgに変更して保存します。

<div class="col-lg-2 col-md-3 col-4"><div id="post-117" class="archive-list-item post-117 directory type-directory status-publish has-post-thumbnail directory_t-index-a"><div class="archive-thumbnail"> <a href="https://seigura.com/directory/117/" data-wpel-link="internal"> <img width="289" height="386" src="https://seigura.com/wp-content/uploads/2025/04/58cb9a44a89c30dd5e23d27a9b0cfa84.jpg" class="trim-mid wp-post-image ls-is-cached lazyloaded" alt="" decoding="async" fetchpriority="high" data-src="https://seigura.com/wp-content/uploads/2025/04/58cb9a44a89c30dd5e23d27a9b0cfa84.jpg"><noscript><img width="289" height="386" src="https://seigura.com/wp-content/uploads/2025/04/58cb9a44a89c30dd5e23d27a9b0cfa84.jpg" class="trim-mid wp-post-image" alt="" decoding="async" fetchpriority="high" data-eio="l" /></noscript> </a></div><div class="archive-desc"><div class="entry-title"><h2><a href="https://seigura.com/directory/117/" rel="bookmark" data-wpel-link="internal">青山 吉能</a></h2></div></div></div></div>