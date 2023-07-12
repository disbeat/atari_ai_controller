from setuptools import setup, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='atari_ai_controller',
      version='0.1',
      description='An artificial intelligence controller for the atari game river raid',
      url='https://github.com/disbeat/atari_ai_controller',
      author='Marco Simoes',
      author_email='msimoes@dei.uc.pt',
      package_dir={"": "src"},
      packages = find_packages(
            where='src',
      ),
      install_requires=required,
      zip_safe=False)