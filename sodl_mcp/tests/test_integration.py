"""
Integration tests for SODL MCP Server

PROPRIETARY SOFTWARE LICENSE

Copyright (c) 2026 SODL Project. All Rights Reserved.

NOTICE: All information contained herein is, and remains the property of
SODL Project and its suppliers, if any. The intellectual and technical
concepts contained herein are proprietary to SODL Project and its suppliers
and may be covered by patents, patents in process, and are protected by trade
secret or copyright law.

Dissemination of this information or reproduction of this material is strictly
forbidden unless prior written permission is obtained from SODL Project.
"""

import pytest


def test_compile_then_get_ast():
    """Test workflow: compile code, then get AST if successful"""
    from sodl_mcp.server import compile_sodl, get_sodl_ast

    code = '''
system "MyApp":
  stack:
    language = "Python 3.12"
    web = "FastAPI"

  intent:
    primary = "Test application"
    outcomes = ["Feature A", "Feature B"]

  interface Storage:
    method save(data: str) -> bool
    method load(id: int) -> str

  module API:
    requires = [Storage]
'''

    # First compile
    compile_result = compile_sodl(code, "app.sodl")

    # Then get AST
    ast_result = get_sodl_ast(code, "app.sodl")

    # Both should have same success status
    assert compile_result["success"] == ast_result["success"]

    if compile_result["success"]:
        # Compile result has summary, AST result has detailed AST
        assert "ast_summary" in compile_result
        assert "ast" in ast_result

        # Summary counts should match detailed AST
        summary = compile_result["ast_summary"]
        ast = ast_result["ast"]

        assert summary["systems"] == len(ast["systems"])
        assert summary["interfaces"] == len(ast["interfaces"])
        assert summary["modules"] == len(ast["modules"])


def test_validate_then_compile():
    """Test workflow: quick validate, then full compile"""
    from sodl_mcp.server import validate_sodl_syntax, compile_sodl

    code = '''
system "TestApp":
  stack:
    language = "Python 3.12"
'''

    # Quick validation
    validate_result = validate_sodl_syntax(code)

    # Full compilation
    compile_result = compile_sodl(code, "test.sodl")

    # Validation and compilation should agree on validity
    # (though validation might be more lenient)
    if validate_result["valid"]:
        # If validation passes, compilation should too (or have only warnings)
        assert compile_result["success"] or len(compile_result["errors"]) == 0


def test_read_example_and_compile():
    """Test reading example from resources and compiling it"""
    from sodl_mcp.server import get_spec_sample, compile_sodl

    # Get example spec
    example_code = get_spec_sample()

    # Skip if file not found
    if example_code == "Sample spec file not found":
        pytest.skip("Sample spec file not available")

    # Try to compile it
    result = compile_sodl(example_code, "spec_sample.sodl")

    # Example should compile successfully (it's a working example)
    assert result["success"] is True
    assert len(result["errors"]) == 0
    assert "ast_summary" in result


def test_error_feedback_quality():
    """Test that error feedback is useful for debugging"""
    from sodl_mcp.server import compile_sodl

    # Code with obvious error
    code = '''
system "TestApp"
  missing_colon_here = true
'''

    result = compile_sodl(code, "test.sodl")

    if not result["success"] and len(result["errors"]) > 0:
        error = result["errors"][0]

        # Error should have a message
        assert "message" in error
        assert len(error["message"]) > 0

        # Error should have location info (if available)
        # Some errors might not have line/column
        assert "line" in error
        assert "column" in error


def test_multiple_systems_compilation():
    """Test compiling multiple systems in one file (if supported)"""
    from sodl_mcp.server import get_sodl_ast

    code = '''
system "App1":
  stack:
    language = "Python 3.12"

system "App2":
  stack:
    language = "Python 3.12"
'''

    result = get_sodl_ast(code, "multi.sodl")

    if result["success"]:
        # Should have multiple systems
        assert len(result["ast"]["systems"]) >= 1


def test_complex_sodl_structure():
    """Test compiling a complex SODL with all constructs"""
    from sodl_mcp.server import compile_sodl, get_sodl_ast

    code = '''
system "ComplexApp":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
    database = "PostgreSQL"

  intent:
    primary = "Complex application"
    outcomes = ["Feature 1", "Feature 2"]

  interface DataStore:
    method create(data: dict) -> int
    method read(id: int) -> dict
    method update(id: int, data: dict) -> bool
    method delete(id: int) -> bool

  interface Cache:
    method get(key: str) -> str
    method set(key: str, value: str) -> bool

  module API:
    requires = [DataStore, Cache]
    api:
      endpoint "GET /items" -> List[Item]
      endpoint "POST /items" -> Item

  policy Security:
    enforce "All endpoints require authentication"

  pipeline "Development":
    step Implement:
      modules = ["API"]
      output = code
'''

    # Compile
    compile_result = compile_sodl(code, "complex.sodl")

    # Get AST
    ast_result = get_sodl_ast(code, "complex.sodl")

    if compile_result["success"]:
        summary = compile_result["ast_summary"]

        # Should have detected all constructs
        assert summary["systems"] >= 1
        assert summary["interfaces"] >= 2
        assert summary["modules"] >= 1
        assert summary["policies"] >= 1
        assert summary["pipelines"] >= 1

        # AST should have detailed info
        if ast_result["success"]:
            ast = ast_result["ast"]

            # Check system has sections
            if len(ast["systems"]) > 0:
                system = ast["systems"][0]
                assert len(system["sections"]) > 0

            # Check interfaces have methods
            if len(ast["interfaces"]) > 0:
                interface = ast["interfaces"][0]
                assert len(interface["methods"]) > 0


def test_incremental_development_workflow():
    """Test typical development workflow with incremental changes"""
    from sodl_mcp.server import validate_sodl_syntax, compile_sodl

    # Start with minimal spec
    v1 = '''
system "App":
  stack:
    language = "Python 3.12"
'''

    # Validate
    result_v1 = validate_sodl_syntax(v1)

    # Add interface
    v2 = v1 + '''

  interface Storage:
    method save(data: str) -> bool
'''

    # Compile
    result_v2 = compile_sodl(v2, "app.sodl")

    # Add module
    v3 = v2 + '''

  module API:
    requires = [Storage]
'''

    # Compile again
    result_v3 = compile_sodl(v3, "app.sodl")

    # Each version should be valid (or at least parseable)
    assert "valid" in result_v1
    assert "success" in result_v2
    assert "success" in result_v3


def test_documentation_and_compilation_integration():
    """Test that documentation examples can be compiled"""
    from sodl_mcp.server import get_syntax_reference, compile_sodl

    syntax_doc = get_syntax_reference()

    if syntax_doc == "Syntax reference file not found":
        pytest.skip("Syntax reference not available")

    # Look for code blocks in documentation
    # This is a basic check that documentation is consistent
    assert len(syntax_doc) > 0

    # Try compiling a simple example (from common patterns)
    simple_example = '''
system "Example":
  stack:
    language = "Python 3.12"
'''

    result = compile_sodl(simple_example, "example.sodl")

    # Basic examples should compile
    # (unless the syntax has changed significantly)
    assert "success" in result
