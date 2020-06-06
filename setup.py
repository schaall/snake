from setuptools import setup

setup(
  name="snake", 
  version="0.1.0",
  description="A toolkit for training reinforcement learning agents on the game snake.", 
  url='https://github.com/mfiless/snake.git',
  author='Leon Shams',
  license='MIT',
  packages=['snake'],
  install_requires=["pygame>=1.9.2"],
  zip_safe=False, 
  python_requires='>=3.6'
)
