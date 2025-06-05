# Miller 3 Data Scraper - Branch Management Guide

## 📋 Branch Structure

This repository uses a **3-branch workflow** for organized development:

```
main (production)
├── qa (quality assurance)
└── dev (development)
```

### Branch Purposes:

- **`main`** - Production-ready, stable code
- **`qa`** - Quality assurance testing environment  
- **`dev`** - Active development and new features

## 🚀 Quick Setup

### Option 1: Complete Setup (Recommended)
```bash
chmod +x "/Users/admin/Desktop/setup_complete_repo.sh"
"/Users/admin/Desktop/setup_complete_repo.sh"
```

### Option 2: Just Branches (if repo already exists)
```bash
chmod +x "/Users/admin/Desktop/setup_git_branches.sh"
"/Users/admin/Desktop/setup_git_branches.sh"
```

## 🔄 Development Workflow

### 1. Feature Development (dev branch)
```bash
git checkout dev
# Make your changes
git add .
git commit -m "Feature: Add new automation capability"
git push origin dev
```

### 2. Quality Assurance (qa branch)
```bash
git checkout qa
git merge dev
# Run tests and validation
git push origin qa
```

### 3. Production Release (main branch)
```bash
git checkout main
git merge qa
git push origin main
```

## 🛠️ Branch Management Helper

Use the branch helper script for common operations:

```bash
chmod +x "/Users/admin/Desktop/branch_helper.sh"
"/Users/admin/Desktop/branch_helper.sh" [command]
```

### Available Commands:
- `status` - Show current branch and status
- `list` - List all branches
- `dev` - Switch to dev branch
- `qa` - Switch to qa branch  
- `main` - Switch to main branch
- `sync` - Sync current branch with remote
- `merge-to-qa` - Merge dev into qa
- `merge-to-main` - Merge qa into main
- `push` - Push current branch to remote
- `pull` - Pull latest changes from remote
- `workflow` - Show recommended workflow

## 📝 Common Commands

### Switch Between Branches
```bash
git checkout dev     # Development work
git checkout qa      # Testing and QA
git checkout main    # Production releases
```

### Check Current Status
```bash
git status           # See current changes
git branch          # See all branches
git log --oneline   # See recent commits
```

### Sync with Remote
```bash
git pull origin dev    # Update dev branch
git pull origin qa     # Update qa branch  
git pull origin main   # Update main branch
```

## 🔒 Branch Protection (Recommended)

For production use, consider setting up branch protection rules on GitHub:

1. Protect `main` branch - require PR reviews
2. Protect `qa` branch - require status checks
3. Allow direct pushes to `dev` for development

## 🎯 Best Practices

1. **Always develop in `dev`** - Never commit directly to main
2. **Test in `qa`** - Use qa branch for thorough testing
3. **Release from `main`** - Only merge tested code to main
4. **Use descriptive commits** - Clear commit messages help track changes
5. **Regular syncing** - Keep branches up to date with remotes

## 🚨 Emergency Hotfixes

For urgent production fixes:
```bash
git checkout main
git checkout -b hotfix/critical-bug-fix
# Make emergency fix
git checkout main
git merge hotfix/critical-bug-fix
git push origin main
# Then merge back to qa and dev
```

## 📞 Support

If you need help with Git operations:
- Use the branch helper script
- Check Git documentation: `git help [command]`
- Refer to this guide for workflow questions
