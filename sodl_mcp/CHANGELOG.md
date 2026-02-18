# Changelog

All notable changes to the sodl MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-02

### Added
- Initial release of sodl MCP Server
- FastMCP server implementation with stdio transport
- 8 documentation resources:
  - `sodl://docs/main` - Main documentation
  - `sodl://docs/syntax` - Syntax reference
  - `sodl://docs/examples` - Examples collection
  - `sodl://docs/api` - API reference
  - `sodl://docs/index` - Documentation index
  - `sodl://docs/readme` - README
  - `sodl://examples/spec_sample` - Sample spec
  - `sodl://examples/library_example` - Library example
- 3 compilation tools:
  - `compile_sodl()` - Full compilation with feedback
  - `validate_sodl_syntax()` - Quick syntax validation
  - `get_sodl_ast()` - Detailed AST inspection
- 1 prompt template:
  - `sodl_helper()` - Context-aware help prompts
- Comprehensive test suite (22 tests, 100% passing)
- Complete documentation (README, SETUP, examples)
- uv package manager support
- Development tools (pytest, black, ruff)

### Features
- Real-time sodl compilation and validation
- Detailed error reporting with line numbers
- AST analysis and inspection
- Integration with sodlcompiler module
- Stdio transport for MCP communication
- JSON response format

### Documentation
- Complete README with usage examples
- Detailed SETUP guide with troubleshooting
- Example MCP configuration files
- Comprehensive test coverage
- MIT License

### Testing
- 22 tests covering all features
- Resource access tests
- Compilation tool tests
- Integration workflow tests
- Error reporting validation

[0.1.0]: https://github.com/sodl/sodl-mcp/releases/tag/v0.1.0
