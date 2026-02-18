"""
Unit tests for the SODL compiler
"""
import unittest
from sodlcompiler.compiler import SODLCompiler
from sodlcompiler.errors import ErrorLevel


class TestSODLCompiler(unittest.TestCase):
    
    def test_basic_compilation(self):
        """Test basic compilation of a simple spec"""
        source = '''
system "TestApp":
  version = "1.0.0"
  stack:
    language = "Python 3.12"
    web = "FastAPI"
'''
        
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_basic.sodl")
        
        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        self.assertIsNotNone(compiler.get_ast())
    
    def test_interface_definition(self):
        """Test compilation of interface definitions"""
        source = '''
interface TestInterface:
  doc = "Test interface for compilation"
  method create(data: str) -> int
  method get(id: int) -> str
  invariants:
    invariant "All operations are thread-safe"
'''
        
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_interface.sodl")
        
        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        self.assertIsNotNone(compiler.get_ast())
    
    def test_module_definition(self):
        """Test compilation of module definitions"""
        source = '''
module TestModule:
  owns = ["Test functionality"]
  requires = [TestInterface]
  api:
    endpoint "GET /test" -> str
    model TestData:
      field id: int
      field name: str
  invariants:
    invariant "Module follows single responsibility principle"
  acceptance:
    test "handles valid requests correctly"
    test "returns appropriate errors for invalid requests"
  artifacts = ["test/module.py"]
'''
        
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_module.sodl")
        
        # Note: This might fail due to undefined TestInterface reference
        # That's expected behavior for our semantic analysis
        self.assertIsNotNone(compiler.get_ast())  # Should still parse syntactically
    
    def test_duplicate_names_error(self):
        """Test that duplicate names are caught by semantic analysis"""
        source = '''
system "TestApp":
  version = "1.0.0"

system "TestApp":
  version = "2.0.0"
'''
        
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_duplicate.sodl")
        
        self.assertFalse(success)  # Should fail due to duplicate system name
        self.assertTrue(compiler.has_errors())
    
    def test_invalid_reference_error(self):
        """Test that invalid references are caught by semantic analysis"""
        source = '''
module TestModule:
  requires = [NonExistentInterface]
'''
        
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_invalid_ref.sodl")
        
        # Compilation should succeed syntactically but have semantic errors
        self.assertIsNotNone(compiler.get_ast())
        self.assertTrue(compiler.has_errors())
    
    def test_model_field_validation(self):
        """Test validation of model field definitions"""
        source = '''
interface StoreInterface:
  method save(data: RecordModel) -> int

module TestModule:
  requires = [StoreInterface]
  api:
    model RecordModel:
      field id: int
      field id: str  # Duplicate field name - should cause error
'''
        
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_model_validation.sodl")
        
        # Should have semantic error for duplicate field name
        self.assertIsNotNone(compiler.get_ast())
        self.assertTrue(compiler.has_errors())


    # ------------------------------------------------------------------
    # template / extends tests
    # ------------------------------------------------------------------

    def test_template_definition(self):
        """Template block is parsed and registered without errors"""
        source = '''
template "BaseSystem":
  stack:
    language = "Python 3.12"
    web = "FastAPI"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_template_def.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        self.assertIsNotNone(compiler.get_ast())

    def test_system_extends_template(self):
        """System inherits stack from template when it has none of its own"""
        source = '''
template "BaseSystem":
  stack:
    language = "Python 3.12"
    web = "FastAPI"

system "MyApp" extends "BaseSystem":
  version = "1.0.0"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_extends.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())

        ast = compiler.get_ast()
        system_block = next(
            s for s in ast.statements
            if hasattr(s, 'name') and hasattr(s.name, 'value') and s.name.value == "MyApp"
        )
        self.assertIsNotNone(system_block.stack_block)
        self.assertEqual(system_block.stack_block.properties.get("language").value, "Python 3.12")

    def test_system_overrides_template(self):
        """Child system value overrides the same property from template"""
        source = '''
template "BaseSystem":
  stack:
    language = "Python 3.12"
    web = "FastAPI"

system "MyApp" extends "BaseSystem":
  stack:
    language = "Python 3.13"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_override.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())

        ast = compiler.get_ast()
        system_block = next(
            s for s in ast.statements
            if hasattr(s, 'name') and hasattr(s.name, 'value') and s.name.value == "MyApp"
        )
        self.assertEqual(system_block.stack_block.properties.get("language").value, "Python 3.13")
        self.assertEqual(system_block.stack_block.properties.get("web").value, "FastAPI")

    def test_extends_unknown_template(self):
        """Error is reported when system extends a non-existent template"""
        source = '''
