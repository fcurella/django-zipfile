import os
from zipfile import ZipFile
from django.template import Context
from django.template.loader import render_to_string
from django.template.loader import TemplateDoesNotExist

import six


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

            container.write_template('mimetype')
            container.write_template('META-INF/container.xml')
            container.write_template('chapter1.html', context=context)

            container.close()
            return response
    """

    def __init__(self, file, template_root=None, *args, **kwargs):
        self.template_root = []
        for root in self._to_list(template_root):
            if not root.endswith('/'):
                root += '/'
            self.template_root.append(root)
        super(TemplateZipFile, self).__init__(file, *args, **kwargs)

    def _templates(self, template_list):
        if self.template_root is not None:
            templates = []
            for root in self.template_root:
                templates += ["%s%s" % (root, template) for template in template_list]
            return templates
        return template_list

    def _filename(self, templates):
        template_name = templates[0]

        if self.template_root is not None:
            template_root = self.template_root[0]
            filename = template_name.split(template_root)[1]
        else:
            filename = template_name.split('/')[-1]

        return filename

    def _to_list(self, var):
        if isinstance(var, six.string_types):
            return [var]
        return var

    def write_template(self, template_list, filename=None, context=None, compress_type=None, optional=False):
        if context is None:
            context = {}

        template_list = self._to_list(template_list)
        templates_hierarchy = self._templates(template_list)

        try:
            render = render_to_string(templates_hierarchy, context)
        except TemplateDoesNotExist:
            if optional:
                return
            else:
                raise

        if filename is None:
            filename = self._filename(templates_hierarchy)

        if compress_type is not None:
            self.writestr(filename, render.encode('utf-8'), compress_type)
        else:
            self.writestr(filename, render.encode('utf-8'))

    def write_template_dir(self, directory, context=None, compress_type=None):

        for root, dirs, files in os.walk(directory):
            for f in files:
                template_name = root + "/" + f
                self.write_template(template_name, context=context, compress_type=compress_type)
