PlaywrightとJavaScriptを用いて、以下のWebサイトからすべての顔写真をダウンロードするソースコードを提案してください。1ページ目に掲載されている顔写真を保存し終わったら2ページ目、2ページ目が終わったら3ページ目と、最後のページまで連続処理をしてください。

＜対象＞
1ページ目： https://seigura.com/directory/
2ページ目以降： https://seigura.com/directory/page/#PAGE#/ （#PAGE#は、2～60までの整数が入る）
各ページには、最大30枚の顔写真が掲載されている。https://seigura.com/wp-content/uploads/からはじまるURLに格納されている画像ファイルを、ローカルに保存する。