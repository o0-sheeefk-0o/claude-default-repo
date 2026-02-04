# Claude Code 概要と実装ガイド

## Claude Code の基本要素

Claude Code は、ターミナル上で動作するエージェント型のコーディング支援ツールであり、以下の拡張要素によって柔軟にカスタマイズできます。

- **スキル（Skills）**
- **フック（Hooks）**
- **サブエージェント（Subagents）**
- **プラグイン（Plugins）**
- **MCP（Model Context Protocol）**

これらを組み合わせることで、プロジェクト固有の開発ワークフローを自動化できます。

---

## スキル（Skills）

スキルは、プロジェクト固有の命令や振る舞いを定義する仕組みです。各スキルは以下のパスに配置します。

```
.claude/skills/<skill-name>/SKILL.md
```

`SKILL.md` には YAML フロントマターを記述し、スキル名や説明を定義します。

### スキル定義例

```md
---
name: explain-code
description: コードをわかりやすい図や日常的な類推で説明する
---

コードを説明するときは、次の要素を含めてください:

1. **日常の例え**: 動作を現実の事象に例えて説明する
2. **図解**: ASCII アートなどで構造や処理フローを示す
3. **ステップ解説**: 処理を順に追って説明する
4. **注意点**: 誤解しやすい点や落とし穴を指摘する
```

スキルは以下の方法で利用できます。

- 自動起動（Claude が文脈から判断）
- `/explain-code` のような **スラッシュコマンド**による明示的起動

---

## フック（Hooks）

フックは、Claude Code のライフサイクル上の特定イベントで、任意の処理を実行する仕組みです。

### 主なイベント例

- `SessionStart`
- `PreToolUse`
- `PostToolUse`

### 設定ファイルによるフック定義

フックは `.claude/settings.json` に JSON 形式で定義します。

#### 例：ファイル編集前に特定ファイルを保護する

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

#### Bash スクリプト例（protect-files.sh）

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
PROTECTED=(".env" ".git/")

for pat in "${PROTECTED[@]}"; do
  if [[ "$FILE_PATH" == *"$pat"* ]]; then
    echo "Blocked: $FILE_PATH" >&2
    exit 2
  fi
done

exit 0
```

この仕組みにより、`.env` や `.git/` 配下への書き込みを自動的にブロックできます。

---

## Python SDK によるフック実装例

Python SDK では、フックを関数として定義できます。

```python
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient

async def check_bash_command(input_data, tool_use_id, context):
    if input_data["tool_name"] != "Bash":
        return {}

    cmd = input_data["tool_input"].get("command", "")
    if "foo.sh" in cmd:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"コマンドに無効なパターンが含まれています: {cmd}"
            }
        }
    return {}
```

条件に応じてツール実行を許可・拒否できます。

---

## サブエージェント（Subagents）

サブエージェントは、特定タスクに特化した独立エージェントです。

### 特徴

- 独立したコンテキスト（プロンプト）
- 使用可能ツールの制限
- 権限・役割の明確化

### 例

- **探索用エージェント**: コード検索専用（読み取り専用）
- **実装用エージェント**: 編集・テスト実行可能

### 定義場所

```
.claude/agents/<agent-name>.md
```

Claude はタスク内容に応じてサブエージェントへ自動委譲（delegation）し、並列処理やコンテキスト分離を行います。

---

## Python / Node.js アプリへの組み込み

Claude Code は CLI ツールですが、公式エージェント SDK によりアプリケーションから直接利用できます。

### Python 例

```bash
pip install claude-agent-sdk
```

```python
import anyio
from claude_agent_sdk import query

async def main():
    async for message in query(prompt="2+2 を計算して"):
        print(message)

anyio.run(main)
```

### Node.js 例

```bash
npm install @anthropic-ai/claude-agent-sdk
```

TypeScript / JavaScript から非対話的に Claude Code を操作できます。

### CLI 実行例

```bash
claude -p "..." --output-format json
```

JSON 出力をパースして後続処理に利用できます。

---

## MCP（Model Context Protocol）連携

MCP を利用すると、外部ツールやデータソースと連携できます。

### 連携例

- GitHub / JIRA
- PostgreSQL
- Sentry
- Slack
- Figma

#### ユースケース例

- JIRA チケットに基づく実装と PR 作成
- Sentry ログの解析
- DB 検索によるユーザー情報取得

---

## 出力スタイル（Output Styles）

- `--output-format json`
- `--json-schema`

これらを使うことで、構造化された出力を取得し、プログラム処理しやすくできます。

---

## 並列実行とパイプライン連携

### 並列実行

```bash
claude -p "task A" &
claude -p "task B" &
```

- `/tasks` でタスク一覧管理
- 実行中セッションへの再接続（テレポート）可能

### Unix パイプライン連携例

```bash
tail -f app.log | claude -p "ログに異常が出たら Slack 通知して"
```

CI/CD や既存ツールと容易に統合できます。

---

## セッション開始時のコンテキスト注入

### CLAUDE.md

- プロジェクトルートに配置
- 新規セッション開始時に自動読み込み
- 開発方針・コーディング規約を記述

### フック（SessionStart）

- 会話途中のコンテキスト再注入
- コンパクション後の情報補完に有効

---

## 推奨される開発スタイル

- 初期段階でディレクトリ構成と設計ドキュメントを用意
- タスクを小さく分割し、目的を明確に指示
- 役割ごとにスキル・サブエージェントを分離
- フックや SDK でテスト・整形・セキュリティを強制

CI パイプライン的な仕組みとして Claude Code を組み込むと効果的です。

---

## まとめ

Claude Code は以下の要素を組み合わせて利用します。

- スキル（SKILL.md）
- フック（settings.json / SDK）
- サブエージェント
- プラグイン
- MCP

Python / Node.js SDK により、アプリケーション内部への組み込みも可能です。公式ドキュメントやサンプルを参照しつつ、実践的に使いこなすことが推奨されます。

---

## 参考資料

- Claude Code 公式ドキュメント
- Claude Agent SDK リファレンス
