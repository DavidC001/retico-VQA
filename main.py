import os
os.environ["RelTR_PATH"] = "./RelTR"

from retico_vision import ScreenModule, WebcamModule, IPCameraModule
from retico_core.debug import DebugModule
from retico_core import network
from retico_core.audio import SpeakerModule
from retico_sceneGraph import SceneGraphModule, SceneGraphDrawingModule, SceneGraphMemory

from retico_whisperasr.whisperasr import WhisperASRModule
from retico_googleasr import GoogleASRModule
from retico_googletts import GoogleTTSModule
from retico_core.audio import MicrophoneModule
from retico_core import audio
import time

from smolagents import CodeAgent, InferenceClientModel, OpenAIServerModel
from smolAgents2 import SmolAgentsModule
# from retico_speechbraintts import SpeechBrainTTSModule
from retico_misty_tts.misty_tts_module import MistyTTSModule
from retico_misty_camera_stream.misty_camera_stream_module import MistyCameraStreamModule

import dotenv
dotenv.load_dotenv()

from tools import get_tools, textualize_scene_graph

webcam = WebcamModule(meta_data={"camera_name": "office"})
webcam2 = IPCameraModule("http://173.165.152.129:8011/axis.-cgi/mjpg/video.cgi", meta_data={"camera_name": "garden"}, width=640, height=480)
# webcam3 = MistyCameraStreamModule(os.getenv("MISTY_IP"), meta_data={"camera_name": "YOU (misty)"}, res_width=640, res_height=480)
# webcam2 = IPCameraModule("http://10.10.1.91:8090/video", meta_data={"camera_name": "kitchen"}, width=640, height=480, username="admin", password="secret")
screen = ScreenModule()
screen2 = ScreenModule()
screen3 = ScreenModule()

scene_graph = SceneGraphModule(topk=25, confidence_threshold=0.15, timeout=1)
scene_graph_drawing = SceneGraphDrawingModule(camera_name="office")
scene_graph_drawing2 = SceneGraphDrawingModule(camera_name="garden")
scene_graph_drawing3 = SceneGraphDrawingModule(camera_name="YOU (misty)")
scene_graph_memory = SceneGraphMemory(model_name="Qwen/Qwen3-Embedding-0.6B")

microphone = MicrophoneModule(rate=16000)
filter = RobotASRFilterModule()
asr = WhisperASRModule(silence_dur=0.2)
model = InferenceClientModel(
    model_id="gpt-4o",
    provider="openai",
    api_key=os.getenv("OPENAI_API_KEY")
)
agent = SmolAgentsModule(
    CodeAgent(
        tools=get_tools(scene_graph_memory)+[textualize_scene_graph],
        model=model
    )
)

tts = MistyTTSModule(os.getenv("MISTY_IP"))
# tts = GoogleTTSModule(
#     language_code="en-US",
#     voice_name="en-US-Standard-C",
#     speaking_rate=1.0,
#     frame_duration=0.2,
# )
# sp = audio.SpeakerModule()


debug = DebugModule()


webcam.subscribe(scene_graph)
webcam2.subscribe(scene_graph)
# webcam3.subscribe(scene_graph)
scene_graph.subscribe(scene_graph_drawing3)
scene_graph.subscribe(scene_graph_drawing2)
scene_graph.subscribe(scene_graph_drawing)
scene_graph_drawing.subscribe(screen)
scene_graph_drawing2.subscribe(screen2)
scene_graph_drawing3.subscribe(screen3)
scene_graph.subscribe(scene_graph_memory)

microphone.subscribe(asr)
asr.subscribe(agent)

agent.subscribe(tts)
# tts.subscribe(sp)

network.run(scene_graph_memory)
network.run(microphone)

input("Press Enter to stop the network...")
print("Stopping the network...")

network.stop(scene_graph_memory)
network.stop(microphone)