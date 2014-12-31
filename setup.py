try:
    import multiprocessing
except ImportError:
    pass

import re
from setuptools import setup

with open('ptt_crawler/__init__.py') as f:
    m = re.findall(r'__version__\s*=\s*"(.*)"', f.read())
    version = m[0]

setup(
    name='ptt_crawler',
    version=version,
    url='https://github.com/youmeb-lab/ptt-crawler',
    license='MIT',
    author='Po-Ying Chen, Jamie Yang',
    author_email='poying.me@gmail.com',
    packages=[
        'ptt_crawler',
        'ptt_crawler.parser',
    ],
    platforms='any',
    install_requires=[
        'requests>=2.5.1',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Traditional)',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ]
)
