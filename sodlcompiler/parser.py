"""
Parser for the SODL DSL

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
from typing import List, Optional, Union
from .lexer import Lexer, Token, TokenType
from .ast import *


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if self.tokens else None
    
    def advance(self):
        """Move to the next token"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def peek(self, offset: int = 1) -> Optional[Token]:
        """Look ahead at a token without advancing"""
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None
    
    def expect(self, token_type: TokenType, error_msg: str = None) -> Token:
        """Expect a specific token type, raise error if not found"""
        # Skip NEWLINE tokens that appear in unexpected places
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()

        if not self.current_token or self.current_token.type != token_type:
            if error_msg is None:
                error_msg = f"Expected {token_type.value}, got {self.current_token.type.value if self.current_token else 'EOF'}"
            raise SyntaxError(f"{error_msg} at line {self.current_token.line if self.current_token else 'unknown'}, column {self.current_token.column if self.current_token else 'unknown'}")

        token = self.current_token
        self.advance()
        return token
    
    def consume(self, token_type: TokenType) -> bool:
        """Consume a token if it matches the type, return True if consumed"""
        # Skip NEWLINE tokens that appear in unexpected places
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()

        if self.current_token and self.current_token.type == token_type:
            self.advance()
            return True
        return False
    
    def parse_program(self) -> Program:
        """Parse the entire program"""
        statements = []

        while self.current_token and self.current_token.type != TokenType.EOF:
            # Skip any NEWLINE/INDENT/DEDENT tokens between top-level statements
            while (self.current_token and
                   self.current_token.type in [TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT]):
                self.advance()

            if not self.current_token or self.current_token.type == TokenType.EOF:
                break

            if self.current_token.type == TokenType.SYSTEM:
                statements.append(self.parse_system_block())
            elif self.current_token.type == TokenType.INTERFACE:
                statements.append(self.parse_interface_block())
            elif self.current_token.type == TokenType.MODULE:
                statements.append(self.parse_module_block())
            elif self.current_token.type == TokenType.PIPELINE:
                statements.append(self.parse_pipeline_block())
            elif self.current_token.type == TokenType.POLICY:
                statements.append(self.parse_policy_block())
            elif self.current_token.type == TokenType.TEMPLATE:
                statements.append(self.parse_template_block())
            else:
                raise SyntaxError(f"Unexpected token {self.current_token.type.value} at line {self.current_token.line}, column {self.current_token.column}")

        return Program(statements=statements)
    
    def parse_system_block(self) -> SystemBlock:
        """Parse a system block"""
        start_line = self.current_token.line
        start_col = self.current_token.column
        self.expect(TokenType.SYSTEM)

        name = self.parse_string_literal()

        extends = None
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
        if self.current_token and self.current_token.type == TokenType.EXTENDS:
            self.advance()  # consume 'extends'
            extends = self.parse_string_literal().value

        self.expect(TokenType.COLON)

        # Parse the body of the system block
        version = None
        stack_block = None
        intent_block = None
        policies = []
        override_ops = []

        # Handle indented block
        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                # Check if this token belongs to the parent (program) level
                if self.current_token.type in [TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE, TokenType.PIPELINE]:
                    # This token belongs to the program level, exit this block
                    break

                if self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "version":
                    self.advance()  # consume 'version'
                    self.expect(TokenType.EQUALS)
                    version = self.parse_string_literal()
                elif self.current_token.type == TokenType.STACK:
                    self.advance()  # consume 'stack'
                    self.expect(TokenType.COLON)
                    stack_block = self.parse_stack_block()
                elif self.current_token.type == TokenType.INTENT:
                    self.advance()  # consume 'intent'
                    self.expect(TokenType.COLON)
                    intent_block = self.parse_intent_block()
                elif self.current_token.type == TokenType.POLICY:
                    # Handle policy blocks inside system
                    policy = self.parse_policy_block()
                    policies.append(policy)
                elif self.current_token.type == TokenType.OVERRIDE:
                    self.advance()  # consume 'override'
                    path = self._parse_dotted_path()
                    self.expect(TokenType.EQUALS)
                    value = self.parse_string_literal()
                    override_ops.append(OverrideStatement(path=path, value=value))
                elif self.current_token.type == TokenType.APPEND:
                    self.advance()  # consume 'append'
                    path = self._parse_dotted_path()
                    self.expect(TokenType.PLUS_EQUALS)
                    value = self.parse_string_literal()
                    override_ops.append(AppendStatement(path=path, value=value))
                elif self.current_token.type == TokenType.REMOVE:
                    self.advance()  # consume 'remove'
                    path = self._parse_dotted_path()
                    self.expect(TokenType.MINUS_EQUALS)
                    value = self.parse_string_literal()
                    override_ops.append(RemoveStatement(path=path, value=value))
                else:
                    raise SyntaxError(f"Unexpected token in system block: {self.current_token.type.value} at line {self.current_token.line}")

            # Only expect DEDENT if we exited normally, not due to a top-level token
            if self.current_token and self.current_token.type == TokenType.DEDENT:
                self.advance()  # consume the DEDENT

        return SystemBlock(
            name=name,
            version=version,
            stack_block=stack_block,
            intent_block=intent_block,
            policies=policies,
            extends=extends,
            override_ops=override_ops,
            line=start_line,
            column=start_col
        )
    
    def parse_template_block(self) -> TemplateBlock:
        """Parse a template block (reusable system prototype)"""
        start_line = self.current_token.line
        start_col = self.current_token.column
        self.expect(TokenType.TEMPLATE)

        name = self.parse_string_literal()

        extends = None
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
        if self.current_token and self.current_token.type == TokenType.EXTENDS:
            self.advance()  # consume 'extends'
            extends = self.parse_string_literal().value

        self.expect(TokenType.COLON)

        version = None
        stack_block = None
        intent_block = None
        policies = []

        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                if self.current_token.type in [
                    TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE,
                    TokenType.PIPELINE, TokenType.TEMPLATE,
                ]:
                    break

                if self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "version":
                    self.advance()
                    self.expect(TokenType.EQUALS)
                    version = self.parse_string_literal()
                elif self.current_token.type == TokenType.STACK:
                    self.advance()
                    self.expect(TokenType.COLON)
                    stack_block = self.parse_stack_block()
                elif self.current_token.type == TokenType.INTENT:
                    self.advance()
                    self.expect(TokenType.COLON)
                    intent_block = self.parse_intent_block()
                elif self.current_token.type == TokenType.POLICY:
                    policies.append(self.parse_policy_block())
                else:
                    raise SyntaxError(
                        f"Unexpected token in template block: {self.current_token.type.value} "
                        f"at line {self.current_token.line}"
                    )

            if self.current_token and self.current_token.type == TokenType.DEDENT:
                self.advance()

        return TemplateBlock(
            name=name,
            version=version,
            stack_block=stack_block,
            intent_block=intent_block,
            policies=policies,
            extends=extends,
            line=start_line,
            column=start_col,
        )

    def parse_stack_block(self) -> StackBlock:
        """Parse a stack block inside a system"""
        start_line = self.current_token.line
        properties = {}

        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                if self.current_token.type == TokenType.IDENTIFIER:
                    prop_name = self.current_token.value
                    self.advance()  # consume property name
                    self.expect(TokenType.EQUALS)
                    prop_value = self.parse_string_literal()
                    properties[prop_name] = prop_value
                else:
                    raise SyntaxError(f"Unexpected token in stack block: {self.current_token.type.value} at line {self.current_token.line}")

            self.expect(TokenType.DEDENT)

        return StackBlock(properties=properties, line=start_line)
    
    def parse_intent_block(self) -> IntentBlock:
        """Parse an intent block inside a system"""
        start_line = self.current_token.line
        primary = None
        outcomes = None
        out_of_scope = None

        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                # Check if this token belongs to a parent block (top-level tokens)
                if self.current_token.type in [TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE, TokenType.PIPELINE]:
                    # This token belongs to the parent program level, exit this block
                    break

                if self.current_token.type == TokenType.PRIMARY:
                    self.advance()  # consume 'primary'
                    self.expect(TokenType.EQUALS)
                    primary = self.parse_string_literal()
                elif self.current_token.type == TokenType.OUTCOMES:
                    self.advance()  # consume 'outcomes'
                    outcomes = self.parse_string_list()
                elif self.current_token.type == TokenType.OUT_OF_SCOPE:
                    self.advance()  # consume 'out_of_scope'
                    out_of_scope = self.parse_string_list()
                else:
                    raise SyntaxError(f"Unexpected token in intent block: {self.current_token.type.value} at line {self.current_token.line}")

            # Only expect DEDENT if we exited normally, not due to a top-level token
            if self.current_token and self.current_token.type == TokenType.DEDENT:
                self.advance()  # consume the DEDENT

        return IntentBlock(
            primary=primary,
            outcomes=outcomes,
            out_of_scope=out_of_scope,
            line=start_line
        )
    
    def parse_string_list(self) -> List[StringLiteral]:
        """Parse a list of string literals"""
        self.expect(TokenType.EQUALS)

        # Skip any NEWLINE/INDENT tokens that might appear after the equals
        while self.current_token and self.current_token.type in [TokenType.NEWLINE, TokenType.INDENT]:
            self.advance()

        self.expect(TokenType.LBRACKET)

        strings = []
        if self.current_token and self.current_token.type != TokenType.RBRACKET:
            while True:
                # Skip NEWLINE tokens between elements
                while self.current_token and self.current_token.type == TokenType.NEWLINE:
                    self.advance()

                strings.append(self.parse_string_literal())
                if not self.consume(TokenType.COMMA):
                    break

        # Handle the case where DEDENT tokens might appear before the closing bracket
        # Skip any DEDENT tokens that appear before the closing bracket
        while self.current_token and self.current_token.type == TokenType.DEDENT:
            self.advance()

        self.expect(TokenType.RBRACKET)

        # Skip any DEDENT tokens after the closing bracket
        while self.current_token and self.current_token.type == TokenType.DEDENT:
            self.advance()

        return strings
    
    def parse_interface_block(self) -> InterfaceBlock:
        """Parse an interface block"""
        start_line = self.current_token.line
        start_col = self.current_token.column
        self.expect(TokenType.INTERFACE)

        name = self.parse_identifier()

        extends = None
        while self.current_token and self.current_token.type == TokenType.NEWLINE:
            self.advance()
        if self.current_token and self.current_token.type == TokenType.EXTENDS:
            self.advance()  # consume 'extends'
            extends = self.parse_identifier().name

        self.expect(TokenType.COLON)

        doc = None
        fields = []
        models = []
        methods = []
        invariants = []

        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                # Check if this token belongs to the parent (program) level
                if self.current_token.type in [TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE, TokenType.PIPELINE]:
                    # This token belongs to the program level, exit this block
                    break

                if self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "doc":
                    self.advance()  # consume 'doc'
                    self.expect(TokenType.EQUALS)
                    doc = self.parse_string_literal()
                elif self.current_token.type == TokenType.FIELD:
                    # Parse field definition
                    self.advance()  # consume 'field'
                    field_name = self.parse_field_name()
                    self.expect(TokenType.COLON)
                    field_type = self.parse_type_annotation()

                    # Check for constraints in parentheses
                    constraints = None
                    if self.current_token and self.current_token.type == TokenType.LPAREN:
                        self.advance()  # consume '('
                        constraint_tokens = []
                        paren_count = 1

                        while paren_count > 0:
                            if self.current_token.type == TokenType.LPAREN:
                                paren_count += 1
                            elif self.current_token.type == TokenType.RPAREN:
                                paren_count -= 1

                            if paren_count > 0 and self.current_token:
                                constraint_tokens.append(self.current_token.value)
                                self.advance()
                            else:
                                break  # Don't consume the closing parenthesis here

                        constraints = ''.join(constraint_tokens)
                        self.expect(TokenType.RPAREN)  # Consume the final closing paren

                    fields.append(FieldDefinition(
                        name=field_name,
                        type_annotation=field_type,
                        constraints=constraints,
                        line=self.current_token.line if self.current_token else 0
                    ))
                elif self.current_token.type == TokenType.MODEL:
                    # Parse model definition inside interface
                    # Note: We don't call self.advance() here because parse_model_definition expects MODEL token
                    model_def = self.parse_model_definition()
                    models.append(model_def)
                elif self.current_token.type == TokenType.METHOD:
                    methods.append(self.parse_method_definition())
                elif self.current_token.type == TokenType.OVERRIDE:
                    self.advance()  # consume 'override'
                    m = self.parse_method_definition()
                    m.is_override = True
                    methods.append(m)
                elif self.current_token.type == TokenType.INVAR:
                    # Parse invariants block
                    self.advance()  # consume 'invariants'
                    self.expect(TokenType.COLON)
                    if self.consume(TokenType.INDENT):
                        while self.current_token and self.current_token.type != TokenType.DEDENT:
                            # Skip NEWLINE tokens inside invariants block
                            if self.current_token.type == TokenType.NEWLINE:
                                self.advance()
                                continue

                            # Check if this token belongs to a parent block
                            if self.current_token.type in [TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE, TokenType.PIPELINE]:
                                # This token belongs to the program level, exit this block
                                break

                            if self.current_token.type == TokenType.INVARIANT:
                                self.advance()  # consume 'invariant'
                                invariants.append(InvariantDefinition(
                                    description=self.parse_string_literal(),
                                    line=self.current_token.line if self.current_token else 0
                                ))
                            else:
                                raise SyntaxError(f"Expected 'invariant' in invariants block, got {self.current_token.type.value}")

                        # Only expect DEDENT if we exited normally from invariants block
                        if self.current_token and self.current_token.type == TokenType.DEDENT:
                            self.advance()  # consume the DEDENT
                else:
                    raise SyntaxError(f"Unexpected token in interface block: {self.current_token.type.value} at line {self.current_token.line}")

            # Only expect DEDENT if we exited normally, not due to a top-level token
            if self.current_token and self.current_token.type == TokenType.DEDENT:
                self.advance()  # consume the DEDENT

        return InterfaceBlock(
            name=name,
            doc=doc,
            fields=fields,
            models=models,
            methods=methods,
            invariants=invariants,
            extends=extends,
            line=start_line,
            column=start_col
        )
    
    def parse_method_definition(self) -> MethodDefinition:
        """Parse a method definition inside an interface"""
        start_line = self.current_token.line
        self.expect(TokenType.METHOD)
        
        name = self.parse_identifier()
        
        # Parse parameters in parentheses
        self.expect(TokenType.LPAREN)
        params = []
        
        if self.current_token and self.current_token.type != TokenType.RPAREN:
            while True:
                param_name = self.parse_identifier()
                self.expect(TokenType.COLON)
                param_type = self.parse_type_annotation()
                params.append((param_name, param_type))
                
                if not self.consume(TokenType.COMMA):
                    break
        
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.ARROW)
        return_type = self.parse_type_annotation()
        
        return MethodDefinition(
            name=name,
            params=params,
            return_type=return_type,
            line=start_line
        )
    
    def parse_module_block(self) -> ModuleBlock:
        """Parse a module block"""
        start_line = self.current_token.line
        start_col = self.current_token.column
        self.expect(TokenType.MODULE)

        name = self.parse_identifier()
        self.expect(TokenType.COLON)

        # Initialize all possible fields
        doc = None
        owns = None
        requires = None
        implements = None
        exports = None
        api_block = None
        invariants = []
        acceptance = []
        artifacts = None
        config_block = None

        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                # Check if this token belongs to the parent (program) level
                if self.current_token.type in [TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE, TokenType.PIPELINE]:
                    # This token belongs to the program level, exit this block
                    break

                if self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "doc":
                    self.advance()  # consume 'doc'
                    self.expect(TokenType.EQUALS)
                    doc = self.parse_string_literal()
                elif self.current_token.type in [TokenType.OWNS, TokenType.REQUIRES, TokenType.IMPLEMENTS,
                                               TokenType.EXPORTS, TokenType.ARTIFACTS]:
                    prop_name = self.current_token.type.name.lower()  # Convert OWNS to "owns"
                    self.advance()  # consume property name
                    if prop_name == "owns":
                        self.expect(TokenType.EQUALS)
                        owns = self.parse_string_list_from_brackets()
                    elif prop_name == "requires":
                        self.expect(TokenType.EQUALS)
                        requires = self.parse_identifier_list()
                    elif prop_name == "implements":
                        self.expect(TokenType.EQUALS)
                        implements = self.parse_identifier_list()
                    elif prop_name == "exports":
                        self.expect(TokenType.EQUALS)
                        exports = self.parse_identifier_list()
                    elif prop_name == "artifacts":
                        self.expect(TokenType.EQUALS)
                        artifacts = self.parse_string_list_from_brackets()
                    else:
                        raise SyntaxError(f"Unexpected property in module block: {prop_name} at line {self.current_token.line}")
                elif self.current_token.type == TokenType.API:
                    self.advance()  # consume 'api'
                    self.expect(TokenType.COLON)
                    api_block = self.parse_api_block()
                elif self.current_token.type == TokenType.INVAR:
                    # Parse invariants block
                    self.advance()  # consume 'invariants'
                    self.expect(TokenType.COLON)
                    if self.consume(TokenType.INDENT):
                        while self.current_token and self.current_token.type != TokenType.DEDENT:
                            # Skip NEWLINE tokens inside invariants block
                            if self.current_token.type == TokenType.NEWLINE:
                                self.advance()
                                continue

                            # Check if this token belongs to a parent block
                            if self.current_token.type in [TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE, TokenType.PIPELINE]:
                                # This token belongs to the program level, exit this block
                                break

                            if self.current_token.type == TokenType.INVARIANT:
                                self.advance()  # consume 'invariant'
                                invariants.append(InvariantDefinition(
                                    description=self.parse_string_literal(),
                                    line=self.current_token.line if self.current_token else 0
                                ))
                            else:
                                raise SyntaxError(f"Expected 'invariant' in invariants block, got {self.current_token.type.value}")

                        # Only expect DEDENT if we exited normally from invariants block
                        if self.current_token and self.current_token.type == TokenType.DEDENT:
                            self.advance()  # consume the DEDENT
                elif self.current_token.type == TokenType.ACCEPTANCE:
                    # Parse acceptance block
                    self.advance()  # consume 'acceptance'
                    self.expect(TokenType.COLON)
                    if self.consume(TokenType.INDENT):
                        while self.current_token and self.current_token.type != TokenType.DEDENT:
                            # Skip NEWLINE tokens inside acceptance block
                            if self.current_token.type == TokenType.NEWLINE:
                                self.advance()
                                continue

                            # Check if this token belongs to a parent block
                            if self.current_token.type in [TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE, TokenType.PIPELINE]:
                                # This token belongs to the program level, exit this block
                                break

                            if self.current_token.type == TokenType.TEST:
                                self.advance()  # consume 'test'
                                acceptance.append(TestDefinition(
                                    description=self.parse_string_literal(),
                                    line=self.current_token.line if self.current_token else 0
                                ))
                            else:
                                raise SyntaxError(f"Expected 'test' in acceptance block, got {self.current_token.type.value}")

                        # Only expect DEDENT if we exited normally from acceptance block
                        if self.current_token and self.current_token.type == TokenType.DEDENT:
                            self.advance()  # consume the DEDENT
                elif self.current_token.type == TokenType.CONFIG:
                    self.advance()  # consume 'config'
                    self.expect(TokenType.COLON)
                    config_block = self.parse_config_block()
                else:
                    raise SyntaxError(f"Unexpected token in module block: {self.current_token.type.value} at line {self.current_token.line}")

            # Only expect DEDENT if we exited normally, not due to a top-level token
            if self.current_token and self.current_token.type == TokenType.DEDENT:
                self.advance()  # consume the DEDENT

        return ModuleBlock(
            name=name,
            doc=doc,
            owns=owns,
            requires=requires,
            implements=implements,
            exports=exports,
            api_block=api_block,
            invariants=invariants,
            acceptance=acceptance,
            artifacts=artifacts,
            config_block=config_block,
            line=start_line,
            column=start_col
        )

    def parse_policy_block(self) -> PolicyBlock:
        """Parse a policy block"""
        start_line = self.current_token.line
        start_col = self.current_token.column
        self.expect(TokenType.POLICY)

        name = self.parse_identifier()
        self.expect(TokenType.COLON)

        rules = []

        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                # Check if this token belongs to the parent (program) level
                if self.current_token.type in [TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE, TokenType.PIPELINE]:
                    # This token belongs to the program level, exit this block
                    break

                if self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "rule":
                    self.advance()  # consume 'rule'
                    description = self.parse_string_literal()
                    
                    # Expect 'severity=' followed by a value
                    if self.current_token and self.current_token.value == "severity":
                        self.advance()  # consume 'severity'
                        self.expect(TokenType.EQUALS)
                        severity = self.parse_identifier()  # severity value like "high", "critical", etc.
                        
                        rules.append(RuleDefinition(
                            description=description,
                            severity=StringLiteral(value=severity.name, line=severity.line, column=severity.column),  # Convert identifier to string literal
                            line=self.current_token.line if self.current_token else 0
                        ))
                    else:
                        raise SyntaxError(f"Expected 'severity=' in rule definition, got {self.current_token.value if self.current_token else 'EOF'} at line {self.current_token.line if self.current_token else 'unknown'}")
                else:
                    raise SyntaxError(f"Unexpected token in policy block: {self.current_token.type.value} at line {self.current_token.line}")

            # Only expect DEDENT if we exited normally, not due to a top-level token
            if self.current_token and self.current_token.type == TokenType.DEDENT:
                self.advance()  # consume the DEDENT

        return PolicyBlock(
            name=name,
            rules=rules,
            line=start_line,
            column=start_col
        )

    def parse_api_block(self) -> APIBlock:
        """Parse an API block inside a module"""
        start_line = self.current_token.line
        endpoints = []
        models = []
        
        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                if self.current_token.type == TokenType.ENDPOINT:
                    endpoints.append(self.parse_endpoint_definition())
                elif self.current_token.type == TokenType.MODEL:
                    models.append(self.parse_model_definition())
                else:
                    raise SyntaxError(f"Unexpected token in api block: {self.current_token.type.value} at line {self.current_token.line}")

            self.expect(TokenType.DEDENT)
        
        return APIBlock(
            endpoints=endpoints,
            models=models,
            line=start_line
        )
    
    def parse_endpoint_definition(self) -> EndpointDefinition:
        """Parse an endpoint definition"""
        start_line = self.current_token.line
        self.expect(TokenType.ENDPOINT)
        
        # Parse endpoint format like "GET /api/todos" -> List[TodoResponse]
        endpoint_str = self.parse_string_literal().value
        
        # Extract HTTP method and path
        parts = endpoint_str.split(' ', 1)
        if len(parts) != 2:
            raise SyntaxError(f"Invalid endpoint format: {endpoint_str}")
        
        method = parts[0]
        path = parts[1]
        
        self.expect(TokenType.ARROW)
        
        # Parse return type - collect all tokens until newline
        return_type_tokens = []
        while self.current_token and self.current_token.type != TokenType.NEWLINE:
            return_type_tokens.append(self.current_token.value)
            self.advance()
        
        return_type = ' '.join(return_type_tokens)
        
        return EndpointDefinition(
            method=method,
            path=path,
            return_type=return_type,
            line=start_line
        )
    
    def parse_model_definition(self) -> ModelDefinition:
        """Parse a model definition inside an API block"""
        start_line = self.current_token.line
        self.expect(TokenType.MODEL)
        
        name = self.parse_identifier()
        self.expect(TokenType.COLON)
        
        fields = []
        
        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                if self.current_token.type == TokenType.FIELD:
                    self.advance()  # consume 'field'
                    field_name = self.parse_field_name()
                    self.expect(TokenType.COLON)
                    field_type = self.parse_type_annotation()

                    # Check for constraints in parentheses
                    constraints = None
                    if self.current_token and self.current_token.type == TokenType.LPAREN:
                        self.advance()  # consume '('
                        constraint_tokens = []
                        paren_count = 1

                        while paren_count > 0:
                            if self.current_token.type == TokenType.LPAREN:
                                paren_count += 1
                            elif self.current_token.type == TokenType.RPAREN:
                                paren_count -= 1

                            if paren_count > 0:
                                constraint_tokens.append(self.current_token.value)
                                self.advance()
                            else:
                                break  # Don't consume the closing parenthesis here

                        constraints = ''.join(constraint_tokens)
                        self.expect(TokenType.RPAREN)  # Consume the final closing paren

                    fields.append(FieldDefinition(
                        name=field_name,
                        type_annotation=field_type,
                        constraints=constraints,
                        line=self.current_token.line if self.current_token else 0
                    ))
                else:
                    raise SyntaxError(f"Expected 'field' in model definition, got {self.current_token.type.value}")

            self.expect(TokenType.DEDENT)
        
        return ModelDefinition(
            name=name,
            fields=fields,
            line=start_line
        )
    
    def parse_config_block(self) -> ConfigBlock:
        """Parse a config block inside a module"""
        start_line = self.current_token.line
        properties = {}

        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                if self.current_token.type == TokenType.IDENTIFIER:
                    prop_name = self.current_token.value
                    self.advance()  # consume property name
                    self.expect(TokenType.EQUALS)
                    prop_value = self.parse_string_literal()
                    properties[prop_name] = prop_value
                else:
                    raise SyntaxError(f"Unexpected token in config block: {self.current_token.type.value} at line {self.current_token.line}")

            self.expect(TokenType.DEDENT)

        return ConfigBlock(properties=properties, line=start_line)
    
    def parse_pipeline_block(self) -> PipelineBlock:
        """Parse a pipeline block"""
        start_line = self.current_token.line
        start_col = self.current_token.column
        self.expect(TokenType.PIPELINE)
        
        name = self.parse_string_literal()
        self.expect(TokenType.COLON)
        
        steps = []
        
        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                # Check if this token belongs to the parent (program) level
                if self.current_token.type in [TokenType.SYSTEM, TokenType.INTERFACE, TokenType.MODULE, TokenType.PIPELINE]:
                    # This token belongs to the program level, exit this block
                    break

                if self.current_token.type == TokenType.STEP:
                    steps.append(self.parse_step_block())
                else:
                    raise SyntaxError(f"Unexpected token in pipeline block: {self.current_token.type.value} at line {self.current_token.line}")

            # Only expect DEDENT if we exited normally, not due to a top-level token
            if self.current_token and self.current_token.type == TokenType.DEDENT:
                self.advance()  # consume the DEDENT
        
        return PipelineBlock(
            name=name,
            steps=steps,
            line=start_line,
            column=start_col
        )
    
    def parse_step_block(self) -> StepBlock:
        """Parse a step block inside a pipeline"""
        start_line = self.current_token.line
        self.expect(TokenType.STEP)

        name = self.parse_identifier()
        self.expect(TokenType.COLON)

        output = None
        require = None
        modules = None
        gate = None

        if self.consume(TokenType.INDENT):
            while self.current_token and self.current_token.type != TokenType.DEDENT:
                # Skip NEWLINE tokens inside blocks
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue

                if self.current_token.type in [TokenType.OUTPUT, TokenType.REQUIRE, TokenType.MODULES, TokenType.GATE]:
                    prop_name = self.current_token.type.name.lower()  # Convert OUTPUT to "output"
                    self.advance()  # consume property name
                    if prop_name == "output":
                        self.expect(TokenType.EQUALS)
                        # Output can be an identifier (like 'design', 'code', 'diff')
                        if self.current_token.type == TokenType.IDENTIFIER:
                            output = Identifier(name=self.current_token.value, line=self.current_token.line, column=self.current_token.column)
                            self.advance()
                        else:
                            output = self.parse_string_literal()
                    elif prop_name == "require":
                        self.expect(TokenType.EQUALS)
                        require = self.parse_string_literal()
                    elif prop_name == "modules":
                        self.expect(TokenType.EQUALS)
                        modules = self.parse_identifier_list()
                    elif prop_name == "gate":
                        self.expect(TokenType.EQUALS)
                        gate = self.parse_string_literal()
                    else:
                        raise SyntaxError(f"Unexpected property in step block: {prop_name} at line {self.current_token.line}")
                else:
                    raise SyntaxError(f"Unexpected token in step block: {self.current_token.type.value} at line {self.current_token.line}")

            self.expect(TokenType.DEDENT)

        return StepBlock(
            name=name,
            output=output,
            require=require,
            modules=modules,
            gate=gate,
            line=start_line
        )
    
    def _parse_dotted_path(self) -> List[str]:
        """Parse a dotted path like stack.language; each segment can be any token."""
        path = [self.current_token.value]
        self.advance()
        while self.current_token and self.current_token.type == TokenType.DOT:
            self.advance()  # consume '.'
            path.append(self.current_token.value)
            self.advance()
        return path

    def parse_string_literal(self) -> StringLiteral:
        """Parse a string literal"""
        # Skip any NEWLINE/INDENT tokens before the string literal
        while self.current_token and self.current_token.type in [TokenType.NEWLINE, TokenType.INDENT]:
            self.advance()

        token = self.expect(TokenType.STRING)
        # Remove quotes from the value
        value = token.value[1:-1]  # Remove first and last character (the quotes)
        return StringLiteral(value=value, line=token.line, column=token.column)
    
    def parse_identifier(self) -> Identifier:
        """Parse an identifier"""
        # Skip any NEWLINE/INDENT tokens before the identifier
        while self.current_token and self.current_token.type in [TokenType.NEWLINE, TokenType.INDENT]:
            self.advance()

        token = self.expect(TokenType.IDENTIFIER)
        return Identifier(name=token.value, line=token.line, column=token.column)
    
    def parse_field_name(self) -> Identifier:
        """Parse a field name which can be an identifier or a keyword"""
        # Skip any NEWLINE/INDENT tokens before the field name
        while self.current_token and self.current_token.type in [TokenType.NEWLINE, TokenType.INDENT]:
            self.advance()

        # Accept either an identifier or any keyword token as a field name
        if not self.current_token:
            raise SyntaxError("Expected field name, got EOF")
        
        # Get all keyword token types
        keyword_types = [getattr(TokenType, name) for name in dir(TokenType) if isinstance(getattr(TokenType, name), TokenType)]
        
        # If current token is an identifier or a keyword, accept it as a field name
        if self.current_token.type == TokenType.IDENTIFIER or self.current_token.type in keyword_types:
            token = self.current_token
            self.advance()
            return Identifier(name=token.value, line=token.line, column=token.column)
        else:
            raise SyntaxError(f"Expected field name (identifier or keyword), got {self.current_token.type.value}")

    def parse_number_literal(self) -> NumberLiteral:
        """Parse a number literal"""
        # Skip any NEWLINE/INDENT tokens before the number literal
        while self.current_token and self.current_token.type in [TokenType.NEWLINE, TokenType.INDENT]:
            self.advance()

        token = self.expect(TokenType.NUMBER)
        return NumberLiteral(value=int(token.value), line=token.line, column=token.column)

    def parse_type_annotation(self) -> TypeAnnotation:
        """Parse a type annotation like str, Optional[type], List[type], Result<T, E>, etc."""
        start_line = self.current_token.line
        start_col = self.current_token.column

        # Check if it's Optional[...] or List[...] (bracket syntax) - support both [] and <>
        if self.current_token.type == TokenType.OPTIONAL or (self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "Optional"):
            self.advance()  # consume 'Optional'
            # Support both square brackets and angle brackets
            if self.current_token.type == TokenType.LBRACKET:
                self.advance()  # consume '['
                inner_type = self.parse_type_annotation()
                self.expect(TokenType.RBRACKET)
            elif self.current_token.type == TokenType.LT:
                self.advance()  # consume '<'
                inner_type = self.parse_type_annotation()
                self.expect(TokenType.GT)
            else:
                self.expect(TokenType.LBRACKET)  # Maintain backward compatibility
            return TypeAnnotation(
                base_type=inner_type.base_type,
                is_optional=True,
                generic_arg=inner_type,
                line=start_line,
                column=start_col
            )
        elif self.current_token.type == TokenType.LIST or (self.current_token.type == TokenType.IDENTIFIER and self.current_token.value == "List"):
            self.advance()  # consume 'List'
            # Support both square brackets and angle brackets
            if self.current_token.type == TokenType.LBRACKET:
                self.advance()  # consume '['
                inner_type = self.parse_type_annotation()
                self.expect(TokenType.RBRACKET)
            elif self.current_token.type == TokenType.LT:
                self.advance()  # consume '<'
                inner_type = self.parse_type_annotation()
                self.expect(TokenType.GT)
            else:
                self.expect(TokenType.LBRACKET)  # Maintain backward compatibility
            return TypeAnnotation(
                base_type=inner_type.base_type,
                is_list=True,
                generic_arg=inner_type,
                line=start_line,
                column=start_col
            )
        elif self.current_token.type == TokenType.IDENTIFIER:
            # Check if it's a generic type with angle brackets, like Result<T, E>
            type_name = self.current_token.value
            self.advance()  # consume the type name
            
            # Check if there's a generic type parameter with angle brackets
            if self.current_token and self.current_token.type == TokenType.LT:
                self.advance()  # consume '<'
                
                # Parse the first generic argument
                first_generic_arg = self.parse_type_annotation()
                
                # Check if there are more generic arguments (comma-separated)
                generic_args = [first_generic_arg]
                while self.current_token and self.current_token.type == TokenType.COMMA:
                    self.advance()  # consume ','
                    generic_args.append(self.parse_type_annotation())
                
                # Expect closing '>'
                self.expect(TokenType.GT)
                
                # Store the first generic argument as the generic_arg for backward compatibility
                # Also store all generic args in the generic_args list
                return TypeAnnotation(
                    base_type=type_name,
                    generic_arg=generic_args[0] if generic_args else None,
                    generic_args=generic_args,
                    line=start_line,
                    column=start_col
                )
            else:
                # Simple type like str, int, TodoInput, etc.
                return TypeAnnotation(base_type=type_name, line=start_line, column=start_col)
        elif self.current_token.type == TokenType.UUID:
            # UUID is a special token type
            self.advance()  # consume 'UUID'
            return TypeAnnotation(base_type="UUID", line=start_line, column=start_col)
        elif self.current_token.type == TokenType.DATETIME:
            # datetime is a special token type
            self.advance()  # consume 'datetime'
            return TypeAnnotation(base_type="datetime", line=start_line, column=start_col)
        else:
            raise SyntaxError(f"Expected type annotation, got {self.current_token.type.value}")
    
    def parse_string_list_from_brackets(self) -> List[StringLiteral]:
        """Parse a list of string literals in brackets"""
        # Skip any NEWLINE/INDENT tokens that might appear before the bracket
        while self.current_token and self.current_token.type in [TokenType.NEWLINE, TokenType.INDENT]:
            self.advance()

        self.expect(TokenType.LBRACKET)

        strings = []
        if self.current_token and self.current_token.type != TokenType.RBRACKET:
            while True:
                # Skip NEWLINE tokens between elements
                while self.current_token and self.current_token.type == TokenType.NEWLINE:
                    self.advance()

                strings.append(self.parse_string_literal())
                if not self.consume(TokenType.COMMA):
                    break

        # Handle the case where DEDENT tokens might appear before the closing bracket
        # Skip any DEDENT tokens that appear before the closing bracket
        while self.current_token and self.current_token.type == TokenType.DEDENT:
            self.advance()

        self.expect(TokenType.RBRACKET)

        # Skip any DEDENT tokens after the closing bracket
        while self.current_token and self.current_token.type == TokenType.DEDENT:
            self.advance()

        return strings
    
    def parse_identifier_list(self) -> List[Identifier]:
        """Parse a list of identifiers or strings in brackets"""
        # Skip any NEWLINE/INDENT tokens that might appear before the bracket
        while self.current_token and self.current_token.type in [TokenType.NEWLINE, TokenType.INDENT]:
            self.advance()

        self.expect(TokenType.LBRACKET)

        identifiers = []
        if self.current_token and self.current_token.type != TokenType.RBRACKET:
            while True:
                # Skip NEWLINE tokens between elements
                while self.current_token and self.current_token.type == TokenType.NEWLINE:
                    self.advance()

                # Accept either identifiers or string literals
                if self.current_token.type == TokenType.STRING:
                    # Parse as string literal and convert to identifier
                    string_lit = self.parse_string_literal()
                    identifiers.append(Identifier(name=string_lit.value, line=string_lit.line, column=string_lit.column))
                else:
                    identifiers.append(self.parse_identifier())
                
                if not self.consume(TokenType.COMMA):
                    break

        self.expect(TokenType.RBRACKET)

        # Skip any DEDENT tokens after the closing bracket
        while self.current_token and self.current_token.type == TokenType.DEDENT:
            self.advance()

        return identifiers


def parse(tokens: List[Token]) -> Program:
    """Convenience function to parse tokens into an AST"""
    parser = Parser(tokens)
    return parser.parse_program()