# Quick Reference Guide

## Local Development Setup

### 1. Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### 2. Run Code Quality Checks Locally

```bash
# Format code with Black
black .

# Sort imports
isort .

# Lint with Pylint
pylint *.py

# Check style with Flake8
flake8 .

# Type checking (optional)
mypy .

# Detect secrets
detect-secrets scan --all-files .
```

### 3. Run All Checks (One Command)
```bash
# Format
black . && isort .

# Then lint
pylint *.py && flake8 .

# And scan for secrets
detect-secrets scan --all-files .
```

## GitHub Actions Workflow

### How It Works
1. **Triggers**: Automatically runs on every push and pull request to `main`/`develop`
2. **Jobs**: Three parallel scanning jobs:
   - Code Quality Checks (Pylint, Flake8, Black)
   - Secrets Detection (TruffleHog, detect-secrets)
   - GitHub Native Scanning (CodeQL)

### View Results
1. Go to **Actions** tab in GitHub
2. Click the latest workflow run
3. Review logs and results

### Check Security Alerts
1. Go to **Security** tab → **Code scanning alerts**
2. Review and remediate any issues

## Typical Workflow

```bash
# 1. Make changes to your code
# 2. Format and lint locally
black . && isort . && pylint *.py

# 3. Test locally
pytest

# 4. Commit and push
git add .
git commit -m "feat: add new feature"
git push origin your-branch

# 5. GitHub Actions automatically runs (check Actions tab)
# 6. Fix any issues the CI pipeline found
# 7. Push again - CI re-runs
# 8. Once all checks pass, create a Pull Request
```

## Common Issues & Solutions

### Issue: Code formatting differs from Black
**Solution**: Run `black . && isort .` before committing

### Issue: Pylint warnings
**Solution**: Fix warnings or add `# pylint: disable=warning-name` comment

### Issue: Secrets detected
**Solution**: 
1. Remove the secret from code
2. Add comment `# pragma: allowlist secret` if it's a false positive
3. Commit with clean history

### Issue: Workflow not running
**Solution**: 
1. Check branch is `main` or `develop`
2. Go to Settings → Actions → General and enable actions
3. Verify workflow file exists in `.github/workflows/`

## File Locations & What They Do

| File | Purpose |
|------|---------|
| `.github/workflows/code-quality-and-secrets-scan.yml` | Main CI workflow |
| `.pylintrc` | Pylint configuration |
| `.flake8` | Flake8 configuration |
| `pyproject.toml` | Black, isort, pytest config |
| `.detect-secrets.cfg` | Secrets detection config |
| `requirements-dev.txt` | Development dependencies |
| `.gitignore` | Files to exclude from Git |
| `.github/dependabot.yml` | Dependency updates |

## Enable Branch Protection (Peace of Mind)

1. Go to Settings → Branches
2. Click "Add rule"
3. Branch name pattern: `main`
4. Enable "Require status checks to pass"
5. Select your workflow checks
6. Save

Now no code can be merged without passing CI checks!

## Environment Variables for CI

If you need to add secrets (like SonarToken):
1. Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value
4. Reference in workflow: `${{ secrets.YOUR_SECRET_NAME }}`

---

**Need Help?** Check the full documentation in [SETUP.md](SETUP.md)
