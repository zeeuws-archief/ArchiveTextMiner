from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ArchiveTextMiner',
    version='1.0.1',
    description='Transform textual information to structured metadata in MDTO-format.',
    author='Muriël Valckx',
    author_email='my.valckx@zeeland.nl',
    url='https://github.com/zeeuws-archief/ArchiveTextMiner',
    packages=find_packages(),
    install_requires=[
        'click',
        'colorama',
        'joblib',
        'langdetect',
        'nltk',
        'numpy',
        'PyPDF2',
        'python-magic',
        'regex',
        'scikit-learn',
        'scipy',
        'setuptools',
        'sentencepiece',
        'six',
        'threadpoolctl',
        'tqdm',
        'transformers',
    ],
    license='EUPL',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'ArchiveTextMiner=ArchiveTextMiner.generator:main',  
        ],
    },
    include_package_data=True,
    package_data={
        '': ['LICENSE.md', 'requirements.txt'],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)

