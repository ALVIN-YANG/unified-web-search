from setuptools import setup, find_packages

setup(
    name="unified-web-search",
    version="1.0.0",
    description="Unified web search tool supporting multiple providers (Tavily, Exa, etc.)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Unified Web Search",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "web-search=search:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
)
