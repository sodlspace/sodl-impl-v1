# Changelog

All notable changes to the SODL Language Support extension will be documented in this file.

## [0.1.0] - 2024-02-24

### Added
- Initial release of SODL Language Support
- Syntax highlighting for `.sodl` files
- Support for all SODL keywords and constructs:
  - Declaration keywords: `system`, `template`, `interface`, `module`, `pipeline`, `step`
  - Control keywords: `extends`, `implements`, `exports`, `requires`, `owns`, `artifacts`, `override`
  - Section keywords: `config`, `intent`, `stack`, `policy`, `rule`, `invariants`, etc.
  - Built-in types: `str`, `int`, `float`, `bool`, `list`, `dict`, `any`
  - Constants: `true`, `false`, severity levels
- Language configuration:
  - Line comments with `#`
  - Auto-closing brackets and quotes
  - Python-like indentation support
  - Folding support with `#region`/`#endregion`
- Basic extension command: "SODL: Show Info"

### Technical
- TextMate grammar for syntax highlighting
- TypeScript-based extension structure
- Debug configuration for Extension Development Host
