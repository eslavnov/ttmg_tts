"""Config flow for the Google Cloud integration."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any, cast

from google.cloud import texttospeech
import voluptuous as vol

from homeassistant.components.file_upload import process_uploaded_file
from homeassistant.components.tts import CONF_LANG
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    FileSelector,
    FileSelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_KEY_FILE,
    CONF_URL,
    CONF_STT_MODEL,
    DEFAULT_LANG,
    DEFAULT_STT_MODEL,
    DOMAIN,
    SUPPORTED_STT_MODELS,
    TITLE,
)
from .helpers import (
    async_tts_voices,
    tts_options_schema,
    tts_platform_schema,
    validate_service_account_info,
)

_LOGGER = logging.getLogger(__name__)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL, default="http://127.0.0.1:8888"): str,
    }
)

class GoogleCloudConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Google Cloud integration."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title=TITLE, data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> GoogleCloudOptionsFlowHandler:
        """Create the options flow."""
        return GoogleCloudOptionsFlowHandler()


class GoogleCloudOptionsFlowHandler(OptionsFlow):
    """Google Cloud options flow."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_URL, default=self.config_entry.data.get(CONF_URL, "http://127.0.0.1:8888")): str,
                }
            ),
        )