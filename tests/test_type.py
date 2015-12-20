import unittest

from llvm.core import Context
from llvm.core import Type
from llvm.core import TypeKind
from llvm.core import Module

class TypeTest(unittest.TestCase):
    def setUp(self):
        self.global_context = Context.GetGlobalContext()

    def testTypeCompare(self):
        a = Type.int8()
        b = Type.int8()

        self.assertEqual(a, b)

        c = Type.int32()
        self.assertTrue(c != a)
    
    def testCreateInt8(self):
        ty = Type.int8(self.global_context)
        self.assertEqual('i8', ty.name)

        ty = Type.int8()
        self.assertEqual('i8', ty.name)

        context = ty.context
        self.assertEqual(context, self.global_context)

        kind = ty.kind
        self.assertEqual(TypeKind.Integer, kind)
        self.assertTrue(ty.is_sized())

    def testCreateInt16(self):
        ty = Type.int16(self.global_context)
        self.assertEqual('i16', ty.name)

        ty = Type.int16()
        self.assertEqual('i16', ty.name)

        context = ty.context
        self.assertEqual(context, self.global_context)
        
    def testCreateInt32(self):
        ty = Type.int32(self.global_context)
        self.assertEqual('i32', ty.name)

        ty = Type.int32()
        self.assertEqual('i32', ty.name)

        context = ty.context
        self.assertEqual(context, self.global_context)

    def testCreateInt12(self):
        ty = Type.int(12, self.global_context)
        self.assertEqual('i12', ty.name)

        ty = Type.int(12)
        self.assertEqual('i12', ty.name)

    def testCreateFloat(self):
        t1 = Type.float()
        t2 = Type.float(self.global_context)

        self.assertEqual(t1, t2)
        self.assertEqual('float', t1.name)

    def testCreateHalf(self):
        t1 = Type.half()
        t2 = Type.half(self.global_context)

        self.assertEqual(t1, t2)
        self.assertEqual('half', t1.name)

    def testCreateDouble(self):
        t1 = Type.double()
        t2 = Type.double(self.global_context)

        self.assertEqual(t1, t2)
        self.assertEqual('double', t1.name)
        
    def testTypeEquality(self):
        ty1 = Type.int8()
        ty2 = Type.int8()

        self.assertEqual(ty1, ty2)
        
    def testCreateInt1(self):
        ty = Type.int1(self.global_context)
        self.assertEqual('i1', ty.name)

        ty = Type.int1()
        self.assertEqual('i1', ty.name)
 
    def testCreateFunction(self):
        ty = Type.int8()
        f = Type.function(ty, [ty], False)

        self.assertEqual('i8 (i8)', f.name)
        self.assertFalse(f.is_function_vararg())

        r = f.return_type()
        self.assertEqual('i8', r.name)
        self.assertEqual(1, f.num_params())

        tys = f.param_types()
        self.assertEqual('i8', tys[0].name)
        self.assertEqual(1, len(tys))

    def testCreatePointer(self):
        ty = Type.int8()
        p = Type.pointer(ty)
        self.assertEqual(0, p.pointer_address_space())
        self.assertEqual('i8*', p.name)

        t = p.element_type()
        self.assertEqual('i8', t.name)

    def testCreateStruct(self):
        ty = Type.int8()
        p = Type.structure([ty, ty], False)

        self.assertEqual('{ i8, i8 }', p.name)
        self.assertEqual(2, p.num_elements())

        elems = p.elements()
        t1 = elems[0]
        self.assertEqual('i8', t1.name)
        t2 = elems[1]
        self.assertEqual('i8', t2.name)

    def testCreateNamedStruct(self):
        ty = Type.create_named_structure(self.global_context, "mystruct")
        self.assertEqual('mystruct', ty.struct_name())

        el = Type.int8()
        ty.set_body([el, el], True)
        self.assertEqual(2, ty.num_elements())
        self.assertTrue(ty.is_packed())

    def testCreateArrayType(self):
        ty = Type.int8()
        a = Type.array(ty, 2)
        self.assertEqual(2, a.array_length())

        t = a.element_type()
        self.assertEqual(ty.name, t.name)
        
    def testCreateVectorType(self):
        ty = Type.int8()
        a = Type.vector(ty, 2)
        self.assertEqual(2, a.vector_size())

        t = a.element_type()
        self.assertEqual(ty.name, t.name)

    def testCreateVoidType(self):
        ty = Type.void()
        self.assertEqual('void', ty.name)

        t = Type.void(context=self.global_context)
        self.assertEqual('void', t.name)

    def testCreateLabelType(self):
        ty = Type.label()
        self.assertEqual('label', ty.name)

        t = Type.label(context=self.global_context)
        self.assertEqual('label', t.name)

    def testCreateFunctionType(self):
        ty = Type.int8()
        ft = Type.function(ty, [ty], False)

        self.assertFalse(ft.is_function_vararg())
        self.assertEqual(ty, ft.return_type())
        self.assertEqual(1, ft.num_params())

        self.assertEqual([ty], ft.param_types())

        f2 = Type.function(ty, [ty], True)
        self.assertTrue(f2.is_function_vararg())
        self.assertEqual([ty], f2.param_types())
        self.assertEqual(1, f2.num_params())

    def testCreateNamedStructInMod(self):
        ctx = Context()
        mod = Module.CreateWithName('mod', ctx)
        ty = Type.create_named_structure(mod.context,
                                         'mystruct')
        el = Type.int8(context=mod.context)
        ty.set_body([el, el], True)
        t = mod.get_type('mystruct')
        
        self.assertEqual(ty, t)

        
if __name__ == '__main__':
    unittest.main()
