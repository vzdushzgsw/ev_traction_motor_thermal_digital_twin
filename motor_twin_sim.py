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
    print("\nBEGINNING MULTI-SCENARIO SIMULATION")    
    telemetry_clipboard = []
    #define 3 different test scenarios: (Name, Amps, Coolant Flow)
    scenarios = [
        ("Slow Cruise", 100, 10.0),
        ("Normal Commute", 250, 6.0),
        ("Overload", 550, 2.0)
    ]    
    for scenario_name, base_amps, base_flow in scenarios:
        print(f"\n--- Running Scenario: {scenario_name} ---")

        #creating new motor (resetting temp to 40) for each test!
        my_motor_twin =  TractionMotorDigitalTwin(baseline_temp=40.0)
        for second in range(1,31):
            my_motor_twin.update_thermal_state(base_amps, base_flow, dt_seconds=1.0)
            status = my_motor_twin.get_health_telemetry() 
            
        # If temp > 140C, trigger the critical boundary (1)
        is_critical = 1 if status['Stator_Temp_C'] > 140.0 else 0
        
        #save data to master list        
        telemetry_clipboard.append({
            'Scenario': scenario_name,
            'Stator_Current_Amps': base_amps,
            'Coolant_Flow_Lmin': base_flow,
            'Stator_Temp_C': status['Stator_Temp_C'],
            'Turtle_Trigger': is_critical
        })
        #Print update to the screen
        print(f"Time: {second}s | Temp: {status['Stator_Temp_C']}°C | Critical Status: {is_critical}")
        #time.sleep(0.05) #speeding up sleep timer

    #once all scenarios are done, generates the master file        
    print("\nSimulation Complete. Generating synthetic data file...")
    powertrain_telemetry_df = pd.DataFrame(telemetry_clipboard)
    powertrain_telemetry_df.to_csv('synthetic_motor_data.csv', index=False)
    print("SUCCESS: 'synthetic_motor_data.csv' created!")
