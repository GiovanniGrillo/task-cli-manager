from setuptools import setup, find_packages

setup(
    name="task-cli-manager",
    version="0.2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "taskcli=task_manager.cli:cli",
        ],
    },
)
