import voluptuous as vol
from homeassistant import config_entries
from .const import CONF_URL, DOMAIN

class TTMGTTSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for TTMG TTS."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="TTMG TTS", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_URL, default="http://127.0.0.1:8888"): str,
                }
            )
        )