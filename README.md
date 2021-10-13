# Instagram_scraper

Seleniumを利用して、instagramの画像を保存するコードです

# 特徴
自分の画像だけではなく、他人が上げている画像も保存することが出来ます    

相互フォローしていれば、鍵アカウントの画像を保存することも出来ます

# 工夫した点
インスタグラムやTwitterなどのサイトは、スクロールすると次の投稿が読み込まれる、非同期コンテンツである。なので、最初の状態のままだと画面の中に表示されている分しかスクレイピングすることができない。  
そのため、課題を解決するために、自動で画面をスクロールしてくれる処理を実装した。


# 注意点
※取得した画像は個人利用までに留めて置いてください    

ログインしてからスクレイピングする仕様になっているので、捨てアカウントを利用してください

