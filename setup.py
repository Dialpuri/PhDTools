from setuptools import setup, find_packages

setup(
    name="phdtools",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests", "pillow", "gemmi"],
    entry_points={
        'console_scripts': [
        'pdbfetch=phdtools.pdbfetch:main',
	    'completeness=phdtools.completeness:_main',
        'removena=phdtools.remove_na:main',
        'removewaters=phdtools.remove_waters:main',
        'removeglycans=phdtools.remove_glycans:main',
        'createmr=phdtools.createmr:main',
        'createdeglyco=phdtools.createdeglyco:main',
        'createdeglycowater=phdtools.createdeglycowater:main',
        'createmtz=phdtools.createmtz:main',
        'linebreaker=phdtools.linebreaker:main',
        'cropper=phdtools.cropper:main',
        ],
    },
    author="Jordan Dialpuri",
    description="Fetch PDB files from the RCSB Protein Data Bank",
    python_requires=">=3.7",
)
