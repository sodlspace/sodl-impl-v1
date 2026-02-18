"""
Error reporting system for the SODL compiler

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
from enum import Enum
from typing import NamedTuple, List, Optional


class ErrorLevel(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class Diagnostic(NamedTuple):
    level: ErrorLevel
    message: str
    line: int
    column: int
    filename: Optional[str] = None
    
    def __str__(self):
        location = f"{self.filename}:{self.line}:{self.column}" if self.filename else f"line {self.line}, column {self.column}"
        return f"[{self.level.value}] {location}: {self.message}"


class ErrorReporter:
    def __init__(self, filename: Optional[str] = None):
        self.diagnostics: List[Diagnostic] = []
        self.filename = filename
    
    def error(self, message: str, line: int = 0, column: int = 0):
        """Report an error"""
        diag = Diagnostic(ErrorLevel.ERROR, message, line, column, self.filename)
        self.diagnostics.append(diag)
        return diag
    
    def warning(self, message: str, line: int = 0, column: int = 0):
        """Report a warning"""
        diag = Diagnostic(ErrorLevel.WARNING, message, line, column, self.filename)
        self.diagnostics.append(diag)
        return diag
    
    def info(self, message: str, line: int = 0, column: int = 0):
        """Report an informational message"""
        diag = Diagnostic(ErrorLevel.INFO, message, line, column, self.filename)
        self.diagnostics.append(diag)
        return diag
    
    def has_errors(self) -> bool:
        """Check if there are any errors"""
        return any(diag.level == ErrorLevel.ERROR for diag in self.diagnostics)
    
    def has_warnings(self) -> bool:
        """Check if there are any warnings"""
        return any(diag.level == ErrorLevel.WARNING for diag in self.diagnostics)
    
    def get_errors(self) -> List[Diagnostic]:
        """Get all errors"""
        return [diag for diag in self.diagnostics if diag.level == ErrorLevel.ERROR]
    
    def get_warnings(self) -> List[Diagnostic]:
        """Get all warnings"""
        return [diag for diag in self.diagnostics if diag.level == ErrorLevel.WARNING]
    
    def get_infos(self) -> List[Diagnostic]:
        """Get all info messages"""
        return [diag for diag in self.diagnostics if diag.level == ErrorLevel.INFO]
    
    def print_diagnostics(self):
        """Print all diagnostics"""
        for diag in self.diagnostics:
            print(diag)
    
    def clear(self):
        """Clear all diagnostics"""
        self.diagnostics.clear()


# Global error reporter instance
_global_reporter = ErrorReporter()


def get_global_error_reporter() -> ErrorReporter:
    """Get the global error reporter instance"""
    return _global_reporter


def reset_global_error_reporter(filename: Optional[str] = None):
    """Reset the global error reporter"""
    global _global_reporter
    _global_reporter = ErrorReporter(filename)