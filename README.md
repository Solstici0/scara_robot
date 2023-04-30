# SCARA
A python library and documentation to interact with Solsticio's Selective 
Compliance Articulated Robot Arm

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

**Software**
- [ ] Define project structure
- [ ] Include logger 
- [ ] Code minimum methods
  * [ ] Inverse kinematics
  * [ ] Homing and initializaiton
  * [ ] Joint class 
  * [ ] Scara class
> Recordatorio wis
Crear clase joint
  + Joint(name, axis, gains)
  + Luego se puede tener un dict {joint.name: joint}
  + Calibration se aplica sobre cada joint (joint.calibrate(),
    tb incluir otras como joint.requeste_state(), etc)
  + Luego esta la clase nelen, que inicializa los joints y tiene
    funciones de más alto nivel (nelen.homing() y nelen.move()
    nelen.move_with_pump(), otras? )

**Mechanical** 
- [ ] Drill octagonal plate
- [ ] Weld octagonal plate to structure
- [ ] Fabricate wheel plates 
- [ ] Weld wheel plates to structure
- [ ] Buy and install wheels 
- [ ] Drill structure and install electrical box

## References
