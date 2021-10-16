from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = '0.5.9'

setup(
    name='QuickStart_Rhy',
    version=VERSION,
    description='Simplify the operation in terminal!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='Simplify the operation in terminal!',
    author='RhythmLian',
    url="https://github.com/Rhythmicc/QuickStart",
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['requests', 'urllib3', 'colorama', 'rarfile', 'PyInquirer', 'rich', 'py7zr'],
    entry_points={
        'console_scripts': [
            'qs = QuickStart_Rhy.main:main'
        ]
    },
)
