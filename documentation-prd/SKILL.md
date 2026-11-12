---
name: documentation-prd
description: Write, improve, or audit a repository's documentation — README, CONTRIBUTING, RELEASING, CHANGELOG, SECURITY, code of conduct, issue/PR templates, per-package READMEs and agent docs (AGENTS.md, CLAUDE.md). Use this whenever the user wants to document a repo, set up or fix project docs, review how well a repo is documented, prepare a project for open source or outside contributors, or write release/contributor guides, even if they only name one file.
---

# Documentation PRD

Produce documentation a newcomer can act on without asking anyone. The section guides below follow what amplication/amplication does well (clear routing, copy-paste setup, explicit conventions). The verify checklist catches the mistakes it makes (broken step numbering, stale links, docs that contradict each other).

## Workflow

1. **Read the repo before writing.** Clone it if you can. Collect the facts the docs will reference:
   - Manifests (package.json, pyproject.toml, go.mod, Cargo.toml...): name, version, runtime versions (`engines`, `requires-python`), scripts
   - Default branch and any integration branch (`next`, `develop`)
   - CI and release workflows in `.github/workflows/`, and release tooling (semantic-release, changesets, release-please, build/twine, goreleaser)
   - Lint, test and hook config (eslint, prettier, ruff, husky, pre-commit, commitlint)
   - Issue and PR templates in `.github/`, with exact filenames
   - License files, devcontainer/Codespaces config, docker-compose, docs site config (mkdocs.yml, docusaurus)
   - Existing docs, the package/app folders, and agent docs (CLAUDE.md, AGENTS.md, .github/copilot-instructions.md)
   - Logo or brand assets (look in `docs/`, `assets/`, `.github/`, `public/`)
2. **Decide which docs this repo needs** (table below).
3. **Write or update each doc** using the section guides. Update existing docs in place and keep whatever is still accurate.
4. **Verify** with the checklist at the end.
5. **Report** the files created or changed (one line each), plus every `TODO(docs):` left and what information it needs.

