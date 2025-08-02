import unittest
import os
import sys

# Add the parent directory to the sys.path to allow importing font_processor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import font_processor as fp

class TestFontProcessor(unittest.TestCase):

    def test_remove_ext(self):
        self.assertEqual(fp.remove_ext("font.ttf"), "font")
        self.assertEqual(fp.remove_ext("archive.zip"), "archive")
        self.assertEqual(fp.remove_ext("no_extension"), "no_extension")
        self.assertEqual(fp.remove_ext("multi.dot.name.otf"), "multi.dot.name")
        self.assertEqual(fp.remove_ext(""), "")
        self.assertEqual(fp.remove_ext(".hiddenfile"), ".hiddenfile")

if __name__ == '__main__':
    unittest.main()