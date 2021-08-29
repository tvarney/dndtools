import unittest

import dnd.value


class TestValue(unittest.TestCase):
    def test_value_normalize_positive_regular(self):
        v = dnd.value.Value(101, 4, 3)
        self.assertEqual(101, v.gp)
        self.assertEqual(4, v.sp)
        self.assertEqual(3, v.cp)

    def test_value_normalize_positive_cp_overflow(self):
        v = dnd.value.Value(101, 4, 33)
        self.assertEqual(101, v.gp)
        self.assertEqual(7, v.sp)
        self.assertEqual(3, v.cp)

    def test_value_normalize_positive_sp_overflow(self):
        v = dnd.value.Value(101, 21, 3)
        self.assertEqual(103, v.gp)
        self.assertEqual(1, v.sp)
        self.assertEqual(3, v.cp)

    def test_value_normalize_positive_overflow_cascade(self):
        v = dnd.value.Value(1, 1, 5321)
        self.assertEqual(54, v.gp)
        self.assertEqual(3, v.sp)
        self.assertEqual(1, v.cp)

    def test_value_normalize_negative_regular(self):
        v = dnd.value.Value(-101, -5, -3)
        self.assertEqual(-101, v.gp)
        self.assertEqual(-5, v.sp)
        self.assertEqual(-3, v.cp)

    def test_value_normalize_negative_cp_overflow(self):
        v = dnd.value.Value(-101, -5, -42)
        self.assertEqual(-101, v.gp)
        self.assertEqual(-9, v.sp)
        self.assertEqual(-2, v.cp)

    def test_value_normalize_negative_sp_overflow(self):
        v = dnd.value.Value(-101, -39, -7)
        self.assertEqual(-104, v.gp)
        self.assertEqual(-9, v.sp)
        self.assertEqual(-7, v.cp)

    def test_value_normalize_negative_overflow_cascasde(self):
        v = dnd.value.Value(-101, -23, -45)
        self.assertEqual(-103, v.gp)
        self.assertEqual(-7, v.sp)
        self.assertEqual(-5, v.cp)

    def test_value_normalize_mixed_positive(self):
        v = dnd.value.Value(101, -3, -4)
        self.assertEqual(100, v.gp)
        self.assertEqual(6, v.sp)
        self.assertEqual(6, v.cp)

    def test_value_normalize_mixed_negative(self):
        v = dnd.value.Value(-101, 3, 4)
        self.assertEqual(-100, v.gp)
        self.assertEqual(-6, v.sp)
        self.assertEqual(-6, v.cp)

    def test_value_str_cp_only(self):
        self.assertEqual("5 cp", str(dnd.value.Value(0, 0, 5)))
        self.assertEqual("-3 cp", str(dnd.value.Value(0, 0, -3)))

    def test_value_str_sp_only(self):
        self.assertEqual("7 sp", str(dnd.value.Value(0, 7, 0)))
        self.assertEqual("-4 sp", str(dnd.value.Value(0, -4, 0)))

    def test_value_str_gp_only(self):
        self.assertEqual("11 gp", str(dnd.value.Value(11, 0, 0)))
        self.assertEqual("-32 gp", str(dnd.value.Value(-32, 0, 0)))

    def test_value_str_sp_cp(self):
        self.assertEqual("2 sp 7 cp", str(dnd.value.Value(0, 2, 7)))
        self.assertEqual("-3 sp -4 cp", str(dnd.value.Value(0, -3, -4)))

    def test_value_str_gp_cp(self):
        self.assertEqual("91 gp 8 cp", str(dnd.value.Value(91, 0, 8)))
        self.assertEqual("-14 gp -3 cp", str(dnd.value.Value(-14, 0, -3)))

    def test_value_str_gp_sp(self):
        self.assertEqual("73 gp 9 sp", str(dnd.value.Value(73, 9, 0)))
        self.assertEqual("-111 gp -1 sp", str(dnd.value.Value(-111, -1, 0)))

    def test_value_str_all(self):
        self.assertEqual("69 gp 4 sp 9 cp", str(dnd.value.Value(69, 4, 9)))
        self.assertEqual("-96 gp -8 sp -1 cp", str(dnd.value.Value(-96, -8, -1)))

    def test_value_neg(self):
        self.assertEqual(-dnd.value.Value(1, 1, 1), dnd.value.Value(-1, -1, -1))

    def test_value_pos(self):
        self.assertEqual(+dnd.value.Value(1, 1, 1), dnd.value.Value(1, 1, 1))

    def test_value_abs(self):
        self.assertEqual(abs(dnd.value.Value(1, 1, 1)), dnd.value.Value(1, 1, 1))
        self.assertEqual(abs(dnd.value.Value(-5, -5, -5)), dnd.value.Value(5, 5, 5))

    def test_value_eq(self):
        self.assertTrue(dnd.value.Value(1, 2, 3) == dnd.value.Value(1, 2, 3))
        self.assertTrue(dnd.value.Value(1, 2, 3) == dnd.value.Value(0, 11, 13))
        self.assertFalse(dnd.value.Value(1, 2, 3) == dnd.value.Value(3, 2, 1))

    def test_value_ne(self):
        self.assertTrue(dnd.value.Value(1, 2, 3) != dnd.value.Value(3, 2, 1))
        self.assertFalse(dnd.value.Value(1, 2, 3) != dnd.value.Value(1, 2, 3))

    def test_value_lt(self):
        self.assertTrue(dnd.value.Value(1, 2, 3) < dnd.value.Value(3, 2, 1))
        self.assertFalse(dnd.value.Value(1, 2, 3) < dnd.value.Value(1, 2, 3))
        self.assertFalse(dnd.value.Value(1, 2, 3) < dnd.value.Value(0, 0, 1))

    def test_value_le(self):
        self.assertTrue(dnd.value.Value(1, 2, 3) <= dnd.value.Value(3, 2, 1))
        self.assertTrue(dnd.value.Value(1, 2, 3) <= dnd.value.Value(1, 2, 3))
        self.assertFalse(dnd.value.Value(1, 2, 3) <= dnd.value.Value(0, 0, 1))

    def test_value_gt(self):
        self.assertFalse(dnd.value.Value(1, 2, 3) > dnd.value.Value(3, 2, 1))
        self.assertFalse(dnd.value.Value(1, 2, 3) > dnd.value.Value(1, 2, 3))
        self.assertTrue(dnd.value.Value(1, 2, 3) > dnd.value.Value(0, 0, 1))

    def test_value_gt(self):
        self.assertFalse(dnd.value.Value(1, 2, 3) >= dnd.value.Value(3, 2, 1))
        self.assertTrue(dnd.value.Value(1, 2, 3) >= dnd.value.Value(1, 2, 3))
        self.assertTrue(dnd.value.Value(1, 2, 3) >= dnd.value.Value(0, 0, 1))

    def test_value_float(self):
        self.assertEqual(float(dnd.value.Value(1, 1, 1)), 1.11)

    def test_value_add(self):
        v1 = dnd.value.Value(10, 8, 7)
        v2 = dnd.value.Value(11, 7, 4)
        v3 = dnd.value.Value(-1, -2, -3)

        self.assertEqual(v1 + v2, dnd.value.Value(22, 6, 1))
        self.assertEqual(v1 + v3, dnd.value.Value(9, 6, 4))

    def test_value_sub(self):
        v1 = dnd.value.Value(10, 8, 7)
        v2 = dnd.value.Value(4, 2, 3)
        v3 = dnd.value.Value(-1, -3, -1)

        self.assertEqual(v1 - v2, dnd.value.Value(6, 6, 4))
        self.assertEqual(v1 - v3, dnd.value.Value(12, 1, 8))

    def test_value_mul_int(self):
        v1 = dnd.value.Value(5, 5, 5)
        self.assertEqual(v1 * 1, v1)
        self.assertEqual(v1 * 0, dnd.value.Value(0, 0, 0))
        self.assertEqual(v1 * 2, dnd.value.Value(11, 1, 0))
        self.assertEqual(v1 * -1, dnd.value.Value(-5, -5, -5))
        self.assertEqual(v1 * -2, dnd.value.Value(-11, -1, 0))

    def test_value_mul_float(self):
        v1 = dnd.value.Value(5, 5, 5)
        self.assertEqual(v1 * 1.0, v1)
        self.assertEqual(v1 * -1.0, -v1)
        self.assertEqual(v1 * 0.5, dnd.value.Value(2, 7, 7))
        self.assertEqual(v1 * 1.5, dnd.value.Value(8, 3, 2))
