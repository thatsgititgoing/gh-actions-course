# GitHub Actions Course - Complete README Guide

A comprehensive, hands-on GitHub Actions course covering fundamentals through advanced topics including custom actions, caching, artifacts, and reusable workflows.

## 📚 Course Overview

This repository contains 21 workflow examples organized into 18 lessons, 3 custom actions, and 4 hands-on React application projects. Each lesson builds upon previous concepts, taking you from basic workflow syntax to creating production-ready CI/CD pipelines.

## 🎯 What You'll Learn

- **Fundamentals**: Jobs, steps, runners, events, and triggers
- **Actions Ecosystem**: Using marketplace actions and creating custom ones
- **Advanced Features**: Caching, artifacts, matrices, environments
- **Reusability**: Composite actions, JavaScript actions, Docker actions, reusable workflows
- **Best Practices**: Optimization, security, and workflow organization

## 📋 Prerequisites

- GitHub account with Actions enabled
- Basic understanding of Git and YAML
- Node.js 18+ (for React app examples)
- Text editor or IDE

## 🗺️ Course Structure

### Part 1: Fundamentals (Lessons 01-03)

| Lesson | Topic | Workflow | Key Concepts |
|--------|-------|----------|--------------|
| 01 | Building Blocks | [01-building-blocks.yaml](.github/workflows/01-building-blocks.yaml) | Jobs, steps, runners, basic syntax |
| 02 | Workflow Events | [02-workflow-events.yaml](.github/workflows/02-workflow-events.yaml) | Triggers, event types, `on` keyword |
| 03 | Workflow Runners | [03-workflow-runners.yaml](.github/workflows/03-workflow-runners.yaml) | Runner types, OS selection, labels |

### Part 2: Working with Actions (Lessons 04-07)

| Lesson | Topic | Workflow | Key Concepts | Hands-on |
|--------|-------|----------|--------------|----------|
| 04 | Using Actions | [04-using-actions.yaml](.github/workflows/04-using-actions.yaml) | Marketplace actions, `uses` keyword | [React App](04-using-actions/) |
| 05 | Filters & Activity Types | [05-1-filters-activity-types.yaml](.github/workflows/05-1-filters-activity-types.yaml) / [05-2-filters-activity-types.yaml](.github/workflows/05-2-filters-activity-types.yaml) | Event filtering, path filters, branch filters |
| 06 | Contexts | [06-contexts.yaml](.github/workflows/06-contexts.yaml) | `github`, `env`, `job`, `runner` contexts |
| 07 | Expressions | [07-expressions.yaml](.github/workflows/07-expressions.yaml) | `${{ }}` syntax, conditionals |

### Part 3: Advanced Features (Lessons 08-16)

| Lesson | Topic | Workflow | Key Concepts | Hands-on |
|--------|-------|----------|--------------|----------|
| 08 | Variables | [08-variables.yaml](.github/workflows/08-variables.yaml) | Environment variables, secrets |
| 09 | Functions | [09-functions.yaml](.github/workflows/09-functions.yaml) | Built-in functions (`contains`, `startsWith`, etc.) |
| 10 | Execution Flow | [10-execution-flow.yaml](.github/workflows/10-execution-flow.yaml) | Job dependencies, `needs`, conditionals |
| 11 | Inputs | [11-inputs.yaml](.github/workflows/11-inputs.yaml) | `workflow_dispatch` inputs, types |
| 12 | Outputs | [12-outputs.yaml](.github/workflows/12-outputs.yaml) | Job outputs, step outputs |
| 13 | Caching | [13-caching.yaml](.github/workflows/13-caching.yaml) | `actions/cache`, dependency caching | [React App](13-caching/) |
| 14 | Artifacts | [14-artifacts.yaml](.github/workflows/14-artifacts.yaml) | Upload/download artifacts, retention | [React App](14-artifacts/) |
| 15 | Matrices | [15-matrices.yaml](.github/workflows/15-matrices.yaml) | Matrix strategies, parallel jobs |
| 16 | Environments | [16-environments.yaml](.github/workflows/16-environments.yaml) | Deployment environments, protection rules |

### Part 4: Custom Actions & Reusability (Lessons 17-18)

