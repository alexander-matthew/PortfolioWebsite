import os

import requests
import base64
from typing import List, Tuple
from urllib.parse import urlparse
import os
from flask.cli import load_dotenv


class GithubAPI:
    def __init__(self):
        load_dotenv()
        self.access_token = os.getenv("GITHUB_ACCESS_TOKEN")
        self.headers = {'Authorization': f"Bearer{self.access_token}",
                        'Accept': 'application/vnd.github.v3+json'
                        }
        self.repo_url = "https://github.com/alexander-matthew/PortfolioWebsite"
        self.base_url = 'https://api.github.com'
        self.target_extensions = {'.py', '.css'}


    def parse_repo_url(self) -> Tuple[str, str]:
        path = urlparse(self.repo_url).path.strip('/')
        parts = path.split('/')
        return parts[0], parts[1]


    def get_repo_contents(self, owner: str, repo: str, path: str = '') -> List[dict]:
        url = f'{self.base_url}/repos/{owner}/{repo}/contents/{path}'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_file_content(self, url: str) -> str:
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        content = response.json().get('content', '')
        return base64.b64decode(content).decode('utf-8')

    def fetch_target_files(self) -> List[Tuple[str, str]]:
        """
        Fetch all .py and .css files from a repository.
        Args:
            repo_url: Full GitHub repository URL
        Returns:
            List of tuples containing (file_path, content)
        """
        owner, repo = self.parse_repo_url()
        contents = []
        to_process = [('', [])]  # (path, breadcrumbs)

        while to_process:
            current_path, breadcrumbs = to_process.pop(0)
            try:
                items = self.get_repo_contents(owner, repo, current_path)

                if not isinstance(items, list):
                    items = [items]

                for item in items:
                    item_path = '/'.join([*breadcrumbs, item['name']])

                    if item['type'] == 'dir':
                        to_process.append((item['path'], [*breadcrumbs, item['name']]))

                    elif item['type'] == 'file':
                        if any(item['name'].endswith(ext) for ext in self.target_extensions):
                            try:
                                content = self.get_file_content(item['url'])
                                contents.append((item_path, content))
                                print(f"Fetched: {item_path}")
                            except Exception as e:
                                print(f"Error fetching {item_path}: {str(e)}")

            except Exception as e:
                print(f"Error accessing {current_path}: {str(e)}")
                continue

        return contents

if __name__ == "__main__":
    github = GithubAPI()
    try:
        files = github.fetch_target_files()
        print(f"\nFound {len(files)} matching files")
    except Exception as e:
        print(f"Error: {str(e)}")