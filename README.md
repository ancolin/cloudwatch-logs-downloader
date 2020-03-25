# cloudwatch-logs-downloader
CloudWatch Logs のログをダウンロードするツール.  
Python で直接実行しても良いし, docker 経由で実行しても良い.

# dependencies
## Python で直接実行する場合
* Python 3.6.8
* その他
    * [requirements](requirements) 参照
## Docker で実行する場合
* Docker
    * Windows の場合 Docker Desktop for Windows でも可
* docker-compose

# 実行方法
## Docker で実行する場合
1. AWS の認証情報を設定する（初回のみ）
    ~~~bash
    $ docker-compose run --rm app aws configure
    ~~~
1. ログをダウンロードする（JSON 形式の場合）
    * JSON 形式の場合
        ~~~bash
        $ docker-compose run --rm app python downloadLogs.py ロググループ名 ログストリーム名 リージョン
        ~~~
    * CSV 形式の場合
        ~~~bash
        $ docker-compose run --rm app python downloadLogs.py ロググループ名 ログストリーム名 リージョン csv
        ~~~
      