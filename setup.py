from setuptools import setup


setup(
    name='basec',
    version='0.1',
    py_modules=['basec'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        basec=basec:cli
    ''',
)
