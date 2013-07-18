import importlib
import glob
import os
import sys

import subprocess

from optparse import make_option

from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings

APP_FORMAT = getattr(settings, "GLOBAL_COMPILE_MODULE_FORMAT", "%s.static")
JS_PROPERTY = getattr(settings, "GLOBAL_COMPILE_JS_PROPERTY", "compile_js")
CSS_PROPERTY = getattr(settings, "GLOBAL_COMPILE_CSS_PROPERTY", "compile_css")

JS_STATIC_DIR = getattr(settings, "GLOBAL_COMPILE_JS_STATIC_DIR", "js")
CSS_STATIC_DIR = getattr(settings, "GLOBAL_COMPILE_JS_STATIC_DIR", "css")

def run_command(*args, **kwargs):
    env = os.environ.copy()
    paths = [x for x in sys.path if len(x) > 1]
    env["PYTHONPATH"] = os.pathsep.join(paths)
    kwargs.setdefault('env', env)
    kwargs.setdefault('cwd', settings.ROOT_DIR)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode

class ExecutingCommand(NoArgsCommand):
    can_import_settings = True
    requires_model_validation = False

    def get_output(self, *args):
        return run_command(*args)

class CompilerCommand(ExecutingCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--test-only',
            action='store_true',
            dest='test-only',
            default=False,
            help='Test only'),
        )

    static_dir      = ''
    module_property = ''

    compile_queue   = []

    def test_file_age(self, a, b):
        try:
            return os.path.getmtime(a) > os.path.getmtime(b)
        except OSError:
            return True

    def test_file(self, name, item):
        return False

    def compile_file(self, name, item):
        return False

    def compile_files(self):
        for name, item in self.compile_queue:
            print "Testing: %s" % name
            if not self.test_file(name, item):
                raise CommandError("Items failed test: '%s', aborting" % name)
        if self.test_only:
            return
        for name, item in self.compile_queue:
            print "Compiling: %s" % name
            if not self.compile_file(name, item):
                raise CommandError("Items failed compile: '%s', aborting" % name)

    def queue_file(self, fname, module):
        return True

    def handle_noargs(self, *args, **options):
        self.test_only = options.get('test-only', False)
        for app in settings.INSTALLED_APPS:
            try:
                module = importlib.import_module(APP_FORMAT % app)
            except ImportError:
                continue
            dirname = os.path.dirname(module.__file__)
            if not dirname.startswith(settings.ROOT_DIR):
                continue
            print "Checking app: %s" % app 

            static_dir = os.path.join(dirname, 'static', self.static_dir)
            static_dir_len = len(static_dir)+1

            static_files = getattr(module, self.module_property, [])
            for glob_path in static_files:
                glob_search = os.path.join(static_dir, glob_path)
                for fname in glob.glob(glob_search):
                    if self.queue_file(fname, module):
                        self.compile_queue.append( (fname[static_dir_len:], fname) )
        self.compile_files()