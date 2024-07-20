import os
import re
import json
from github import Github
from pathlib import Path

def main():
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    issues_file = Path('issues.json')
    if issues_file.exists():
        with issues_file.open('r', encoding='utf-8') as f:
            issues_data = json.load(f)
    else:
        issues_data = {}

    books_path = Path('books')
    for md_file in books_path.glob('*.md'):
        with md_file.open('r', encoding='utf-8') as file:
            content = file.read()
            book_title = content.split('\n')[0].strip('#').strip()
            print(f"Processing book: {book_title}")

            if book_title not in issues_data:
                issues_data[book_title] = {}

            # Extract labels
            labels_match = re.search(r'\*\*Labels:\*\* (.+)', content)
            labels = labels_match.group(1).split(', ') if labels_match else []

            chapters = re.findall(r'- \[\s\] (.+)', content)
            for chapter in chapters:
                chapter = chapter.strip()
                issue_title = f"[{book_title}] {chapter}"
                issue_body = f"Track the progress of reading chapter '{chapter}' in '{book_title}'."
                issue_exists = False
                for issue in repo.get_issues(state='open'):
                    if issue.title == issue_title and issue.body == issue_body:
                        issues_data[book_title][chapter] = issue.number
                        issue_exists = True
                        break
                if not issue_exists:
                    issue = repo.create_issue(title=issue_title, body=issue_body, labels=labels)
                    issues_data[book_title][chapter] = issue.number
                    print(f"Created issue: {issue_title}")

    with issues_file.open('w', encoding='utf-8') as f:
        json.dump(issues_data, f, indent=4)
    print(f"Updated issues data saved to {issues_file}")

if __name__ == "__main__":
    main()
