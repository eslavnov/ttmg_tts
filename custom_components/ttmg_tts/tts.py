from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, cast
import voluptuous as vol

from homeassistant.components.tts import (
    CONF_LANG,
    PLATFORM_SCHEMA as TTS_PLATFORM_SCHEMA,
    Provider,
    TextToSpeechEntity,
    TtsAudioType,
    Voice,
)
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DOMAIN,
    CONF_URL,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            TTMGTTSEntity(
                config_entry,
            )
        ]
    )


class BaseTTMGProvider:

    def __init__(
        self,
        options_schema: vol.Schema,
    ) -> None:
        self._options_schema = options_schema

    @callback
    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        return None

    async def _async_get_tts_audio(
        self,
    ) -> TtsAudioType:
        return "mp3", None


class TTMGTTSEntity(BaseTTMGProvider, TextToSpeechEntity):
  
    def __init__(
        self,
        entry: ConfigEntry,
    ) -> None:
        self._attr_unique_id = f"{entry.entry_id}"
        self._attr_name = entry.title
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer="TTMG",
            model="TTS",
            entry_type=dr.DeviceEntryType.SERVICE,
        )
        self._attr_default_language = "en-US"  
        self._attr_supported_languages = ["en-US"]
        self._entry = entry

    @property
    def default_language(self) -> str:
        return "en-US"
      
    @property
    def supported_languages(self) -> list[str]:
        return self._attr_supported_languages
      
    async def async_get_tts_audio(
        self, 
    ) -> TtsAudioType:
        return None, None


class TTMGTTSProvider(BaseTTMGProvider, Provider):
    def __init__(
        self,
        options_schema: vol.Schema,
    ) -> None:
        super().__init__(options_schema)
        self.name = "TTMG TTS"

    async def async_get_tts_audio(
        self,
    ) -> TtsAudioType:
        return None, None
