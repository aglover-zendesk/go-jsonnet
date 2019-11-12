# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from setuptools import setup
from setuptools import Extension
from setuptools.command.build_ext import build_ext as BuildExt
from subprocess import Popen, PIPE

DIR = os.path.abspath(os.path.dirname(__file__))
LIB_DIR = DIR + '/c-bindings'
MODULE_SOURCES = ['cpp-jsonnet/python/_jsonnet.c']

def get_version():
    # TODO think about it (how to get the version)
    return '0.14.0'

class BuildJsonnetExt(BuildExt):
    def run(self):
        p = Popen(['go', 'build', '-o', 'libgojsonnet.a', '-buildmode=c-archive'], cwd=LIB_DIR, stdout=PIPE)
        p.wait()

        if p.returncode != 0:
            raise Exception('Could not build libgojsonnet.so')

        BuildExt.run(self)

jsonnet_ext = Extension(
    '_jsonnet',
    sources=MODULE_SOURCES,
    extra_objects=[
        LIB_DIR + '/libgojsonnet.a',
    ],
    include_dirs = ['cpp-jsonnet/include'],
    language='c++',
)

setup(name='gojsonnet',
    url='https://jsonnet.org',
    description='Python bindings for Jsonnet - The data templating language ',
    author='David Cunningham',
    author_email='dcunnin@google.com',
    version=get_version(),
    cmdclass={
        'build_ext': BuildJsonnetExt,
    },
    ext_modules=[jsonnet_ext],
    test_suite="python._jsonnet_test",
)
