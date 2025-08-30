# codex_trial

このリポジトリには、**guess_number.py** という簡単な Python アプリケーションが含まれています。

このプログラムは 1 から 20 の間でランダムな数を選び、ユーザーが正しい数を入力するまで繰り返し推測させます。

実行するには次のコマンドを使用します:

```bash
python guess_number.py
```

## Status

This game is now complete and ready for you to play. Enjoy guessing!

## Web UI
ブラウザで `index.html` を開くと、モデル評価の一覧が表示されます。初回ロード時には「サンプルモデル」が読み込まれ、評価データはブラウザの LocalStorage に保存されます。

主な機能:

- ✅ 規格タグ (GDPR/ISO/NIST/OSS/SLSA) によるフィルター
- ✅ 右上の「管理者ログイン」からのダッシュボードアクセス (ID: `admin` / PW: `0000`)
- ✅ ダッシュボードでのモデル追加・評価ステータス更新
- ✅ ヘッダーのボタンで日本語/英語の切り替え

モデル名を入力して「リサーチ登録」を押すと、ChatGPT Deep Research API を通じて各評価項目の情報を収集し、状態を自動入力します。

ローカルで動作させるには OpenAI API キーを環境変数 `OPENAI_API_KEY` に設定し、次のコマンドでサーバーを起動して `http://localhost:8000/index.html` を開きます:

```bash
OPENAI_API_KEY=<your key> node server.js
```
