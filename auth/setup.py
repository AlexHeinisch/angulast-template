import setuptools

# mostly used to satisfy IDEs
setuptools.setup(
    name='auth-service',
    version='1',
    packages=setuptools.find_packages(include=['app', 'app.*'])
)
