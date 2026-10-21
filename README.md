# Git Auto Contribution 🚀

A Python automation tool that simplifies Git workflows by detecting changed files, committing them individually, and pushing them to GitHub.

Instead of manually staging, committing, and pushing every file, run one Python script from your project directory.

## ✨ Features

- **Automatic change detection:** Detects modified, deleted, and untracked files.
- **Individual commits:** Creates a separate commit for each eligible file.
- **Automatic commit messages:** Generates messages such as `Add example.py`, `Update example.py`, and `Delete example.py`.
- **Automatic GitHub push:** Pushes commits to the configured remote repository.
- **Multi-project support:** Use the same script across different Git repositories.
- **Basic safety checks:** Checks for certain sensitive filenames and stops when it encounters some unsupported Git states.
- **No extra Python packages required:** Uses Python's standard library and the Git command-line tool.

## 🛠️ Requirements

- Python 3.9 or later
- Git installed and available in your terminal
- A Git repository connected to a remote, such as GitHub
- An upstream branch configured for the current branch
- GitHub authentication configured for pushing

## 📁 Project Structure

```text
Git-Auto-Contribution/
├── git_auto_contribute.py
└── README.md
```

## 🚀 Installation

### 1. Clone the repository

```powershell
git clone https://github.com/Arsalan-Dev-Cloud/git-auto-contribute.git
```

### 2. Enter the project directory

```powershell
cd git-auto-contribute
```

### 3. Check the requirements

```powershell
python --version
git --version
```

## 💻 Usage

You can run the script from any Git repository. You do not need to copy it into every project.

For example, to automate commits in a Python practice repository:

```powershell
cd "E:\Python-Practice"
python "E:\Git-Auto-Contribution\git_auto_contribute.py"
```

To use it with your AI learning repository:

```powershell
cd "E:\ai-from-scratch"
python "E:\Git-Auto-Contribution\git_auto_contribute.py"
```

Replace the example paths with your own project paths when necessary.

### How it works

1. Detects eligible file changes in the current Git repository.
2. Identifies a changed file.
3. Stages that file individually.
4. Generates an appropriate commit message.
5. Commits the file.
6. Pushes the commit to the configured remote.
7. Continues until eligible changes are processed or an error stops the automation.

## 🔧 Setting Up a New Project

For a new local project that is not yet connected to GitHub:

1. Create an empty repository on GitHub.
2. Open PowerShell in your local project directory.
3. Initialize Git if necessary.
4. Connect the GitHub remote.
5. Make and push the initial commit.
6. Run the automation script for subsequent changes.

Example:

```powershell
git init
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

Replace the URL with your actual repository URL. If the repository already has commits, reconcile its history before performing the initial push.

## 🔍 Verify Your Changes

Check the repository status:

```powershell
git status
```

View recent commits:

```powershell
git log -5 --oneline
```

Confirm the remote configuration:

```powershell
git remote -v
```

## ⚠️ Safety Notes

- Review your changes before running the script.
- Never commit passwords, API keys, access tokens, private keys, or other sensitive information.
- Filename-based checks cannot guarantee that file contents are safe.
- Automatic commits and pushes can publish unintended changes if you have not reviewed them.
- The script requires a suitable Git repository and configured upstream branch.
- Keep a backup of important work and inspect errors before rerunning the script.
- Git commit messages are generated automatically and may need improvement for more descriptive project history.

## 🎯 Use Cases

- Python practice repositories
- Daily AI-from-scratch learning projects
- Personal coding projects
- Educational repositories
- Small projects where individual file commits are useful

## 🧑‍💻 Author

**Arsalan-Dev-Cloud**

GitHub: [@Arsalan-Dev-Cloud](https://github.com/Arsalan-Dev-Cloud)

## 📄 License

No license has been specified yet. If you intend to distribute this project publicly, consider adding an appropriate open-source license.

---

⭐ If you find this project useful, consider starring the repository on GitHub.