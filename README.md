## 使い方

### スキルの使い方

```shell
/implement-feature ユーザー登録APIを追加したい
/design-review この Service 設計どう？
/generate-tests この Service クラスのテストを書いて
```

### サブエージェントの使い方

```shell
@architect
この機能の設計を考えて

@implementer
この設計を元に実装して

@reviewer
この変更をレビューして
```

## チーム開発で Claude Code を使うときの大原則

**Claude Code は「自由に使わせない」方がうまく回る**

理由は単純で、

- 人によって使い方がブレる
- Claude の裁量が大きすぎる
- レビュー地獄になる

なので「Claude がやっていいこと／ダメなこと」を先に固定します。

---

### ① チーム共通ルール（CLAUDE.md）

**これは「人間の合意文書」**

`.claude/CLAUDE.md` は Claude向けでもあり、チームメンバー向けでもあるのが重要。

最小構成（実務向け）

```md
# Claude Code 利用ルール

## Claude に許可する作業

- 既存設計に沿った実装
- テストコードの作成
- ドキュメント作成
- リファクタ提案（実行は人間判断）

## Claude に禁止する作業

- ディレクトリ構成の変更
- アーキテクチャ変更
- 依存ライブラリ追加
- DBスキーマ変更

## 実装ルール

- Controller → Service → Repository を厳守
- Service は HTTP / DB に依存しない
- Repository 以外で副作用禁止
```

**効果**

- 新人もベテランも同じ前提
- 「Claudeが勝手にやった」が消える
- レビュー基準が揃う

---

### ② チームで使う skills を固定する

**なぜ「勝手に skill 作らせない」？**

自由にすると：

- 変な skill が増える
- 何を使えばいいか分からない
- 再現性が死ぬ

➡︎ チーム公式 skill だけ使う

#### チーム標準 skill セット（現実解）

```text
.claude/skills/
├─ design-review/
├─ implement-feature/
├─ generate-tests/
├─ refactor/
└─ create-pr/
```

**ルール**

- skill は 勝手に追加しない
- 追加したい場合は PR + 合意
- SKILL.md はレビュー対象

#### 例：implement-feature をチーム仕様にする

```md
制約:

- 既存 public API を変更しない
- ログ出力を勝手に増やさない
- エラーハンドリング方針を守る
```

➡︎ 全員に毎回言わなくてよくなる

---

### ③ agents を「役割固定」で使う

**チーム利用で一番効くポイント**

> Claude を一人の天才にしない

代わりに：

- architect（設計）
- implementer（実装）
- reviewer（レビュー）

に分ける。

#### チームルール例

- architect
  - 設計だけ
  - コード禁止
- implementer
  - 設計変更禁止
  - TODO 消化専用
- reviewer
  - バグ・責務違反指摘のみ
  - 実装しない

➡︎ 人間の分業をそのまま AI に写す

#### 実際の使い方

```shell
@architect この機能の設計を考えて
```

```shell
@implementer この設計を元に実装して
```

```shell
@reviewer この変更をレビューして
```

---

### ④ hooks で「ルール違反を物理的に止める」

**チーム開発で hooks は必須**

理由：

- ルールは守られない
- Claude も人もミスる

➡︎ 止めるしかない

#### 最低限入れる hooks

1. 危険ファイル保護（必須）

   ```
   .env
   package-lock.json
   pyproject.toml
   migration/
   ```

   ➡︎ Claude が触れたら即ブロック

1. 自動テスト実行（推奨）

   Claude がコード書いたら
   - テスト走らせる
   - 落ちたら警告

   これで
   「Claude が書いたけど動かない」が消える

---

### ⑤ PR レビュー時のチームルール

#### やってはいけないこと

- Claude が書いたから OK
- 人が全部読むの放棄

#### 正しいレビュー観点

**人間が見るところ**

- 設計
- 責務
- 境界
- 将来変更耐性

**Claude に任せるところ**

- コード量
- テスト網羅
- ドキュメント

➡︎ 役割分担を明確にする

---

### ⑥ チーム導入の段階的ステップ（超重要）

#### 一気に入れない

- フェーズ1
  - 個人で Claude Code
  - テンプレ repo 作る

- フェーズ2
  - 小さい機能だけ Claude
  - skill 2〜3 個

- フェーズ3
  - PR 作成まで自動化
  - hooks 導入

- フェーズ4
  - チーム標準化

### まとめ（これだけ覚えて）

- Claude Code は 権限を絞るほど強い
- rules → skills → agents → hooks の順
- 「自由に使わせない」が成功の鍵
- 人間の役割は 設計と最終判断
