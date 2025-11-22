import sys
import importlib

# Check Python version
print(f"Python version: {sys.version}")

# List of packages to check
packages = [
    "torch",
    "tensorflow",
    "keras",
    "tf_keras",
    "sentence_transformers",
    "pandas",
    "streamlit",
    "transformers"
]

print("\nInstalled package versions:")

for package in packages:
    try:
        mod = importlib.import_module(package)
        print(f"{package}: {mod.__version__}")
    except ModuleNotFoundError:
        print(f"{package}: Not installed")
