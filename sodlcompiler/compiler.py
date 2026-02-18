"""
Main compiler class for the SODL DSL

Business Source License 1.1

Copyright (c) 2026 SODL Project License text copyright (c) 2017 MariaDB
Corporation Ab. "Business Source License" is a trademark of MariaDB
Corporation Ab.

Licensor: SODL Project

Licensed Work: SODL v0.3

Change Date: 2030-02-16

Change License: Apache License, Version 2.0

Additional Use Grant

You may use, copy, modify, create derivative works of, publicly perform,
publicly display, and redistribute the Licensed Work for any purpose,
including commercial purposes, provided that you do not use the Licensed
Work in a Competitive Offering.
"""
from typing import Optional
from .lexer import lex
from .parser import parse
from .semantic_analyzer import SemanticAnalyzer
from .errors import ErrorReporter, reset_global_error_reporter
from .ast import Program


class SODLCompiler:
    def __init__(self):
        self.error_reporter = ErrorReporter()
        self.ast: Optional[Program] = None
    
    def compile(self, source_code: str, filename: str = "<input>") -> bool:
        """
        Compile the source code and return True if compilation succeeds (no errors)
        """
        # Reset the error reporter
        self.error_reporter = ErrorReporter(filename)
        reset_global_error_reporter(filename)
        
        try:
            # Lexical analysis
            tokens = lex(source_code)
            
            # Syntactic analysis (parsing)
            self.ast = parse(tokens)
            
            # Semantic analysis
            analyzer = SemanticAnalyzer(self.error_reporter)
            analyzer.analyze(self.ast)
            
            return not self.error_reporter.has_errors()
        
        except Exception as e:
            self.error_reporter.error(str(e))
            return False
    
    def get_ast(self) -> Optional[Program]:
        """Get the parsed AST"""
        return self.ast
    
    def get_error_reporter(self) -> ErrorReporter:
        """Get the error reporter"""
        return self.error_reporter
    
    def has_errors(self) -> bool:
        """Check if there are compilation errors"""
        return self.error_reporter.has_errors()
    
    def has_warnings(self) -> bool:
        """Check if there are compilation warnings"""
        return self.error_reporter.has_warnings()
    
    def print_diagnostics(self):
        """Print all diagnostics"""
        self.error_reporter.print_diagnostics()


def compile_source(source_code: str, filename: str = "<input>") -> SODLCompiler:
    """Convenience function to compile source code"""
    compiler = SODLCompiler()
    compiler.compile(source_code, filename)
    return compiler