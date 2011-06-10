from setuptools import setup

setup(name='txroutes',
        version='0.0.2',
        author='Zach Steindler',
        author_email='steiza@coffeehousecoders.org',
        url='http://github.com/steiza/txroutes',
        description='Provides routes-like dispatching for twisted.web.server',
        long_description='''Frequently, it's much easier to describe your website layout using routes instead of Resource from twisted.web.resource. This small library lets you dispatch with routes in your twisted.web application.''',
        keywords='twisted, web, routes',
        classifiers=['Programming Language :: Python', 'License :: OSI Approved :: BSD License'],
        license='BSD',
        packages=['txroutes'],
        package_data={'txroutes': ['*']},
        install_requires=['routes', 'twisted'],
        )

