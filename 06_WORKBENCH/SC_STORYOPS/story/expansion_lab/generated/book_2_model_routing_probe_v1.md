# Book 2 Model Routing Probe v1

Date: 2026-05-14

Purpose: prevent Book 2 expansion from repeating the Book 1 failure modes where slow/default prose routes compressed accepted text, copied base paragraphs, or stalled without useful monitor output.

## Route Decision

- Book 2 draft route: `qwen/qwen3.5-122b-a10b`
- Book 2 control route: `openai/gpt-oss-120b`
- Kimi and MiniMax routes: opt-in only after a fresh probe
- Mistral Large route: opt-in slow lane only after Chapter 09 Stage 1 produced no artifact within the smoke threshold

## Probe Notes

| Model | Probe result | Book 2 status |
| --- | --- | --- |
| `openai/gpt-oss-120b` | Fast and callable; best current control/repair route | default control |
| `qwen/qwen3.5-122b-a10b` | Re-probe returned in `4.8s` with a usable Book 2 sample after client support for `reasoning_content` extraction | default draft |
| `mistralai/mistral-large-3-675b-instruct-2512` | Callable on a small probe, but Chapter 09 Stage 1 produced no artifact after several minutes and was stopped | opt-in slow lane only |
| `mistralai/mistral-medium-3.5-128b` | Callable but generic and less chapter-specific | fallback only |
| `mistralai/mistral-large` | Listed, but account call returned `404 Function not found for account` | unavailable |
| `mistralai/mistral-large-2-instruct` | Listed, but account call returned `404 Function not found for account` | unavailable |
| `mistralai/mistral-small-4-119b-2603` | Timed out on a small probe | not a default route |
| `qwen/qwen3-next-80b-a3b-instruct` | Fast but drifted toward generic lab/CRISPR language | diagnostic fallback only |
| `nvidia/llama-3.3-nemotron-super-49b-v1.5` | Callable, but returned reasoning-only content shape during probe | diagnostic fallback only after client extraction support |
| `meta/llama-4-maverick-17b-128e-instruct` | Callable, but generic portal/cosmos sample drifted away from project voice | not a prose authority |
| `minimaxai/minimax-m2.7` | Timed out on a small probe | not a default route |
| `moonshotai/kimi-k2.6` | Timed out on a small probe; Book 1 showed compression/copy-repeat behavior | not a default route |
| `z-ai/glm-5.1` | Timed out on a small probe | not a default route |
| `deepseek-ai/deepseek-v4-flash` | Timed out on a small probe | not a default route |
| `deepseek-ai/deepseek-v4-pro` | Timed out on a small probe | not a default route |
| `writer/palmyra-creative-122b` | Listed by `/models`, but account call returned `404 Function not found for account` | unavailable |

## Runner Implications

- The runner must honor `control_pass` as well as legacy `control_model`.
- Listed model availability is not enough; a route must pass a small callable probe before becoming a default.
- Pending NVIDIA `202` polling must respect the caller timeout so monitor visibility remains trustworthy.
- Additive insert-first growth is now the default from Stage 1; full-chapter rewrites are too slow and too risky for accepted-baseline expansion.
