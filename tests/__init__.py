import unittest
from StringIO import StringIO
from django_zipfile import TemplateZipFile
from zipfile import ZIP_DEFLATED
import os


class TestTemplateZipFile(unittest.TestCase):
    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        self.fh = StringIO()
        self.zipfile = TemplateZipFile(self.fh, mode='w', compression=ZIP_DEFLATED, template_root=['override/', 'default/'])

    def test_names(self):
        templates = self.zipfile._templates(['one.txt'])
        self.assertEqual(['override/one.txt', 'default/one.txt'], templates)

        filename = self.zipfile._filename(templates)
        self.assertEqual('one.txt', filename)

        templates = self.zipfile._templates(['two.txt', 'one.txt'])
        self.assertEqual(['override/two.txt', 'override/one.txt', 'default/two.txt', 'default/one.txt'], templates)

        templates = self.zipfile._templates(['folderone/oneone.txt'])
        self.assertEqual(['override/folderone/oneone.txt', 'default/folderone/oneone.txt'], templates)

        filename = self.zipfile._filename(templates)
        self.assertEqual('folderone/oneone.txt', filename)

        templates = self.zipfile._templates(['folderone/onetwo.txt', 'folderone/oneone.txt'])
        self.assertEqual(['override/folderone/onetwo.txt', 'override/folderone/oneone.txt', 'default/folderone/onetwo.txt', 'default/folderone/oneone.txt'], templates)

if __name__ == '__main__':
    unittest.main()
