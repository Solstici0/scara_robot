# SCARA
[![Documentation Status](https://readthedocs.org/projects/scara-robot/badge/?version=latest)](https://scara-robot.readthedocs.io/en/latest/?badge=latest)

A python library and documentation to interact with Solsticio's Selective 
Compliance Articulated Robot Arm

You can read the SCARA robot documentation [here](https://scara-robot.readthedocs.io/en/latest/)

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
