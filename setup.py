from setuptools import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='atari_ai_controller',
      version='0.1',
      description='An artificial intelligence controller for the atari game river raid',
      url='https://github.com/disbeat/atari_ai_controller',
      author='Marco Simoes',
      author_email='msimoes@dei.uc.pt',
      packages=['configs', 'emg', 'pose_tracker', 'ai', 'atari_emulator'],
      package_dir={'configs': 'src/configs', 'emg': 'src/emg', 'pose_tracker': 'src/pose_tracker', 'ai': 'src/ai', 'atari_emulator': 'src/atari_emulator'},
      install_requires=required,
      zip_safe=False)