Never invent facts. If something can't be found in the repo (review time, CLA, support channel), write `TODO(docs): <what's needed>` instead of guessing, and list it in the report. A wrong command or a dead link costs a newcomer more than a visible gap does.

## Which docs a repo needs

| Repo | Needs |
|---|---|
| Any repo | README, LICENSE |
| Accepts outside contributions | + CONTRIBUTING, CODE_OF_CONDUCT, issue and PR templates |
| Publishes releases (package, image, app) | + RELEASING, CHANGELOG |
| Public, or handles user data or credentials | + SECURITY |
| Monorepo or multiple apps | + a README per package/app |
| Worked on with AI coding agents, or already has agent docs | + AGENTS.md (and CLAUDE.md if Claude Code is used) |
| Has an external docs site | README still covers install and a first example on its own; deeper content links out |

Scale depth to project size. A solo library's CONTRIBUTING can be 20 lines; don't pad.

## README

In this order:

1. **Logo, name and a one-line tagline, centered at the top.** The logo is the first thing a visitor sees, so it sets the project's identity before any text. Put the logo, name, tagline and badges in one centered block:

   ```html
   <p align="center">
     <picture>
       <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg">
       <img src="docs/assets/logo-light.svg" alt="<Project> logo" width="200">
     </picture>
   </p>
   <h1 align="center"><Project></h1>
   <p align="center"><one-line tagline></p>
   ```

   Store the logo in the repo (not a hotlinked or expiring URL), and give it alt text and a fixed width so it renders the same everywhere. Use the `<picture>` dark variant only if a dark version exists; otherwise a single `<img>` is fine. If the repo has no logo, leave `TODO(docs): add a logo at <path>` rather than inventing one.
2. **Badges** for real signals only: CI status, version/registry, license, community channel. Every badge must resolve.
3. **Screenshot or demo** if there's a UI, with alt text.
4. **Introduction:** what it does, who it's for, why use it, in 2-4 short paragraphs. Key features as a text list. If features are shown as images, add the text too.
5. **Usage / Quickstart:** the fastest path to value. An install command and a minimal working example, or the hosted option if one exists. Link tutorials.
6. **Development** (if people run it from source):
   - Prerequisites with versions stated inline, not "see package.json"
   - The one-click option if present (Codespaces, devcontainer)
   - Architecture in 1-3 sentences (e.g. "Nx monorepo; apps live under packages/")
   - One numbered list of setup steps, each with a copy-paste command block
   - How to run each component, calling out components that must run together
   - Pointers to per-package READMEs
7. **Resources:** docs, community, blog, issue tracker, each with a one-line purpose.
8. **Contributing:** 2-3 lines, links to CONTRIBUTING and the code of conduct, and direct links to the bug, feature and docs issue templates.
9. **License:** name it and link it. Explain any exceptions, such as directories under a different license.

## CONTRIBUTING

1. **Welcome**, listing the kinds of contributions accepted (code, docs, issues, guides).
2. **Route by intent:** a question goes to the community channel; a bug goes to the bug template (security bugs go to SECURITY.md, never public issues); a missing feature goes to the feature template.
3. **Big vs small changes:** major features start with an issue proposal; small fixes go straight to a PR. Say what won't be accepted, if known.
4. **Stack overview** with links, so contributors know what they need to learn.
5. **Finding work:** links to label searches like `good first issue` (only labels that exist), plus non-code options such as docs issues.
6. **Numbered workflow from fork to merged PR**, each step with its command: fork, clone (with the correct branch), set up (link to the README Development section), branch, make changes, **run tests and lint locally (exact commands)**, commit, push, open the PR.
7. **Branch naming:** the convention plus one example per type.
8. **Commit messages:** the format, the list of types, a list of scopes that matches the actual packages, and one example. Say whether commitlint or hooks enforce it.
9. **Pull requests:** title format, target branch (call it out prominently if it isn't the default), what the template asks for, required CI checks, what review looks like and roughly how long it takes, and reassurance that imperfect PRs are welcome.
10. **Legal:** CLA or DCO requirements, if any, and how contributions to differently licensed directories are handled.
11. **Code of conduct** link.

## RELEASING

Written for maintainers, so the release process doesn't live in one person's head. Derive it from the release tooling actually in the repo.

1. **Overview:** what gets released (packages, images, docs) and where (registry, GitHub Releases, docs host).
2. **Versioning:** the scheme (SemVer, CalVer), pre-release tags, and what counts as breaking.
3. **Who can release:** required roles and permissions, and the secrets needed, by name and where they're stored. Never their values.
4. **When:** the cadence or trigger (merge to main, tag push, manual dispatch).
5. **Steps,** numbered with commands: prepare (branch, changelog, version bump), tag, build, publish, deploy docs, create the GitHub release, announce. Mark which steps are automated and by which workflow file.
6. **Verify:** how to confirm the release worked (install it, check the registry page, run a smoke test).
7. **Hotfixes and backports.**
8. **Rollback:** yank or deprecate, revert tags, re-publish.

## Other files

- **CHANGELOG:** Keep a Changelog format (Unreleased on top; Added, Changed, Deprecated, Removed, Fixed, Security), newest first, a version and date per entry, matching the git tags. If tooling generates it, say so at the top.
- **SECURITY:** supported versions, a private reporting channel (GitHub private vulnerability reporting or an email), what to include in a report, and expected response time.
- **CODE_OF_CONDUCT:** adopt the Contributor Covenant rather than writing one, and fill in the enforcement contact.
- **Issue templates:** bug (steps, expected vs actual, version, environment), feature (problem, proposal, alternatives), docs request. Prefer YAML forms. Add `config.yml` sending questions to the community channel.
- **PR template:** linked issue, what and why, how it was tested, and a checklist (tests, docs updated, conventions followed).
- **Agent docs (AGENTS.md, CLAUDE.md):** the same rules a human contributor follows, written as short instructions for an agent: setup, build, test and lint commands; branch, commit and PR conventions; code style; repo layout; and things not to touch (generated code, `ee/`-style licensed directories, secrets). Take every command and convention from CONTRIBUTING so the two never disagree; if they'd duplicate a long section, link to CONTRIBUTING instead of copying it. If both files exist, keep one as the source and have the other point to it (e.g. CLAUDE.md containing `@AGENTS.md`).
- **Package README** (monorepos): its purpose, how it fits the whole, how to run and test just this package, and its config and env vars.

## Verify before finishing

Docs usually go wrong by drifting from the repo, not by bad writing, so check every claim against the repo:

- [ ] Every command exists (manifest scripts, tools that setup installs). Run setup and test commands if you can.
- [ ] Every file path, anchor and template link resolves.
- [ ] Branch names match the repo, and README and CONTRIBUTING agree on the clone branch and PR target.
- [ ] Version requirements match the manifest.
- [ ] Commit scopes and package lists cover every package.
- [ ] Numbered lists count correctly, with one list per procedure (prerequisites aren't mixed into steps).
- [ ] Images have alt text, and nothing important appears only in an image.
- [ ] The docs don't contradict each other (README vs CONTRIBUTING vs RELEASING vs templates).
- [ ] Agent docs match CONTRIBUTING: same commands, branches, commit format and PR target.
- [ ] The README opens with a centered logo that loads from the repo and has alt text (or a `TODO(docs):` if there's no logo).
- [ ] No secrets, tokens or internal URLs.
- [ ] Spelling pass.

## Audit-only requests

If the user only wants an assessment, use the same section guides and checklist without editing files. For each doc, report what's good, what's missing, and what's wrong (with evidence: the file and line, or the conflicting doc), then give the top 3 fixes.
