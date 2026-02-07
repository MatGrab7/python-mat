# CI/CD Pipeline Setup Guide

This guide explains how to set up and use the automated code quality and secrets scanning pipeline for your repository.

## 📋 What's Included

The CI pipeline includes:
1. **Code Quality Scanning**
   - Pylint - Python code linting
   - Flake8 - Style guide enforcement
   - Black - Code formatting verification
   - Optional: SonarQube/SonarCloud for advanced analysis

2. **Secrets Detection**
   - TruffleHog - Scans for exposed secrets, API keys, tokens
   - detect-secrets - Pattern-based secret detection
   - GitHub's native secret scanning

3. **Security Analysis**
   - CodeQL - GitHub's native security analysis tool
   - Dependabot - Dependency vulnerability updates

## 🚀 Quick Start

### Step 1: Commit and Push Files
All configuration files have been created in your repository:
- `.github/workflows/code-quality-and-secrets-scan.yml` - Main workflow
- `.pylintrc` - Pylint configuration
- `.flake8` - Flake8 configuration
- `pyproject.toml` - Black, isort, mypy, pytest configuration
- `.detect-secrets.cfg` - Secrets detection configuration
- `.github/dependabot.yml` - Dependency scanning configuration
- `requirements-dev.txt` - Development dependencies

Just push these files to your repository.

### Step 2: Verify GitHub Actions is Enabled
1. Go to your GitHub repository
2. Click **Settings** → **Actions** → **General**
3. Ensure "Allow all actions and reusable workflows" is enabled

### Step 3: (Optional) Enable GitHub Advanced Security
For enhanced features:
1. Go to **Settings** → **Code security and analysis**
2. Enable "Dependabot alerts"
3. Enable "Dependabot security updates"
4. Enable "Secret scanning" (available on all public repos)

## 🔧 Workflow Triggers

The pipeline automatically runs on:
- Every push to `main` and `develop` branches
- Every pull request to `main` and `develop` branches

To view results:
1. Go to **Actions** tab in your repository
2. Click on the workflow run
3. See detailed logs and results

## 📊 Viewing Results

### In GitHub UI
1. **Actions Tab**: See workflow runs and logs
2. **Security Tab**: View CodeQL alerts, secret scanning results
3. **Pull Requests**: See inline code review comments from security checks

### Local Testing (Optional)
Test tools locally before pushing:

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run individual tools
pylint *.py
flake8 .
black --check .
detect-secrets scan --all-files

# Run all formatters and linters
black .
isort .
pylint *.py
flake8 .
```

## ⚙️ Configuration Details

### Code Quality Tools

**Pylint** (`.pylintrc`)
- Max line length: 120 characters
- Max attributes per class: 7
- Max function arguments: 5

**Flake8** (`.flake8`)
- Max line length: 120 characters
- Ignores: E203, W503, E501

**Black** (`pyproject.toml`)
- Line length: 120 characters
- Python target: 3.11+

**isort** (`pyproject.toml`)
- Follows Black configuration
- Groups imports in standard order

### Secrets Detection

**TruffleHog**
- Scans all files for exposed secrets
- Checks: API keys, tokens, credentials, private keys
- Runs on: All branches

**detect-secrets**
- Pattern-based detection
- Configured in `.detect-secrets.cfg`
- Detects: AWS keys, GitHub tokens, Stripe keys, etc.

## 🚨 Handling False Positives

### Ignore Specific Secrets
Add comments to your code to exclude false positives:

```python
password = "hardcoded_password"  # pragma: allowlist secret
```

### Update detect-secrets Baseline
Create a baseline to reduce false positives:

```bash
pip install detect-secrets
detect-secrets scan --all-files > .secrets.baseline
```

## 🔐 Adding Secrets to GitHub Actions (Optional)

If using SonarQube/SonarCloud:

1. **Get your token**: Login to SonarCloud/SonarQube
2. **Add to GitHub**:
   - Go to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add:
     - Name: `SONAR_HOST_URL`, Value: `https://sonarcloud.io`
     - Name: `SONAR_TOKEN`, Value: `<your-token>`

## 📝 Customizing the Workflow

### Exclude Specific Files
Edit `.github/workflows/code-quality-and-secrets-scan.yml`:

```yaml
- name: Run pylint
  run: |
    pylint **/*.py --ignore=tests,migrations
```

### Add More Security Tools
Examples to add to the workflow:

```yaml
- name: Run Bandit (Security)
  run: bandit -r . -ll || true

- name: Check Dependencies
  run: safety check || true
```

### Require Checks to Pass
To prevent merging when checks fail, add branch protection:
1. Settings → Branches → Add Rule
2. Require status checks to pass before merging
3. Select the checks you want to require

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow not triggered | Check Settings → Actions is enabled; push to `main`/`develop` |
| TruffleHog fails | Verify default branch name in repo settings |
| CodeQL timeout | Large repos may timeout; can increase timeout or exclude paths |
| False secret alerts | Add comments with `pragma: allowlist secret` or update baseline |
| Python version error | Check your code uses Python 3.11+ syntax |

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [TruffleHog GitHub](https://github.com/trufflesecurity/trufflehog)
- [CodeQL Documentation](https://codeql.github.com/)
- [SonarQube Docs](https://docs.sonarqube.org/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/)

## ✅ Checklist

- [ ] Committed all new files to repository
- [ ] Pushed changes to GitHub
- [ ] Verified workflow appears in Actions tab
- [ ] Workflow runs successfully on next commit
- [ ] Review results in Security or Actions tab
- [ ] (Optional) Set up branch protection rules
- [ ] (Optional) Configure SonarQube if desired

---

**Your CI/CD pipeline is now ready!** Every commit will be automatically scanned for code quality issues and security vulnerabilities.
