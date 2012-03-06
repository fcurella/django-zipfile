Django Zipfile
======================================

A subclass of ``zipfile.Zipfile`` that works with Django templates.


Usage:

::

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

You can also specify multiple roots for your templates:

::

    container = TemplateZipFile(response, mode='w', compression=ZIP_DEFLATED, template_root=['myapp/myzipskeleton/override/', 'myapp/myzipskeleton/default/'])

as well as multiple templates when you add files:

::

    container.write_template(['override.html', 'default.html'], filename="chapter1.html")

TemplateZipFile will look for templates in the specified order, first by root, then by template name. For example:

::

    myzipfile = TemplateZipFile(response, mode='w', compression=ZIP_DEFLATED, template_root=['override/', 'default/'])
    myzipfile.write_template(['two.txt', 'one.txt'], filename='myfile.txt')

    # Will use the first existing template from ['override/two.txt', 'override/one.txt', 'default/two.txt', 'default/one.txt']

If none of the templates can be found, ``write_template`` will raise a TemplateDoesNotExist error.

You can specify a file as optional with ``optional=True``

::

    myzipfile.write_template(['two.txt', 'one.txt'], filename='myfile.txt', optional=True)

Doing so will silently swallow the TemplateDoesNotExist exception.
