VERSION = (0, 0, 1)

from zipfile import ZipFile
from django.template import Context
from django.template.loader import get_template


class TemplateZipFile(ZipFile, object):
    """
    Usage::
    
        from zipfile import ZIP_DEFLATED
        from django_zipfile import TemplateZipFile
    
        def myview(request, object_id):
            obj = get_object_or_404(MyModel, pk=object_id)
            context = {
                'object': object
            }
            response = HttpResponse(mimetype='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=myfile.zip'
            container = TemplateZipFile(response, mode='w', compression=ZIP_DEFLATED, template_root='myapp/myzipskeleton/')

            container.add_template('mimetype')
            container.add_template('META-INF/container.xml')
            container.add_template('chapter1.html', context=c)

            container.close()
            return response
    """
    def __init__(self, file, template_root=None, *args, **kwargs):
        self.template_root = template_root
        return super(TemplateZipFile, self).__init__(file, *args, **kwargs)

    def add_template(self, template_name, filename=None, context=None):
        self.debug = 3
        if context is None:
            c = Context({})
        else:
            c = Context(context)

        if self.template_root is not None:
            template_name = self.template_root + template_name

        template = get_template(template_name)
        render = template.render(c)

        if filename is None:
            if self.template_root is not None:
                arc_filename = template_name.split(self.template_root)[1]
            else:
                arc_filename = template_name.split('/')[-1]
        self.writestr(arc_filename, render)
