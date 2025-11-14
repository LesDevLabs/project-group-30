from setuptools import find_packages, setup

setup(
    name="assistant-bot-G30",
    version="0.1.1",
    author="Group 30 (2025)",
    author_email="lestyshchenko@gmail.com, sagepol@gmail.com, 444ten@gmail.com, koliaepov@gmail.com, valerian.demichev@gmail.com, 3t.zarudenska@gmail.com",
    description="Асистент-бот для управління контактами з підтримкою різних форматів збереження",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LesDevLabs/project-group-30",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    install_requires=["colorama", "rich"],
    entry_points={
        "console_scripts": [
            "assistant-bot-G30=assistant_bot_g30.cli_entry:run",
        ],
    },
)
