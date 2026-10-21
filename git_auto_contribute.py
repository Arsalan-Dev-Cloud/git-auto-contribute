
import subprocess
import sys
from pathlib import Path


def run_git(*args):
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def stop(message):
    print(f"\nSTOP: {message}")
    sys.exit(1)


def get_repo_root():
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        stop("Run this script inside a Git repository.")

    return Path(result.stdout.strip()).resolve()


def get_changes():
    result = run_git(
        "status", "--porcelain=v1", "-z",
        "--untracked-files=all"
    )

    if result.returncode != 0:
        stop("Could not read Git status.")

    changes = []

    for entry in result.stdout.split("\0"):
        if not entry:
            continue

        if len(entry) < 4 or entry[2] != " ":
            stop("Unexpected Git status format.")

        status = entry[:2]
        path = entry[3:]

        # Rename/copy entries contain a second path in -z format.
        if "R" in status or "C" in status:
            stop(
                f"Rename/copy detected for {path}. "
                "Handle renames manually before running."
            )

        if (
            "U" in status
            or status in {"AA", "DD"}
        ):
            stop(f"Resolve merge conflict first: {path}")

        changes.append((path, status))

    return changes


def is_sensitive(path):
    parts = path.replace("\\", "/").lower().split("/")
    filename = parts[-1]

    if filename.startswith(".env") and filename not in {
        ".env.example", ".env.sample", ".env.template"
    }:
        return True

    if filename in {
        "id_rsa", "id_ed25519",
        "credentials.json", "secrets.json"
    }:
        return True

    if Path(filename).suffix in {
        ".pem", ".key", ".p12", ".pfx"
    }:
        return True

    return any(
        word in part
        for part in parts
        for word in ("secret", "password", "credential", "token")
    )


def make_message(path, status):
    filename = Path(path.replace("\\", "/")).name

    if "D" in status:
        return f"Delete {filename}"

    if status == "??":
        return f"Add {filename}"

    return f"Update {filename}"


def ensure_clean_index():
    result = run_git("diff", "--cached", "--quiet")

    if result.returncode == 1:
        stop(
            "Staged changes already exist. Commit or unstage them "
            "manually before running this automation."
        )

    if result.returncode != 0:
        stop("Could not verify the staging area.")


def main():
    print("=" * 60)
    print("     FULLY AUTOMATED GIT CONTRIBUTION TOOL")
    print("=" * 60)
    print(f"Repository: {REPO_ROOT}")

    branch = run_git("branch", "--show-current")

    if branch.returncode != 0 or not branch.stdout.strip():
        stop("Checkout a normal branch before running.")

    upstream = run_git(
        "rev-parse", "--abbrev-ref",
        "--symbolic-full-name", "@{upstream}"
    )

    if upstream.returncode != 0:
        stop(
            "Current branch has no upstream. Configure its "
            "remote tracking branch before running."
        )

    ensure_clean_index()

    # Avoid silently processing files while a merge is in progress.
    merge_head = run_git("rev-parse", "-q", "--verify", "MERGE_HEAD")

    if merge_head.returncode == 0:
        stop("A merge is in progress. Finish it manually first.")

    print(f"Branch: {branch.stdout.strip()}")
    print(f"Upstream: {upstream.stdout.strip()}")
    print("\nStarting automatic file-by-file commits and pushes...")

    processed = set()
    success_count = 0

    while True:
        changes = get_changes()

        # Skip paths already successfully processed this run.
        pending = [
            (path, status)
            for path, status in changes
            if path not in processed
        ]

        if not pending:
            break

        path, status = pending[0]

        print("\n" + "-" * 60)
        print(f"File: {path}")
        print(f"Status: {status}")

        if is_sensitive(path):
            stop(
                f"Potentially sensitive filename detected: {path}. "
                "Review it manually before committing."
            )

        message = make_message(path, status)
        print(f"Commit message: {message}")

        # Confirm the index is still empty before staging.
        ensure_clean_index()

        # Stage exactly one path. -- safely handles leading dashes.
        result = run_git("add", "-A", "--", path)

        if result.returncode != 0:
            print(result.stderr)
            stop(f"Could not stage {path}.")

        # Verify that only the selected path is staged.
        staged = run_git("diff", "--cached", "--name-only", "-z")

        if staged.returncode != 0:
            stop("Could not verify staged paths.")

        staged_paths = [
            p for p in staged.stdout.split("\0") if p
        ]

        if staged_paths != [path]:
            stop(
                "Staged paths do not match the selected file. "
                "No commit or push attempted; inspect Git status."
            )

        result = run_git("commit", "-m", message, "--", path)

        if result.returncode != 0:
            print(result.stderr)
            stop(
                f"Commit failed for {path}. Inspect Git status "
                "before continuing."
            )

        print(f"Committed: {message}")

        result = run_git("push")

        if result.returncode != 0:
            print(result.stderr)
            stop(
                f"Push failed after committing {path}. "
                "Fix the issue and run 'git push' manually. "
                "Do not recreate the commit."
            )

        print(f"Pushed successfully: {path}")

        processed.add(path)
        success_count += 1

    print("\n" + "=" * 60)
    print("AUTOMATION COMPLETE")
    print(f"Files committed and pushed: {success_count}")
    print("=" * 60)


if __name__ == "__main__":
    REPO_ROOT = get_repo_root()

    if not Path.cwd().resolve().is_relative_to(REPO_ROOT):
        stop("Run this script from inside the repository.")

    main()