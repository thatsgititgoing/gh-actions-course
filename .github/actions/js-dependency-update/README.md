# JavaScript Action: Update NPM Dependencies

A JavaScript-based GitHub Action that checks for NPM package updates and automates dependency management by creating pull requests when updates are available.

## Type

**JavaScript Action** - Node.js action using `@actions/core`, `@actions/exec`, and `@actions/github` packages.

## Purpose

This action automates the dependency update workflow:
1. Runs `npm update` in the specified directory
2. Detects if `package.json` or `package-lock.json` changed
3. Creates a pull request with the updates (when configured)
4. Helps keep dependencies up-to-date automatically

**Use cases**:
- Scheduled dependency updates (weekly/monthly)
- Automated security patches
- Keep dependencies current
- Reduce manual maintenance

## Location

`.github/actions/js-dependency-update/`

## Usage

### Basic Example

```yaml
steps:
  - uses: actions/checkout@v4

  - name: Check for Dependency Updates
    uses: ./.github/actions/js-dependency-update
    with:
      working-directory: ./my-app
      gh-token: ${{ secrets.GITHUB_TOKEN }}
```

### Full Example with Scheduled Run

```yaml
name: Weekly Dependency Updates

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  workflow_dispatch:      # Manual trigger

jobs:
  update-dependencies:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'

      - name: Check and Update Dependencies
        uses: ./.github/actions/js-dependency-update
        with:
          base-branch: main
          target-branch: update-dependencies
          working-directory: ./app
          gh-token: ${{ secrets.GITHUB_TOKEN }}
          debug: true
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `base-branch` | Branch used as base for update checks | No | `main` |
| `target-branch` | Branch from which PR is created | No | `update-dependencies` |
| `working-directory` | Directory containing `package.json` | Yes | - |
| `gh-token` | GitHub token with PR write permissions | Yes | - |
| `debug` | Enable debug logging | No | `false` |

### Input Details

#### `base-branch`
- **Type**: String
- **Default**: `main`
- **Purpose**: The branch to merge updates into
- **Validation**: Alphanumeric, hyphens, underscores, dots, forward slashes
- **Examples**:
  - `main`
  - `master`
  - `develop`
  - `release/v2.0`

#### `target-branch`
- **Type**: String
- **Default**: `update-dependencies`
- **Purpose**: Name of the branch created for the PR
- **Validation**: Same as `base-branch`
- **Examples**:
  - `update-dependencies`
  - `deps/npm-updates`
  - `chore/dependency-updates`

**Note**: If branch exists, it will be updated; otherwise it will be created.

#### `working-directory`
- **Type**: String
- **Required**: Yes
- **Purpose**: Path to directory containing `package.json` and `package-lock.json`
- **Validation**: Alphanumeric, hyphens, underscores, forward slashes
- **Examples**:
  - `.` (root directory)
  - `./app`
  - `packages/frontend`
  - `services/api`

#### `gh-token`
- **Type**: String (secret)
- **Required**: Yes
- **Purpose**: Authentication token for creating PRs
- **Permissions needed**:
  - `contents: write` - Push commits
  - `pull-requests: write` - Create PRs
- **Examples**:
  - `${{ secrets.GITHUB_TOKEN }}` - Built-in token
  - `${{ secrets.PAT }}` - Personal access token

**Security**: Token is automatically masked in logs using `core.setSecret()`.

#### `debug`
- **Type**: Boolean
- **Default**: `false`
- **Purpose**: Enable verbose logging for troubleshooting
- **Examples**:
  - `'true'`
  - `'false'`

## How It Works

### Step-by-Step Flow

```
1. Validate Inputs
   ├─> Check base-branch format
   ├─> Check target-branch format
   └─> Check working-directory format

2. Log Configuration (if debug enabled)
   ├─> Base branch: main
   ├─> Target branch: update-dependencies
   └─> Working directory: ./app

3. Run npm update
   └─> Execute: npm update
   └─> Working directory: ./app
   └─> Updates package.json and package-lock.json

4. Check for Changes
   └─> Execute: git status -s package*.json
   └─> If changes detected:
       ├─> Log: "There are updates available!"
       └─> [Future] Create PR with changes
   └─> If no changes:
       └─> Log: "No updates at this point in time."

5. Exit
   └─> Action completes
