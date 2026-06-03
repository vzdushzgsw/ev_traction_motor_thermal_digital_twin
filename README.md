## EV Traction Motor Thermal Digital Twin

### Data Generation
Wanted to move beyond CAD and explore real-time thermodynamic simulation. This repository acts as a physical "Digital Twin" of an EV traction motor. 

It uses fundamental heat transfer equations to simulate stator copper losses and internal temperature accumulation over a continuous driving cycle.

**The Output:** This Python script generates synthetic CSV telemetry data based on real physics (`synthetic_motor_data.csv`).

--------------
### Integration

The data generated in this repository is directly consumed by my [Traction Motor Predictive ML Model](https://github.com/vzdushzgsw/traction-motor-thermal-predictive-model) to train a vehicle control unit override system.
