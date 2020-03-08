# MotorRefGen
Generate realistic reference speed and load trajectories for electrical motor.

### Matlab python engine installation (if not already done for MotorSim library)
```
cd /usr/local/MATLAB/{VERSION}/extern/engines/
sudo chmod -R 775 python
cd python
pip install -e .
```

### Install this library
```
pip install -r requirements.txt
pip install -e .
```

### Run tests
```
pytest
```
