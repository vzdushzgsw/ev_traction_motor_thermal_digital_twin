import numpy as np
import pandas as pd
import time

class TractionMotorDigitalTwin:
    def __init__(self, baseline_temp=30.0):
        print("Initializing Virtual Asset: EV Traction Motor Digital Twin...")
        self.winding_resistance_ohm = 0.05
        self.thermal_capacitance = 1200.0
        self.cooling_efficiency_factor = 45.0
        
        self.stator_temperature_celsius = baseline_temp
        self.cumulative_thermal_stress = 0.0

    def update_thermal_state(self, current_amps, coolant_flow_lmin, ambient_temp=25.0, dt_seconds=1.0):
        # I²R Copper Losses
        heat_generated = (current_amps ** 2) * self.winding_resistance_ohm
        
        # Convection Cooling
        effective_cooling = self.cooling_efficiency_factor * (coolant_flow_lmin / 5.0)
        heat_dissipated = effective_cooling * (self.stator_temperature_celsius - ambient_temp)
        
        # Thermodynamics: Net Heat updates Temperature
        net_heat = heat_generated - heat_dissipated
        self.stator_temperature_celsius += (net_heat / self.thermal_capacitance) * dt_seconds

    def get_health_telemetry(self):
        return {"Stator_Temp_C": round(self.stator_temperature_celsius, 2)}

# SIMULATION RUNTIME & DATA EXPORT
if __name__ == "__main__":
    my_motor_twin = TractionMotorDigitalTwin(baseline_temp=40.0)
    print("\nBEGINNING TRANSIENT CYCLE SIMULATION")
    
    telemetry_clipboard = []
    
    # 10-second driving cycle: (Amps, Coolant Flow L/min)
    driving_cycle = [
        (150, 6.0), (250, 6.0), (380, 4.0), (420, 3.5), (450, 3.0),
        (450, 3.0), (350, 5.0), (200, 8.0), (100, 10.0), (80, 12.0)
    ]
    
    for second, (amps, flow) in enumerate(driving_cycle, start=1):
        my_motor_twin.update_thermal_state(amps, flow, dt_seconds=1.0)
        status = my_motor_twin.get_health_telemetry()
        
        # If temp > 140C, trigger the critical boundary (1)
        is_critical = 1 if status['Stator_Temp_C'] > 140.0 else 0
        
        telemetry_clipboard.append({
            'Stator_Current_Amps': amps,
            'Coolant_Flow_Lmin': flow,
            'Turtle_Trigger': is_critical
        })
        print(f"Time: {second}s | Temp: {status['Stator_Temp_C']}°C | Critical Status: {is_critical}")
        time.sleep(0.2)
        
    print("\nSimulation Complete. Generating synthetic data file...")
    powertrain_telemetry_df = pd.DataFrame(telemetry_clipboard)
    powertrain_telemetry_df.to_csv('synthetic_motor_data.csv', index=False)
    print("SUCCESS: 'synthetic_motor_data.csv' created!")
