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
