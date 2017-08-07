from setuptools import setup

setup(
    name='hits_project',
    version='0.1',
    packages=['gui'],
    install_requires=[
        'psycopg2==2.6.2'
    ],
    entry_points={
        'gui_scripts': [
            'hits_project_gui = gui:main'
        ]
    }
    )