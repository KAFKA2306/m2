"""Setup script for economic analysis system."""
from setuptools import setup, find_packages
from pathlib import Path
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('
setup(
    name="economic-ultrathink",
    version="2.0.0",
    description="Automated economic analysis and visualization system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="KAFKA2306",
    author_email="noreply@github.com",
    url="https://github.com/KAFKA2306/m2",
    packages=find_packages(),
    package_dir={"": "src"},
    package_data={
        "config": ["*.yml", "*.yaml"],
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-mock>=3.10.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License", 
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="economic analysis, financial data, visualization, dashboard, automation",
    entry_points={
        "console_scripts": [
            "economic-update=refactored_update_data:main",
            "economic-viz=economic_ultrathink_dashboard:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/KAFKA2306/m2/issues",
        "Source": "https://github.com/KAFKA2306/m2",
        "Dashboard": "https://kafka2306.github.io/m2/",
    },
)