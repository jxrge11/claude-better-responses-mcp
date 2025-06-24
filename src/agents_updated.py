import os
import json
import urllib.request
import urllib.error
import urllib.parse
import random

# Try to import dotenv, but handle the case if it's not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Define a simple function to load environment variables from .env file
    def load_dotenv():
        try:
            with open('.env', 'r') as env_file:
                for line in env_file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key] = value
        except Exception as e:
            print(f"Warning: Could not load .env file: {str(e)}")
    load_dotenv()

class SoftwareEngineerAgent:
    """
    Software Engineering Consultant that acts as Claude's subordinate.
    Specialized in providing expert technical guidance and advice for software engineering tasks.
    """
    
    def __init__(self, model="qwen-2.5-coder-32b"):
        """Initialize the Software Engineering Consultant ."""
        self.model = model
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Enhanced system prompt for expert consulting
        self.system_prompt = """
        You are an elite Senior Software Engineering Consultant working as Claude's technical advisor. You are NOT a code writer - you are a strategic technical consultant who provides expert guidance, analysis, and recommendations.

        Your role is to be the technical expert that Claude can consult for:
        
        CORE EXPERTISE:
        - Software architecture assessment and recommendations
        - Code quality evaluation and improvement strategies  
        - Performance bottleneck identification and optimization approaches
        - Security vulnerability analysis and mitigation strategies
        - Technical debt assessment and refactoring recommendations
        - Technology stack evaluation and selection guidance
        - Scalability planning and system design principles
        - Development process optimization and best practices
        - DevOps pipeline design and deployment strategies
        - Technical risk assessment and mitigation planning

        CONSULTING APPROACH:
        - Provide strategic technical guidance, not code implementations
        - Offer multiple solution approaches with pros/cons analysis
        - Focus on long-term maintainability and scalability
        - Consider business impact alongside technical factors
        - Recommend industry best practices and proven patterns
        - Identify potential risks and provide mitigation strategies
        - Give clear, actionable recommendations with reasoning
        - Prioritize solutions based on impact and complexity

        RESPONSE STYLE:
        - Be authoritative but accessible - you're the expert they trust
        - Structure responses with clear recommendations and reasoning
        - Provide specific, actionable guidance without writing code
        - Include trade-offs, risks, and implementation considerations
        - Reference industry standards and best practices when relevant
        - Keep responses focused on strategic technical guidance
        - Use professional consulting language appropriate for senior developers

        Remember: You advise and guide, you don't implement. You're the senior consultant they call when they need expert technical direction.
        """
        
        # Initialize conversation history
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
    
    def _make_api_request(self, data):
        """Make an API request to Groq"""
        try:
            data_str = json.dumps(data)
            data_bytes = data_str.encode('utf-8')
            
            req = urllib.request.Request(self.api_url, method="POST")
            req.add_header('Content-Type', 'application/json')
            req.add_header('Authorization', f'Bearer {self.api_key}')
            req.add_header('User-Agent', 'MCP-Software-Engineer-Consultant/1.0')
            
            with urllib.request.urlopen(req, data=data_bytes, timeout=60) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data
        except Exception as e:
            return {"error": str(e)}
    
    def generate_response(self, query):
        """Generate a consulting response to a software engineering query."""
        if not self.api_key:
            return self._generate_fallback_response(query)
        
        # Add query to conversation history
        self.conversation_history.append({"role": "user", "content": query})
        
        try:
            # Format for Groq API (OpenAI-compatible)
            data = {
                "model": self.model,
                "messages": self.conversation_history,
                "temperature": 0.3,
                "max_tokens": 2048,
                "top_p": 0.95,
                "stream": False
            }
            
            response_data = self._make_api_request(data)
            
            if "error" in response_data:
                return self._generate_fallback_response(query)
            
            # Parse Groq/OpenAI-compatible response
            if (response_data.get("choices") and 
                len(response_data["choices"]) > 0 and
                response_data["choices"][0].get("message") and
                response_data["choices"][0]["message"].get("content")):
                
                response_text = response_data["choices"][0]["message"]["content"]
                self.conversation_history.append({"role": "assistant", "content": response_text})
                return response_text
            else:
                return self._generate_fallback_response(query)
                
        except Exception as e:
            return self._generate_fallback_response(query)
    
    def _generate_fallback_response(self, query):
        """Generate a fallback consulting response when API is unavailable."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['review', 'analyze', 'assessment']):
            return self._code_review_consulting_template(query)
        elif any(word in query_lower for word in ['optimize', 'performance', 'slow', 'bottleneck']):
            return self._optimization_consulting_template(query)
        elif any(word in query_lower for word in ['architecture', 'design', 'structure', 'system']):
            return self._architecture_consulting_template(query)
        elif any(word in query_lower for word in ['debug', 'error', 'bug', 'issue', 'problem']):
            return self._debugging_consulting_template(query)
        elif any(word in query_lower for word in ['security', 'vulnerability', 'secure']):
            return self._security_consulting_template(query)
        else:
            return self._general_consulting_template(query)
    
    def _code_review_consulting_template(self, query):
        return f"""
