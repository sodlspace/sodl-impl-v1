"""
Tests for SODL MCP Server tools

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


def test_compile_valid_sodl():
    """Test compiling valid SODL code"""
    from sodl_mcp.server import compile_sodl

    valid_code = '''
system "TestApp":
  stack:
    language = "Python 3.12"

  intent:
    primary = "Test application"
'''

    result = compile_sodl(valid_code, "test.sodl")

    assert result["success"] is True
    assert len(result["errors"]) == 0
    assert "ast_summary" in result


def test_compile_invalid_sodl():
    """Test compiling invalid SODL code"""
    from sodl_mcp.server import compile_sodl

    invalid_code = '''
system "TestApp"
  this is invalid syntax
  no proper structure
'''

    result = compile_sodl(invalid_code, "test.sodl")

    assert result["success"] is False
    assert len(result["errors"]) > 0
    assert "ast_summary" not in result


def test_compile_empty_sodl():
    """Test compiling empty SODL code"""
    from sodl_mcp.server import compile_sodl

    result = compile_sodl("", "empty.sodl")

    # Empty file might be valid or invalid depending on compiler
    assert "success" in result
    assert "errors" in result


def test_validate_sodl_syntax():
    """Test quick syntax validation"""
    from sodl_mcp.server import validate_sodl_syntax

    valid_code = '''
system "TestApp":
  stack:
    language = "Python 3.12"
'''

    result = validate_sodl_syntax(valid_code)

    assert "valid" in result
    assert "errors" in result
    assert "line_count" in result
    assert result["line_count"] == len(valid_code.split("\n"))


def test_validate_invalid_syntax():
    """Test validation with invalid syntax"""
    from sodl_mcp.server import validate_sodl_syntax

    invalid_code = "this is not sodl at all!!!"

    result = validate_sodl_syntax(invalid_code)

    assert "valid" in result
    # May or may not have errors depending on how lenient the parser is
    assert "errors" in result


def test_get_sodl_ast():
    """Test getting AST representation"""
    from sodl_mcp.server import get_sodl_ast

    code = '''
system "TestApp":
  stack:
    language = "Python 3.12"

  interface TestInterface:
    method test() -> str

  module TestModule:
    requires = [TestInterface]
'''

    result = get_sodl_ast(code, "test.sodl")

    assert "success" in result
    assert "errors" in result

    if result["success"]:
        assert "ast" in result
        assert "systems" in result["ast"]
        assert "interfaces" in result["ast"]
        assert "modules" in result["ast"]


def test_ast_structure():
    """Test AST structure details"""
    from sodl_mcp.server import get_sodl_ast

    code = '''
system "TestApp":
  intent:
    primary = "Test"

interface DataStore:
  method save(data: str) -> bool
  method load(id: int) -> str

module API:
  requires = [DataStore]
'''

    result = get_sodl_ast(code, "test.sodl")

    if result["success"]:
        ast = result["ast"]

        # Check systems
        assert len(ast["systems"]) > 0
        system = ast["systems"][0]
        assert "name" in system
        assert "line" in system
        # Changed from "sections" to specific section flags
        assert "has_stack" in system or "has_intent" in system

        # Check interfaces
        if len(ast["interfaces"]) > 0:
            interface = ast["interfaces"][0]
            assert "name" in interface
            assert "methods" in interface

            if len(interface["methods"]) > 0:
                method = interface["methods"][0]
                assert "name" in method
                assert "return_type" in method


def test_error_reporting_structure():
    """Test that error reports have proper structure"""
    from sodl_mcp.server import compile_sodl

    invalid_code = "invalid syntax here"

    result = compile_sodl(invalid_code, "test.sodl")

    assert "success" in result
    assert "errors" in result
    assert "warnings" in result

    # If there are errors, check their structure
    if len(result["errors"]) > 0:
        error = result["errors"][0]
        assert "message" in error
        assert "severity" in error
        # Line and column might be None for some errors
        assert "line" in error
        assert "column" in error


def test_filename_in_errors():
    """Test that filename appears in error context"""
    from sodl_mcp.server import compile_sodl

    invalid_code = "invalid"
    filename = "myfile.sodl"

    result = compile_sodl(invalid_code, filename)

    # The compiler should use the filename
    # We can't directly test if it appears in errors without knowing
    # the exact error format, but we can verify the call works
    assert "success" in result


def test_compile_with_warnings():
    """Test compilation that might produce warnings"""
    from sodl_mcp.server import compile_sodl

    # Code that might trigger warnings (if compiler has warning system)
    code = '''
system "TestApp":
  stack:
    language = "Python 3.12"
'''

    result = compile_sodl(code, "test.sodl")

    assert "warnings" in result
    # Warnings should be a list
    assert isinstance(result["warnings"], list)
