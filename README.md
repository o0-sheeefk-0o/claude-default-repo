# Claude Code チーム運用テンプレート

このリポジトリは、チームで Claude Code を安全・一貫に使うための設定テンプレートです。

---

## このリポジトリの構成

```
.claude/
├── CLAUDE.md              # Claude への共通指示（チーム合意文書）
├── rules/                 # 追加ルール（自動読み込み）
│   ├── testing.md
│   └── frontend/
├── commands/              # スラッシュコマンド定義
│   ├── commit.md          # コミット作成
│   ├── explain-project.md # プロジェクト概要説明
│   └── update-readme.md   # README 更新
├── skills/                # スキル定義
│   ├── design-review/
│   ├── implement-feature/
│   └── generate-tests/
├── agents/                # サブエージェント定義
│   ├── architect.md
│   ├── implementer.md
│   └── reviewer.md
├── hooks/                 # 自動実行スクリプト
│   ├── protect-files.sh   # 危険ファイル保護
│   └── run-tests.sh       # 自動テスト実行
├── settings.json          # フック・権限設定
└── settings.local.json    # 個人設定（git 管理外推奨）
```

---

## 日常の使い方

### スキル・コマンド（スラッシュコマンド）

定義済みのスキルとコマンドを呼び出して、作業を標準化します。

```shell
# スキル（設計・実装・テスト支援）
/implement-feature ユーザー登録APIを追加したい
/design-review この Service 設計どう？
/generate-tests この Service クラスのテストを書いて

# コマンド（ワークフロー自動化）
/explain-project
/commit
/update-readme
```

### サブエージェント

役割を分離して Claude に委譲します。

```shell
@architect この機能の設計を考えて
@implementer この設計を元に実装して
@reviewer この変更をレビューして
```

---

## チーム運用の大原則

**Claude Code は「自由に使わせない」方がうまく回る**

- 人によって使い方がブレる
- Claude の裁量が大きすぎる
- レビュー地獄になる

➡︎ 「Claude がやっていいこと／ダメなこと」を先に固定する

---

## 設定ファイルの役割と運用ルール

### CLAUDE.md ― チームの合意文書

`.claude/CLAUDE.md` は Claude への指示であり、チームメンバーへの規約でもあります。

**変更する場合は PR + チーム合意が必要。**

### スキル・コマンド ― チーム標準を固定する

勝手に追加・変更しない。追加したい場合は PR + 合意を取る。

**スキル（`skills/`）**

| スキル | 用途 |
|--------|------|
| `implement-feature` | 既存設計を守って機能実装 |
| `design-review` | 設計の破綻をレビュー |
| `generate-tests` | 既存コードから網羅的なテストを生成 |

**コマンド（`commands/`）**

| コマンド | 用途 |
|----------|------|
| `commit` | チーム規約に沿ったコミットメッセージを作成してコミット |
| `explain-project` | プロジェクトの概要・アーキテクチャ・規約を説明 |
| `update-readme` | プロジェクトの実態を調査して README を同期 |

### サブエージェント ― 役割を固定して使う

| エージェント | できること | できないこと |
|---|---|---|
| `architect` | 設計のみ | コードを書く |
| `implementer` | TODO 消化・実装 | 設計変更 |
| `reviewer` | バグ・責務違反の指摘 | 実装 |

### Hooks ― ルール違反を物理的に止める

設定済みの hooks：

- **protect-files.sh**：`.env` など危険ファイルへの書き込みをブロック
- **run-tests.sh**：コード変更後にテストを自動実行

新しい hooks を追加する場合も PR + 合意が必要。

---

## PR レビュー時の役割分担

| 人間が見る | Claude に任せる |
|---|---|
| 設計・責務・境界 | コード量・網羅性 |
| 将来の変更耐性 | テスト・ドキュメント |

「Claude が書いたから OK」はしない。設計判断は必ず人間が行う。

---

## チーム導入ステップ

| フェーズ | やること |
|---|---|
| 1 | 個人で使い始め、テンプレ repo を fork |
| 2 | 小さい機能だけ Claude に任せ、スキル 2〜3 個を試す |
| 3 | PR 作成まで自動化・hooks を導入 |
| 4 | チーム標準として定着させる |

---

## まとめ

- Claude Code は **権限を絞るほど強い**
- `CLAUDE.md` → スキル → エージェント → hooks の順に整備する
- 「自由に使わせない」が成功の鍵
- 人間の役割は **設計と最終判断**
