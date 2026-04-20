import os
import json
import networkx as nx
from pathlib import Path
try:
    from openai import OpenAI
except ImportError:
    print("Please install openai: pip install openai")
    exit(1)

# ==========================================
# 1. ADD YOUR OPENAI API KEY HERE
# ==========================================
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "sk-proj-YOUR_API_KEY_HERE")

class KalpGraphBrain:
    """
    Retrieves Graph context.
    """
    def __init__(self, project_path: str):
        self.base_path = Path(project_path)
        self.graph_path = self.base_path / "graphify-out/graph.json"
        self.graph = self._initialize_graph()

    def _initialize_graph(self):
        if not self.graph_path.exists():
            raise FileNotFoundError("Knowledge graph not found. Run 'graphify update .' in terminal first.")
        
        with open(self.graph_path, 'r') as f:
            data = json.load(f)
        return nx.node_link_graph(data, edges='links')

    def get_node_details(self, node_name: str):
        """Gets info for a specific component and its direct neighbors"""
        if node_name not in self.graph:
            return f"[Memory Miss] '{node_name}' not found."
        
        node_data = self.graph.nodes[node_name]
        neighbors = list(self.graph.neighbors(node_name))
        
        return f"""
        Node: {node_name}
        Type: {node_data.get('type', 'Module')}
        Summary: {node_data.get('summary', 'No summary')}
        Directly connected to: {', '.join(neighbors[:10])}
        """

    def find_connection_logic(self, start_node: str, end_node: str):
        """Finds the path between two modules"""
        try:
            path = nx.shortest_path(self.graph, source=start_node, target=end_node)
            return f"Logic Flow: {' -> '.join(path)}"
        except nx.NetworkXNoPath:
            return f"No direct path found between {start_node} and {end_node}."
        except nx.NodeNotFound as e:
            return str(e)


def run_ai_agent(user_query: str, brain: KalpGraphBrain):
    """
    Orchestrates the Graphify Memory fetching and generating answers using OpenAI.
    """
    print(f"\n--- User Query: {user_query} ---")
    print("🧠 Fetching memory from Graphify...")

    # 1. Hardcoded logic for demo purposes (you can dynamically extract node names using an LLM first).
    # Since we know the prompt involves hotel rooms, let's fetch those specific nodes.
    memory_context = ""
    if "hotel" in user_query.lower() or "room" in user_query.lower():
        memory_context += brain.find_connection_logic("hotel_hotelroom", "hotel_create_room") + "\n"
        memory_context += brain.get_node_details("hotel_create_room")

    print(f"✅ Memory Retrieved:\n{memory_context}")

    # 2. Build the LLM Prompt
    system_prompt = f"""
You are an expert software architect AI for the KalpZero codebase. 
Use the provided graph memory context to explain how the code works under the hood.

=== Graph Memory Context ===
{memory_context}
"""

    print("🤖 Sending to OpenAI...\n")
    
    # 3. Call OpenAI
    client = OpenAI()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # or gpt-4, gpt-3.5-turbo
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.3
        )
        
        print("\n=== AI RESPONSE ===")
        print(response.choices[0].message.content)
        print("===================\n")
    except Exception as e:
        print("❌ OpenAI API Error. Did you set your API Key?")
        print(e)


if __name__ == "__main__":
    brain = KalpGraphBrain(".")
    run_ai_agent("How are hotel rooms linked to the creation endpoint?", brain)
