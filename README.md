 # シンプルFastAPIテンプレート

- API開発のベースとなるシンプルなFastAPIのテンプレートを作成しました
- 随時アップデート予定です

---

## 実行手順

- Dockerコンテナを作成・起動

    ```shell
    docker compose -f compose.yml -f compose.test.yml up -d
    ```
  
- DBマイグレーションを実行

    ```shell
    make db_upgrade
    ```

- Swagger UIを表示

    [http://localhost:8000/docs](http://localhost:8000/docs)
