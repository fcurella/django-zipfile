import unittest
from StringIO import StringIO
from django_zipfile import TemplateZipFile
from zipfile import ZIP_DEFLATED
from django.template.loader import render_to_string
from django.template.loader import TemplateDoesNotExist
import os


class TestTemplateZipFile(unittest.TestCase):
    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        self.fh = StringIO()
        self.zipfile1 = TemplateZipFile(self.fh, mode='w', compression=ZIP_DEFLATED, template_root=['override', 'default/'])
        self.zipfile2 = TemplateZipFile(self.fh, mode='w', compression=ZIP_DEFLATED, template_root='override/',)

    def test_names(self):
        templates = self.zipfile1._templates(['one.txt'])
        self.assertEqual(['override/one.txt', 'default/one.txt'], templates)

        filename = self.zipfile1._filename(templates)
        self.assertEqual('one.txt', filename)

        templates = self.zipfile1._templates(['two.txt', 'one.txt'])
        self.assertEqual(['override/two.txt', 'override/one.txt', 'default/two.txt', 'default/one.txt'], templates)

        templates = self.zipfile1._templates(['folderone/oneone.txt'])
        self.assertEqual(['override/folderone/oneone.txt', 'default/folderone/oneone.txt'], templates)

        filename = self.zipfile1._filename(templates)
        self.assertEqual('folderone/oneone.txt', filename)

        templates = self.zipfile1._templates(['folderone/onetwo.txt', 'folderone/oneone.txt'])
        self.assertEqual(['override/folderone/onetwo.txt', 'override/folderone/oneone.txt', 'default/folderone/onetwo.txt', 'default/folderone/oneone.txt'], templates)

        templates = self.zipfile2._templates(['one.txt'])
        self.assertEqual(['override/one.txt'], templates)

        filename = self.zipfile2._filename(templates)
        self.assertEqual('one.txt', filename)

        templates = self.zipfile2._templates(['two.txt', 'one.txt'])
        self.assertEqual(['override/two.txt', 'override/one.txt'], templates)

        templates = self.zipfile2._templates(['folderone/oneone.txt'])
        self.assertEqual(['override/folderone/oneone.txt'], templates)

        filename = self.zipfile2._filename(templates)
        self.assertEqual('folderone/oneone.txt', filename)

        templates = self.zipfile2._templates(['folderone/onetwo.txt', 'folderone/oneone.txt'])
        self.assertEqual(['override/folderone/onetwo.txt', 'override/folderone/oneone.txt'], templates)

    def test_adding_files(self):
        self.assertRaises(TemplateDoesNotExist, self.zipfile1.add_template, 'abc.html')

if __name__ == '__main__':
    unittest.main()
