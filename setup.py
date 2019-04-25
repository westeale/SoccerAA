from setuptools import setup

setup(
    name='SoccerAA',
    version='1.0',
    packages=['app', 'app.tracking', 'app.detection', 'app.image_handling', 'app.result_processing',
              'app.template_processing'],
    url='',
    license='',
    author='Alex, Phil',
    author_email='',
    description='Advertisment analysis tool',
    install_requires=['opencv-contrib-python==3.4.2.17', 'numpy', 'termcolor']
)