| Lesson | Topic | Workflow | Key Concepts | Hands-on |
|--------|-------|----------|--------------|----------|
| 17-1 | Custom Composite Actions | [17-1-custom-actions-composite.yaml](.github/workflows/17-1-custom-actions-composite.yaml) | Composite actions, reusable steps | [React App](17-custom-actions/) |
| 17-2 | Custom JavaScript Actions | [17-2-custom-actions-js.yaml](.github/workflows/17-2-custom-actions-js.yaml) | Node.js actions, `@actions/core` |
| 17-3 | Custom Docker Actions | [17-3-custom-actions-docker.yaml](.github/workflows/17-3-custom-actions-docker.yaml) | Containerized actions |
| 18-1 | Reusable Workflows (Caller) | [18-1-reusable-workflows.yaml](.github/workflows/18-1-reusable-workflows.yaml) | Calling reusable workflows |
| 18-2 | Reusable Workflows (Called) | [18-2-reusable-workflow.yaml](.github/workflows/18-2-reusable-workflow.yaml) | Creating reusable workflows |

## 🔧 Custom Actions Built in This Course

This course includes 3 production-ready custom actions:

### 1. composite-cache-deps (Composite Action)
**Location**: [.github/actions/composite-cache-deps/](.github/actions/composite-cache-deps/)
**Purpose**: Cache Node.js dependencies with automatic dev/prod detection
**Documentation**: [README](.github/actions/composite-cache-deps/README.md)

**Features**:
- Automatic dependency caching based on `package-lock.json`
- Dev vs Prod mode support
- Configurable Node.js version
- Cache hit detection output

### 2. docker-ping-url (Docker Action)
**Location**: [.github/actions/docker-ping-url/](.github/actions/docker-ping-url/)
**Purpose**: Health check for deployed applications with retry logic
**Documentation**: [README](.github/actions/docker-ping-url/README.md)

**Features**:
- Configurable retry attempts and delays
- HTTP 200 verification
- Containerized for consistent execution
- Useful for deployment verification

### 3. js-dependency-update (JavaScript Action)
**Location**: [.github/actions/js-dependency-update/](.github/actions/js-dependency-update/)
**Purpose**: Automatically check for NPM updates and create PRs
**Documentation**: [README](.github/actions/js-dependency-update/README.md)

**Features**:
- Automated dependency update detection
- Creates pull requests automatically
- Configurable base and target branches
- Debug mode for troubleshooting

## 🚀 Quick Start

### 1. Fork This Repository

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/github-actions-course.git
cd github-actions-course
```

### 2. Enable GitHub Actions

- Go to your repository on GitHub
- Click **Actions** tab
- Enable workflows if prompted

### 3. Start with Lesson 01

**Option A: Via GitHub UI**
1. Go to **Actions** tab
2. Select "01 - Building Blocks" workflow
3. Click **Run workflow** → **Run workflow** button
4. View the workflow run and examine the logs

**Option B: Trigger via Git (for event-based workflows)**
```bash
# Lesson 02 demonstrates various event triggers
git commit --allow-empty -m "Test workflow events"
git push
```

### 4. Work Through Lessons Sequentially

For best learning outcomes:
1. Read the workflow YAML file before running
2. Run the workflow and examine logs
3. Modify the workflow to experiment
4. Check the documentation for detailed explanations

### 5. Hands-on React Projects

For lessons with React applications:

```bash
# Example: Lesson 04
cd 04-using-actions/react-app
npm install
npm test          # Run tests locally
npm run build     # Build application

