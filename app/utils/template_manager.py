import markdown2
from pathlib import Path
from bs4 import BeautifulSoup  # Ensure this is installed via `pip install beautifulsoup4`

class TemplateManager:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.templates_dir = self.root_dir / 'email_templates'

    def _read_template(self, filename: str) -> str:
        template_path = self.templates_dir / filename
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _apply_email_styles(self, html: str) -> str:
        styles = {
            'body': 'font-family: Arial, sans-serif; font-size: 16px; color: #333333; background-color: #ffffff; line-height: 1.5;',
            'h1': 'font-size: 24px; color: #333333; font-weight: bold; margin-top: 20px; margin-bottom: 10px;',
            'p': 'font-size: 16px; color: #666666; margin: 10px 0; line-height: 1.6;',
            'a': 'color: #0056b3; text-decoration: none; font-weight: bold;',
            'footer': 'font-size: 12px; color: #777777; padding: 20px 0;',
            'ul': 'list-style-type: none; padding: 0;',
            'li': 'margin-bottom: 10px;'
        }

        soup = BeautifulSoup(html, "html.parser")

        # Apply styles to each matching tag
        for tag_name, style in styles.items():
            for tag in soup.find_all(tag_name):
                existing_style = tag.get("style", "")
                tag["style"] = f"{existing_style} {style}".strip()

        # Wrap everything in a styled <div>
        wrapper = soup.new_tag("div", style=styles["body"])
        wrapper.append(soup)
        return str(wrapper)

    def render_template(self, template_name: str, **context) -> str:
        header = self._read_template('header.md')
        footer = self._read_template('footer.md')
        main_template = self._read_template(f'{template_name}.md')
        main_content = main_template.format(**context)

        full_markdown = f"{header}\n{main_content}\n{footer}"
        html_content = markdown2.markdown(full_markdown)
        return self._apply_email_styles(html_content)
