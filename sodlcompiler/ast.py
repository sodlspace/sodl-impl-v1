"""
AST nodes for the SODL DSL

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
from dataclasses import dataclass, field


@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line: int = 0
    column: int = 0


@dataclass
class Identifier(ASTNode):
    """Identifier node"""
    name: str = ""

    def __post_init__(self):
        if self.name == "":
            raise ValueError("Identifier name cannot be empty")


@dataclass
class StringLiteral(ASTNode):
    """String literal node"""
    value: str = ""

    def __post_init__(self):
        # Allow empty string literals as they might be valid in some contexts
        pass


@dataclass
class NumberLiteral(ASTNode):
    """Number literal node"""
    value: int = 0


@dataclass
class TypeAnnotation(ASTNode):
    """Type annotation like str, int, Optional[type], List[type], Result<T, E>"""
    base_type: str = ""
    is_optional: bool = False
    is_list: bool = False
    generic_arg: Optional['TypeAnnotation'] = None  # For Optional[type] or List[type] - first generic arg
    generic_args: List['TypeAnnotation'] = field(default_factory=list)  # For multiple generic args like Result<T, E>

    def __post_init__(self):
        if self.base_type == "":
            raise ValueError("TypeAnnotation base_type cannot be empty")


@dataclass
class FieldDefinition(ASTNode):
    """Field definition inside a model"""
    name: Identifier = field(default_factory=Identifier)
    type_annotation: TypeAnnotation = field(default_factory=TypeAnnotation)
    constraints: Optional[str] = None  # Additional constraints like (1-3) or (ge=1, le=3)


@dataclass
class ModelDefinition(ASTNode):
    """Model definition inside a module"""
    name: Identifier = field(default_factory=Identifier)
    fields: List[FieldDefinition] = field(default_factory=list)


@dataclass
class MethodDefinition(ASTNode):
    """Method definition inside an interface"""
    name: Identifier = field(default_factory=Identifier)
    params: List[tuple[Identifier, TypeAnnotation]] = field(default_factory=list)  # List of (name, type) tuples
    return_type: TypeAnnotation = field(default_factory=TypeAnnotation)
    is_override: bool = False


@dataclass
class EndpointDefinition(ASTNode):
    """Endpoint definition inside a module API"""
    method: str = ""  # GET, POST, PUT, DELETE, etc.
    path: str = ""
    return_type: str = ""  # Return type description

    def __post_init__(self):
        if self.method == "":
            raise ValueError("EndpointDefinition method cannot be empty")
        if self.path == "":
            raise ValueError("EndpointDefinition path cannot be empty")


@dataclass
class InvariantDefinition(ASTNode):
    """Invariant definition"""
    description: StringLiteral = field(default_factory=StringLiteral)


@dataclass
class TestDefinition(ASTNode):
    """Test definition inside acceptance criteria"""
    description: StringLiteral = field(default_factory=StringLiteral)


@dataclass
class OverrideStatement(ASTNode):
    """Explicit override operator: override block.field = value"""
    path: List[str] = field(default_factory=list)
    value: 'StringLiteral' = field(default_factory=lambda: StringLiteral())


@dataclass
class AppendStatement(ASTNode):
    """Explicit append operator: append block.field += value"""
    path: List[str] = field(default_factory=list)
    value: 'StringLiteral' = field(default_factory=lambda: StringLiteral())


@dataclass
class RemoveStatement(ASTNode):
    """Explicit remove operator: remove block.field -= value"""
    path: List[str] = field(default_factory=list)
    value: 'StringLiteral' = field(default_factory=lambda: StringLiteral())


@dataclass
class TemplateBlock(ASTNode):
    """Template definition block — a reusable prototype for SystemBlock"""
    name: StringLiteral = field(default_factory=StringLiteral)
    version: Optional[StringLiteral] = None
    stack_block: Optional['StackBlock'] = None
    intent_block: Optional['IntentBlock'] = None
    policies: List['PolicyBlock'] = field(default_factory=list)
    extends: Optional[str] = None


@dataclass
class SystemBlock(ASTNode):
    """System definition block"""
    name: StringLiteral = field(default_factory=StringLiteral)
    version: Optional[StringLiteral] = None
    stack_block: Optional['StackBlock'] = None
    intent_block: Optional['IntentBlock'] = None
    policies: Optional[List['PolicyBlock']] = field(default_factory=list)
    extends: Optional[str] = None
    override_ops: List[Union[OverrideStatement, AppendStatement, RemoveStatement]] = field(default_factory=list)


@dataclass
class StackBlock(ASTNode):
    """Stack definition inside a system"""
    # Values are StringLiteral for scalar properties, List[StringLiteral] for list properties
    properties: dict = field(default_factory=dict)


@dataclass
class IntentBlock(ASTNode):
    """Intent definition inside a system"""
    primary: Optional[StringLiteral] = None
    outcomes: Optional[List[StringLiteral]] = field(default_factory=list)
    out_of_scope: Optional[List[StringLiteral]] = field(default_factory=list)


@dataclass
class InterfaceBlock(ASTNode):
    """Interface definition block"""
    name: Identifier = field(default_factory=Identifier)
    doc: Optional[StringLiteral] = None
    fields: Optional[List[FieldDefinition]] = field(default_factory=list)
    models: Optional[List[ModelDefinition]] = field(default_factory=list)
    methods: Optional[List[MethodDefinition]] = field(default_factory=list)
    invariants: Optional[List[InvariantDefinition]] = field(default_factory=list)
    extends: Optional[str] = None


@dataclass
class ModuleBlock(ASTNode):
    """Module definition block"""
    name: Identifier = field(default_factory=Identifier)
    doc: Optional[StringLiteral] = None
    owns: Optional[List[StringLiteral]] = field(default_factory=list)
    requires: Optional[List[Identifier]] = field(default_factory=list)
    implements: Optional[List[Identifier]] = field(default_factory=list)
    exports: Optional[List[Identifier]] = field(default_factory=list)
    api_block: Optional['APIBlock'] = None
    invariants: Optional[List[InvariantDefinition]] = field(default_factory=list)
    acceptance: Optional[List[TestDefinition]] = field(default_factory=list)
    artifacts: Optional[List[StringLiteral]] = field(default_factory=list)
    config_block: Optional['ConfigBlock'] = None


@dataclass
class APIBlock(ASTNode):
    """API definition inside a module"""
    endpoints: Optional[List[EndpointDefinition]] = field(default_factory=list)
    models: Optional[List[ModelDefinition]] = field(default_factory=list)


@dataclass
class ConfigBlock(ASTNode):
    """Configuration block inside a module"""
    properties: dict = field(default_factory=dict)


@dataclass
class RuleDefinition(ASTNode):
    """Rule definition inside a policy"""
    description: StringLiteral = field(default_factory=StringLiteral)
    severity: StringLiteral = field(default_factory=StringLiteral)  # e.g., "critical", "high", "medium", "low"


@dataclass
class PolicyBlock(ASTNode):
    """Policy definition block"""
    name: Identifier = field(default_factory=Identifier)
    rules: List[RuleDefinition] = field(default_factory=list)


@dataclass
class PipelineBlock(ASTNode):
    """Pipeline definition block"""
    name: StringLiteral = field(default_factory=StringLiteral)
    steps: List['StepBlock'] = field(default_factory=list)


@dataclass
class StepBlock(ASTNode):
    """Step definition inside a pipeline"""
    name: Identifier = field(default_factory=Identifier)
    output: Optional[StringLiteral] = None
    require: Optional[StringLiteral] = None
    modules: Optional[List[Identifier]] = field(default_factory=list)
    gate: Optional[StringLiteral] = None


@dataclass
class Program(ASTNode):
    """Root node representing the entire program"""
    statements: List[Union[SystemBlock, InterfaceBlock, ModuleBlock, PipelineBlock, 'PolicyBlock', TemplateBlock]] = field(default_factory=list)