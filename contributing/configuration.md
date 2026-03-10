# Repository configuration

<h2>Table of contents</h2>

- [1. Repository structure](#1-repository-structure)
- [2. GitHub templates](#2-github-templates)
  - [2.1. Issue templates](#21-issue-templates)
    - [2.1.1. `01-task.yml` — Lab Task](#211-01-taskyml--lab-task)
    - [2.1.2. `02-bug-report.yml` — Bug Report](#212-02-bug-reportyml--bug-report)
    - [2.1.3. `config.yml`](#213-configyml)
  - [2.2. PR template (`pull_request_template.md`)](#22-pr-template-pull_request_templatemd)
- [3. VS Code settings (`.vscode/settings.json`)](#3-vs-code-settings-vscodesettingsjson)
- [4. VS Code recommended extensions (`.vscode/extensions.json`)](#4-vs-code-recommended-extensions-vscodeextensionsjson)
  - [4.1. Rules for extensions](#41-rules-for-extensions)
- [5. Task runner and package manager config](#5-task-runner-and-package-manager-config)
  - [5.1. Rules for task runner](#51-rules-for-task-runner)
- [6. Docker and deployment pattern](#6-docker-and-deployment-pattern)
- [7. Agent configuration (`AGENTS.md`)](#7-agent-configuration-agentsmd)
  - [7.1. File layout](#71-file-layout)
  - [7.2. `AGENTS.md` structure](#72-agentsmd-structure)
  - [7.3. Creating symlinks](#73-creating-symlinks)
- [8. Checklist before publishing](#8-checklist-before-publishing)

Use this file when configuring the repository structure, templates, editor settings, and deployment infrastructure.

---

## 1. Repository structure

Create the following directory and file layout. Items marked *(conditional)* are included only when the lab needs them.

```text
<repo-root>/
├── README.md                          # Main entry point
├── AGENTS.md                          # Agent/AI coding assistant configuration (canonical)
├── CLAUDE.md -> AGENTS.md             # Symlink (Claude)
├── QWEN.md -> AGENTS.md               # Symlink (Qwen)
├── index.md                           # Repository index
├── lab/
│   ├── tasks/
│   │   ├── setup.md                   # Full first-time lab setup
│   │   ├── setup-simple.md            # Lab-specific setup (returning students)
│   │   ├── required/
│   │   │   ├── task-1.md
│   │   │   ├── task-2.md
│   │   │   └── ...
│   │   └── optional/
│   │       ├── task-1.md
│   │       └── ...
│   └── images/                        # Task-specific screenshots and diagrams
│       └── ...
├── wiki/                              # Reference docs for tools & concepts
│   ├── vs-code.md
│   ├── git.md
│   ├── git-workflow.md                # Reusable Git workflow procedure
│   ├── git-vscode.md
│   ├── github.md
│   ├── shell.md
│   ├── ...                            # One file per tool/concept
│   └── images/                        # Wiki screenshots organized by tool
│       ├── vs-code/
│       ├── gitlens/
│       └── ...
├── contributing/                      # Lab authoring conventions
│   ├── configuration.md               # Repo structure, templates, settings, deployment, checklist
│   └── conventions/                   # Detailed conventions by topic
│       ├── agents/
│       ├── git/
│       ├── implementation/
│       ├── meetings/
│       └── writing/
├── docs/                              # Application architecture docs (conditional)
│   ├── design/                        # Architecture and domain model
│   └── requirements/                  # Vision and requirements
├── instructors/                       # Internal design notes (not student-facing)
│   ├── README.md
│   ├── course.md
│   ├── ideas.md
│   ├── meetings/                      # Lab meeting notes and transcripts
│   ├── file-reviews/                  # Review findings for lab files
│   └── scripts/                       # Utility scripts
├── .agents/                           # Agent skill definitions (canonical)
│   └── skills/                        # One subdirectory per skill
├── .claude -> .agents                 # Symlink (Claude)
├── .qwen -> .agents                   # Symlink (Qwen)
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── 01-task.yml                # Lab Task issue form
│   │   ├── 02-bug-report.yml          # Bug Report issue form
│   │   └── config.yml                 # blank_issues_enabled: false
│   ├── pull_request_template.md       # PR template with checklist
│   └── workflows/                     # GitHub Actions (optional)
├── .vscode/
│   ├── settings.json                  # Editor, formatter, ToC settings
│   └── extensions.json                # Recommended VS Code extensions
├── backend/                           # Application source code (conditional)
├── frontend/                          # Application source code (conditional)
├── .gitignore
├── .env.example                       # Template for local env vars (conditional)
├── .env.docker.example                # Template for Docker env vars (conditional)
├── .dockerignore                      # (conditional — only if using Docker)
├── Dockerfile                         # (conditional — only if using Docker)
├── docker-compose.yml                 # (conditional — only if using Docker)
└── <package-manager-config>           # e.g., pyproject.toml, package.json
```

---

## 2. GitHub templates

> The templates below are the canonical starting point. The actual files in `.github/` may include lab-specific additions.

### 2.1. Issue templates

#### 2.1.1. `01-task.yml` — Lab Task

```yaml
name: Lab Task
description: Track work for a specific lab task
title: "[Task] <short title>"
labels: ["task"]
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Summarize what this task is about in your own words.
      placeholder: |
        Make X work with Y ...
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Plan
      description: What do you plan to do to complete this task?
      placeholder: |
        - [ ] Step 1
        - [ ] Step 2
        ...
    validations:
      required: true
```

#### 2.1.2. `02-bug-report.yml` — Bug Report

Same structure as `01-task.yml`. Required fields:

- `Brief problem description`
- `Steps to Reproduce`
- `Expected Result`
- `Actual Result`

#### 2.1.3. `config.yml`

```yaml
blank_issues_enabled: false
```

### 2.2. PR template (`pull_request_template.md`)

```markdown
## Summary

- Closes #<issue-number>

----

## Checklist

- [ ] I made this PR to the `main` branch **of my fork (NOT the course instructors' repo)**.
- [ ] I see `base: main` <- `compare: <branch>` above the PR title.
- [ ] I edited the line `- Closes #<issue-number>`.
- [ ] I wrote clear commit messages.
- [ ] I reviewed my own diff before requesting review.
- [ ] I understand the changes I'm submitting.
```

---

## 3. VS Code settings (`.vscode/settings.json`)

> The template below is the canonical starting point. The actual file in `.vscode/` may include lab-specific additions.

```json
{
  "git.autofetch": true,
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 500,
  "editor.formatOnSave": true,
  "[markdown]": {
    "editor.defaultFormatter": "DavidAnson.vscode-markdownlint"
  },
  "markdown.extension.toc.levels": "2..6",
  "workbench.sideBar.location": "right",
  "markdown.preview.scrollEditorWithPreview": false,
  "markdown.preview.scrollPreviewWithEditor": false
}
```

Add language-specific formatter settings as needed (e.g., Python with Ruff, JS with Prettier).

---

## 4. VS Code recommended extensions (`.vscode/extensions.json`)

> The template below is the canonical starting point. The actual file in `.vscode/` may include lab-specific additions.

Provide a curated list of recommended extensions so students can install them all at once:

```json
{
  "recommendations": [
    // Language support (adjust per lab): Python, Node.js, Go, Rust, etc.

    // Git
    "eamodio.gitlens",

    // Remote development (if lab uses SSH/VMs/containers)
    "ms-vscode-remote.remote-ssh",

    // Markdown authoring and preview
    "DavidAnson.vscode-markdownlint",
    "yzhang.markdown-all-in-one",

    // GitHub integration
    "github.vscode-pull-request-github",

    // File format support (include what the lab uses)
    "tamasfe.even-better-toml",

    // Useful utilities
    "usernamehw.errorlens",
    "gruntfuggly.todo-tree",
    "ms-vsliveshare.vsliveshare"
  ]
}
```

### 4.1. Rules for extensions

- Group extensions by purpose with `//` comments.
- Include extensions for: the lab's programming language, Git, remote development, Markdown, GitHub, and relevant file formats.
- The setup doc instructs students to install these via `Extensions` > `Filter` > `Recommended` > `Install Workspace Recommended extensions`.

---

## 5. Task runner and package manager config

Define common project commands using a task runner so students run simple commands rather than remembering complex CLI invocations.

Choose a task runner appropriate for the lab's ecosystem:

- **Python**: `pyproject.toml` + [`poethepoet`](https://poethepoet.natn.io/) (run via `uv run poe <task>`)
- **Node.js**: `package.json` scripts (run via `npm run <task>`)
- **Go / Rust / other**: `Makefile` or `Taskfile.yml` (run via `make <task>` or `task <task>`)

Example with `pyproject.toml` + `poethepoet`:

```toml
[tool.poe.tasks.dev]
help = "Run server after static analysis"
sequence = ["check", "start"]

[tool.poe.tasks.test]
help = "Run pytest"
cmd = "pytest"
```

Example with `package.json`:

```json
{
  "scripts": {
    "dev": "npm run check && npm run start",
    "start": "node src/index.js",
    "check": "npm run format && npm run lint",
    "test": "jest"
  }
}
```

### 5.1. Rules for task runner

- Students run a single short command (e.g., `uv run poe dev`, `npm run dev`) — no need to memorize raw commands.
- Document task runner commands in `> [!NOTE]` blocks the first time they appear:

  ```markdown
  > [!NOTE]
  > `<runner>` can run tasks specified in the `<config-file>`.
  ```

---

## 6. Docker and deployment pattern

> Include this section only if the lab involves containerization or remote deployment. Omit the Docker/deployment files from the repository structure if not needed.

If the lab involves deployment:

1. Provide `.env.example` and `.env.docker.example` as templates.
2. Students copy them to `.env.secret` and `.env.docker.secret` (which are `.gitignore`d via the `*.secret` pattern in `.gitignore`).
3. Use `docker-compose.yml` with environment variable substitution from the `.env.docker.secret` file:

   ```yaml
   services:
     app:
       build: .
       ports:
         - ${APP_HOST_ADDRESS}:${APP_HOST_PORT}:${APP_CONTAINER_PORT}
       environment:
         - PORT=${APP_CONTAINER_PORT}
     caddy:
       image: caddy:2-alpine
       depends_on:
         - app
       ports:
         - ${CADDY_HOST_ADDRESS}:${CADDY_HOST_PORT}:${CADDY_CONTAINER_PORT}
       volumes:
         - ./caddy/Caddyfile:/etc/caddy/Caddyfile
   ```

4. Include a reverse proxy service (e.g., Caddy) in `docker-compose.yml`.
5. Use a multi-stage `Dockerfile` for production builds (builder stage + slim runtime).
6. Deployment task flow: SSH into VM → clone repo → create `.env.docker.secret` → `docker compose up --build -d`.
7. Distinguish local vs remote env differences:
   - Local: `APP_HOST_ADDRESS=127.0.0.1` (localhost only).
   - Remote: `CADDY_HOST_ADDRESS=0.0.0.0` (accessible from outside).
8. **Use an institutional container registry** (e.g., Harbor cache proxy) for base images to avoid Docker Hub rate limits ("too many requests" errors). Reference the registry in `docker-compose.yml` image fields instead of pulling directly from Docker Hub.

---

## 7. Agent configuration (`AGENTS.md`)

The repository uses a single canonical agent configuration file that all AI coding assistants read.

### 7.1. File layout

```text
<repo-root>/
├── AGENTS.md                  # Canonical agent configuration (edit this file)
├── CLAUDE.md -> AGENTS.md     # Symlink — Claude reads this
├── QWEN.md -> AGENTS.md       # Symlink — Qwen reads this
└── .agents/
    ├── settings.local.json    # Agent tool-permission settings (not committed)
    └── skills/
        └── <skill-name>/
            └── SKILL.md       # One skill per subdirectory
```

Agent tool directories (`.claude/`, `.qwen/`) are symlinks to `.agents/` so all agents share the same skill definitions.

### 7.2. `AGENTS.md` structure

`AGENTS.md` is the single source of truth for agent instructions. It follows the same structure as `CLAUDE.md`:

```markdown
# Lab authoring conventions

## When editing `lab/tasks/`

Read before making changes:

- [`contributing/conventions/writing/common.md`](...) — writing conventions
- [`contributing/conventions/writing/tasks.md`](...) — task structure

## When editing `wiki/`
...
```

- Use `##` sections keyed to the action (e.g., `When editing X`).
- Each section lists the relevant convention files to read before making changes.
- `CLAUDE.md` and `QWEN.md` are symlinks — never edit them directly; edit `AGENTS.md`.

### 7.3. Creating symlinks

```bash
ln -s AGENTS.md CLAUDE.md
ln -s AGENTS.md QWEN.md
ln -s .agents .claude
ln -s .agents .qwen
```

---

## 8. Checklist before publishing

- [ ] `AGENTS.md` exists at repo root with `CLAUDE.md` and `QWEN.md` as symlinks to it.
- [ ] All cross-references use relative paths and are valid.
- [ ] Issue templates (`01-task.yml`, `02-bug-report.yml`) are configured.
- [ ] PR template has a checklist.
- [ ] `.vscode/settings.json` and `.vscode/extensions.json` are configured.
- [ ] `.gitignore` excludes generated files and secrets for the lab's ecosystem.
- [ ] Branch protection rules are documented.
**Conditional (include when applicable):**

- [ ] `.env.example` files are provided; `.env.secret` files are gitignored (if the lab uses environment variables).
- [ ] `.dockerignore` excludes tests, docs, `.git/`, build caches, markdown files (if the lab uses Docker).
- [ ] Task runner commands are documented in the config file (if the lab uses a task runner).
- [ ] Docker images use an institutional container registry (if the lab uses Docker in an institutional setting).
