from setuptools import setup, find_packages
from typing import List

requirement_list = []

def get_requirements() -> List[str]:
    """
    This function returns a list of all the required packages
    """
    try:
        with open("requirements.txt", 'r') as f:
            lines = f.readlines() 
            
            # process each line
            for line in lines:
                requirement = line.strip() # remove any empty space
                # ignore empty lines and '-e.'
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
        return requirement_list
    
    except FileNotFoundError:
        print("requirements.txt file is not found")

    except Exception as e:
        raise e

setup(
    name="NetworkSecurity",
    author="Aryan Savant",
    author_email="aryansavant31@gmail.com",
    version="0.0.1",
    packages=find_packages(), # finds wherever we have __init__.py
    install_requires=get_requirements()

)
