from setuptools import setup

setup(name='webhooks server',
      version='0.1',
      description='Simple webhooks server',
      author='Mark Duppenthaler',
      author_email='mduppes@gmail.com',
      license='MIT',
      packages=['webhooks'],
      install_requires=[
          'Flask',
          'records',
      ],
      zip_safe=False)
