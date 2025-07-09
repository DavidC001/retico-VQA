import os
os.environ["RelTR_PATH"] = "C:/Users/david/Documents/progetto/retico-sceneGraph/RelTR"

from retico_vision import ScreenModule, WebcamModule
from retico_core.debug import DebugModule
from retico_core import network
from retico_sceneGraph import SceneGraphModule, SceneGraphDrawingModule, SceneGraphMemory
import time

from smolagents import CodeAgent, InferenceClientModel

import dotenv
dotenv.load_dotenv()

from tools import get_tools, textualize_scene_graph

webcam = WebcamModule(meta_data={"camera_name": "office"})
screen = ScreenModule()
scene_graph = SceneGraphModule(topk=10, confidence_threshold=0.2)
scene_graph_drawing = SceneGraphDrawingModule()
scene_graph_memory = SceneGraphMemory()
debug = DebugModule()


webcam.subscribe(scene_graph)
# webcam.subscribe(screen)
# scene_graph.subscribe(debug)
scene_graph.subscribe(scene_graph_drawing)
scene_graph_drawing.subscribe(screen)
scene_graph.subscribe(scene_graph_memory)

# Initialize a model (using Hugging Face Inference API)
model = InferenceClientModel(
    model_id="gpt-4.1-nano",
    provider='openai',
    api_key=os.getenv("OPENAI_API_KEY"),
)  # Uses a default model

# Create an agent with no tools
agent = CodeAgent(tools=get_tools(scene_graph_memory)+[textualize_scene_graph], model=model)

network.run(webcam)

breakpoint()
print("Stopping the network...")

network.stop(webcam)