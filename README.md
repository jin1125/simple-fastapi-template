 # シンプルFastAPIテンプレート

- API開発のベースとなるシンプルなFastAPIのテンプレートを作成しました
- 随時アップデート予定です

---

## 環境構築

- `.env.example`ファイルをコピーして`.env`ファイルを作成

- 必要に応じて`.env`の定義を変更

- Dockerコンテナを作成・起動

    ```commandline
    docker compose -f compose.yml -f compose.test.yml up -d
    ```

- `app`と`db`と`test_db`のコンテナが起動していることを確認

    ```commandline
    docker compose ps
    ```

- DBマイグレーションを実行

    ```commandline
    make db_upgrade
    ```

- APIドキュメントを表示
  
  http://localhost:8000/docs など
