"""Support for the TTMG TTS service."""

from __future__ import annotations

import requests
import logging
from typing import Any
import json
import voluptuous as vol

from homeassistant.components.tts import (
    Provider,
    TextToSpeechEntity,
    TtsAudioType,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    CONF_URL,
)

_LOGGER = logging.getLogger(__name__)


async def async_get_engine(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> TTMGProvider:
    """Set up TTMG TTS component."""
    return TTMGProvider(hass)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TTMG TTS platform via config entry."""
    async_add_entities([TTMGTTSEntity(config_entry)])


class TTMGTTSEntity(TextToSpeechEntity):
    """The TTMG TTS API entity."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Init TTMG TTS service."""
        self._attr_name = "TTMG TTS"
        self._attr_unique_id = config_entry.entry_id
        self._attr_default_language = "en-US"  
        self._attr_supported_languages = ["en-US"]

    def get_tts_audio(
        self, message: str,
    ) -> TtsAudioType:
        """Load TTMG TTS"""
        if message != "Processing your request, please wait...":
          x = requests.post(CONF_URL+"/preload-text/ttmg_tts/", json={"text": json.dumps(message) }) 
        return "mp3", None


class TTMGProvider(Provider):
    """The TTMG TTS API provider."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Init TTMG TTS service."""
        self.hass = hass
        self.name = "TTMG TTS"

    def get_tts_audio(
        self, message: str,
    ) -> TtsAudioType:
        """Load TTMG TTS"""
        if message != "Processing your request, please wait...":
          x = requests.post(CONF_URL+"/preload-text/ttmg_tts/", json={"text": json.dumps(message) }) 
        return "mp3", None
