#!/usr/bin/env python3
"""
Debug the lexer step by step
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
    
    # Debug step by step
    step = 0
    while lexer.pos < len(lexer.text) and step < 20:  # Limit steps to prevent infinite loop
        print(f"\nStep {step}: pos={lexer.pos}, line={lexer.line}, col={lexer.column}")
        print(f"  Current char: '{lexer.text[lexer.pos] if lexer.pos < len(lexer.text) else 'EOF'}'")
        
        matched = False
        for pattern, token_type in lexer.token_patterns:
            regex = re.compile(pattern)
            match = regex.match(lexer.text, lexer.pos)
            
            if match:
                value = match.group(0)
                print(f"  Matched: '{value}' with pattern {pattern}")
                
                if token_type is None:
                    print(f"    Skipping (no token)")
                    lexer._advance(len(value))
                elif token_type == Lexer.TokenType.NEWLINE:
                    print(f"    Found NEWLINE, handling indentation...")
                    # Handle indentation after newline
                    indent_level, new_pos = lexer._get_indent_level(lexer.pos + len(value))
                    print(f"    Indent level: {indent_level}, new_pos: {new_pos}")
                    
                    # Update position to skip the indentation
                    lexer.pos = new_pos
                    lexer.column = indent_level + 1
                    print(f"    Updated pos to {lexer.pos}, column to {lexer.column}")
                    
                    # This is where the issue occurs - we need to handle INDENT tokens
                    tokens = lexer._handle_indentation(indent_level)
                    print(f"    Generated {len(tokens)} indentation tokens")
                    
                    lexer._advance(len(value))  # Advance past the newline
                else:
                    print(f"    Creating token: {token_type.value} with value '{value}'")
                    lexer._advance(len(value))
                
                matched = True
                break
        
        if not matched:
            print(f"  No match at position {lexer.pos}, char: '{lexer.text[lexer.pos]}'")
            break
        
        step += 1

if __name__ == "__main__":
    main()