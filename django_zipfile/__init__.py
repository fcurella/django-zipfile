VERSION = (0, 1, 7)

# This tries to import TemplateZipFile only when django is installed.
# For example, when installing via pip, setup.py executes this file before
# installing Django, even if that's specified as dependency.
try:
    import django
    django_present = True
except ImportError:
    django_present = False

# We still want to catch eventual ImportErrors that are due to TemplateZipFile.
if django_present:
    from django_zipfile.templatezipfile import TemplateZipFile
