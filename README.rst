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

        container.add_template('mimetype')
        container.add_template('META-INF/container.xml')
        container.add_template('chapter1.html', context=context)

        container.close()
        return response
