# hello.py
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
import logging
import random
import importlib
import sys

# Import the Qwen-powered software engineering consultant agent
from agents import SoftwareEngineerAgent, TemplateSoftwareEngineerAgent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables 
load_dotenv()

# --- Create an MCP server ---
mcp = FastMCP("SoftwareEngineeringConsultantServer")

# --- Add simple tools (optional, for context) ---
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource (optional)
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# --- Define the Enhanced Software Engineering Consultant Tool ---
@mcp.tool()
def ask_software_engineer(prompt: str) -> str:
    """
    Consults Claude's Elite Software Engineering Advisor for expert technical guidance.
    This agent acts as Claude's senior technical consultant, specializing in strategic 
    software engineering advice, architecture decisions, performance optimization, 
    security strategies, and technical leadership guidance.
    
    The consultant provides:
    - Strategic technical guidance and architecture recommendations
    - Code quality assessment frameworks and improvement strategies
    - Performance optimization strategies and bottleneck analysis
    - Security consulting and risk assessment approaches
    - Technical debt evaluation and refactoring recommendations
    - Development process optimization and best practices
    - Technology selection guidance and trade-off analysis
    
    Note: This is a consulting service - provides expert advice and strategic guidance,
    not code implementation.
    
    Args:
        prompt: The software engineering challenge, architecture question, or technical 
               strategy topic requiring expert consultation.
    """
    print(f"Software Engineering Consultant processing consultation: '{prompt}'")

    try:
        # Create the enhanced software engineering consultant agent
        agent = SoftwareEngineerAgent(model="qwen-2.5-coder-32b")
        agent.api_key = os.environ.get("GROQ_API_KEY", "")
        
        # Force reload to ensure we're using the latest changes
        try:
            importlib.reload(sys.modules['agents'])
        except KeyError:
            # Module not loaded yet, that's fine
            pass
        
        # Validate API key and print debug info
        template_agent = TemplateSoftwareEngineerAgent()
        key_status = template_agent.debug_api_key(agent.api_key)
        print(f"Groq API key status: {key_status}")
        
        if agent.api_key and len(agent.api_key) > 10:
            print(f"Groq API key: {agent.api_key[:8]}...{agent.api_key[-5:]}")
        else:
            print("Warning: Groq API key is missing or invalid. Using enhanced fallback consulting responses.")
        
        # Generate strategic consulting response
        result = agent.generate_response(prompt)
        
        # Make sure we have a valid consultation response
        if result and isinstance(result, str) and len(result) > 0:
            return result
        else:
            print("API returned empty response, using enhanced consulting template.")
            return template_agent.generate_response(prompt)
        
    except Exception as error:
        print(f"Error during software engineering consultation: {error}")
        # Fall back to enhanced consulting templates on error
        print("Using enhanced fallback consulting responses due to error.")
        template_agent = TemplateSoftwareEngineerAgent()
        return template_agent.generate_response(prompt)

# --- Add additional consulting resource ---
@mcp.resource("consultation://{topic}")
def get_consultation_framework(topic: str) -> str:
    """Get a strategic framework for software engineering consultation topics"""
    frameworks = {
        "architecture": "Strategic Architecture Assessment Framework: Current State → Future Vision → Migration Strategy → Risk Mitigation",
        "performance": "Performance Optimization Framework: Measurement → Bottleneck Analysis → Solution Strategy → Implementation Planning",
        "security": "Security Strategy Framework: Threat Assessment → Risk Analysis → Control Implementation → Monitoring Strategy",
        "quality": "Code Quality Framework: Standards Definition → Assessment Metrics → Improvement Strategy → Process Integration",
        "scaling": "Scalability Framework: Capacity Analysis → Growth Planning → Technology Strategy → Implementation Roadmap"
    }
    return frameworks.get(topic.lower(), f"Comprehensive Software Engineering Consultation Framework for {topic}")

# --- How to run the enhanced server ---
if __name__ == "__main__":
    print("Starting Claude's Enhanced Software Engineering Consultant Server...")
    print("Powered by Qwen-2.5-Coder-32B for expert technical guidance")
    print("\n" + "="*70)
    print("ENHANCED FEATURES:")
    print("✓ Strategic software engineering consultation")
    print("✓ Architecture and design guidance") 
    print("✓ Performance optimization strategies")
    print("✓ Security consulting and risk assessment")
    print("✓ Technical leadership and decision support")
    print("✓ 128K context window for complex consultations")
    print("✓ Enhanced fallback templates for offline consulting")
    print("="*70)
    print("\nTo run this server, use the FastMCP entry point command:")
    print("fastmcp run hello:mcp --reload")
    print("="*70 + "\n")
