import random
import time
from typing import Dict, Any


class EnergySessionSimulator:
    def __init__(self):
        self.session_id = 1
        self.start_time = time.time()
        self.cumulative_duration = 0
        self.cumulative_energy = 0
        self.devices = {"device1": False, "device2": False, "device3": False,
                        "device4": False, "device5": False, "device6": False}  # Demo devices :)

    def simulate_energy_session_payload(self) -> Dict[str, Any]:
        """
        Simulate a payload representing an energy delivery session, typical in a household setting
        with multiple devices. This simulation reflects the variable energy consumption as 
        different devices are turned on and off over time.

        In each simulation step, the method randomly changes the status (on/off) of each device,
        affecting the cumulative energy consumption rate. The cumulative energy and duration are
        updated based on the time elapsed and the number of active devices.

        The method also calculates the cost of energy consumed, considering a predefined rate.

        Returns:
            Dict[str, Any]: A dictionary containing the session's ongoing data, including:
                - 'session_id': Identifier for the session.
                - 'energy_delivered_in_kWh': Total energy delivered in the session (rounded to 2 decimals).
                - 'duration_in_seconds': Total duration of the session in seconds.
                - 'session_cost_in_cents': Total cost of the energy delivered, calculated at a specific rate.
        """
        current_time = time.time()
        # Time elapsed since the start of the session
        elapsed_time = current_time - self.start_time

        # Update cumulative duration and energy
        self.cumulative_duration += elapsed_time

        # Simulate devices turning on/off
        for device in self.devices:
            self.devices[device] = random.choice([True, False])

        # Calculate energy consumption based on active devices
        active_devices = sum(self.devices.values())
        # Adjusting the rate based on active devices
        energy_rate = 0.0001 * active_devices

        # Demo charging rate in kWh per second
        self.cumulative_energy += elapsed_time * energy_rate

        # Demo cost model
        rate_per_kWh = 23.0  # Rate per kWh (cents)
        session_cost_in_cents = round(self.cumulative_energy * rate_per_kWh)

        message = {
            "session_id": self.session_id,
            "energy_delivered_in_kWh": round(self.cumulative_energy, 2),
            "duration_in_seconds": int(self.cumulative_duration),
            "session_cost_in_cents": session_cost_in_cents
        }

        self.start_time = current_time  # Reset start time for next interval
        return message