# Then trigger the workflow to see it run in CI
```

## 📖 Detailed Lesson Notes

### Lesson 01: Building Blocks
**Workflow**: [01-building-blocks.yaml](.github/workflows/01-building-blocks.yaml)

Learn the fundamental structure of GitHub Actions:
- **Jobs**: Multiple jobs running in parallel
- **Steps**: Sequential tasks within a job
- **Runners**: Ubuntu Linux execution environment
- **Basic commands**: `echo`, exit codes

**Key takeaway**: Workflows consist of jobs, jobs consist of steps.

---

### Lesson 04: Using Actions
**Workflow**: [04-using-actions.yaml](.github/workflows/04-using-actions.yaml)
**Hands-on**: [04-using-actions/react-app/](04-using-actions/)

Your first real-world CI/CD pipeline:
- Checkout code with `actions/checkout@v5`
- Setup Node.js with `actions/setup-node@v4`
- Install dependencies with `npm ci`
- Run unit tests

**Key takeaway**: Actions from GitHub Marketplace eliminate boilerplate code.

---

### Lesson 13: Caching
**Workflow**: [13-caching.yaml](.github/workflows/13-caching.yaml)
**Hands-on**: [13-caching/react-app/](13-caching/)

Speed up workflows with dependency caching:
- Cache `node_modules` using `actions/cache@v3`
- Cache key based on `package-lock.json` hash
- Conditional caching with workflow inputs
- Measure time savings (typically 30-60 seconds)

**Key takeaway**: Caching dramatically improves workflow performance.

---

### Lesson 14: Artifacts
**Workflow**: [14-artifacts.yaml](.github/workflows/14-artifacts.yaml)
**Hands-on**: [14-artifacts/react-app/](14-artifacts/)

Share data between jobs and preserve build outputs:
- Upload build artifacts with `actions/upload-artifact@v4`
- Download artifacts in later jobs
- Configure retention periods
- Access artifacts from GitHub UI

**Key takeaway**: Artifacts enable multi-job workflows and debugging.

---

### Lesson 17: Custom Actions
**Workflows**:
- [17-1-custom-actions-composite.yaml](.github/workflows/17-1-custom-actions-composite.yaml)
- [17-2-custom-actions-js.yaml](.github/workflows/17-2-custom-actions-js.yaml)
- [17-3-custom-actions-docker.yaml](.github/workflows/17-3-custom-actions-docker.yaml)

**Hands-on**: [17-custom-actions/react-app/](17-custom-actions/)

Build your own reusable actions:
- **Composite**: Combine multiple steps into one action
- **JavaScript**: Use Node.js for complex logic
- **Docker**: Containerized actions for any language

**Key takeaway**: Custom actions enable organization-wide reusability.

## 🎓 Learning Path

### Beginner Track (Lessons 01-07)
**Time**: ~2-3 hours
**Goal**: Understand workflow basics and how to use marketplace actions

1. Complete lessons 01-03 to learn syntax
2. Work through lesson 04 with the React app
3. Study lessons 05-07 for advanced triggers and expressions

### Intermediate Track (Lessons 08-14)
**Time**: ~3-4 hours
**Goal**: Build production-ready CI/CD pipelines

1. Master variables and secrets (08)
2. Learn workflow control flow (09-12)
3. Optimize with caching and artifacts (13-14)
4. Practice with React app examples

### Advanced Track (Lessons 15-18)
**Time**: ~4-5 hours
**Goal**: Create reusable, scalable workflows

1. Implement matrix strategies (15)
2. Configure deployment environments (16)
3. Build all 3 types of custom actions (17)
4. Create reusable workflows (18)

## 💡 Pro Tips

### 1. Use Workflow Dispatch for Testing
Most workflows use `workflow_dispatch` so you can trigger them manually:
```yaml
on: workflow_dispatch
```

### 2. Check Workflow Logs
Always examine the detailed logs:
- Click on the workflow run
- Expand each step to see output
- Look for warnings and errors

### 3. Use the GitHub Actions Extension
Install VSCode extension for YAML validation:
- **GitHub Actions** by GitHub
- Provides autocomplete and validation

### 4. Read the Source
Workflows are heavily commented - read the YAML files to understand concepts:
```yaml
# Comments explain every step
- name: Example Step
  run: echo "Learning by doing!"
```

### 5. Experiment Safely
Fork the repo and experiment:
- Modify workflows
- Add new steps
- Break things and learn from errors

## 📚 Additional Resources

### Official Documentation
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Marketplace](https://github.com/marketplace?type=actions)

### Key Concepts Reference
- **Workflow**: Automated process defined in `.github/workflows/`
- **Job**: Set of steps executing on the same runner
- **Step**: Individual task (run command or action)
- **Runner**: Server that executes workflows (GitHub-hosted or self-hosted)
- **Action**: Reusable unit of code (marketplace or custom)

### Workflow File Locations
All workflow files are in:
```
.github/
├── workflows/          # Workflow definitions
│   ├── 01-building-blocks.yaml
│   ├── 02-workflow-events.yaml
│   └── ...
└── actions/            # Custom actions
    ├── composite-cache-deps/
    ├── docker-ping-url/
    └── js-dependency-update/
```

## 🔍 Troubleshooting

### Workflow Not Triggering
- Check if Actions are enabled in repository settings
- Verify YAML syntax with VSCode extension
- Ensure trigger conditions are met (`on:` section)

### Permission Errors
- Check `GITHUB_TOKEN` permissions in workflow
- Verify repository settings → Actions → General
- Ensure secrets are properly configured

### Cache/Artifacts Issues
- Verify cache key is unique and correct
- Check artifact retention settings
- Ensure upload/download paths match

### Custom Action Errors
- Read the action's README and `action.yaml`
- Verify all required inputs are provided
- Check action version/path is correct

## 🤝 Contributing

Found an issue or want to improve a lesson?
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 Notes

- All workflows use `workflow_dispatch` for manual triggering
- React apps are for demonstration - focus is on workflow concepts
- Custom actions showcase different implementation approaches
- Workflows are numbered for recommended learning order

## 📄 License

This course material is provided for educational purposes.

---

**Ready to start?** Head to [Lesson 01](.github/workflows/01-building-blocks.yaml) and click the "Actions" tab to run your first workflow!
