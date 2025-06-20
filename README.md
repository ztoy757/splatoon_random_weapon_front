# Splatoon3 Random Weapon Generator

Splatoon3の武器をランダムに選択するStreamlitアプリケーションです。

## 機能

- 🎲 ランダムに武器を1〜18個選択
- 🦑 美しいカードレイアウトで武器情報を表示
- 📊 選択された武器の統計情報表示
- 🎨 カテゴリーごとの色分け
- 🔄 MockoonによるAPI代替機能

## 開発環境構築

### Devcontainerを使用（推奨）

1. VSCodeでプロジェクトを開く
2. Command Palette (`Ctrl+Shift+P`) で "Dev Containers: Reopen in Container" を実行
3. コンテナビルド完了後、Streamlitアプリを起動

### 手動セットアップ

```bash
# 依存関係インストール
pip install -r requirements.txt

# Streamlitアプリ起動
streamlit run streamlit_app.py
```

## 使用方法

### Streamlitアプリケーション

1. ブラウザで `http://localhost:8501` にアクセス
2. スライダーで選択する武器数を設定（1〜18個）
3. 「🎲 ランダム武器を生成」ボタンをクリック
4. 選択された武器がカード形式で表示されます

### MockoonによるAPI代替

MockoonはバックエンドAPIの代替として動作します：

- **ポート**: 3001
- **エンドポイント**:
  - `GET /` - ヘルスチェック
  - `GET /health` - サービス状態確認
  - `GET /random-weapon` - ランダム武器取得

### 利用可能なポート

- **3000**: Mockoon API
- **8000**: FastAPI（将来の拡張用）
- **8501**: Streamlit アプリケーション

## 武器データ

18種類のSplatoon3武器データを含んでいます：

- **シューター系**: スプラシューター、プライムシューター、52ガロンなど
- **チャージャー系**: スプラチャージャー、リッター4Kなど
- **ローラー系**: カーボンローラー、スプラローラーなど
- **その他**: フデ、スピナー、マニューバー、スロッシャー、シェルター、ストリンガー、ワイパー

各武器には以下の情報が含まれます：
- 武器名
- カテゴリー
- サブウェポン
- スペシャルウェポン

## ファイル構成

```
.devcontainer/
├── devcontainer.json      # VSCode devcontainer設定
├── docker-compose.yml     # コンテナオーケストレーション
├── Dockerfile            # 開発環境イメージ
└── mockoon/
    └── mockoon-config.json # MockoonAPI設定

streamlit_app.py          # メインアプリケーション
requirements.txt          # Python依存関係
README.md                # このファイル
```

## CI/CD

GitHub Actionsを使用した自動化：

- **コード品質チェック**: Black（フォーマット）、isort（インポート整理）
- **テスト実行**: pytest
- **コードレビュー**: Claude AIによる自動レビュー（日本語）

### コマンド

```bash
# コードフォーマット
black .

# インポート順序整理  
isort .

# 両方を一度に実行
black . && isort .
```

### セットアップ

1. GitHubリポジトリの Settings > Secrets で `ANTHROPIC_API_KEY` を設定
2. PRを作成すると自動的にテストとレビューが実行されます

## 技術スタック

- **Python**: 3.11
- **Streamlit**: 1.28.1
- **Mockoon**: API モック
- **Docker**: 開発環境
- **VSCode DevContainers**: 統合開発環境
- **GitHub Actions**: CI/CD
- **Claude AI**: 自動コードレビュー