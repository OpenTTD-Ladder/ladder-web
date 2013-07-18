import os

from ..base import CompilerCommand, CSS_PROPERTY, CSS_STATIC_DIR

class Command(CompilerCommand):
    static_dir      = CSS_STATIC_DIR
    module_property = CSS_PROPERTY

    def queue_file(self, fname, module):
        return self.test_file_age(fname, ''.join([os.path.splitext(fname)[0], '.css']))

    def test_file(self, name, item):
        stdout, _, _ = self.get_output("recess", item)
        failed = " error" in stdout or "Error" in stdout
        if failed:
            print ""
            print stdout
        return not failed

    def compile_file(self, name, item):
        parts = os.path.splitext(item)
        css_file = ''.join([parts[0], '.css'])
        min_css = ''.join([parts[0], '.min.css'])
        css_out, _, _ = self.get_output("recess", "--compile", item)
        min_out, _, _ = self.get_output("recess", "--compress", item)

        with open(css_file, 'w') as fh:
            fh.write(css_out)

        with open(min_css, 'w') as fh:
            fh.write(min_out)
        return True