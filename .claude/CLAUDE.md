# プロジェクト概要

- Web API サーバ
- クリーンアーキテクチャを意識
- Controller → Service → Repository の依存方向を厳守

# 技術スタック

- Node.js + Express（または FastAPI）
- DB アクセスは Repository に限定

# コーディング規約

- Service で HTTP に依存しない
- Repository は副作用を隠蔽する
- テストしやすさ優先

# Claude への指示

- 既存設計を壊さない
- 変更前に必ず影響範囲を列挙
- 勝手にディレクトリ構造を変えない
