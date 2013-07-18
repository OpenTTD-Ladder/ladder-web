import os
from django.conf import settings

jshintfile = os.path.join(settings.ROOT_DIR, '.jshintrc')

from ..base import CompilerCommand, JS_PROPERTY, JS_STATIC_DIR

class Command(CompilerCommand):
    static_dir      = JS_STATIC_DIR
    module_property = JS_PROPERTY


    def queue_file(self, fname, module):
        if fname.endswith('.min.js'):
            return False
        return self.test_file_age(fname, ''.join([os.path.splitext(fname)[0], '.min.js']))

    def test_file(self, name, item):
        stdout, _, ret = self.get_output("jshint", "--config", jshintfile, item)

        if ret != 0:
            print ""
            for line in stdout.splitlines():
                if line.startswith(item):
                    print name, line[len(item):]
        return ret == 0

    def compile_file(self, name, item):
        parts = os.path.splitext(item)
        min_js = ''.join([parts[0], '.min.js'])
        js, _, _ = self.get_output("uglifyjs", "-nc", item)
        with open(min_js, 'w') as fh:
            fh.write(js)

        return True