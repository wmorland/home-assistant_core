"""Support for the SwitchBot Evaporative Humidifier (Auto-refill)."""

from typing import Any

from switchbot_api import CommonCommands, HumidifierCommands

from homeassistant.components.humidifier import (
    MODE_AUTO,
    MODE_SLEEP,
    HumidifierDeviceClass,
    HumidifierEntity,
    HumidifierEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import SwitchbotCloudData
from .const import DOMAIN
from .entity import SwitchBotCloudEntity

_SWITCHBOT_HUMIDIFIER_MODES: dict[str, int] = {
    "level_4": 1,
    "level_3": 2,
    "level_2": 3,
    "level_1": 4,
    "humidity": 5,
    MODE_SLEEP: 6,
    MODE_AUTO: 7,
    "drying": 8,
}


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up SwitchBot Cloud entry."""
    data: SwitchbotCloudData = hass.data[DOMAIN][config.entry_id]
    async_add_entities(
        SwitchBotCloudHumidifier(data.api, device, coordinator)
        for device, coordinator in data.devices.humidifiers
    )


class SwitchBotCloudHumidifier(SwitchBotCloudEntity, HumidifierEntity):
    """Representation of a SwitchBot Evaporative Humidifier (Auto-refill)."""

    _attr_name = None

    _attr_available_modes = list(_SWITCHBOT_HUMIDIFIER_MODES.keys())
    _attr_device_class = HumidifierDeviceClass.HUMIDIFIER
    _attr_supported_features = HumidifierEntityFeature.MODES

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the device on."""
        await self.send_api_command(CommonCommands.ON)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the device off."""
        await self.send_api_command(CommonCommands.OFF)

    async def async_set_humidity(self, humidity: int) -> None:
        """Set the target humidity level."""
        await self.send_api_command(
            HumidifierCommands.SET_MODE,
            parameters={
                "mode": _SWITCHBOT_HUMIDIFIER_MODES["humidity"],
                "targetHumidify": humidity,
            },
        )

    async def async_set_mode(self, mode: str) -> None:
        """Set the mode of the humidifier."""
        await self.send_api_command(
            "set_mode", parameters={"mode": _SWITCHBOT_HUMIDIFIER_MODES[mode]}
        )
