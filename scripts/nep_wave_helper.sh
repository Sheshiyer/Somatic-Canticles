#!/usr/bin/env bash

if [[ -n "${ZSH_VERSION:-}" ]]; then
  setopt local_options no_unset
else
  set -u
fi

_nep_repo_root() {
  if git_root=$(git rev-parse --show-toplevel 2>/dev/null); then
    printf '%s\n' "$git_root"
  else
    pwd
  fi
}

_nep_state_dir() {
  printf '%s/.wave_runtime\n' "$(_nep_repo_root)"
}

_nep_log_dir() {
  printf '%s/logs\n' "$(_nep_state_dir)"
}

_nep_pid_dir() {
  printf '%s/pids\n' "$(_nep_state_dir)"
}

_nep_status_dir() {
  printf '%s/status\n' "$(_nep_state_dir)"
}

_nep_meta_dir() {
  printf '%s/meta\n' "$(_nep_state_dir)"
}

_nep_now() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

nep_init() {
  mkdir -p "$(_nep_log_dir)" "$(_nep_pid_dir)" "$(_nep_status_dir)" "$(_nep_meta_dir)"
}

_nep_path_log() { printf '%s/%s.log\n' "$(_nep_log_dir)" "$1"; }
_nep_path_pid() { printf '%s/%s.pid\n' "$(_nep_pid_dir)" "$1"; }
_nep_path_status() { printf '%s/%s.status\n' "$(_nep_status_dir)" "$1"; }
_nep_path_exit() { printf '%s/%s.exit\n' "$(_nep_status_dir)" "$1"; }
_nep_path_cmd() { printf '%s/%s.cmd\n' "$(_nep_meta_dir)" "$1"; }
_nep_path_started() { printf '%s/%s.started\n' "$(_nep_meta_dir)" "$1"; }
_nep_path_finished() { printf '%s/%s.finished\n' "$(_nep_meta_dir)" "$1"; }
_nep_path_runner() { printf '%s/%s.runner.sh\n' "$(_nep_meta_dir)" "$1"; }

_nep_write_status() {
  local task_id="$1"
  local value="$2"
  printf '%s\n' "$value" > "$(_nep_path_status "$task_id")"
}

_nep_read_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    tr -d '\n' < "$path"
  fi
}

