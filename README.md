# Markdown Issue Tracker
This repository contains a workflow script that automatically detects Markdown files in a specified folder, creates issues for each task listed, and closes issues as tasks are marked complete.


## Usage

1. [Configure Actions Permissions](#configure-actions-permissions)
2. [Create and Add a Personal Access Token for GitHub Actions](#creating-and-adding-a-personal-access-token-for-github-actions)

3. Create a workflow file named `use-common-workflow.yml` in the `/.github/workflows` directory of your repository with the following content:
```yml
name: Use Common Workflow

on:
  push:
    paths:
      - 'books/**.md'
  workflow_dispatch:

jobs:
  callCommonWorkflow:
    uses: hwahyeon/book-reading-actions-pat/.github/workflows/common-workflow.yml@main
    secrets: inherit
```


4. Place your Markdown files in the `/books/` directory. Each Markdown file should follow this structure:

```markdown
# Book Title

**Labels:** label1, label2

- [ ] Chapter 1
- [ ] Chapter 2
- [x] Chapter 3
```

5. Once the workflow file is added to the repository and changes are committed, GitHub Actions will automatically run the script to scan the books folder, create issues for unchecked tasks, and close issues for checked tasks.

6. Go to the `Actions` tab in your repository and ensure the workflow is enabled and configured correctly.

## Detailed Instructions

### Configure Actions Permissions
1. Click on the `Settings` tab of the repository where you want to apply this workflow.
2. Click `Actions` under `Code and automation`.
3. Under `Actions permissions`, select `Allow all actions and reusable workflows`.
4. Under `Workflow permissions`, select `Read and write permissions`.


### Creating and Adding a Personal Access Token for GitHub Actions
To enable full issue tracking functionality with GitHub Actions, you may need to use a Personal Access Token (PAT). Follow these steps to create and add a PAT to your repository.

#### Creating a Personal Access Token
1. GitHub `Settings` (Not repository Settings) → `Developer settings` → `Personal access tokens` → `Tokens (classic)` → `Generate new token`
2. In the `Note` field, enter a description for the token, e.g., "GitHub Actions Reading Token".
3. Select the expiration period under `Expiration` according to your needs.
4. Select the required permissions:
    - repo: Full control of private repositories.
    - workflow: Ability to trigger workflows.
    - admin: Full control of repository hooks.
    - Add additional permissions as needed.
5. Click the "Generate token" button.
6. Copy the generated token. It will only be shown once, so save it securely.

#### Adding the `Personal Access Token` to GitHub Secrets
1. Go to the `Settings` tab of the repository where you will use the `Personal Access Token`.
2. In the left sidebar, click on `Secrets and variables` → `Actions`.
3. Click the "New repository secret" button.
4. In the "Name" field, enter `PERSONAL_ACCESS_TOKEN`, and in the "Value" field, paste the previously copied Personal Access Token.
5. Click the "Add secret" button to save the token.


## Example
Given a Markdown file named `example_book.md` in the `/books/` folder with the following content:
```markdown
# Book Title

**Labels:** reading, example

- [ ] Chapter 1: Introduction
- [ ] Chapter 2: Getting Started with Examples
- [x] Chapter 3: Advanced Example
```

The script will:
- Create issues for "Introduction" and "Chapter 1" with titles in the format `[Book Title] Chapter: Chapter Title`, such as `[Example Book] Chapter1: Introduction`.
- Attach the specified labels (`reading`, `example`) to the created issues.
- Not create an issue for "Chapter 2" since it is marked as completed.
- Close the issue for "Chapter 2" if it is open.

## Markdown Issue Tracker GitHub Action Flowchart
```text
Start (Push to Repository / Manual Trigger)
          ↓
Check for Markdown File Changes in 'books' Directory
          ↓
Changed Markdown Files Found?  ----→ No ----→ End
          ↓
          Yes
          ↓
Load Issues Data from 'issues.json'
          ↓
Issues File Exists?  ----→ No ----→ Initialize Issues Data
          ↓
          Yes
          ↓
For Each Changed Markdown File:
          ↓
Extract Book Title and Labels
          ↓
Extract Unchecked Chapters
          ↓
For Each Unchecked Chapter:
          ↓
Issue Already Exists in issues.json? ----→ Yes ----→ Skip
          ↓
          No
          ↓
Create Issue with Labels
          ↓
Add New Issue Number to issues.json
          ↓
Extract Checked Chapters
          ↓
For Each Checked Chapter:
          ↓
Issue Already Exists and Open? ----→ No ----→ Skip
          ↓
          Yes
          ↓
Close Issue
          ↓
Remove Issue from issues.json
          ↓
Save Updated issues.json
          ↓
End
```
