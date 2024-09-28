from setuptools import find_packages, setup

from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements
setup(
    name='DeltaX',
    version='1.1.1',
    description='This project of Data Analysis with AI',
    author='Qadeer Ahmad',
    license='',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)