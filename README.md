## Introduction

Yet another code sandbox for agent RL training ... but in jupyter notebook style.
- Like jupyter notebook, user can execute multiple code blocks in the same session. All functions and variables are automatically stored after code execution.
- Like jupyter notebook, when calling `plt.show` in the code block, a base64 format image will be returned via `image` field.
- Like jupyter notebook, if the last line of code has no left value, the right value will be returned via `result` field.
- While there is no docker or any other vitualization, to ensure safety, all code executions are guarded by HumanEval safe prefix.

Usage:

Step 1: Start a redis server, change the redis host, port, and password based on your redis.conf

Step 2: Start serving
```bash
python fast_api_server.py
```
