import witty

from setuptools import setup


setup(
    name="witty",
    version=witty.__version__,
    description="A TTY workitem tool for TFS",
    author="Ohad Lutzky",
    author_email="ohad@lutzky.net",
    license="GPL",
    py_modules=["witty"],
    entry_points={
        'console_scripts': [
            'witty = witty:main',
        ],
    },
)
