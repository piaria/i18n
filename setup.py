
from setuptools import setup

setup(
    name="i18n",
    version="0.1",
    py_modules=["i18n"],
    include_package_data=True,
    install_requires=["click", "polib", "translators"],
    entry_points="""
        [console_scripts]
        i18n=i18n:cli
    """,
)