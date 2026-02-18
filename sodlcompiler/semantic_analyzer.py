"""
Semantic analyzer for the SODL DSL
Validates the AST and reports semantic errors/warnings

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
from typing import Dict, Set, Union
from .ast import *
from .errors import ErrorReporter, get_global_error_reporter


class SemanticAnalyzer:
    def __init__(self, error_reporter: ErrorReporter = None):
        self.error_reporter = error_reporter or get_global_error_reporter()
        self.symbol_table: Dict[str, ASTNode] = {}
        self.interfaces: Set[str] = set()
        self.modules: Set[str] = set()
        self.systems: Set[str] = set()
        self.pipelines: Set[str] = set()
        self.templates: Dict[str, TemplateBlock] = {}
        self.resolved_templates: Set[str] = set()
        self.resolved_interfaces: Set[str] = set()

    def analyze(self, program: Program):
        """Multi-pass analysis: templates → template chains → interfaces → everything else"""
        # Pass 1: register all templates
        for stmt in program.statements:
            if isinstance(stmt, TemplateBlock):
                self.visit_TemplateBlock(stmt)
        # Pass 2: resolve template inheritance chains (multi-level)
        self._resolve_all_templates()
        # Pass 3a: register all interfaces (name only, so forward refs work)
        for stmt in program.statements:
            if isinstance(stmt, InterfaceBlock):
                self._register_interface(stmt)
        # Pass 3b: merge interface inheritance
        for stmt in program.statements:
            if isinstance(stmt, InterfaceBlock) and stmt.extends:
                self._merge_interface(stmt)
        # Pass 4: everything else (systems, modules, pipelines, policies)
        for stmt in program.statements:
            if not isinstance(stmt, (TemplateBlock, InterfaceBlock)):
                self.visit(stmt)
        # Pass 5: full visit of interfaces (type checking etc.)
        for stmt in program.statements:
            if isinstance(stmt, InterfaceBlock):
                self.visit_InterfaceBlock(stmt)
    
    def visit(self, node: ASTNode):
        """Visit a node and dispatch to the appropriate method"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: ASTNode):
        """Generic visit method for nodes without specific visitors"""
        for field_name, field_value in node.__dict__.items():
            if isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, ASTNode):
                        self.visit(item)
            elif isinstance(field_value, ASTNode):
                self.visit(field_value)
    
    def visit_TemplateBlock(self, node: TemplateBlock):
        """Register a template in the template registry"""
        name = node.name.value
        if name in self.templates:
            self.error_reporter.error(
                f"Duplicate template: {name}",
                node.line, node.column,
            )
        else:
            self.templates[name] = node
            self.symbol_table[name] = node

    def visit_SystemBlock(self, node: SystemBlock):
        """Visit a system block"""
        if node.extends:
            tmpl = self.templates.get(node.extends)
            if tmpl is None:
                self.error_reporter.error(
                    f"Extends unknown template: '{node.extends}'",
                    node.line, node.column,
                )
            else:
                self._merge_template(node, tmpl)

        # Apply explicit override/append/remove operators after template merge
        self._apply_override_ops(node)

        system_name = node.name.value
        if system_name in self.systems:
            self.error_reporter.error(
                f"Duplicate system name: {system_name}",
                node.line, node.column
            )
        else:
            self.systems.add(system_name)
            self.symbol_table[system_name] = node

        # Visit child nodes
        if node.stack_block:
            self.visit(node.stack_block)
        if node.intent_block:
            self.visit(node.intent_block)

    def _merge_template(self, node: Union[SystemBlock, TemplateBlock], tmpl: TemplateBlock):
        """Merge template fields into node — child values take precedence"""
        if node.stack_block is None and tmpl.stack_block:
            node.stack_block = tmpl.stack_block
        elif node.stack_block and tmpl.stack_block:
            merged = {**tmpl.stack_block.properties, **node.stack_block.properties}
            node.stack_block.properties = merged

        if node.intent_block is None and tmpl.intent_block:
            node.intent_block = tmpl.intent_block

        existing_policy_names = {p.name.name for p in (node.policies or [])}
        for p in tmpl.policies:
            if p.name.name not in existing_policy_names:
                node.policies = (node.policies or []) + [p]

    def _apply_override_ops(self, system: SystemBlock):
        """Apply explicit override/append/remove statements to the system block"""
        for op in system.override_ops:
            if len(op.path) != 2:
                self.error_reporter.error(
                    f"Override path must be 'block.field', got: '{'.'.join(op.path)}'",
                    op.line, op.column,
                )
                continue
            block_name, field_name = op.path
            if block_name == "stack":
                if system.stack_block is None:
                    system.stack_block = StackBlock()
                props = system.stack_block.properties
                if isinstance(op, OverrideStatement):
                    props[field_name] = op.value
                elif isinstance(op, AppendStatement):
                    existing = props.get(field_name, [])
                    if isinstance(existing, StringLiteral):
                        existing = [existing]
                    props[field_name] = existing + [op.value]
                elif isinstance(op, RemoveStatement):
                    existing = props.get(field_name, [])
                    if isinstance(existing, list):
                        props[field_name] = [v for v in existing if v.value != op.value.value]
            else:
                self.error_reporter.error(
                    f"Override path target '{block_name}' is not supported (only 'stack' is supported)",
                    op.line, op.column,
                )

    # ---------------------------------------------------------------
    # Template multi-level inheritance (Feature C)
    # ---------------------------------------------------------------

    def _resolve_all_templates(self):
        """Resolve template inheritance chains for all registered templates"""
        for name in list(self.templates.keys()):
            self._resolve_template_chain(name, set())

    def _resolve_template_chain(self, name: str, visiting: Set[str]):
        """Recursively resolve the inheritance chain for a single template"""
        if name in self.resolved_templates:
            return
        if name in visiting:
            self.error_reporter.error(
                f"Circular template inheritance involving: '{name}'",
                self.templates[name].line, self.templates[name].column,
            )
            return
        visiting = visiting | {name}
        tmpl = self.templates[name]
        if tmpl.extends:
            parent_name = tmpl.extends
            if parent_name not in self.templates:
                self.error_reporter.error(
                    f"Template '{name}' extends unknown template: '{parent_name}'",
                    tmpl.line, tmpl.column,
                )
            else:
                self._resolve_template_chain(parent_name, visiting)
                self._merge_template(tmpl, self.templates[parent_name])
        self.resolved_templates.add(name)

    # ---------------------------------------------------------------
    # Interface inheritance (Feature B)
    # ---------------------------------------------------------------

    def _register_interface(self, node: InterfaceBlock):
        """Register interface name in symbol table without full visitation"""
        interface_name = node.name.name
        if interface_name in self.interfaces:
            self.error_reporter.error(
                f"Duplicate interface name: {interface_name}",
                node.line, node.column,
            )
        else:
            self.interfaces.add(interface_name)
            self.symbol_table[interface_name] = node

    def _merge_interface(self, child: InterfaceBlock):
        """Merge parent interface methods and fields into child (child values win)"""
        parent = self.symbol_table.get(child.extends)
        if not isinstance(parent, InterfaceBlock):
            self.error_reporter.error(
                f"Interface '{child.name.name}' extends unknown interface: '{child.extends}'",
                child.line, child.column,
            )
            return
        # Merge methods: child methods with is_override=True replace parent method of same name;
        # new child methods are additive; parent methods not overridden are inherited.
        child_method_names = {m.name.name for m in (child.methods or [])}
        for m in (parent.methods or []):
            if m.name.name not in child_method_names:
                child.methods = (child.methods or []) + [m]
        # Merge fields: child fields take precedence
        child_field_names = {f.name.name for f in (child.fields or [])}
        for f in (parent.fields or []):
            if f.name.name not in child_field_names:
                child.fields = (child.fields or []) + [f]
        # Merge invariants
        existing_invs = {i.description.value for i in (child.invariants or [])}
        for inv in (parent.invariants or []):
            if inv.description.value not in existing_invs:
                child.invariants = (child.invariants or []) + [inv]

    def visit_InterfaceBlock(self, node: InterfaceBlock):
        """Visit an interface block (after inheritance has been merged)"""
        interface_name = node.name.name
        # Registration already happened in _register_interface; skip re-registration
        if interface_name not in self.interfaces:
            self.interfaces.add(interface_name)
            self.symbol_table[interface_name] = node

        # Visit child nodes
        if node.fields:
            for field in node.fields:
                self.visit(field)
        if node.models:
            for model in node.models:
                self.visit(model)
        if node.methods:
            for method in node.methods:
                self.visit(method)
        if node.invariants:
            for invariant in node.invariants:
                self.visit(invariant)
    
    def visit_ModuleBlock(self, node: ModuleBlock):
        """Visit a module block"""
        module_name = node.name.name
        if module_name in self.modules:
            self.error_reporter.error(
                f"Duplicate module name: {module_name}",
                node.line, node.column
            )
        else:
            self.modules.add(module_name)
            self.symbol_table[module_name] = node

        # Visit doc if present
        if node.doc:
            pass  # Just visit it if needed for further processing

        # Validate requires references
        if node.requires:
            for req in node.requires:
                if req.name not in self.interfaces and req.name not in self.modules:
                    self.error_reporter.error(
                        f"Reference to undefined interface or module: {req.name}",
                        req.line, req.column
                    )

        # Validate implements references
        if node.implements:
            for impl in node.implements:
                if impl.name not in self.interfaces:
                    self.error_reporter.error(
                        f"Reference to undefined interface: {impl.name}",
                        impl.line, impl.column
                    )

        # Validate exports references
        if node.exports:
            for exp in node.exports:
                if exp.name not in self.interfaces:
                    self.error_reporter.error(
                        f"Reference to undefined interface: {exp.name}",
                        exp.line, exp.column
                    )

        # Visit child nodes
        if node.api_block:
            self.visit(node.api_block)
        if node.invariants:
            for invariant in node.invariants:
                self.visit(invariant)
        if node.acceptance:
            for test in node.acceptance:
                self.visit(test)
    
    def visit_APIBlock(self, node: APIBlock):
        """Visit an API block"""
        if node.endpoints:
            for endpoint in node.endpoints:
                self.visit(endpoint)
        if node.models:
            for model in node.models:
                self.visit(model)
    
    def visit_ModelDefinition(self, node: ModelDefinition):
        """Visit a model definition"""
        # Check for duplicate field names
        field_names = set()
        for field in node.fields:
            if field.name.name in field_names:
                self.error_reporter.error(
                    f"Duplicate field name in model {node.name.name}: {field.name.name}",
                    field.line, field.column
                )
            else:
                field_names.add(field.name.name)
        
        # Visit child nodes
        for field in node.fields:
            self.visit(field)
    
    def visit_MethodDefinition(self, node: MethodDefinition):
        """Visit a method definition"""
        # Check for duplicate parameter names
        param_names = set()
        for param_name, param_type in node.params:
            if param_name.name in param_names:
                self.error_reporter.error(
                    f"Duplicate parameter name in method {node.name.name}: {param_name.name}",
                    param_name.line, param_name.column
                )
            else:
                param_names.add(param_name.name)
        
        # Visit child nodes
        for param_name, param_type in node.params:
            self.visit(param_type)
        self.visit(node.return_type)
    
    def visit_TypeAnnotation(self, node: TypeAnnotation):
        """Visit a type annotation"""
        # Check if the base type is valid
        known_types = {
            'str', 'int', 'float', 'bool', 'UUID', 'datetime',
            'Optional', 'List', 'Dict', 'Any'
        }
        
        # For generic types like Optional[type] or List[type], check the inner type
        if node.is_optional or node.is_list:
            if node.generic_arg:
                self.visit(node.generic_arg)
        else:
            # For simple types, check if it's a known type
            if node.base_type not in known_types and node.base_type not in self.symbol_table:
                self.error_reporter.warning(
                    f"Unknown type: {node.base_type}",
                    node.line, node.column
                )
    
    def visit_PipelineBlock(self, node: PipelineBlock):
        """Visit a pipeline block"""
        pipeline_name = node.name.value
        if pipeline_name in self.pipelines:
            self.error_reporter.error(
                f"Duplicate pipeline name: {pipeline_name}",
                node.line, node.column
            )
        else:
            self.pipelines.add(pipeline_name)
            self.symbol_table[pipeline_name] = node
        
        # Visit child nodes
        for step in node.steps:
            self.visit(step)
    
    def visit_StepBlock(self, node: StepBlock):
        """Visit a step block"""
        # Validate module references in the step
        if node.modules:
            for module_ref in node.modules:
                if module_ref.name not in self.modules:
                    self.error_reporter.error(
                        f"Reference to undefined module: {module_ref.name}",
                        module_ref.line, module_ref.column
                    )

    def visit_PolicyBlock(self, node: PolicyBlock):
        """Visit a policy block"""
        policy_name = node.name.name
        if policy_name in self.symbol_table:
            self.error_reporter.error(
                f"Duplicate policy name: {policy_name}",
                node.line, node.column
            )
        else:
            self.symbol_table[policy_name] = node

        # Visit child nodes (rules)
        for rule in node.rules:
            self.visit(rule)