```

### What npm update Does

```bash
# Before
package.json: "express": "^4.18.0"
package-lock.json: express@4.18.0

# npm update runs
# Finds newer version: express@4.19.2

# After
package.json: "express": "^4.19.2"  # Updated
package-lock.json: express@4.19.2   # Updated
```

**Important**: Only updates within semver range (e.g., `^4.0.0` updates to `4.x.x`, not `5.0.0`).

## Implementation Details

### File Structure

```
.github/actions/js-dependency-update/
├── action.yaml          # Action definition
├── index.js             # Main JavaScript code
├── package.json         # Action dependencies
├── package-lock.json    # Locked dependency versions
├── node_modules/        # Installed dependencies
└── README.md            # This file
```

### Dependencies

```json
{
  "dependencies": {
    "@actions/core": "1.10.1",    // Input/output handling, logging
    "@actions/exec": "1.1.1",     // Execute shell commands
    "@actions/github": "6.0.0"    // GitHub API (Octokit)
  }
}
```

### Key Code Segments

#### Input Validation

```javascript
const validateBranchName = ({ branchName }) =>
  /^[a-zA-Z0-9_\-\.\/]+$/.test(branchName);

if (!validateBranchName({ branchName: baseBranch })) {
  core.setFailed('Invalid base-branch name...');
  return;
}
```

**Why validate**: Prevents command injection and ensures valid Git branch names.

#### Executing npm update

```javascript
await exec.exec('npm update', [], {
  cwd: workingDir,  // Run in specified directory
});
```

#### Checking for Changes

```javascript
const gitStatus = await exec.getExecOutput(
  'git status -s package*.json',
  [],
  { cwd: workingDir }
);

if (gitStatus.stdout.length > 0) {
  // Updates found!
} else {
  // No updates
}
```

## Current Status

### ✅ Implemented Features

- [x] Parse and validate inputs
- [x] Run `npm update`
- [x] Detect changes to `package*.json`
- [x] Debug logging
- [x] Input validation (security)

### 🚧 Planned Features (Per Code Comments)

- [ ] Add and commit files to target-branch
- [ ] Create PR to base-branch using Octokit API
- [ ] Set action outputs

**Note**: This is an educational action demonstrating JavaScript action concepts. Full PR creation can be implemented using `@actions/github`.

## Real-World Example

```yaml
name: Monthly Dependency Updates

on:
  schedule:
    # First day of every month at 9 AM UTC
    - cron: '0 9 1 * *'
  workflow_dispatch:

jobs:
  update-deps:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'

      - name: Update Dependencies
        uses: ./.github/actions/js-dependency-update
        with:
          base-branch: main
          target-branch: deps/monthly-update-${{ github.run_number }}
          working-directory: .
          gh-token: ${{ secrets.GITHUB_TOKEN }}
          debug: true
```

## Comparison: JavaScript vs Other Action Types

| Feature | JavaScript | Composite | Docker |
|---------|------------|-----------|--------|
| **Language** | JavaScript | YAML | Any |
| **Speed** | Fast (~2s) | Fast | Slower (build) |
| **API Access** | Full (Octokit) | Via CLI | Via CLI |
| **Complexity** | Medium | Low | High |
| **Use case** | Complex logic | Combine steps | Any language |

**This action** uses JavaScript because:
- Needs programmatic logic (validation, conditionals)
- Uses GitHub API (for future PR creation)
- Faster than Docker
- Standard for GitHub Actions ecosystem

## Testing the Action

### Local Testing (Node.js)

```bash
cd .github/actions/js-dependency-update

# Install dependencies
npm install

# Set inputs as environment variables
export INPUT_BASE-BRANCH=main
export INPUT_TARGET-BRANCH=test-updates
export INPUT_WORKING-DIRECTORY=../../17-custom-actions/react-app
export INPUT_GH-TOKEN=$GITHUB_TOKEN
export INPUT_DEBUG=true

# Run action
node index.js
```

### GitHub Actions Testing

```yaml
name: Test JS Action

on: workflow_dispatch

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'

      - name: Test Dependency Update Action
        uses: ./.github/actions/js-dependency-update
        with:
          working-directory: ./17-custom-actions/react-app
          gh-token: ${{ secrets.GITHUB_TOKEN }}
          debug: true
