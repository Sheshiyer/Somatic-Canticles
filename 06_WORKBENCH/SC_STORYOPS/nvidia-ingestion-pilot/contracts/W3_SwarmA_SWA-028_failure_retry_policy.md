# SWA-028 Contract: Failure and Retry Policy

## Retry Classes
- Transient API/network errors: retry with backoff
- Deterministic schema errors: no retry, fix data
- Hard validation failures: reroute to control lane

## Retry Limits
- Max transient retries: 3
- Max reroute attempts per batch: 1

## Logging
- Every retry event records cause, attempt number, and outcome.
