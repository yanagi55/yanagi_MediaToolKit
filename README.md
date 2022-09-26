## yanagi_MediaToolKit
---
動画とか画像とか文章とか投稿したりをワンコインサーバーでやるやつ 


### 特徴
- git pushするとgithubのコードを読んでデプロイまで全自動でやります
  - ConcourseCIで視認出来ます(たのしい)
- ビルドをローカルでやるので非力なサーバーでも負荷を抑えられます
  - 転送量は増えます クラウドでなくVPS想定
- コンテナを2つ以上配置してnginxでリバースプロキシさせ、ローリングアップデートで更新時のダウンタイムが無いです
  - ただしRDBは1つ

### 注記
- ローカルでConcourseCIとDockerレジストリを立て、その間の通信をLetsEncrypt証明書(DNS認証)で解決してます
  - DNS自体は外部
  - 認証局とDNSを自前で立てられるならきっとそっちのほうが楽です
- 本体にPythonを含むためDebian、RDBほかにAlpine使ってます

### 環境
- win10

### 履歴
- 2022.09 個人情報を削除して公開
- 2021.09-12 ざっくり開発
