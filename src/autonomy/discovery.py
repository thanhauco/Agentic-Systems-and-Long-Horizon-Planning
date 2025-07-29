from typing import List, Dict, Any
from ..tools.registry import ToolRegistry

class CapabilityExplorer:
    """
    Allows the agent to dynamically discover what it is capable of 
    given its current credentials and tool registry.
    """
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def discover_capabilities(self, agent_credentials: Dict[str, Any]) -> List[str]:
        """
        Scans available tools to infer capabilities.
        Example: if I have a AWS token, I have 'cloud_access'.
        """
        capabilities = []
        print("[Explorer] Scanning environment and credentials...")
        
        # Simulated credential-to-capability mapping
        if agent_credentials.get("AWS_ACCESS_KEY"):
            capabilities.append("cloud_access")
        if agent_credentials.get("DB_CONNECTION_STRING"):
            capabilities.append("database_access")
        if agent_credentials.get("GITHUB_TOKEN"):
            capabilities.append("vcs_access")
            
        print(f"[Explorer] Discovered capabilities: {capabilities}")
        return capabilities

    def get_authorized_tools(self, capabilities: List[str]) -> List[str]:
        return self.registry.list_available(capabilities)
