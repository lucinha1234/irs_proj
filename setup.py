from setuptools import setup, find_packages

setup(
    name="xmlcsvtool",
    version="0.1.0",
    packages=["xmlcsvconvert"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        'gui_scripts': [
            'xmlcsv-gui = gui:main',  # Only if you wrap root.mainloop() in a `main()` function
        ],
    },
)
