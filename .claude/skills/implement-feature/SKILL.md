---
name: implement-feature
description: 既存設計を守って機能実装する
---

実装手順:

1. 影響を受ける層（route/service/repository）を列挙
2. インターフェースを先に定義
3. テストを先に作成
4. 実装
5. 副作用がないか確認

制約:

- Service は HTTP / DB を直接扱わない
- Repository 以外で外部通信禁止
