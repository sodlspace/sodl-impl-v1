#!/usr/bin/env python3
"""Debug tokenization around line 19-20"""
from sodlcompiler.lexer import lex

# Sample text from spec.sodl around lines 17-22
text = '''interface TodoStore:
  doc = "Persistent storage for advanced todo items"
  method create(todo: TodoInput) -> TodoItem'''

print("Tokenizing:")
print(text)
print("\n" + "="*60 + "\n")

tokens = lex(text)
for i, token in enumerate(tokens):
    print(f"{i:3d}: {token.type.name:15s} '{token.value}' at {token.line}:{token.column}")