```

## Troubleshooting

### Invalid Branch Name Error

**Problem**: "Invalid base-branch name..."

**Cause**: Branch name contains invalid characters

**Solution**:
```yaml
# ✓ Valid
base-branch: main
base-branch: feature/my-branch
base-branch: v2.0-release

# ✗ Invalid
base-branch: my branch      # Space not allowed
base-branch: branch@123     # @ not allowed
base-branch: "branch:name"  # : not allowed
```

### npm update Fails

**Problem**: Error during `npm update`

**Checks**:

1. **package.json exists**:
   ```yaml
   - name: List files
     run: ls -la
     working-directory: ./app
   ```

2. **Node.js is installed**:
   ```yaml
   - name: Setup Node
     uses: actions/setup-node@v4
     with:
       node-version: '20.x'
   ```

3. **Dependencies are installable**:
   ```yaml
   - name: Install first
     run: npm ci
     working-directory: ./app
   ```

### No Updates Detected

**Problem**: Action always reports "No updates at this point in time"

**Possible causes**:

1. **Dependencies are up-to-date**
   ```bash
   # Check manually
   npm outdated
   ```

2. **Semver constraints too strict**
   ```json
   // package.json
   {
     "dependencies": {
       "express": "4.18.0"  // ✗ Exact version - won't update
       "express": "^4.18.0" // ✓ Allows minor/patch updates
     }
   }
   ```

3. **Wrong working directory**
   ```yaml
   # Ensure path is correct
   working-directory: ./correct/path/to/app
   ```

### Permission Denied for gh-token

**Problem**: "Resource not accessible by integration"

**Solution**: Grant permissions in workflow

```yaml
jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write        # Required for commits
      pull-requests: write   # Required for PRs

    steps:
      - uses: ./.github/actions/js-dependency-update
        with:
          gh-token: ${{ secrets.GITHUB_TOKEN }}
```

## Best Practices

### 1. Use Scheduled Workflows

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Mondays
    # Or
    - cron: '0 9 1 * *'  # Monthly on 1st

  workflow_dispatch:      # Allow manual runs
```

### 2. Limit Scope

```yaml
# Update specific app, not entire monorepo at once
working-directory: ./packages/api
```

### 3. Set Proper Permissions

```yaml
permissions:
  contents: write         # Minimum required
  pull-requests: write    # For future PR feature
```

### 4. Use Debug for Initial Setup

```yaml
# Enable during testing
debug: true

# Disable in production
debug: false
```

### 5. Unique Branch Names

```yaml
# Avoid conflicts with dynamic names
target-branch: deps/update-${{ github.run_number }}
# Example: deps/update-123
```

## Security Considerations

### Input Validation

All inputs are validated with regex:
```javascript
/^[a-zA-Z0-9_\-\.\/]+$/  // Allowed characters
```

**Prevents**:
- Command injection
- Path traversal
- Malicious branch names

### Token Handling

```javascript
core.setSecret(ghToken);  // Masks token in logs
```

**Always masked** in output:
```
✓ Token: ***
✗ Token: ghp_abc123xyz
```

### Permissions

Use principle of least privilege:
```yaml
permissions:
  contents: write         # Only what's needed
  pull-requests: write
  # NOT: permissions: write-all
```

## Extending the Action

### Add PR Creation

```javascript
const github = require('@actions/github');
const octokit = github.getOctokit(ghToken);

await octokit.rest.pulls.create({
  owner: github.context.repo.owner,
  repo: github.context.repo.repo,
  title: 'Update NPM dependencies',
  head: targetBranch,
  base: baseBranch,
  body: 'Automated dependency updates'
});
```

### Add Outputs

```javascript
// In action.yaml
outputs:
  updates-available:
    description: Whether updates were found

// In index.js
core.setOutput('updates-available', gitStatus.stdout.length > 0);
```

## Related Resources

- **Workflow Example**: [17-2-custom-actions-js.yaml](../../workflows/17-2-custom-actions-js.yaml)
- **GitHub Docs**: [Creating JavaScript Actions](https://docs.github.com/en/actions/creating-actions/creating-a-javascript-action)
- **@actions/core**: [Documentation](https://github.com/actions/toolkit/tree/main/packages/core)
- **@actions/github**: [Documentation](https://github.com/actions/toolkit/tree/main/packages/github)

## License

This action is part of the GitHub Actions Course educational materials.
