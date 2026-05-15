# GitHub Issue Seed Instructions (SWA)

This file pairs with `swa_issue_payloads.json` for bulk issue creation.

## Suggested command pattern

```bash
jq -c '.[]' 06_WORKBENCH/SC_STORYOPS/nvidia-ingestion-pilot/swa_issue_payloads.json | while read -r item; do
  title=$(echo "$item" | jq -r '.title')
  body=$(echo "$item" | jq -r '.body')
  labels=$(echo "$item" | jq -r '.labels | join(",")')
  gh issue create --title "$title" --body "$body" --label "$labels"
done
```

## Notes
- Review labels/milestones before execution.
- Run on the target repository root with authenticated `gh`.
- Dependencies should be cross-linked after issue numbers are created.
