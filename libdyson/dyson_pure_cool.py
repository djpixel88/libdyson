"""Dyson Pure Cool fan."""

from typing import Optional

from .dyson_device import DysonFanDevice


class DysonPureCool(DysonFanDevice):
    """Dyson Pure Cool fan."""

    @property
    def fan_power(self) -> bool:
        """Return fan power of the device."""
        return self._get_field_value(self._status, "fpwr") == "ON"

    @property
    def auto_mode(self) -> bool:
        """Return auto mode status."""
        return self._get_field_value(self._status, "auto") == "ON"

    @property
    def oscillation(self) -> bool:
        """Return oscillation status."""
        return self._get_field_value(self._status, "oson") == "OION"

    @property
    def oscillation_status(self) -> bool:
        """Return the status of oscillation."""
        return self._get_field_value(self._status, "oscs") == "ON"

    @property
    def oscillation_angle_low(self) -> int:
        """Return oscillation low angle."""
        return int(self._get_field_value(self._status, "osal"))

    @property
    def oscillation_angle_high(self) -> int:
        """Return oscillation high angle."""
        return int(self._get_field_value(self._status, "osau"))

    @property
    def front_airflow(self) -> bool:
        """Return if airflow from front is on."""
        return self._get_field_value(self._status, "fdir") == "ON"

    @property
    def night_mode_speed(self) -> int:
        """Return speed in night mode."""
        return int(self._get_field_value(self._status, "nmdv"))

    @property
    def carbon_filter_life(self) -> Optional[int]:
        """Return carbon filter life in percentage."""
        filter_life = self._get_field_value(self._status, "cflr")
        if filter_life == "INV":
            return None
        return int(filter_life)

    @property
    def hepa_filter_life(self) -> Optional[int]:
        """Return HEPA filter life in percentage."""
        return int(self._get_field_value(self._status, "hflr"))

    @property
    def particulate_matter_2_5(self):
        """Return PM 2.5 in micro grams per cubic meter."""
        return int(self._get_environmental_field_value("pm25"))

    @property
    def particulate_matter_10(self):
        """Return PM 2.5 in micro grams per cubic meter."""
        return int(self._get_environmental_field_value("pm10"))

    @property
    def volatile_organic_compounds(self):
        """Return VOCs in micro grams per cubic meter."""
        return int(self._get_environmental_field_value("va10"))

    @property
    def nitrogen_dioxide(self):
        """Return nitrogen dioxide level in micro grams per cubic meter."""
        return int(self._get_environmental_field_value("noxl"))

    def turn_on(self) -> None:
        """Turn on the device."""
        self._set_configuration(fpwr="ON")

    def turn_off(self) -> None:
        """Turn off the device."""
        self._set_configuration(fpwr="OFF")

    def _set_speed(self, speed: int) -> None:
        self._set_configuration(fpwr="ON", fnsp=f"{speed:04d}")

    def enable_auto_mode(self) -> None:
        """Turn on auto mode."""
        self._set_configuration(auto="ON")

    def disable_auto_mode(self) -> None:
        """Turn off auto mode."""
        self._set_configuration(auto="OFF")

    def enable_oscillation(
        self,
        angle_low: Optional[int] = None,
        angle_high: Optional[int] = None,
    ) -> None:
        """Turn on oscillation."""
        if angle_low is None:
            angle_low = self.oscillation_angle_low
        if angle_high is None:
            angle_high = self.oscillation_angle_high

        if not 5 <= angle_low <= 355:
            raise ValueError("angle_low must be between 5 and 355")
        if not 5 <= angle_high <= 355:
            raise ValueError("angle_high must be between 5 and 355")
        if angle_low != angle_high and angle_low + 30 > angle_high:
            raise ValueError(
                "angle_high must be either equal to angle_low or at least 30 larger than angle_low"
            )

        self._set_configuration(
            oson="OION",
            fpwr="ON",
            ancp="CUST",
            osal=f"{angle_low:04d}",
            osau=f"{angle_high:04d}",
        )

    def disable_oscillation(self) -> None:
        """Turn off oscillation."""
        self._set_configuration(oson="OIOF")

    def enable_continuous_monitoring(self) -> None:
        """Turn on continuous monitoring."""
        self._set_configuration(
            fpwr="ON" if self.fan_power else "OFF",  # Not sure about this
            rhtm="ON",
        )

    def disable_continuous_monitoring(self) -> None:
        """Turn off continuous monitoring."""
        self._set_configuration(
            fpwr="ON" if self.fan_power else "OFF",
            rhtm="OFF",
        )

    def enable_front_airflow(self) -> None:
        """Turn on front airflow."""
        self._set_configuration(fdir="ON")

    def disable_front_airflow(self) -> None:
        """Turn off front airflow."""
        self._set_configuration(fdir="OFF")
