import subprocess
import sys


def main():
    print("Running MyPy Type Checks...")
    mypy_result = subprocess.run([sys.executable, "-m", "mypy", "."], check=False)

    if mypy_result.returncode != 0:
        print("MyPy failed. Aborting further checks.")
        sys.exit(mypy_result.returncode)

    print("\nRunning Pytest Unit Tests...")
    pytest_result = subprocess.run([sys.executable, "-m", "pytest"], check=False)

    # Stop met de exit code van Pytest
    sys.exit(pytest_result.returncode)


if __name__ == "__main__":
    main()
