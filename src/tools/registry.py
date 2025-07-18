from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional

@dataclass
class ToolMetadata:
    name: str
    description: str
    capability_requirements: List[str] = field(default_factory=list)
    risk_level: int = 1 # 1 (low) to 10 (high)

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.metadata: Dict[str, ToolMetadata] = {}

    def register_tool(self, func: Callable, metadata: ToolMetadata):
        self.tools[metadata.name] = func
        self.metadata[metadata.name] = metadata
        print(f"[ToolRegistry] Registered tool: {metadata.name} (Risk: {metadata.risk_level})")

    def call_tool(self, name: str, agent_capabilities: List[str], **kwargs) -> Any:
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found in registry")
        
        meta = self.metadata[name]
        
        # Check capability constraints
        for req in meta.capability_requirements:
            if req not in agent_capabilities:
                raise PermissionError(f"Agent lacks required capability: '{req}' for tool '{name}'")
        
        # Trigger caution for high-risk tools
        if meta.risk_level > 7:
            print(f"[ToolRegistry] WARNING: Executing high-risk tool '{name}'")

        return self.tools[name](**kwargs)

    def list_available(self, agent_capabilities: List[str]) -> List[str]:
        available = []
        for name, meta in self.metadata.items():
            if all(req in agent_capabilities for req in meta.capability_requirements):
                available.append(name)
        return available
