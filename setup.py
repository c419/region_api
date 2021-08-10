from setuptools import setup

setup(
   name='region_api',
   version='1.0',
   description='API for branched regions and cities',
   author='Vladimir Naprasnikov',
   author_email='v.naprsanikov@gmail.com',
   packages=['region_api'],
   include_package_data=True,
   install_requires=['flask', 'flask_restful', 'flask_sqlalchemy', 'PyJWT', 'pytest'], #external packages as dependencies
)
