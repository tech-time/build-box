TODO: Add a note on virtualenv setup


### Activate virtualenv:
. ~/projects/build-box-venv/bin/activate

### Tests 
#### Run all test (in src):
`(build-box-venv) pi@raspberrypi:~/projects/build-box/src $ python -m pytest`

#### Run specific test (in src):
`(build-box-venv) pi@raspberrypi:~/projects/build-box/src $ python -m pytest tests/test_leddigits.py`

#### Run tests from pycharm
~~~~
Run -> Edit Configurations

+ -> Python tests -> py.test
Target: Python
First input field:  tests

Working directory : C:\Users\XXXXX\PycharmProjects\build-box\src
~~~~

### Launch
#### Run main (in src)
`(build-box-venv) pi@raspberrypi:~/projects/build-box/src $ python -m buildbox.buildbox`

