"""
Tests for SODL MCP Server resources

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
from pathlib import Path


def test_documentation_resources():
    """Test that documentation resources return content"""
    # Import here to avoid issues during collection
    from sodl_mcp.server import (
        get_main_documentation,
        get_syntax_reference,
        get_examples_collection,
        get_api_reference,
        get_documentation_index,
        get_readme,
    )

    # Test main documentation
    main_doc = get_main_documentation()
    assert main_doc != "Documentation file not found"
    assert len(main_doc) > 1000  # Should be comprehensive
    assert "SODL" in main_doc or "sodl" in main_doc.lower()

    # Test syntax reference
    syntax_doc = get_syntax_reference()
    assert syntax_doc != "Syntax reference file not found"
    assert len(syntax_doc) > 500

    # Test examples collection
    examples_doc = get_examples_collection()
    assert examples_doc != "Examples collection file not found"
    assert len(examples_doc) > 500

    # Test API reference
    api_doc = get_api_reference()
    assert api_doc != "API reference file not found"
    assert len(api_doc) > 500

    # Test documentation index
    index_doc = get_documentation_index()
    assert index_doc != "Documentation index file not found"

    # Test README
    readme_doc = get_readme()
    assert readme_doc != "README file not found"


def test_example_resources():
    """Test that example SODL files return content"""
    from sodl_mcp.server import get_spec_sample, get_library_example

    # Test spec sample
    spec_sample = get_spec_sample()
    assert spec_sample != "Sample spec file not found"

    # Test library example
    library_example = get_library_example()
    assert library_example != "Library example file not found"


def test_resources_are_valid_sodl():
    """Test that example resources contain valid SODL syntax"""
    from sodl_mcp.server import get_spec_sample, get_library_example

    spec_sample = get_spec_sample()
    library_example = get_library_example()

    # Check for common SODL keywords
    sodl_keywords = ["system", "module", "interface", "pipeline"]

    # At least one should have these keywords (if files exist)
    if spec_sample != "Sample spec file not found":
        has_keywords = any(keyword in spec_sample.lower() for keyword in sodl_keywords)
        assert has_keywords, "Spec sample should contain SODL keywords"

    if library_example != "Library example file not found":
        has_keywords = any(keyword in library_example.lower() for keyword in sodl_keywords)
        assert has_keywords, "Library example should contain SODL keywords"


def test_documentation_contains_expected_sections():
    """Test that documentation contains expected sections"""
    from sodl_mcp.server import get_main_documentation, get_syntax_reference

    main_doc = get_main_documentation()
    if main_doc != "Documentation file not found":
        # Should contain section headers
        assert "#" in main_doc  # Markdown headers

    syntax_doc = get_syntax_reference()
    if syntax_doc != "Syntax reference file not found":
        # Should contain syntax patterns
        assert "#" in syntax_doc  # Markdown headers
