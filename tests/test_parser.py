import unittest
from parser.parser import parse

class ParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse(self):
        result = parse("https://kplc.co.ke/img/full/zSxZeOMiFWWi_Interruptions%20-%2016.04.2020.pdf")
        self.assertNotEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
