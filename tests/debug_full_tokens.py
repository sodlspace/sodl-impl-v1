#!/usr/bin/env python3
"""Debug full spec file tokenization"""
from sodlcompiler.lexer import lex

# Read the spec file
with open('sodl/spec.sodl', 'r') as f:
    text = f.read()

print("Tokenizing full spec file...")
print("="*60 + "\n")

tokens = lex(text)

# Show tokens around line 19-20 (let's say from token at line 18 to line 22)
for i, token in enumerate(tokens):
    if 18 <= token.line <= 22:
        print(f"{i:3d}: {token.type.name:15s} {repr(token.value):50s} at {token.line}:{token.column}")
