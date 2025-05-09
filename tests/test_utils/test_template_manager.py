import pytest
from app.utils.template_manager import TemplateManager

@pytest.fixture
def template_manager():
    return TemplateManager()

def test_apply_email_styles(template_manager):
    raw_html = "<h1>Title</h1><p>Hello <a href='#'>world</a></p><footer>Bye</footer>"
    styled = template_manager._apply_email_styles(raw_html)

    assert 'style=' in styled
    assert '<h1 style=' in styled
    assert '<p style=' in styled
    assert '<footer style=' in styled
    assert '<a' in styled and 'style="color: #0056b3' in styled  # Updated assertion

def test_render_template_combines_content(monkeypatch, template_manager):
    # Mock the _read_template method
    def mock_read_template(filename):
        if filename == 'header.md':
            return "# Header"
        elif filename == 'footer.md':
            return "_Footer_"
        elif filename == 'welcome.md':
            return "Hello, {name}!"

    monkeypatch.setattr(template_manager, '_read_template', mock_read_template)

    result = template_manager.render_template('welcome', name='Sylvia')
    
    assert "Hello, Sylvia!" in result
    assert "<h1" in result  # Header should convert to HTML h1
    assert "<em>Footer</em>" in result  # Markdown footer

def test_render_template_injects_context(monkeypatch, template_manager):
    monkeypatch.setattr(template_manager, '_read_template', lambda filename: "Hi {username}" if filename == "message.md" else "")
    result = template_manager.render_template('message', username="ChatGPT")
    assert "Hi ChatGPT" in result
