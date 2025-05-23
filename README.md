# SCARA
[![Documentation Status](https://readthedocs.org/projects/scara-robot/badge/?version=latest)](https://scara-robot.readthedocs.io/en/latest/?badge=latest) ![Flake8 Linting](https://github.com/Solstici0/scara_robot/actions/workflows/lint.yml/badge.svg)


A python library and documentation to interact with Solsticio's Selective 
Compliance Articulated Robot Arm

You can read the SCARA robot documentation [here](https://scara-robot.readthedocs.io/en/latest/)

## Connecting with the real robot

If the `SCARA` network is available, you can connect with 
the robot via ssh. To achieve that do:
1. Connect to the SCARA netwotk. the password is: `scara_nelen`
2. Connect to the robot using the ssh protocol:
``` bash
$ ssh ubuntu@192.168.0.101 
# password: rfidudes 
# Then activate the nelen env (already created)
$ source nelen/bin/activate
```

## Usage

You can start by creating a virtual environment and install scara package 
in development mode:

```bash
$ python -m venv nelen
$ source nelen/bin/activate
$ pip install -e .
```

Then you can validate that everything is working well by importing the library 
and create an scara object

``` bash
$ python 
>>> import scara
>>> scara.Robot()
```

### Tree structure


## TODO



**Hardware**
- [ ] Install Pull-up pcbs
- [ ] Install CAN pcb 
- [ ] Install fans
- [ ] Include minimum hardware documentation 

**Software**
- [X] Define project structure
- [X] Include logger 
- [X] Code minimum methods
  * [X] Inverse kinematics
  * [X] Homing and initializaiton
  * [X] Joint class 
  * [X] Scara class
- [ ] Include tests
  * [ ] Inverse kinematics
  * [ ] With FakeOdrv
- [ ] Handle errors!

**Mechanical** 
- [ ] Drill octagonal plate
- [ ] Weld octagonal plate to structure
- [ ] Fabricate wheel plates 
- [ ] Weld wheel plates to structure
- [ ] Buy and install wheels 
- [ ] Drill structure and install electrical box

**All**
- [ ] Improve documentation
  * [ ] Include introduction
  * [ ] Include links to thesis

## References