_nep_pid_alive() {
  local pid="$1"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

nep_run() {
  if [[ $# -lt 2 ]]; then
    printf 'usage: nep_run <task-id> <command...>\n' >&2
    return 1
  fi

  local task_id="$1"
  shift
  local cmd="$*"

  nep_init

  local pid_file status_file exit_file log_file cmd_file started_file finished_file
  local runner_file
  pid_file="$(_nep_path_pid "$task_id")"
  status_file="$(_nep_path_status "$task_id")"
  exit_file="$(_nep_path_exit "$task_id")"
  log_file="$(_nep_path_log "$task_id")"
  cmd_file="$(_nep_path_cmd "$task_id")"
  started_file="$(_nep_path_started "$task_id")"
  finished_file="$(_nep_path_finished "$task_id")"
  runner_file="$(_nep_path_runner "$task_id")"

  if [[ -f "$pid_file" ]]; then
    local existing_pid
    existing_pid="$(_nep_read_file "$pid_file")"
    if _nep_pid_alive "$existing_pid"; then
      printf 'task %s is already running with pid %s\n' "$task_id" "$existing_pid" >&2
      return 1
    fi
  fi

  printf '%s\n' "$cmd" > "$cmd_file"
  printf '%s\n' "$(_nep_now)" > "$started_file"
  rm -f "$exit_file" "$finished_file"
  : > "$log_file"
  _nep_write_status "$task_id" "running"

  cat > "$runner_file" <<EOF
#!/usr/bin/env bash
set -u

task_id=$(printf '%q' "$task_id")
repo_root=$(printf '%q' "$(_nep_repo_root)")
status_file=$(printf '%q' "$status_file")
exit_file=$(printf '%q' "$exit_file")
finished_file=$(printf '%q' "$finished_file")
log_file=$(printf '%q' "$log_file")
cmd=$(printf '%q' "$cmd")

_nep_runner_now() {
  date '+%Y-%m-%dT%H:%M:%S%z'
}

{
  printf '[%s] task=%s status=running\n' "\$(_nep_runner_now)" "\$task_id"
  printf '[%s] cwd=%s\n' "\$(_nep_runner_now)" "\$repo_root"
  printf '[%s] cmd=%s\n' "\$(_nep_runner_now)" "\$cmd"
  cd "\$repo_root"
  bash -lc "\$cmd"
  code=\$?
  printf '%s\n' "\$code" > "\$exit_file"
  printf '%s\n' "\$(_nep_runner_now)" > "\$finished_file"
  if [[ "\$code" -eq 0 ]]; then
    printf '[%s] task=%s status=ok exit=%s\n' "\$(_nep_runner_now)" "\$task_id" "\$code"
    printf 'ok\n' > "\$status_file"
  else
    printf '[%s] task=%s status=failed exit=%s\n' "\$(_nep_runner_now)" "\$task_id" "\$code"
    printf 'failed\n' > "\$status_file"
  fi
} >> "\$log_file" 2>&1
EOF

  chmod +x "$runner_file"

  local pid
  pid="$(
    RUNNER_FILE="$runner_file" python3 - <<'PY'
import os
import subprocess
import sys

runner = os.environ["RUNNER_FILE"]
proc = subprocess.Popen(
    [runner],
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    start_new_session=True,
)
print(proc.pid)
PY
  )"
  printf '%s\n' "$pid" > "$pid_file"
  printf 'started %s pid=%s log=%s\n' "$task_id" "$pid" "$log_file"
}

nep_status() {
  nep_init
  printf '%-12s %-10s %-8s %-24s %s\n' "TASK" "STATUS" "PID" "STARTED" "EXIT"

  local found=0
  local status_file task_id status pid started exit_code pid_file
  for status_file in "$(_nep_status_dir)"/*.status; do
    [[ -e "$status_file" ]] || continue
    found=1
    task_id="$(basename "$status_file" .status)"
    status="$(_nep_read_file "$status_file")"
    pid_file="$(_nep_path_pid "$task_id")"
    pid="$(_nep_read_file "$pid_file")"
    started="$(_nep_read_file "$(_nep_path_started "$task_id")")"
    exit_code="$(_nep_read_file "$(_nep_path_exit "$task_id")")"
    if [[ "$status" == "running" ]] && ! _nep_pid_alive "$pid"; then
      status="stale"
    fi
    printf '%-12s %-10s %-8s %-24s %s\n' "$task_id" "$status" "${pid:-"-"}" "${started:-"-"}" "${exit_code:-"-"}"
  done

  if [[ "$found" -eq 0 ]]; then
    printf 'no tracked tasks yet\n'
  fi
}

nep_tail() {
  if [[ $# -lt 1 || $# -gt 2 ]]; then
    printf 'usage: nep_tail <task-id> [lines]\n' >&2
    return 1
  fi
  local task_id="$1"
  local lines="${2:-40}"
  local log_file
  log_file="$(_nep_path_log "$task_id")"
  if [[ ! -f "$log_file" ]]; then
    printf 'no log for %s\n' "$task_id" >&2
    return 1
  fi
  tail -n "$lines" "$log_file"
}

nep_failures() {
  nep_init
  local found=0
  local status_file task_id status
  for status_file in "$(_nep_status_dir)"/*.status; do
    [[ -e "$status_file" ]] || continue
    task_id="$(basename "$status_file" .status)"
    status="$(_nep_read_file "$status_file")"
    if [[ "$status" == "failed" || "$status" == "stale" ]]; then
      found=1
      printf '=== %s (%s) ===\n' "$task_id" "$status"
      nep_tail "$task_id" 20
      printf '\n'
    fi
  done
  if [[ "$found" -eq 0 ]]; then
    printf 'no failed or stale tasks\n'
  fi
}

nep_stop() {
  if [[ $# -ne 1 ]]; then
    printf 'usage: nep_stop <task-id>\n' >&2
    return 1
  fi
  local task_id="$1"
  local pid
  pid="$(_nep_read_file "$(_nep_path_pid "$task_id")")"
  if ! _nep_pid_alive "$pid"; then
    printf 'task %s is not running\n' "$task_id" >&2
    return 1
  fi
  kill "$pid"
  printf '%s\n' "$(_nep_now)" > "$(_nep_path_finished "$task_id")"
  _nep_write_status "$task_id" "stopped"
  printf 'stopped %s pid=%s\n' "$task_id" "$pid"
}

nep_monitor() {
  local interval="${1:-5}"
  while true; do
    clear
    printf '[%s] wave monitor\n\n' "$(_nep_now)"
    nep_status
    printf '\n'
    nep_failures
    sleep "$interval"
  done
}

nep_help() {
  cat <<'EOF'
Available commands:
  nep_init
  nep_run <task-id> <command...>
  nep_status
  nep_tail <task-id> [lines]
  nep_failures
  nep_stop <task-id>
  nep_monitor [interval-seconds]

Examples:
  source scripts/nep_wave_helper.sh
  nep_run NEP-003 "python3 scripts/run_repo_synthesis.py"
  nep_status
  nep_tail NEP-003 50
  nep_monitor 5
EOF
}

_nep_dispatch() {
  local cmd="${1:-help}"
  shift || true
  case "$cmd" in
    init) nep_init "$@" ;;
    run) nep_run "$@" ;;
    status) nep_status "$@" ;;
    tail) nep_tail "$@" ;;
    failures) nep_failures "$@" ;;
    stop) nep_stop "$@" ;;
    monitor) nep_monitor "$@" ;;
    help|--help|-h) nep_help ;;
    *)
      printf 'unknown command: %s\n' "$cmd" >&2
      nep_help >&2
      return 1
      ;;
  esac
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  _nep_dispatch "$@"
fi
