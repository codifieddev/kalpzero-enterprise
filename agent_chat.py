import json
import networkx as nx
from pathlib import Path

class KalpGraphBrain:
    """
    Acts as the 'Hippocampus' for Kalptree agents, providing 
    contextual memory retrieval from the Dzinly/Kalp knowledge graph.
    """
    def __init__(self, project_path: str):
        self.base_path = Path(project_path)
        self.graph_path = self.base_path / "graphify-out/graph.json"
        self.report_path = self.base_path / "graphify-out/GRAPH_REPORT.md"
        self.graph = self._initialize_graph()

    def _initialize_graph(self):
        if not self.graph_path.exists():
            raise FileNotFoundError("Knowledge graph not found. Run '/graphify .' in chat first.")
        
        with open(self.graph_path, 'r') as f:
            data = json.load(f)
        # Convert the JSON back into a live mathematical graph
        return nx.node_link_graph(data, edges='links')

    def get_summary(self):
        """Returns the high-level 'Rules of the House' for the agent."""
        with open(self.report_path, 'r') as f:
            return f.read()

    def get_node_details(self, node_name: str):
        """Retrieves specific details and neighbors for a node (e.g., 'Service Mongo')."""
        if node_name not in self.graph:
            return f"Error: '{node_name}' is not in the current project memory."
        
        node_data = self.graph.nodes[node_name]
        neighbors = list(self.graph.neighbors(node_name))
        
        return {
            "identity": node_name,
            "type": node_data.get('type', 'Module'),
            "summary": node_data.get('summary', 'No summary available.'),
            "connections": neighbors
        }

    def find_connection_logic(self, start_node: str, end_node: str):
        """Finds the shortest path between two modules (e.g., Client Page -> Service Mongo)."""
        try:
            path = nx.shortest_path(self.graph, source=start_node, target=end_node)
            return f"Logic Flow: {' -> '.join(path)}"
        except nx.NetworkXNoPath:
            return "No direct logic path found between these modules."

# --- HOW THE AGENT USES THIS ---
def talk_to_agent(user_query, brain: KalpGraphBrain):
    """
    This is the loop where your AI agent (like Veda) 
    'thinks' before it answers you.
    """
    # 1. The Agent checks if the query involves specific modules
    # Example: User asks "How does the Client Page talk to the Database?"
    
    if "hotel" in user_query.lower() or "room" in user_query.lower():
        # The agent 'recalls' the connection from memory
        memory_context = brain.find_connection_logic("hotel_hotelroom", "hotel_create_room")
        
        prompt = f"""
        System Context: {memory_context}
        User Question: {user_query}
        Instruction: Use the Logic Flow provided above to explain the architecture.
        """
        # Here you would call your LLM (Gemini/Claude) with this prompt
        print(f"Agent is using memory: {memory_context}")
        return "Thinking process complete..."

# Usage on your server
if __name__ == "__main__":
    kalp_brain = KalpGraphBrain("/mnt/data/kalpzero-enterprise")
    talk_to_agent("How are hotel rooms linked to the creation endpoint?", kalp_brain)