# Open-Source Readiness Checklist

Use this checklist to review a project before a public release. It is a planning guide, not blanket permission to make every change. Respect the safety boundaries in [safety-boundaries.md](safety-boundaries.md).

## Repository and security

- [ ] Remove exposed credentials from active files and rotate them; plan historical cleanup separately if needed.
- [ ] Remove oversized or generated files from version control where appropriate.
- [ ] Add safeguards against committing secrets and build artifacts.
- [ ] Make the commit history understandable; coordinate before rewriting shared history.
- [ ] Remove clearly unused code and obsolete temporary files.
- [ ] Resolve or document CI failures; consider a main-branch status badge.
- [ ] Prepare a release if the project uses versioned releases.
- [ ] Address evidenced security alerts and provide a private vulnerability-reporting path.
- [ ] Review dependencies and consider automated update tooling.

## Project information and contributor experience

- [ ] Add a license after the owner chooses one.
- [ ] Make the README explain the problem, solution, setup, and links to deeper resources.
- [ ] Add contribution instructions and a code of conduct.
- [ ] Document installation, running, debugging, testing, building, deployment, and troubleshooting.
- [ ] Link a public API collection when relevant.
- [ ] Add issue templates that match the project's support needs.
- [ ] Follow the documentation from a clean environment when the user requests verification.

## Sharing and launch

- [ ] Ask relevant peers or target users for direct feedback.
- [ ] Share in communities where target users already gather, following their rules.
- [ ] Recognize the work involved in releasing and maintaining the project.

Keep launch promotion and outreach separate from repository edits. Do not contact people or publish announcements unless the user requests it.
