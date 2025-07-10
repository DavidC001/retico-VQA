import requests

from retico_core import AbstractConsumingModule, UpdateType
from retico_core.text import TextIU

class MistyTTSModule(AbstractConsumingModule):
    """A module that converts a text sentence into speech
    and plays it through the Misty robot's speakers."""

    @staticmethod
    def name():
        return "Misty TTS Module"

    @staticmethod
    def description():
        return "A module that converts text to speech and plays it through the Misty robot's speakers."

    @staticmethod
    def input_ius():
        return [TextIU]

    @staticmethod
    def output_iu():
        return None

    def __init__(self, ip, pitch=0, speech_rate=0, voice=None, flush=False, utterance_id=None, language="en-US", **kwargs):
        super().__init__(**kwargs)
        self.ip = ip
        self.pitch = pitch
        self.speech_rate = speech_rate
        self.voice = voice
        self.flush = flush
        self.utterance_id = utterance_id
        self.language = language

        self.latest_input_iu = None

    def process_update(self, update_message):
        if not update_message:
            return None
        final = False
        for iu, ut in update_message:
            if ut == UpdateType.ADD:
                self.current_input.append(iu)
                self.latest_input_iu = iu
            elif ut == UpdateType.REVOKE:
                self.revoke(iu)
            elif ut == UpdateType.COMMIT:
                final = True
        if final:
            self.misty_speak(self.get_current_text())
            self.empty_current_text()

    def get_current_text(self):
        return " ".join(iu.text for iu in self.current_input)

    def empty_current_text(self):
        self.current_input = []

    def misty_speak(self, text):
        """Converts the text in the input IU to speech and plays it with Misty robot's speakers."""

        url = (f"http://{self.ip}/api/tts/speak?text={text}&pitch={self.pitch}&speechRate={self.speech_rate}&"
               f"voice={self.voice}&flush={str(self.flush).lower()}&utteranceId={self.utterance_id}&"
               f"language={self.language})")
        try:
            response = requests.post(url)
            response.raise_for_status()
            return {"status": "success", "message": response.json()}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}

