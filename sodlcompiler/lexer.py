"""
Lexer for the SODL DSL

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
import re
from enum import Enum
from typing import List, NamedTuple


class TokenType(Enum):
    # Keywords
    SYSTEM = "SYSTEM"
    INTERFACE = "INTERFACE"
    MODULE = "MODULE"
    PIPELINE = "PIPELINE"
    METHOD = "METHOD"
    ENDPOINT = "ENDPOINT"
    MODEL = "MODEL"
    FIELD = "FIELD"
    IMPLEMENTS = "IMPLEMENTS"
    EXPORTS = "EXPORTS"
    REQUIRES = "REQUIRES"
    OWNS = "OWNS"
    API = "API"
    INVAR = "INVAR"  # invariants shortened
    INVARIANT = "INVARIANT"
    ACCEPTANCE = "ACCEPTANCE"
    TEST = "TEST"
    ARTIFACTS = "ARTIFACTS"
    STACK = "STACK"
    INTENT = "INTENT"
    PRIMARY = "PRIMARY"
    OUTCOMES = "OUTCOMES"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    CONFIG = "CONFIG"
    STEP = "STEP"
    OUTPUT = "OUTPUT"
    REQUIRE = "REQUIRE"
    GATE = "GATE"
    MODULES = "MODULES"
    TEMPLATE = "TEMPLATE"
    EXTENDS = "EXTENDS"
    OVERRIDE = "OVERRIDE"
    APPEND = "APPEND"
    REMOVE = "REMOVE"
    PLUS_EQUALS = "PLUS_EQUALS"    # +=
    MINUS_EQUALS = "MINUS_EQUALS"  # -=

    # Literals
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    
    # Operators and punctuation
    EQUALS = "EQUALS"          # =
    COLON = "COLON"            # :
    COMMA = "COMMA"            # ,
    DOT = "DOT"                # .
    HYPHEN = "HYPHEN"          # -
    LPAREN = "LPAREN"          # (
    RPAREN = "RPAREN"          # )
    LBRACKET = "LBRACKET"      # [
    RBRACKET = "RBRACKET"      # ]
    LBRACE = "LBRACE"          # {
    RBRACE = "RBRACE"          # }
    LT = "LT"                  # <
    GT = "GT"                  # >
    ARROW = "ARROW"            # ->
    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    
    # Special values
    OPTIONAL = "OPTIONAL"
    LIST = "LIST"
    UUID = "UUID"
    DATETIME = "DATETIME"
    POLICY = "POLICY"

    EOF = "EOF"


class Token(NamedTuple):
    type: TokenType
    value: str
    line: int
    column: int


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        
        # Define token patterns as (regex, token_type) tuples
        # NOTE: Order matters - longer matches should come before shorter ones
        self.token_patterns = [
            # Comments - though not in the example, good to have
            (r'#.*', None),  # Skip comments
            
            # Keywords
            (r'\bsystem\b', TokenType.SYSTEM),
            (r'\binterface\b', TokenType.INTERFACE),
            (r'\bmodule\b', TokenType.MODULE),
            (r'\bpipeline\b', TokenType.PIPELINE),
            (r'\bmethod\b', TokenType.METHOD),
            (r'\bendpoint\b', TokenType.ENDPOINT),
            (r'\bmodel\b', TokenType.MODEL),
            (r'\bfield\b', TokenType.FIELD),
            (r'\bimplements\b', TokenType.IMPLEMENTS),
            (r'\bexports\b', TokenType.EXPORTS),
            (r'\brequires\b', TokenType.REQUIRES),
            (r'\bowns\b', TokenType.OWNS),
            (r'\bapi\b', TokenType.API),
            (r'\binvariants\b', TokenType.INVAR),
            (r'\binvariant\b', TokenType.INVARIANT),
            (r'\bacceptance\b', TokenType.ACCEPTANCE),
            (r'\btest\b', TokenType.TEST),
            (r'\bartifacts\b', TokenType.ARTIFACTS),
            (r'\bstack\b', TokenType.STACK),
            (r'\bintent\b', TokenType.INTENT),
            (r'\bprimary\b', TokenType.PRIMARY),
            (r'\boutcomes\b', TokenType.OUTCOMES),
            (r'\bout_of_scope\b', TokenType.OUT_OF_SCOPE),
            (r'\bconfig\b', TokenType.CONFIG),
            (r'\bstep\b', TokenType.STEP),
            (r'\boutput\b', TokenType.OUTPUT),
            (r'\brequire\b', TokenType.REQUIRE),
            (r'\bgate\b', TokenType.GATE),
            (r'\bmodules\b', TokenType.MODULES),
            (r'\btemplate\b', TokenType.TEMPLATE),
            (r'\bextends\b', TokenType.EXTENDS),
            (r'\boverride\b', TokenType.OVERRIDE),
            (r'\bappend\b', TokenType.APPEND),
            (r'\bremove\b', TokenType.REMOVE),

            # Special types
            (r'\bOptional\b', TokenType.OPTIONAL),
            (r'\bList\b', TokenType.LIST),
            (r'\bUUID\b', TokenType.UUID),
            (r'\bdatetime\b', TokenType.DATETIME),
            (r'\bpolicy\b', TokenType.POLICY),
            
            # Operators and punctuation
            (r'\+=', TokenType.PLUS_EQUALS),
            (r'-=', TokenType.MINUS_EQUALS),
            (r'->', TokenType.ARROW),
            (r'<', TokenType.LT),
            (r'>', TokenType.GT),
            (r'=', TokenType.EQUALS),
            (r':', TokenType.COLON),
            (r',', TokenType.COMMA),
            (r'\.', TokenType.DOT),
            (r'-', TokenType.HYPHEN),
            (r'\(', TokenType.LPAREN),
            (r'\)', TokenType.RPAREN),
            (r'\[', TokenType.LBRACKET),
            (r'\]', TokenType.RBRACKET),
            (r'\{', TokenType.LBRACE),
            (r'\}', TokenType.RBRACE),
            
            # String literals (both single and double quoted)
            (r'"([^"\\]|\\.)*"', TokenType.STRING),
            (r"'([^'\\]|\\.)*'", TokenType.STRING),
            
            # Numbers
            (r'\d+', TokenType.NUMBER),
            
            # Identifiers (must come after keywords)
            (r'[a-zA-Z_][a-zA-Z0-9_-]*', TokenType.IDENTIFIER),
            
            # Whitespace - handled specially
            (r'[ \t]+', None),  # Skip regular whitespace between tokens
            (r'\n', TokenType.NEWLINE),
        ]
        
        # Track indentation levels
        self.indent_stack = [0]
        self.at_line_start = True
    
    def tokenize(self) -> List[Token]:
        """Tokenize the input text with indentation handling"""
        tokens = []
        
        while self.pos < len(self.text):
            # Check if we're at the beginning of a line
            if self.pos > 0 and self.text[self.pos - 1] == '\n':
                self.at_line_start = True
            
            matched = False
            
            for pattern, token_type in self.token_patterns:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                
                if match:
                    value = match.group(0)
                    
                    # Handle indentation at line start
                    if self.at_line_start and token_type in (None,) and pattern == r'[ \t]+':
                        # This is indentation whitespace at the start of a line
                        indent_size = self._calculate_indent_size(value)
                        
                        # Determine if we need INDENT or DEDENT tokens
                        current_indent = self.indent_stack[-1]
                        
                        if indent_size > current_indent:
                            # New indentation level
                            self.indent_stack.append(indent_size)
                            tokens.append(Token(TokenType.INDENT, "", self.line, 1))
                        elif indent_size < current_indent:
                            # Dedent - pop indentation levels
                            while len(self.indent_stack) > 1 and indent_size < self.indent_stack[-1]:
                                self.indent_stack.pop()
                                tokens.append(Token(TokenType.DEDENT, "", self.line, 1))
                            
                            if indent_size != self.indent_stack[-1]:
                                raise IndentationError(f"Inconsistent indentation at line {self.line}")
                        
                        # Skip the indentation whitespace
                        self._advance(len(value))
                        self.at_line_start = False  # No longer at line start after processing indentation
                        matched = True
                        break
                    
                    # If at line start and we see a non-whitespace, non-newline token,
                    # check if we need to generate DEDENT tokens (indentation is 0)
                    if self.at_line_start and token_type not in (None, TokenType.NEWLINE) and pattern != r'[ \t]+':
                        # This is a non-whitespace token at line start (no indentation)
                        # Generate DEDENT tokens to go back to indentation level 0
                        while len(self.indent_stack) > 1 and 0 < self.indent_stack[-1]:
                            self.indent_stack.pop()
                            tokens.append(Token(TokenType.DEDENT, "", self.line, 1))
                        self.at_line_start = False
                    
                    # Handle regular tokens
                    if token_type is None:
                        if pattern == r'#.*':  # Comment
                            self._advance(len(value))
                        elif pattern == r'[ \t]+':  # Regular whitespace between tokens
                            self._advance(len(value))
                        else:
                            self._advance(len(value))
                    elif token_type == TokenType.NEWLINE:
                        # Process newline
                        tokens.append(Token(token_type, value, self.line, self.column))
                        self._advance(len(value))
                        self.at_line_start = True
                    else:
                        # Regular token
                        tokens.append(Token(token_type, value, self.line, self.column))
                        self._advance(len(value))
                        self.at_line_start = False
                    
                    matched = True
                    break
            
            if not matched:
                raise SyntaxError(f"Illegal character '{self.text[self.pos]}' at line {self.line}, column {self.column}")
        
        # Add final DEDENT tokens to close all scopes
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, "", self.line, self.column))
        
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
    
    def _calculate_indent_size(self, whitespace):
        """Calculate the indentation size considering tabs as 4 spaces"""
        size = 0
        for char in whitespace:
            if char == ' ':
                size += 1
            elif char == '\t':
                # Align to next multiple of 4
                size = ((size // 4) + 1) * 4
        return size
    
    def _advance(self, count: int):
        """Advance the position counter"""
        for char in self.text[self.pos:self.pos + count]:
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        self.pos += count


def lex(text: str) -> List[Token]:
    """Convenience function to tokenize text"""
    lexer = Lexer(text)
    return lexer.tokenize()


if __name__ == "__main__":
    # Test the lexer with a simple example
    sample_code = '''system "AdvancedTodoApp":
  version = "1.0.0"
  stack:
    language = "Python 3.12"
'''
    
    tokens = lex(sample_code)
    for token in tokens:
        print(f"{token.type.value}: '{token.value}' at {token.line}:{token.column}")