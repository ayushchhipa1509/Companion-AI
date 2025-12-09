"""
Memory Extraction Module

Extracts structured information from user chat history:
- User preferences
- Emotional patterns
- Facts worth remembering
"""

from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json


class MemoryExtractor:
    """
    Extracts structured memory from user chat messages.
    
    Uses LLM with structured output parsing to identify:
    1. User preferences (likes, dislikes, habits)
    2. Emotional patterns (mood trends, stress triggers)
    3. Facts worth remembering (name, role, constraints, goals)
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize the memory extractor.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.3,  # Lower temperature for more consistent extraction
            api_key=api_key
        )
        self.parser = JsonOutputParser()
        
    def extract_memory(self, chat_messages: List[str]) -> Dict[str, Any]:
        """
        Extract structured memory from chat history.
        
        Args:
            chat_messages: List of user messages (strings)
            
        Returns:
            Dictionary with keys: 'preferences', 'emotional_patterns', 'facts'
        """
        # Combine messages into a single context
        chat_history = "\n".join([f"Message {i+1}: {msg}" for i, msg in enumerate(chat_messages)])
        
        # Design prompt for structured extraction
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at analyzing human communication patterns and extracting meaningful insights.

Your task is to analyze the following chat messages from a single user and extract structured information.

Analyze the messages carefully and identify:

1. **User Preferences**: 
   - What they like/dislike (tools, languages, work styles, activities)
   - Habits and routines they mention
   - Communication preferences
   - Format as a list of specific, concrete preferences

2. **Emotional Patterns**:
   - Recurring emotional states (anxiety, excitement, frustration, calm)
   - Triggers that cause specific emotions
   - Overall emotional tone trends
   - Format as a description of patterns observed

3. **Facts Worth Remembering**:
   - Personal information (name, role, job title if mentioned)
   - Constraints (budget limits, technical limitations, time constraints)
   - Goals and aspirations
   - Important context about their situation
   - Format as a list of key facts

Be specific and evidence-based. Only include information that is clearly present in the messages.
Do not make assumptions beyond what is stated."""),
            ("user", """Analyze these {count} chat messages and extract the structured information:

{chat_history}

Return your analysis as a JSON object with exactly these keys:
- "preferences": array of strings (each preference as a separate item)
- "emotional_patterns": string (description of emotional patterns observed)
- "facts": array of strings (each fact as a separate item)

{format_instructions}""")
        ])
        
        # Create chain with JSON parsing
        chain = prompt | self.llm | self.parser
        
        try:
            result = chain.invoke({
                "count": len(chat_messages),
                "chat_history": chat_history,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            # Ensure all required keys exist
            memory = {
                "preferences": result.get("preferences", []),
                "emotional_patterns": result.get("emotional_patterns", "No clear patterns detected."),
                "facts": result.get("facts", [])
            }
            
            return memory
            
        except Exception as e:
            # Fallback if parsing fails - return neutral defaults
            return {
                "preferences": [],
                "emotional_patterns": "Neutral (Extraction failed, using default)",
                "facts": []
            }
    
    def format_memory_summary(self, memory: Dict[str, Any]) -> str:
        """
        Format memory into a readable summary string for use in prompts.
        
        Args:
            memory: The extracted memory dictionary
            
        Returns:
            Formatted string summary
        """
        summary_parts = []
        
        if memory.get("preferences"):
            summary_parts.append("**User Preferences:**")
            for pref in memory["preferences"]:
                summary_parts.append(f"- {pref}")
        
        if memory.get("emotional_patterns"):
            summary_parts.append(f"\n**Emotional Patterns:** {memory['emotional_patterns']}")
        
        if memory.get("facts"):
            summary_parts.append("\n**Key Facts:**")
            for fact in memory["facts"]:
                summary_parts.append(f"- {fact}")
        
        return "\n".join(summary_parts) if summary_parts else "No memory extracted yet."

