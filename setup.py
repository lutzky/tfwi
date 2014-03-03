import tfwi

from setuptools import setup


setup(
    name="tfwi",
    version=tfwi.__version__,
    description="A Team Foundation Work Item tool",
    author="Ohad Lutzky",
    author_email="ohad@lutzky.net",
    license="GPL",
    py_modules=["tfwi"],
    test_suite="tfwi",
    entry_points={
        'console_scripts': [
            'tfwi = tfwi:main',
        ],
    },
)
