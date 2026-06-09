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
    print("Generating comprehensive dataset (Safe + Critical)...")
    telemetry_clipboard = []
    
    # to test a wide range
    for amps in np.linspace(100, 700, 25):  
        for flow in np.linspace(0.5, 5.0, 10): 
            
            # Reset motor for every scenario
            twin = TractionMotorDigitalTwin(baseline_temp=30.0)
            
            # Simulate 60 seconds of operation
            for _ in range(60):
                twin.update_thermal_state(amps, flow, dt_seconds=1.0)
            
            temp = twin.stator_temperature_celsius
            is_critical = 1 if temp > 140.0 else 0
            
            # Append this "outcome" to our data list
            telemetry_clipboard.append({
                'Stator_Current_Amps': amps,
                'Coolant_Flow_Lmin': flow,
                'Stator_Temp_C': temp,
                'Turtle_Trigger': is_critical
            })

    # Save and confirm
    df = pd.DataFrame(telemetry_clipboard)
    df.to_csv('synthetic_motor_data.csv', index=False)
    
    # Verification
    print(f"Data generated! Critical events found: {df['Turtle_Trigger'].sum()}")