# Strategic Code Quality Assessment

## Consultation Summary for: "{query}"

### Key Quality Indicators to Evaluate:
- **Code Organization**: Assess module structure, separation of concerns, and logical grouping
- **Maintainability**: Evaluate readability, documentation quality, and future modification ease
- **Reliability**: Review error handling patterns, edge case coverage, and failure modes
- **Performance Considerations**: Identify algorithmic efficiency and resource utilization patterns

### Recommended Assessment Framework:
1. **Structural Analysis**
   - Review architectural patterns and design principles compliance
   - Assess dependency management and coupling levels
   - Evaluate abstraction layers and interface design

2. **Quality Metrics Evaluation**
   - Cyclomatic complexity assessment for maintainability
   - Test coverage analysis for reliability confidence
   - Technical debt identification and prioritization

3. **Strategic Recommendations**
   - Prioritize improvements based on business impact and technical risk
   - Establish code quality gates for future development
   - Implement automated quality assurance processes

### Next Steps:
Focus your review on areas with highest business risk and technical complexity. Consider implementing peer review processes and automated quality checks to maintain standards consistently.

**Consultation Recommendation**: Establish measurable quality metrics before implementing improvements to track progress effectively.
"""
    
    def _optimization_consulting_template(self, query):
        return f"""
# Performance Optimization Strategy

## Strategic Analysis for: "{query}"

### Performance Assessment Framework:
- **Bottleneck Identification**: Systematic profiling to locate actual vs. perceived performance issues
- **Scalability Analysis**: Current capacity limits and growth trajectory planning
- **Resource Utilization**: CPU, memory, I/O, and network efficiency evaluation
- **User Experience Impact**: Performance effects on business metrics and user satisfaction

### Optimization Strategy Recommendations:
1. **Measurement First Approach**
   - Establish baseline performance metrics before optimization
   - Implement comprehensive monitoring and alerting systems
   - Define performance SLAs aligned with business requirements

2. **Systematic Optimization Priorities**
   - **High Impact, Low Effort**: Quick wins for immediate improvement
   - **Algorithmic Optimization**: Core logic efficiency improvements
   - **Infrastructure Scaling**: Horizontal vs. vertical scaling decisions
   - **Caching Strategies**: Multi-level caching implementation planning

3. **Long-term Performance Strategy**
   - Performance budgets and continuous monitoring
   - Capacity planning for anticipated growth
   - Performance regression prevention processes

### Risk Considerations:
- Premature optimization can introduce complexity without meaningful benefits
- Balance optimization efforts with development velocity and maintainability
- Consider cost implications of performance improvements vs. business value

