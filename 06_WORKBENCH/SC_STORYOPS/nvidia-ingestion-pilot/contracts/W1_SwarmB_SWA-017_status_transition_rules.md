# SWA-017 Contract: Status Transition Rules

## Valid Transitions
- Backlog -> Ready
- Ready -> In Progress
- In Progress -> Validation
- Validation -> Done
- Any state -> Blocked
- Blocked -> Ready

## Invalid Transitions
- Backlog -> Done (disallowed)
- In Progress -> Done (requires validation state)

## Exit Rule
- A task can move to Done only with linked validation evidence.
