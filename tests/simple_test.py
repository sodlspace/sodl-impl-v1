#!/usr/bin/env python3
"""
Simple test to debug the lexer issue
"""
from sodlcompiler.lexer import Lexer
import re

def main():
    # Simple test case
    text = 'system "AdvancedTodoApp":\n  version = "1.0.0"'
    
    print("Testing with simple text:")
    print(repr(text))
    print()
    
    lexer = Lexer(text)
    
    # Manually go through the tokenization process
    pos = 0
    while pos < len(text):
        matched = False
        
        for pattern, token_type in lexer.token_patterns:
            regex = re.compile(pattern)
            match = regex.match(text, pos)
            
            if match:
                value = match.group(0)
                print(f"Matched: '{value}' with pattern {pattern}, token_type: {token_type}")
                
                if token_type is None:
                    if pattern == r'[ \t]+':  # Whitespace
                        print(f"  Skipping whitespace: {repr(value)}")
                    elif pattern == r'#.*':  # Comment
                        print(f"  Skipping comment: {repr(value)}")
                else:
                    print(f"  Creating token: {token_type.value} with value '{value}'")
                
                pos += len(value)
                matched = True
                break
        
        if not matched:
            print(f"No match at position {pos}, char: '{text[pos]}' (ord: {ord(text[pos])})")
            break
    
    print("\nNow testing the actual lexer:")
    try:
        tokens = lexer.tokenize()
        print(f"Success! Generated {len(tokens)} tokens")
        for i, token in enumerate(tokens):
            print(f"  {i}: {token.type.value} '{token.value}' at {token.line}:{token.column}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()