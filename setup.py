import os
from setuptools import setup

from distutils.core import setup
from distutils.command.install import install as install_org
from distutils.command.install_data import install_data as install_data_org

#from pandaclienttools import panda_pkg_info

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# set overall prefix for bdist_rpm
class install_panda_clienttools(install_org):
    def initialize_options (self):
        install_org.initialize_options(self)

setup(
    name = "panda-clienttools",
    version = "0.0.3",
    author = "Pavlo Svirin",
    author_email = "psvirin@bnl.gov",
    description = ("Client tools to be used for job submissions for non-HEP PanDA customers"),
    license = "BSD",
    keywords = "PanDA",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['panda-clienttools'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
#    py_modules=['panda-clienttools'],
    data_files=[
        # config and cron files
        ('bin', ['scripts/bin/pansub', 'scripts/bin/pansub2', 'scripts/bin/panstat', 'scripts/bin/pankill']),
        ('scripts', ['scripts/spawner.py', 'scripts/retry-jobs.py', 'scripts/spawner_wf.py', 'scripts/create_yaml.sh', 'scripts/get_stat.py','scripts/kill_jobs.py', 'scripts/submitter.py',  'scripts/submitter2.py', 'scripts/graph-easy.pl']),
        ('share', ['share/template_proposal.tmpl'])
     ],
    cmdclass={'install': install_panda_clienttools}
)
