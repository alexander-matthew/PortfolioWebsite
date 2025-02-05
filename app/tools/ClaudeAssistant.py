import anthropic
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Union, Tuple
from pathlib import Path


class Claude:

    def __init__(self):
        load_dotenv()
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = anthropic.Anthropic(api_key=api_key)

    def ask_question(self, system_prompt: str, user_message: str) -> str:
        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_message
                            }
                        ]
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error calling Claude: {e}")
            raise


class SoftwareEngineer(Claude):
    """Generate daily motivational quotes using Claude"""

    def __init__(self):
        super().__init__()
        self.root_dir = Path('/Users/amatthew/PycharmProjects/PortfolioWebsite/app').resolve()
        self.target_extensions = {'.py', '.css'}
        self.ignore_dirs = {'.git', '.idea', '__pycache__', 'venv', '.venv', 'node_modules', '.env'}

    def create_new_feature(self, message: str) -> str:
        codebase = self.read_codebase()

        prompt = f"""
                You are an expert software engineer tasked with adding new features to the codebase. 
                We are building a website to serve as my resume inspired by 'myspace'.
                We are going to be working in plotly dash and python. Do not create react elements.

                Focus on:
                1. Code structure and organization
                2. Readability and brevity
                3. Best practices and patterns
                4. Performance implications
                5. Style (make it look cool)

                If possible, only re-write code where needed. Dont regurgitate code that already exists. 
                Here is our codebase:
                
                {codebase}
                """

        return self.ask_question(prompt, message)

    def read_codebase_structure(self) -> List[Path]:
        """ reads all files in the directory, ignores certain filetypes"""
        target_files = []

        for root, dirs, files in os.walk(self.root_dir):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.target_extensions:
                    # Get relative path from root_dir
                    rel_path = file_path.relative_to(self.root_dir)
                    target_files.append(rel_path)

        return sorted(target_files)

    def read_file_content(self, file_path: Path) -> Tuple[str, int]:
        """
        Returns:
            Tuple of (content, line_count)
        """
        full_path = self.root_dir / file_path
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                line_count = len(content.splitlines())
                return content, line_count
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            return f"Error reading file: {str(e)}", 0

    def read_codebase(self) -> str:
        """Format all found files into a structured text block."""
        files = self.read_codebase_structure()

        # Start with a header
        formatted_text = f"# Code Contents from {self.root_dir}\n"
        formatted_text += f"Total files found: {len(files)}\n\n"

        total_lines = 0

        # Group files by directory
        current_dir = None
        for file_path in files:
            # Check if we've moved to a new directory
            file_dir = str(file_path.parent)
            if file_dir != current_dir:
                current_dir = file_dir
                formatted_text += f"\n## Directory: {current_dir if current_dir != '.' else 'root'}\n\n"

            # Read and format file content
            content, line_count = self.read_file_content(file_path)
            total_lines += line_count

            # Add file header with metadata
            formatted_text += f"{'=' * 80}\n"
            formatted_text += f"File: {file_path.name}\n"
            formatted_text += f"Lines: {line_count}\n"
            formatted_text += f"{'=' * 80}\n\n"

            # Add the file content
            formatted_text += content.strip() + "\n\n"

        # Add summary at the end
        formatted_text += f"\n{'=' * 80}\n"
        formatted_text += f"Summary:\n"
        formatted_text += f"Total files: {len(files)}\n"
        formatted_text += f"Total lines of code: {total_lines}\n"

        return formatted_text

    def save_formatted_codebase(self, output_file: str = "codebase_contents.txt"):
        formatted_text = self.read_codebase()
        output_path = self.root_dir / output_file

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)

        return output_path


def main():
    # Initialize reader at current directory
    charles = SoftwareEngineer()
    charles.save_formatted_codebase()


if __name__ == "__main__":
    main()