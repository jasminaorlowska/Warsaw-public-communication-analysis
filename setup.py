from setuptools import setup, find_namespace_packages

setup(
    name='bus_analysis_python',
    version='0.1.0',
    description='MIMUW PROJECT',
    author='jasmina.orlowska',
    author_email='jo448417@students.mimuw.edu.pl',
    packages=find_namespace_packages(),
    install_requires=['geopy',
                      'numpy',
                      'pandas',
                      'concurrent',
                      'requests',
                      'typing',
                      'schedule'
                      ]
)
