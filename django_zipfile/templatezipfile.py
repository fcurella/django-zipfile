import sys
import os
from zipfile import ZipFile
from django.template import Context
from django.template.loader import render_to_string


class TemplateZipFile(ZipFile, object):
    """
    Usage::
    
        from zipfile import ZIP_DEFLATED
        from django_zipfile import TemplateZipFile
    
        def myview(request, object_id):
            obj = get_object_or_404(MyModel, pk=object_id)
            context = {
                'object': obj
            }
            response = HttpResponse(mimetype='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=myfile.zip'
            container = TemplateZipFile(response, mode='w', compression=ZIP_DEFLATED, template_root='myapp/myzipskeleton/')

            container.add_template('mimetype')
            container.add_template('META-INF/container.xml')
            container.add_template('chapter1.html', context=context)

            container.close()
            return response
    """
    def __init__(self, file, template_root=None, *args, **kwargs):
        self.template_root = template_root
        return super(TemplateZipFile, self).__init__(file, *args, **kwargs)

    def _check_individual_compression_supported(self, compress_type):
        if compress_type is not None:
            if compress_type != self.compress_type and sys.version_info < (2, 7):
                raise "Python2.7 is required for individual file compression."

    def _template_name(self, template):
        if self.template_root is not None:
            return self.template_root + template
        return template

    def add_template(self, template_list, filename=None, context=None, compress_type=None):
        self._check_individual_compression_supported(compress_type)
        if context is None:
            c = Context({})
        else:
            c = Context(context)

        templates = []

        if isinstance(template_list, basestring):
            templates = [self._template_name(template_list)]
        else:
            for template in template_list:
                templates.append(self._template_name(template))

        render = render_to_string(templates, c)

        if filename is None:
            template_name = templates[0]

            if self.template_root is not None:
                filename = template_name.split(self.template_root)[1]
            else:
                filename = template_name.split('/')[-1]

        if compress_type is not None:
            self.writestr(filename, render, compress_type)
        else:
            self.writestr(filename, render)

    def add_template_dir(self, directory, context=None, compress_type=None):
        self._check_individual_compression_supported(compress_type)

        for root, dirs, files in os.walk(directory):
            for f in files:
                template_name = root + "/" + f
                self.add_template(template_name, context=context, compress_type=compress_type)
