# エンドツーエンドテスト

このディレクトリには、Splatoon武器ジェネレーター用のPlaywrightベースのエンドツーエンドテストが含まれています。

## 前提条件

1. 依存関係をインストール: `pip install -r requirements.txt`
2. Playwrightブラウザをインストール: `python -m playwright install`
3. アプリケーションを起動: `streamlit run app.py` （またはメインアプリファイル）

## テストの実行

### 全てのe2eテストを実行
```bash
pytest tests/e2e/
```

### 表示可能なブラウザで実行（デバッグ用）
```bash
HEADLESS=false pytest tests/e2e/
```

### 異なるURLに対して実行
```bash
MOCKOON_API_URL=http://localhost:3000 pytest tests/e2e/
```

## 環境変数

- `MOCKOON_API_URL`: アプリケーションURL（優先）
- `BASE_URL`: アプリケーションURL（フォールバック、デフォルト: http://localhost:8501）
- `HEADLESS`: ブラウザヘッドレスモード（デフォルト: true）

## テスト証跡

テスト実行中にスクリーンショットが自動的に `evidence/` ディレクトリに保存されます。