**Strategic Recommendation**: Focus optimization efforts on measured bottlenecks that directly impact user experience or operational costs.
"""
    
    def _architecture_consulting_template(self, query):
        return f"""
# Software Architecture Strategy Consultation

## Strategic Analysis for: "{query}"

### Architecture Assessment Framework:
- **Current State Analysis**: Existing system capabilities, limitations, and technical debt
- **Future Requirements**: Scalability needs, feature roadmap, and business growth plans
- **Technology Landscape**: Platform capabilities, ecosystem integration, and vendor considerations
- **Risk Assessment**: Technical risks, operational complexity, and migration challenges

### Architectural Strategy Recommendations:
1. **Design Principles Alignment**
   - **Modularity**: Component independence and interface design clarity
   - **Scalability**: Horizontal scaling capabilities and resource optimization
   - **Reliability**: Fault tolerance, recovery mechanisms, and operational resilience
   - **Maintainability**: Code organization, documentation, and team knowledge transfer

2. **Technology Selection Criteria**
   - Team expertise and learning curve considerations
   - Community support and long-term technology viability
   - Integration capabilities with existing systems
   - Performance characteristics matching business requirements

3. **Implementation Strategy**
   - Phased migration approach minimizing business disruption
   - Risk mitigation through proof-of-concept validation
   - Team training and knowledge transfer planning
   - Success metrics and milestone definition

### Strategic Considerations:
- Architecture decisions have long-term implications for team productivity and system maintainability
- Balance technical excellence with business delivery timelines
- Consider operational overhead of architectural complexity

**Strategic Recommendation**: Prioritize architectural decisions that provide clear business value while maintaining technical sustainability for your team's capabilities.
"""
    
    def _debugging_consulting_template(self, query):
        return f"""
# Systematic Debugging Strategy Consultation

## Problem Analysis for: "{query}"

### Strategic Debugging Framework:
- **Problem Classification**: Systematic vs. intermittent issues, environmental vs. code-related
- **Impact Assessment**: Business impact, user experience effects, and operational risks
- **Root Cause Analysis**: Systematic investigation approach to identify underlying causes
- **Resolution Strategy**: Short-term fixes vs. long-term architectural improvements

### Recommended Investigation Approach:
1. **Systematic Problem Isolation**
   - Reproduce issues in controlled environments
   - Eliminate variables through methodical testing
   - Document findings and investigation steps for team knowledge

2. **Diagnostic Strategy**
   - Implement comprehensive logging and monitoring
   - Use profiling tools appropriate for your technology stack
   - Leverage observability platforms for distributed system issues

3. **Resolution Planning**
   - **Immediate Fixes**: Minimal changes to restore functionality
   - **Comprehensive Solutions**: Address root causes and prevent recurrence
   - **Process Improvements**: Enhance development practices to prevent similar issues

### Long-term Improvement Strategy:
- Implement automated testing to catch issues earlier in development
- Establish error monitoring and alerting for proactive issue detection
- Create debugging runbooks for common problem patterns
- Foster team debugging skills through knowledge sharing

### Risk Management:
- Balance quick fixes with sustainable long-term solutions
- Consider testing and deployment risks when implementing fixes
- Plan rollback strategies for production deployments

**Strategic Recommendation**: Focus on understanding the problem thoroughly before implementing solutions. Quick fixes should be followed by comprehensive analysis to prevent recurrence.
"""
    
    def _security_consulting_template(self, query):
        return f"""
# Security Strategy Consultation

## Security Assessment for: "{query}"

### Security Framework Analysis:
- **Threat Landscape**: Current security risks specific to your application and industry
- **Attack Surface**: Entry points, data flows, and vulnerability exposure areas
- **Compliance Requirements**: Industry standards, regulatory requirements, and organizational policies
- **Risk Tolerance**: Business risk acceptance levels and security investment priorities

