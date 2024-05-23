from setuptools import setup, find_packages

setup(
    name='notebook_package',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'notebook = notebook.notebook:main'
        ]
    },
    install_requires=[
        # Add any dependencies your project requires here
    ],
)