system "MyApp" extends "NoSuchTemplate":
  version = "1.0.0"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_unknown_template.sodl")

        self.assertFalse(success)
        self.assertTrue(compiler.has_errors())

    def test_duplicate_template(self):
        """Error is reported when two templates share the same name"""
        source = '''
template "BaseSystem":
  stack:
    language = "Python 3.12"

template "BaseSystem":
  stack:
    language = "Go"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_duplicate_template.sodl")

        self.assertFalse(success)
        self.assertTrue(compiler.has_errors())


    # ------------------------------------------------------------------
    # Feature A: override / append / remove operators
    # ------------------------------------------------------------------

    def test_override_replaces_stack_property(self):
        """override operator replaces an inherited scalar stack property"""
        source = '''
template "Base":
  stack:
    language = "Python 3.12"
    web = "FastAPI"

system "MyApp" extends "Base":
  override stack.language = "Python 3.13"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_override_replace.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        ast = compiler.get_ast()
        system = next(s for s in ast.statements if hasattr(s, 'name') and hasattr(s.name, 'value') and s.name.value == "MyApp")
        self.assertEqual(system.stack_block.properties["language"].value, "Python 3.13")
        self.assertEqual(system.stack_block.properties["web"].value, "FastAPI")

    def test_append_adds_to_stack_list(self):
        """append operator creates a list-valued stack property"""
        source = '''
system "MyApp":
  stack:
    language = "Python 3.12"
  append stack.testing += "pytest"
  append stack.testing += "pytest-asyncio"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_append.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        ast = compiler.get_ast()
        system = next(s for s in ast.statements if hasattr(s, 'name') and hasattr(s.name, 'value') and s.name.value == "MyApp")
        testing = system.stack_block.properties.get("testing")
        self.assertIsInstance(testing, list)
        self.assertEqual(len(testing), 2)
        self.assertEqual(testing[0].value, "pytest")
        self.assertEqual(testing[1].value, "pytest-asyncio")

    def test_remove_from_stack_list(self):
        """remove operator deletes an item from a list-valued stack property"""
        source = '''
system "MyApp":
  stack:
    language = "Python 3.12"
  append stack.testing += "pytest"
  append stack.testing += "pytest-cov"
  remove stack.testing -= "pytest-cov"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_remove.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        ast = compiler.get_ast()
        system = next(s for s in ast.statements if hasattr(s, 'name') and hasattr(s.name, 'value') and s.name.value == "MyApp")
        testing = system.stack_block.properties.get("testing")
        self.assertIsInstance(testing, list)
        self.assertEqual(len(testing), 1)
        self.assertEqual(testing[0].value, "pytest")

    def test_override_without_extends(self):
        """override operator works on a system's own stack without extends"""
        source = '''
system "MyApp":
  stack:
    language = "Python 3.12"
  override stack.language = "Python 3.13"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_override_no_extends.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        ast = compiler.get_ast()
        system = next(s for s in ast.statements if hasattr(s, 'name') and hasattr(s.name, 'value') and s.name.value == "MyApp")
        self.assertEqual(system.stack_block.properties["language"].value, "Python 3.13")

    def test_override_invalid_path_error(self):
        """override with unsupported block target reports a semantic error"""
        source = '''
