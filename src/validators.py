import ast

def validate_python_code(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def contains_playwright_command(code: str) -> bool:
    return "page." in code
