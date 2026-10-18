import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    UNIT_PERCENT,
    DEVICE_CLASS_BATTERY,
    ICON_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
    UNIT_CELSIUS,
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_ACCURACY_DECIMALS,
)

from . import WavinAHC9000

CONF_PARENT_ID = "wavin_ahc9000_id"
CONF_CHANNEL = "channel"
CONF_TYPE = "type"

CONFIG_SCHEMA = sensor.sensor_schema().extend(
    {
        cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
        cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
        cv.Required(CONF_TYPE): cv.one_of(
            "battery",
            "temperature",
            "comfort_setpoint",
            "floor_temperature",
            "floor_min_temperature",
            "floor_max_temperature",
            lower=True,
        ),
    }
)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_PARENT_ID])

    cfg = dict(config)

    if cfg[CONF_TYPE] == "battery":
        cfg.setdefault(CONF_DEVICE_CLASS, DEVICE_CLASS_BATTERY)
        cfg.setdefault(CONF_UNIT_OF_MEASUREMENT, UNIT_PERCENT)
        cfg.setdefault(CONF_ICON, ICON_BATTERY)
        cfg.setdefault(CONF_ACCURACY_DECIMALS, 0)
    else:
        cfg.setdefault(CONF_DEVICE_CLASS, DEVICE_CLASS_TEMPERATURE)
        cfg.setdefault(CONF_UNIT_OF_MEASUREMENT, UNIT_CELSIUS)
        cfg.setdefault(CONF_ACCURACY_DECIMALS, 1)

    sens = await sensor.new_sensor(cfg)

    if cfg[CONF_TYPE] == "battery":
        cg.add(hub.add_channel_battery_sensor(cfg[CONF_CHANNEL], sens))

    elif cfg[CONF_TYPE] == "comfort_setpoint":
        cg.add(hub.add_channel_comfort_setpoint_sensor(cfg[CONF_CHANNEL], sens))

    elif cfg[CONF_TYPE] == "floor_temperature":
        cg.add(hub.add_channel_floor_temperature_sensor(cfg[CONF_CHANNEL], sens))

    elif cfg[CONF_TYPE] == "floor_min_temperature":
        cg.add(hub.add_channel_floor_min_temperature_sensor(cfg[CONF_CHANNEL], sens))

    elif cfg[CONF_TYPE] == "floor_max_temperature":
        cg.add(hub.add_channel_floor_max_temperature_sensor(cfg[CONF_CHANNEL], sens))

    else:
        cg.add(hub.add_channel_temperature_sensor(cfg[CONF_CHANNEL], sens))

    cg.add(hub.add_active_channel(cfg[CONF_CHANNEL]))