system "MyApp":
  stack:
    language = "Python 3.12"
  override intent.primary = "new"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_override_bad_path.sodl")

        self.assertFalse(success)
        self.assertTrue(compiler.has_errors())

    # ------------------------------------------------------------------
    # Feature B: interface extends InterfaceName
    # ------------------------------------------------------------------

    def test_interface_inherits_parent_methods(self):
        """Child interface inherits methods not defined in child"""
        source = '''
interface Storage:
  method save(data: str) -> str
  method retrieve(key: str) -> str

interface ImageStorage extends Storage:
  method get_thumbnail(key: str) -> str
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_iface_extends.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        ast = compiler.get_ast()
        child = next(s for s in ast.statements if isinstance(s, __import__('sodlcompiler.ast', fromlist=['InterfaceBlock']).InterfaceBlock) and s.name.name == "ImageStorage")
        method_names = {m.name.name for m in child.methods}
        self.assertIn("save", method_names)
        self.assertIn("retrieve", method_names)
        self.assertIn("get_thumbnail", method_names)

    def test_interface_override_method(self):
        """override method in child replaces the parent's method of the same name"""
        source = '''
interface Storage:
  method save(data: str) -> str

interface ImageStorage extends Storage:
  override method save(data: str) -> str
  method list_all() -> str
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_iface_override_method.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        ast = compiler.get_ast()
        from sodlcompiler.ast import InterfaceBlock
        child = next(s for s in ast.statements if isinstance(s, InterfaceBlock) and s.name.name == "ImageStorage")
        save_methods = [m for m in child.methods if m.name.name == "save"]
        self.assertEqual(len(save_methods), 1)
        self.assertTrue(save_methods[0].is_override)

    def test_interface_extends_unknown_error(self):
        """Error is reported when interface extends a non-existent interface"""
        source = '''
interface Child extends NonExistent:
  method foo() -> str
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_iface_unknown.sodl")

        self.assertFalse(success)
        self.assertTrue(compiler.has_errors())

    def test_interface_inherits_fields(self):
        """Child interface inherits field definitions from parent"""
        source = '''
interface Base:
  field id: str

interface Extended extends Base:
  field name: str
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_iface_fields.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        ast = compiler.get_ast()
        from sodlcompiler.ast import InterfaceBlock
        child = next(s for s in ast.statements if isinstance(s, InterfaceBlock) and s.name.name == "Extended")
        field_names = {f.name.name for f in child.fields}
        self.assertIn("id", field_names)
        self.assertIn("name", field_names)

    # ------------------------------------------------------------------
    # Feature C: multi-level template inheritance
    # ------------------------------------------------------------------

    def test_template_extends_template(self):
        """Template B inherits stack properties from template A"""
        source = '''
template "Base":
  stack:
    language = "Python 3.12"

template "WebBase" extends "Base":
  stack:
    web = "FastAPI"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_tmpl_extends_tmpl.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())

    def test_system_extends_derived_template(self):
        """System inherits accumulated stack from a multi-level template chain"""
        source = '''
template "Base":
  stack:
    language = "Python 3.12"

template "WebBase" extends "Base":
  stack:
    web = "FastAPI"

system "MyApp" extends "WebBase":
  version = "1.0.0"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_system_derived_tmpl.sodl")

        self.assertTrue(success)
        self.assertFalse(compiler.has_errors())
        ast = compiler.get_ast()
        system = next(s for s in ast.statements if hasattr(s, 'name') and hasattr(s.name, 'value') and s.name.value == "MyApp")
        self.assertIsNotNone(system.stack_block)
        self.assertEqual(system.stack_block.properties["language"].value, "Python 3.12")
        self.assertEqual(system.stack_block.properties["web"].value, "FastAPI")

    def test_template_extends_unknown_error(self):
        """Error is reported when template extends a non-existent template"""
        source = '''
template "Child" extends "NoSuchParent":
  stack:
    language = "Python 3.12"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_tmpl_unknown.sodl")

        self.assertFalse(success)
        self.assertTrue(compiler.has_errors())

    def test_circular_template_inheritance_error(self):
        """Error is reported when templates form a circular inheritance chain"""
        source = '''
template "A" extends "B":
  stack:
    language = "Python 3.12"

template "B" extends "A":
  stack:
    web = "FastAPI"
'''
        compiler = SODLCompiler()
        success = compiler.compile(source, "test_tmpl_circular.sodl")

        self.assertFalse(success)
        self.assertTrue(compiler.has_errors())


if __name__ == '__main__':
    unittest.main()