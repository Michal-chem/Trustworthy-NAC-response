from setuptools import setup

setup(
    name="SampleSizeCalculator",
    version="1.0",
    description="A tool for sample size assessment based on Cox-Snell and EPV calculations.",
    author="Your Name",
    author_email="your_email@example.com",
    py_modules=["your_script_name"],
    install_requires=[
        "numpy",
        "statsmodels",
    ],
    entry_points={
        "console_scripts": [
            "samplesize=your_script_name:main",  # Adjust if you use a `main()` function
        ],
    },
)