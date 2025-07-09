from smolagents import tool
from retico_sceneGraph import SceneGraphMemory, SceneGraphEmbedder
import networkx as nx

@tool
def textualize_scene_graph(scene_graph: nx.Graph) -> str:
    """
    Convert the scene graph to a human-readable text format
    
    Args:
        scene_graph (nx.Graph): The scene graph to convert.
        
    Returns:
        str: A string representation of the scene graph in the form of triplets.
    """
    triplets = SceneGraphEmbedder.generate_triplets(scene_graph)
    
    return "\n".join(triplets)

def get_tools(graph_memory_module: SceneGraphMemory):
    """Get tools for the VQA module"""
    
    @tool
    def get_camera_names()-> list[str]:
        """Get the names of all cameras in the available to query."""
        cameras = graph_memory_module.get_camera_names()
        return cameras

    @tool
    def get_scene_graph(camera_name: str = None)-> nx.Graph:
        """
        Get the current scene graph for a specific camera.
        
        Args:
            camera_name (str): The name of the camera to get the scene graph for.
            
        Returns:
            nx.Graph: The scene graph for the specified camera.
        """
        scene_graph = graph_memory_module.get_scene_graph(camera_name=camera_name)
        return scene_graph

    @tool
    def query_camera(camera_name: str, query: str)-> nx.Graph:
        """
        Query the scene graph for a specific camera using keywords with a RAG on the scene graph triples.
        
        Args:
            camera_name (str): The name of the camera to query.
            query (str): The natural language query to execute.

        Returns:
            nx.Graph: The result of the query as a scene subgraph.
        """
        scene_graph = graph_memory_module.query_camera(camera_name=camera_name, query=query)
        return scene_graph
    
    @tool
    def query_all_cameras(query: str)-> dict[str,nx.Graph]:
        """
        Query all cameras using keywords with a RAG on the scene graph triples.
        
        Args:
            query (str): The natural language query to execute.
            
        Returns:
            dict[str, nx.Graph]: A dictionary mapping camera names to their respective scene subgraphs.
        """
        scene_graphs = graph_memory_module.query_memory(query=query)
        return scene_graphs

    return [get_camera_names, get_scene_graph, query_camera, query_all_cameras]