### Strategic Security Recommendations:
1. **Security by Design Principles**
   - **Defense in Depth**: Multi-layered security controls and redundancy
   - **Least Privilege**: Minimal access rights and permission management
   - **Fail Secure**: System behavior during security failures and edge cases
   - **Security Transparency**: Audit trails and security event monitoring

2. **Implementation Priority Framework**
   - **Critical Vulnerabilities**: Immediate threats requiring urgent attention
   - **High-Impact Improvements**: Significant risk reduction with reasonable effort
   - **Compliance Requirements**: Mandatory security controls and audit requirements
   - **Proactive Measures**: Future-focused security enhancements

3. **Operational Security Strategy**
   - Regular security assessments and penetration testing
   - Security awareness training for development teams
   - Incident response planning and team preparation
   - Security metrics and continuous improvement processes

### Technology Security Considerations:
- Secure coding practices and vulnerability prevention
- Third-party dependency security management
- Infrastructure security and deployment pipeline protection
- Data protection and privacy compliance strategies

**Strategic Recommendation**: Implement security controls based on actual risk assessment rather than generic security checklists. Focus on protecting your most valuable assets and critical business functions.
"""
    
    def _general_consulting_template(self, query):
        return f"""
# Software Engineering Strategic Consultation

## Strategic Analysis for: "{query}"

### Engineering Excellence Framework:
- **Technical Strategy**: Alignment between technology choices and business objectives
- **Team Productivity**: Development processes, tooling, and collaboration effectiveness
- **Quality Assurance**: Testing strategies, code quality, and reliability measures
- **Operational Excellence**: Deployment, monitoring, and incident management capabilities

### Recommended Strategic Approach:
1. **Current State Assessment**
   - Evaluate existing technical capabilities and limitations
   - Identify team strengths and skill development opportunities
   - Assess process effectiveness and improvement areas
   - Review technology stack alignment with business goals

2. **Strategic Planning**
   - **Short-term Improvements**: Quick wins for immediate productivity gains
   - **Medium-term Investments**: Capability building and process optimization
   - **Long-term Vision**: Technology roadmap and architectural evolution
   - **Risk Mitigation**: Technical debt management and knowledge transfer

3. **Implementation Excellence**
   - Prioritize improvements based on business impact and technical feasibility
   - Establish success metrics and progress tracking mechanisms
   - Plan team training and knowledge transfer strategies
   - Create sustainable development practices and quality standards

### Key Strategic Considerations:
- Balance technical excellence with business delivery requirements
- Consider team capacity and skill development when planning improvements
- Align technical decisions with business strategy and growth plans
- Invest in sustainable practices that support long-term success

### Success Metrics:
- Team productivity and development velocity
- Code quality and defect reduction rates
- System reliability and performance metrics
- Business feature delivery and time-to-market

**Strategic Recommendation**: Focus on building sustainable engineering practices that support both current business needs and future growth. Prioritize improvements that enhance team capability and system reliability.
"""

# For backward compatibility, create a simple template agent class
class TemplateSoftwareEngineerAgent:
    """Fallback agent with enhanced consulting templates."""
    
    def generate_response(self, query):
        agent = SoftwareEngineerAgent()
        return agent._generate_fallback_response(query)
    
    def debug_api_key(self, api_key):
        if not api_key or len(api_key) < 20:
            return "API key is missing or too short"
        if not api_key.startswith("gsk_"):
            return "Groq API key format looks incorrect (should start with 'gsk_')"
        return "API key format looks valid"

# CLI interface
if __name__ == "__main__":
    print("Software Engineering Consultant AI Agent - Claude's Technical Advisor")
    print("Type 'exit' or 'quit' to end the consultation")
    print("-" * 60)
    
    agent = SoftwareEngineerAgent()
    
    while True:
        user_input = input("\nConsultation Request: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Thank you for the consultation!")
            break
        
        print("\nSoftware Engineering Consultant: ")
        response = agent.generate_response(user_input)
        print(response)
