"""Support gathering system information of hosts which are running glances."""

from __future__ import annotations
import logging

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    UnitOfDataRate,
    UnitOfInformation,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CPU_ICON, DOMAIN
from .coordinator import Glances2ConfigEntry, Glances2DataUpdateCoordinator
_LOGGER = logging.getLogger(__name__)

@dataclass(frozen=True, kw_only=True)
class Glances2SensorEntityDescription(SensorEntityDescription):
    """Describe Glances sensor entity."""
    type: str
    type: dict
    type: list



SENSOR_TYPES = {
    ("fs", "disk_use_percent"): Glances2SensorEntityDescription(
        key="disk_use_percent",
        type="fs",
        translation_key="disk_usage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("fs", "disk_use"): Glances2SensorEntityDescription(
        key="disk_use",
        type="fs",
        translation_key="disk_used",
        native_unit_of_measurement=UnitOfInformation.GIBIBYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("fs", "disk_free"): Glances2SensorEntityDescription(
        key="disk_free",
        type="fs",
        translation_key="disk_free",
        native_unit_of_measurement=UnitOfInformation.GIBIBYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("diskio", "read"): Glances2SensorEntityDescription(
        key="read",
        type="diskio",
        translation_key="diskio_read",
        suggested_display_precision=3,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABYTES_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("diskio", "write"): Glances2SensorEntityDescription(
        key="write",
        type="diskio",
        translation_key="diskio_write",
        suggested_display_precision=3,
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABYTES_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("mem", "memory_use_percent"): Glances2SensorEntityDescription(
        key="memory_use_percent",
        type="mem",
        translation_key="memory_usage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("mem", "memory_use"): Glances2SensorEntityDescription(
        key="memory_use",
        type="mem",
        translation_key="memory_use",
        native_unit_of_measurement=UnitOfInformation.MEBIBYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("mem", "memory_free"): Glances2SensorEntityDescription(
        key="memory_free",
        type="mem",
        translation_key="memory_free",
        native_unit_of_measurement=UnitOfInformation.MEBIBYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("memswap", "swap_use_percent"): Glances2SensorEntityDescription(
        key="swap_use_percent",
        type="memswap",
        translation_key="swap_usage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("memswap", "swap_use"): Glances2SensorEntityDescription(
        key="swap_use",
        type="memswap",
        translation_key="swap_use",
        native_unit_of_measurement=UnitOfInformation.GIBIBYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("memswap", "swap_free"): Glances2SensorEntityDescription(
        key="swap_free",
        type="memswap",
        translation_key="swap_free",
        native_unit_of_measurement=UnitOfInformation.GIBIBYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("load", "processor_load"): Glances2SensorEntityDescription(
        key="processor_load",
        type="load",
        translation_key="processor_load",
        icon=CPU_ICON,
        suggested_display_precision=3,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("load", "processor_load_1m"): Glances2SensorEntityDescription(
        key="processor_load_1m",
        type="load",
        translation_key="processor_load_1m",
        icon=CPU_ICON,
        suggested_display_precision=3,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("load", "processor_load_5m"): Glances2SensorEntityDescription(
        key="processor_load_5m",
        type="load",
        translation_key="processor_load_5m",
        icon=CPU_ICON,
        suggested_display_precision=3,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("processcount", "process_running"): Glances2SensorEntityDescription(
        key="process_running",
        type="processcount",
        translation_key="process_running",
        icon=CPU_ICON,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("processcount", "process_total"): Glances2SensorEntityDescription(
        key="process_total",
        type="processcount",
        translation_key="process_total",
        icon=CPU_ICON,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("processcount", "process_thread"): Glances2SensorEntityDescription(
        key="process_thread",
        type="processcount",
        translation_key="process_threads",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("processcount", "process_sleeping"): Glances2SensorEntityDescription(
        key="process_sleeping",
        type="processcount",
        translation_key="process_sleeping",
        icon=CPU_ICON,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("cpu", "cpu_use_percent"): Glances2SensorEntityDescription(
        key="cpu_use_percent",
        type="cpu",
        translation_key="cpu_usage",
        native_unit_of_measurement=PERCENTAGE,
        icon=CPU_ICON,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("sensors", "temperature_core"): Glances2SensorEntityDescription(
        key="temperature_core",
        type="sensors",
        translation_key="temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("sensors", "temperature_hdd"): Glances2SensorEntityDescription(
        key="temperature_hdd",
        type="sensors",
        translation_key="temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("sensors", "fan_speed"): Glances2SensorEntityDescription(
        key="fan_speed",
        type="sensors",
        translation_key="fan_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("sensors", "battery"): Glances2SensorEntityDescription(
        key="battery",
        type="sensors",
        translation_key="charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("containers", "containerslist"): Glances2SensorEntityDescription(
        key="containerslist",
        type="containers",
        translation_key="containerslist",
    ),
    ("containers", "container_cpu_use"): Glances2SensorEntityDescription(
        key="container_cpu_use",
        type="containers",
        translation_key="percontainer_cpu_use",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("containers", "container_memory_use"): Glances2SensorEntityDescription(
        key="container_memory_use",
        type="containers",
        translation_key="percontainer_memory_use",
        native_unit_of_measurement=UnitOfInformation.MEBIBYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("docker", "docker_active"): Glances2SensorEntityDescription(
        key="docker_active",
        type="docker",
        translation_key="container_active",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("docker", "docker_cpu_use"): Glances2SensorEntityDescription(
        key="docker_cpu_use",
        type="docker",
        translation_key="container_cpu_usage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("docker", "docker_memory_use"): Glances2SensorEntityDescription(
        key="docker_memory_use",
        type="docker",
        translation_key="container_memory_used",
        native_unit_of_measurement=UnitOfInformation.MEBIBYTES,
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("raid", "used"): Glances2SensorEntityDescription(
        key="used",
        type="raid",
        translation_key="raid_used",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("computed", "uptime"): Glances2SensorEntityDescription(
        key="uptime",
        type="computed",
        translation_key="uptime",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    ("gpu", "mem"): Glances2SensorEntityDescription(
        key="mem",
        type="gpu",
        translation_key="gpu_memory_usage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("gpu", "proc"): Glances2SensorEntityDescription(
        key="proc",
        type="gpu",
        translation_key="gpu_processor_usage",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
    ),
    ("gpu", "temperature"): Glances2SensorEntityDescription(
        key="temperature",
        type="gpu",
        translation_key="temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("gpu", "fan_speed"): Glances2SensorEntityDescription(
        key="fan_speed",
        type="gpu",
        translation_key="fan_speed",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("network", "rx"): Glances2SensorEntityDescription(
        key="rx",
        type="network",
        translation_key="network_rx",
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        device_class=SensorDeviceClass.DATA_RATE,
        suggested_display_precision=3,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("network", "tx"): Glances2SensorEntityDescription(
        key="tx",
        type="network",
        translation_key="network_tx",
        native_unit_of_measurement=UnitOfDataRate.BYTES_PER_SECOND,
        suggested_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        suggested_display_precision=3,
        device_class=SensorDeviceClass.DATA_RATE,
        state_class=SensorStateClass.MEASUREMENT,
    ), 
    ("amps", "resultcount"): Glances2SensorEntityDescription(
        key="resultcount",
        type="amps",
        translation_key="amps_resultcount",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ("amps", "result"): Glances2SensorEntityDescription(
        key="result",
        type="amps",
        translation_key="amps_result",
    ),
    ("raid", "available"): Glances2SensorEntityDescription(
        key="available",
        type="raid",
        translation_key="raid_available",
    ),
    ("raid", "status"): Glances2SensorEntityDescription(
        key="status",
        type="raid",
        translation_key="raid_status",
    ),
    ("raid", "type"): Glances2SensorEntityDescription(
        key="type",
        type="raid",
        translation_key="raid_type",
    ),
}


   


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: Glances2ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Glances sensors."""

    coordinator = config_entry.runtime_data
    entities: list[Glances2Sensor] = []

    for sensor_type, sensors in coordinator.data.items():
        _LOGGER.debug("sensor_type async setup : %s",str(sensor_type))
        if sensor_type in ["fs", "diskio", "sensors", "raid", "gpu", "network","amps"]:
            entities.extend(
                Glances2Sensor(
                    coordinator,
                    sensor_description,
                    sensor_label,
                )
                for sensor_label, params in sensors.items()   
                for param in params
                if (sensor_description := SENSOR_TYPES.get((sensor_type, param)))
            )
        else:
            for sensor in sensors:
               _LOGGER.debug("   sensor async setup : %s",str(sensor))
   
            entities.extend(
                Glances2Sensor(
                    coordinator,
                    sensor_description,
                )
                for sensor in sensors
                if (sensor_description := SENSOR_TYPES.get((sensor_type, sensor)))
            )

           
    async_add_entities(entities)


class Glances2Sensor(CoordinatorEntity[Glances2DataUpdateCoordinator], SensorEntity):
    """Implementation of a Glances2 sensor."""

    entity_description: Glances2SensorEntityDescription
    _attr_has_entity_name = True
    _data_valid: bool = False

    def __init__(
        self,
        coordinator: Glances2DataUpdateCoordinator,
        description: Glances2SensorEntityDescription,
        sensor_label: str = "",
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        # _LOGGER.debug("Glances2Sensor init")
        self._sensor_label = sensor_label
        self.entity_description = description
        
        # _LOGGER.debug("_attr_translation_placeholders %s",str(sensor_label))
        if sensor_label:
            self._attr_translation_placeholders = {"sensor_label": sensor_label}
            self._attr_name = f"{sensor_label}_{description.key}"
        else:
            self._attr_name = f"{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer="Glances2",
            name=coordinator.host,
        )
        # self._attr_name = f"{sensor_label}_{description.key}"
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}-{sensor_label}-{description.key}"
        )
        # _LOGGER.debug("Sensor Label %s",sensor_label)
        # _LOGGER.debug("Description %s", description)
        # _LOGGER.debug("_attr_unique_id %s",self._attr_unique_id)
        # # _LOGGER.debug("description name %s",self.entity_description.name)
        self._update_native_value()

    @property
    def available(self) -> bool:
        """Set sensor unavailable when native value is invalid."""
        return super().available and self._data_valid

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_native_value()
        super()._handle_coordinator_update()

    def _update_native_value(self) -> None:
        """Update sensor native value from coordinator data."""
        data = self.coordinator.data.get(self.entity_description.type)
        # _LOGGER.debug("entity_description.type %s",str(self.entity_description.type))
        # _LOGGER.debug("entity_description.key %s",str(self.entity_description.key))
        # _LOGGER.debug("sensor label %s",str(self._sensor_label))
        # _LOGGER.debug("_numeric_state_expected %s",str(self._numeric_state_expected))
        # _LOGGER.debug("data: %s",str(data))
        
        if data and (dict_val := data.get(self._sensor_label)):
            self._attr_native_value = dict_val.get(self.entity_description.key)
        elif data and (self.entity_description.key in data):
            self._attr_native_value = data.get(self.entity_description.key)
        else:
            self._attr_native_value = None
            # self._attr_native_value = 'None'
        self._update_data_valid()
        # _LOGGER.debug("data_valid: %s",str(self._data_valid))

    def _update_data_valid(self) -> None:
        self._data_valid = self._attr_native_value is not None 
        # and (
        #     not self._numeric_state_expected
        #     or isinstance(self._attr_native_value, (int, float))
        #     or (isinstance(self._attr_native_value, str)and self._attr_native_value.isnumeric())
        # )