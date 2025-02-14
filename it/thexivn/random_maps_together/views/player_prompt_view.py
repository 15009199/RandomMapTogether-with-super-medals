import re
import logging
from pyplanet.views.generics.alert import AlertView

logger = logging.getLogger(__name__)

class PlayerPromptView(AlertView):
    template_name = 'random_maps_together/prompt.xml'

    def __init__(self, message, buttons=None, manager=None, default='', validator=None, entry=True):
        super().__init__(message, "md", buttons, manager)
        self.data["buttons"] = buttons or []
        self.disable_alt_menu = True
        self.entry = entry

        self.default = default
        self.validator = validator or self.validate_input

        self.data['default'] = self.default
        self.data["entry"] = self.entry

    async def wait_for_input(self):  # pragma: no cover
        """
        Wait for input and return it.
        :return: Returns the string value of the user.
        """
        return await self.response_future

    def validate_input(self, value):  # pragma: no cover
        if self.entry and not value:
            raise ValueError("Empty value given!")

    async def handle(self, player, action, values, **kwargs):  # pragma: no cover
        # Try to parse the button id instead of the whole action string.
        button = None
        try:
            match = re.search(r'button_([0-9]+)$', action)
            if match:
                button = match.group(1)
            match = re.search(r'button_(ok)$', action)
            if match:
                button = match.group(1)
        except:
            pass

        if button == "ok":
            try:
                value = values.get("prompt_value", self.default)
                self.validator(value)
                self.response_future.set_result(value)
                await self.close(player)
            except Exception as e:
                self.data['errors'] = str(e)
                await self.display([player.login])

        elif button:
            self.response_future.set_result(self.data["buttons"][int(button)])
            await self.close(player)

    @classmethod
    async def prompt_for_input(cls, player, message, buttons=None, entry=True, validator=None, default=None):
        prompt_view = cls(message, buttons, entry=entry, validator=validator, default=default)
        await prompt_view.display([player])
        player_input = await prompt_view.wait_for_input()
        await prompt_view.destroy()
        if isinstance(player_input, dict):
            return player_input.get("value", player_input["name"])
        else:
            return player_input
