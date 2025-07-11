from smolagents import tool
from retico_sceneGraph import SceneGraphMemory, SceneGraphEmbedder
import networkx as nx

@tool
def textualize_scene_graph(scene_graph: nx.Graph) -> str:
    """
    Convert a scene graph into a human-readable text format containing relationship triplets.
    
    This function extracts all relationship triplets from the scene graph and formats them
    as natural language phrases. The output is intended for internal processing and analysis
    rather than direct user presentation.
    
    Args:
        scene_graph (nx.Graph): A NetworkX graph representing the scene with nodes as objects
                               and edges as relationships between objects.
        
    Returns:
        str: A newline-separated string containing all triplets in the scene graph formatted
             as readable phrases (e.g., "person wearing hat", "car on street"). This output
             is optimized for internal processing and may not be suitable for direct user display.
    """
    triplets = SceneGraphEmbedder.generate_triplets(scene_graph)
    
    return "\n".join(triplets)

def get_tools(graph_memory_module: SceneGraphMemory):
    """
    Create and return a collection of tools for interacting with the Visual Question Answering (VQA) system.
    
    This function generates a set of tools that provide access to scene graph data from multiple cameras,
    enabling querying and analysis of visual scenes for VQA applications.
    
    Args:
        graph_memory_module (SceneGraphMemory): The scene graph memory module that manages
                                               camera data and provides querying capabilities.
    
    Returns:
        list: A list of tool functions that can be used for:
              - Discovering available cameras
              - Retrieving complete scene graphs
              - Querying specific cameras with natural language
              - Searching across all cameras simultaneously
    """
    
    @tool
    def get_camera_names()-> list[str]:
        """
        Retrieve the names of all available cameras in the system.
        
        This function returns a list of all camera identifiers that are currently
        available for querying scene graphs. Use this to discover which cameras
        you can access before making specific camera queries.
        
        Returns:
            list[str]: A list of camera names/identifiers that can be used with
                      other camera-specific functions like get_scene_graph() or query_camera().
        """
        cameras = graph_memory_module.get_camera_names()
        return cameras

    @tool
    def get_scene_graph(camera_name: str = None)-> nx.Graph:
        """
        Retrieve the complete scene graph for a specific camera.
        
        This function returns the full scene graph containing all detected objects
        and their relationships as captured by the specified camera. The scene graph
        represents the current state of the visual scene with nodes as objects and
        edges as spatial/semantic relationships.
        
        Args:
            camera_name (str, optional): The identifier of the camera to get the scene graph for.
                                       If None, returns the scene graph from the default camera.
            
        Returns:
            nx.Graph: A NetworkX graph representing the complete scene with:
                     - Nodes: Detected objects with their properties
                     - Edges: Relationships between objects (spatial, semantic, etc.)
        """
        scene_graph = graph_memory_module.get_scene_graph(camera_name=camera_name)
        return scene_graph

    @tool
    def query_camera(camera_name: str, query: str, topk:int=1)-> nx.Graph:
        """
        Search and retrieve relevant scene graph content from a specific camera using keyword queries.
        
        This function performs a semantic search on the scene graph triplets using RAG (Retrieval-Augmented Generation)
        to find the most relevant objects and relationships matching your query. It's useful for finding specific
        objects, relationships, or scenes based on natural language descriptions.
        
        Args:
            camera_name (str): The identifier of the camera to search within.
            query (str): Natural language query or keywords to search for (e.g., "person wearing red shirt",
                        "objects on table", "cars in parking lot").
            topk (int, optional): Maximum number of most relevant triplets to return. Defaults to 1.
                                 Higher values return more comprehensive but potentially less focused results.

        Returns:
            nx.Graph: A filtered scene subgraph containing only the most relevant objects and relationships
                     that match the query. The graph structure is the same as the full scene graph but
                     contains only the topk most relevant triplets.
        """
        scene_graph = graph_memory_module.query_camera(camera_name=camera_name, query=query, topk=topk)
        return scene_graph
    
    @tool
    def query_all_cameras(query: str, topk:int=1)-> dict[str,nx.Graph]:
        """
        Search and retrieve relevant scene graph content across all available cameras simultaneously.
        
        This function performs a semantic search across all cameras in the system using RAG (Retrieval-Augmented Generation)
        to find the most relevant objects and relationships matching your query. It's particularly useful for
        finding objects or scenes when you don't know which camera contains them, or when you want to
        compare results across multiple viewpoints.
        
        Args:
            query (str): Natural language query or keywords to search for across all cameras
                        (e.g., "person with blue jacket", "red car", "objects on desk").
            topk (int, optional): Maximum number of most relevant triplets to return per camera.
                                 Defaults to 1. Higher values provide more comprehensive results
                                 but may include less relevant matches.

        Returns:
            dict[str, nx.Graph]: A dictionary mapping camera names to their respective filtered scene subgraphs.
                               Each subgraph contains only the most relevant objects and relationships
                               that match the query for that specific camera. Cameras with no relevant
                               matches may return empty graphs.
        """
        scene_graphs = graph_memory_module.query_memory(query=query, topk=topk)
        return scene_graphs

    return [get_camera_names, get_scene_graph, query_camera, query_all_cameras]