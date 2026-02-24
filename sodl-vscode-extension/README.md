# SODL Language Support for VS Code

Syntax highlighting for **SODL** (Specification Orchestration Definition Language) - a domain-specific language for controlled AI-driven code generation through explicit specifications.

## Features

- 🎨 **Syntax Highlighting** for `.sodl` files
- 🔧 **Auto-closing brackets** and quotes
- 📝 **Line comments** with `#`
- 🔤 **Keyword highlighting** for all SODL constructs
- 📦 **Smart indentation** support

## SODL Syntax Overview

SODL uses a Python-like indentation-based syntax. Here's a quick example:

```sodl
system "MyApp":
  version = "1.0.0"
  
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    database = "PostgreSQL"
  
  intent:
    primary = "Build a modern web application"
    outcomes = [
      "RESTful API with full CRUD operations",
      "User authentication and authorization"
    ]
  
  interface UserRepository:
    doc = "Repository for user data access"
    method create(user: UserInput) -> User
    method get_by_id(id: int) -> Optional[User]
    method delete(id: int) -> bool
  
  module UserAPI:
    requires = [UserRepository]
    api:
      endpoint "GET /users" -> List[User]
      endpoint "POST /users" -> User (201)
      endpoint "DELETE /users/{id}" -> Empty (204)
  
  policy CodeQuality:
    rule "All functions must have type hints" severity=high
    rule "Maintain test coverage above 80%" severity=medium
```

## Language Constructs

The extension highlights the following SODL constructs:

### Declaration Keywords
- `system`, `template`, `interface`, `module`, `pipeline`, `step`

### Control Keywords
- `extends`, `implements`, `exports`, `requires`, `owns`, `artifacts`, `override`

### Section Keywords
- `config`, `intent`, `stack`, `policy`, `rule`, `invariants`, `invariant`
- `method`, `doc`, `version`, `primary`, `outcomes`, `out_of_scope`
- `gate`, `output`, `require`, `modules`

### Types
- `str`, `int`, `float`, `bool`, `list`, `dict`, `any`

### Constants
- `true`, `false`
- Severity levels: `high`, `medium`, `low`

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/sodlspace/sodl-impl-v1.git
   cd sodl-impl-v1/sodl-vscode-extension
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Compile TypeScript:
   ```bash
   npm run compile
   ```

4. Run the extension (F5 in VS Code) or package it:
   ```bash
   npm install -g @vscode/vsce
   vsce package
   ```

5. Install the `.vsix` file in VS Code

## Usage

1. Open or create a file with `.sodl` extension
2. The syntax highlighting will activate automatically
3. Use `#` for line comments
4. Enjoy proper indentation and bracket matching

## Commands

The extension provides the following command:

- **SODL: Show Info** - Display information about SODL language

Access commands via `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) and type "SODL".

## Configuration

The extension contributes the following to VS Code:

- **Language ID**: `sodl`
- **File Extensions**: `.sodl`
- **Scope Name**: `source.sodl`

## Development

### Debugging

1. Open the extension folder in VS Code
2. Press `F5` to launch the Extension Development Host
3. Open a `.sodl` file to test syntax highlighting

### Building

```bash
# Compile TypeScript
npm run compile

# Watch mode
npm run watch

# Lint
npm run lint
```

## License

This extension is part of the SODL project. See the main repository for license information.

## Links

- [SODL Main Repository](https://github.com/sodlspace/sodl-impl-v1)
- [SODL Documentation](https://sodlspace.github.io/sodl-impl-v1/)
- [Report Issues](https://github.com/sodlspace/sodl-impl-v1/issues)
