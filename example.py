import os
# os.environ["RelTR_PATH"] = "./RelTR"

from retico_vision import ScreenModule, WebcamModule
from retico_core.debug import DebugModule
from retico_core import network
from retico_core.audio import SpeakerModule
from retico_sceneGraph import SceneGraphModule, SceneGraphDrawingModule, SceneGraphMemory

from retico_whisperasr.whisperasr import WhisperASRModule
from retico_core.audio import MicrophoneModule
import time

from smolagents import CodeAgent, InferenceClientModel, OpenAIServerModel
from smolAgents2 import SmolAgentsModule
from retico_speechbraintts import SpeechBrainTTSModule

import dotenv
dotenv.load_dotenv()

from tools import get_tools, textualize_scene_graph

webcam = WebcamModule(meta_data={"camera_name": "office"})
screen = ScreenModule()
scene_graph = SceneGraphModule(topk=20, confidence_threshold=0.15)
scene_graph_drawing = SceneGraphDrawingModule()
scene_graph_memory = SceneGraphMemory()

microphone = MicrophoneModule(rate=16000)
asr = WhisperASRModule()
model = InferenceClientModel(
    model_id="gpt-4.1-mini",
    provider="openai",
    api_key=os.getenv("OPENAI_KEY")
)


agent = SmolAgentsModule(
    CodeAgent(
        tools=get_tools(scene_graph_memory)+[textualize_scene_graph],
        model=model
    )
)

tts = SpeechBrainTTSModule()
sp = SpeakerModule(rate=18000)

debug = DebugModule()


webcam.subscribe(scene_graph)
scene_graph.subscribe(scene_graph_drawing)
scene_graph_drawing.subscribe(screen)
scene_graph.subscribe(scene_graph_memory)

microphone.subscribe(asr)
asr.subscribe(agent)

agent.subscribe(tts)
tts.subscribe(sp)

network.run(webcam)
network.run(microphone)

breakpoint()
print("Stopping the network...")

network.stop(webcam)
network.stop(microphone)