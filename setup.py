"""
Setup configuration for Depix.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().strip().split('\n')
    requirements = [r.strip() for r in requirements if r.strip() and not r.startswith('#')]

setup(
    name="depix",
    version="2.0.0",
    author="Sipke Mellema",
    author_email="",
    description="A tool to recover plaintext from pixelized screenshots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/depix",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: Creative Commons License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "depix=depix:main",
            "depix-show-boxes=tool_show_boxes:main",
            "depix-gen-pixelated=tool_gen_pixelated:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt"],
    },
    keywords=[
        "depixelization",
        "image-processing",
        "security",
        "computer-vision",
        "template-matching",
        "opencv",
        "redaction",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/depix/issues",
        "Source": "https://github.com/yourusername/depix",
        "Documentation": "https://github.com/yourusername/depix#readme",
    },
)
