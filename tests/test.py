import unittest
from src.versions_kaneryu.versions import Version, releaseTypes

class TestVersion(unittest.TestCase):
    def setUp(self):
        self.version_basic = Version("1.2.3")
        self.version_with_appendage = Version("1.2.3-a4")
        self.version_tuple_basic = (1, 2, 3, "")
        self.version_tuple_with_appendage = (1, 2, 3, "a4")

    def test_fromTuple(self):
        version = Version.fromTuple(self.version_tuple_basic)
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(version.appendage, "")

    def test_fromTuple_with_appendage(self):
        version = Version.fromTuple(self.version_tuple_with_appendage)
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(version.appendage, "a4")
        
        
    def test_toTuple(self):
        version_tuple = self.version_basic.toTuple()
        self.assertEqual(version_tuple, self.version_tuple_basic)
    
    def test_toTuple_with_appendage(self):
        version_tuple = self.version_with_appendage.toTuple()
        self.assertEqual(version_tuple, self.version_tuple_with_appendage)

    def test_str(self):
        self.assertEqual(str(self.version_basic), "Version 1.2.3")
        self.assertEqual(str(self.version_with_appendage), "Version 1.2.3 Alpha 4")
    
    def test_repr(self):
        self.assertEqual(repr(self.version_basic), "1.2.3")
        self.assertEqual(repr(self.version_with_appendage), "1.2.3-a4")
    
    def test_hash(self):
        self.assertEqual(hash(self.version_basic), hash(str(self.version_basic)))
        self.assertEqual(hash(self.version_with_appendage), hash(str(self.version_with_appendage)))
    
    def test_fromDict(self):
        version_dict = {
            "major": 1,
            "minor": 2,
            "patch": 3,
            "releaseType": releaseTypes.RELEASE,
            "revision": 0
        }
        version = Version.fromDict(version_dict)
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(version.appendage, "")
    
    def test_fromDict_with_appendage(self):
        version_dict = {
            "major": 1,
            "minor": 2,
            "patch": 3,
            "releaseType": releaseTypes.ALPHA,
            "revision": 4
        }
        
        version = Version.fromDict(version_dict)
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(version.appendage, "a4")
    
    def test_toDict_with_appendage(self):
        version_dict = self.version_with_appendage.toDict()
        self.assertEqual(version_dict["major"], 1)
        self.assertEqual(version_dict["minor"], 2)
        self.assertEqual(version_dict["patch"], 3)
        self.assertEqual(version_dict["releaseType"], releaseTypes.ALPHA)
        self.assertEqual(version_dict["revision"], 4)
    
    def test_toDict(self):
        version_dict = self.version_basic.toDict()
        self.assertEqual(version_dict["major"], 1)
        self.assertEqual(version_dict["minor"], 2)
        self.assertEqual(version_dict["patch"], 3)
        self.assertEqual(version_dict["releaseType"], releaseTypes.RELEASE)
        self.assertEqual(version_dict["revision"], 0)
    
    def test_toList(self):
        version_list = self.version_basic.toList()
        self.assertEqual(version_list, [1, 2, 3, ""])
    
    def test_toList_with_appendage(self):
        version_list = self.version_with_appendage.toList()
        self.assertEqual(version_list, [1, 2, 3, "a4"])
    
    def test_fromList(self):
        version = Version.fromList([1, 2, 3, ""])
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(version.appendage, "")
    
    def test_fromList_with_appendage(self):
        version = Version.fromList([1, 2, 3, "a4"])
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(version.appendage, "a4")
    
    def test_getWarning(self):
        version01 = Version("1.2.3")
        version02 = Version("1.2.6")
        
        version11 = Version("1.2.3-b1")
        version12 = Version("1.2.3-b2")
        
        version21 = Version("1.2.3-a1")
        version22 = Version("1.2.3-a2")
        
        self.assertEqual(version01.getWarning(version02), "Version 1.2.3 is older than Version 1.2.6")
        self.assertEqual(version11.getWarning(version12), "Version 1.2.3 Beta 1 is older than Version 1.2.3 Beta 2")
        self.assertEqual(version21.getWarning(version22), "Version 1.2.3 Alpha 1 is older than Version 1.2.3 Alpha 2")
        self.assertEqual(version21.getWarning(version11), "Version 1.2.3 Alpha 1 is older than Version 1.2.3 Beta 1")
        

    
    def test_comparisons(self):
        version01 = Version("1.2.3")
        version02 = Version("1.2.6")
        
        version11 = Version("1.2.3-b1")
        version12 = Version("1.2.3-b2")
        
        version21 = Version("1.2.3-a1")
        version22 = Version("1.2.3-a2")
        
        def test_no_channels(version1, version2):
            self.assertTrue(version1 == version1)
            self.assertTrue(version1 < version2)
            self.assertTrue(version1 <= version2)
            self.assertTrue(version2 > version1)
            self.assertTrue(version2 >= version1)
            self.assertTrue(version1 != version2)
        
        def test_channels(version11, version12, version21, version22):
            self.assertTrue(version11 == version11)
            self.assertTrue(version11 < version12)
            self.assertTrue(version11 <= version12)
            self.assertTrue(version12 > version11)
            self.assertTrue(version12 >= version11)
            self.assertTrue(version11 != version12)
            
            self.assertTrue(version21 == version21)
            self.assertTrue(version21 < version22)
            self.assertTrue(version21 <= version22)
            self.assertTrue(version22 > version21)
            self.assertTrue(version22 >= version21)
            self.assertTrue(version21 != version22)
            
            # Test between channels (beta > alpha)
            self.assertTrue(version11 > version21)
            self.assertTrue(version11 >= version21)
            self.assertTrue(version21 < version11)
            self.assertTrue(version21 <= version11)
            self.assertTrue(version11 != version21)
            
            # Test between channels (beta < release), (alpha < release)
            self.assertTrue(version11 < version01)
            self.assertTrue(version11 <= version01)
            self.assertTrue(version01 > version11)
            self.assertTrue(version01 >= version11)
            self.assertTrue(version11 != version01)
            
            self.assertTrue(version21 < version01)
            self.assertTrue(version21 <= version01)
            self.assertTrue(version01 > version21)
            self.assertTrue(version01 >= version21)
            self.assertTrue(version21 != version01)
        
        test_no_channels(version01, version02)
        test_channels(version11, version12, version21, version22)
            


if __name__ == "__main__":
    unittest.main()