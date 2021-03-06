"""Support for Rfplayer sensors."""
from .rfpparser import PACKET_FIELDS, UNITS
import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from . import (
    CONF_ALIASES,
    CONF_AUTOMATIC_ADD,
    CONF_DEVICES,
    DATA_DEVICE_REGISTER,
    DATA_ENTITY_LOOKUP,
    EVENT_KEY_ID,
    EVENT_KEY_SENSOR,
    EVENT_KEY_UNIT,
    SIGNAL_AVAILABILITY,
    SIGNAL_HANDLE_EVENT,
    TMP_ENTITY,
    RfplayerDevice,
)

SENSOR_ICONS = {
    "humidity": "mdi:water-percent",
    "battery": "mdi:battery",
    "temperature": "mdi:thermometer",
}

CONF_SENSOR_TYPE = "sensor_type"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_AUTOMATIC_ADD, default=True): cv.boolean,
        vol.Optional(CONF_DEVICES, default={}): {
            cv.string: vol.Schema(
                {
                    vol.Optional(CONF_NAME): cv.string,
                    vol.Required(CONF_SENSOR_TYPE): cv.string,
                    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
                    vol.Optional(CONF_ALIASES, default=[]): vol.All(
                        cv.ensure_list, [cv.string]
                    ),
                }
            )
        },
    },
    extra=vol.ALLOW_EXTRA,
)


def lookup_unit_for_sensor_type(sensor_type):
    """Get unit for sensor type.

    Async friendly.
    """
    field_abbrev = {v: k for k, v in PACKET_FIELDS.items()}

    return UNITS.get(field_abbrev.get(sensor_type))


def devices_from_config(domain_config):
    """Parse configuration and add Rfplayer sensor devices."""
    devices = []
    for device_id, config in domain_config[CONF_DEVICES].items():
        _LOGGER.debug("devices_from_config: %s",str(device_id))
        if ATTR_UNIT_OF_MEASUREMENT not in config:
            config[ATTR_UNIT_OF_MEASUREMENT] = lookup_unit_for_sensor_type(
                config[CONF_SENSOR_TYPE]
            )
        device = RfplayerSensor(device_id, **config)
        devices.append(device)

    return devices


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Rfplayer platform."""
    async_add_entities(devices_from_config(config))

    async def add_new_device(event):
        """Check if device is known, otherwise create device entity."""
        device_id = event[EVENT_KEY_ID]

        device = RfplayerSensor(
            device_id,
            event[EVENT_KEY_SENSOR],
            event[EVENT_KEY_UNIT],
            initial_event=event,
        )
        # Add device entity
        async_add_entities([device])

    if config[CONF_AUTOMATIC_ADD]:
        hass.data[DATA_DEVICE_REGISTER][EVENT_KEY_SENSOR] = add_new_device


class RfplayerSensor(RfplayerDevice):
    """Representation of a Rfplayer sensor."""

    def __init__(
        self, device_id, sensor_type, unit_of_measurement, initial_event=None, **kwargs
    ):
        """Handle sensor specific args and super init."""
        self._sensor_type = sensor_type
        self._unit_of_measurement = unit_of_measurement
        _LOGGER.debug("RfplayerSensor id:%s,sensor_type:%s,unit_of_measurement:%s",
                       device_id,sensor_type,unit_of_measurement)
        super().__init__(device_id, initial_event=initial_event, **kwargs)

    def _handle_event(self, event):
        """Domain specific event handler."""
        self._state = event["value"]

    async def async_added_to_hass(self):
        """Register update callback."""
        # Remove temporary bogus entity_id if added
        tmp_entity = TMP_ENTITY.format(self._device_id)
        if (
            tmp_entity
            in self.hass.data[DATA_ENTITY_LOOKUP][EVENT_KEY_SENSOR][self._device_id]
        ):
            self.hass.data[DATA_ENTITY_LOOKUP][EVENT_KEY_SENSOR][
                self._device_id
            ].remove(tmp_entity)

        # Register id and aliases
        self.hass.data[DATA_ENTITY_LOOKUP][EVENT_KEY_SENSOR][self._device_id].append(
            self.entity_id
        )
        if self._aliases:
            for _id in self._aliases:
                self.hass.data[DATA_ENTITY_LOOKUP][EVENT_KEY_SENSOR][_id].append(
                    self.entity_id
                )
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_AVAILABILITY, self._availability_callback
            )
        )
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                SIGNAL_HANDLE_EVENT.format(self.entity_id),
                self.handle_event_callback,
            )
        )

        # Process the initial event now that the entity is created
        if self._initial_event:
            self.handle_event_callback(self._initial_event)

    @property
    def unit_of_measurement(self):
        """Return measurement unit."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return value."""
        return self._state

    @property
    def icon(self):
        """Return possible sensor specific icon."""
        if self._sensor_type in SENSOR_ICONS:
            return SENSOR_ICONS[self._sensor_type]
