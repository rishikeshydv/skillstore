# Safety Boundaries

Routine cleanup permits focused, reversible edits. Treat actions that can disrupt collaborators, invalidate credentials, delete user data, change access, or publish externally as separate owner decisions.

## Do not do these as routine cleanup

- Rewrite Git history, force-push, delete branches, or strip blobs from history.
- Delete files or assets whose purpose is uncertain.
- Rotate or revoke credentials, change repository permissions or security settings, enable services, publish a release, or make the repository public.
- Contact people, post announcements, or promote the project.

Explain the risk and what decision or authorization is needed before proceeding with these actions.

## If you find a suspected secret

- Do not reproduce the value in output, logs, or a command line.
- Identify the affected file or history location with the value redacted.
- Advise the owner to revoke or rotate the credential promptly. Removing a secret from a file or Git history does not make a leaked credential safe.
- Do not rewrite history. If the owner wants historical removal, describe options such as BFG Repo-Cleaner or `git filter-repo` and explain that a coordinated force-push may disrupt collaborators.

## If you find large or generated files

First determine whether the file is expected project content, a required fixture, or generated output. Recommend an ignore rule or history cleanup when appropriate, but do not delete uncertain content or rewrite history automatically.
