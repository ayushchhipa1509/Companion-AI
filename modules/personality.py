"""
Personality Engine Module

Transforms agent responses based on:
- Selected personality style (calm mentor, witty friend, therapist-style)
- Extracted user memory (preferences, emotions, facts)
"""

from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class PersonalityEngine:
    """
    Transforms responses to match a selected personality style while
    incorporating user memory for personalization.
    """
    
    # Personality definitions with clear instructions
    PERSONALITIES = {
        "calm_mentor": {
            "name": "Calm Mentor",
            "description": "Patient, step-by-step guidance with reassurance",
            "traits": "patient, methodical, reassuring, encouraging, breaks down complex topics into simple steps"
        },
        "witty_friend": {
            "name": "Witty Friend",
            "description": "Casual, humorous, and relatable",
            "traits": "casual, humorous, uses slang and jokes, relatable, friendly banter, light-hearted"
        },
        "therapist_style": {
            "name": "Therapist-Style",
            "description": "Empathetic, reflective, and supportive",
            "traits": "empathetic, reflective, asks thoughtful questions, validates feelings, supportive, non-judgmental"
        },
        "neutral": {
            "name": "Standard AI",
            "description": "Neutral, professional assistant",
            "traits": "neutral, professional, informative, straightforward"
        }
    }
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize the personality engine.
        
        Args:
            api_key: OpenAI API key
            model: Model to use
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.7,  # Higher temperature for more personality variation
            api_key=api_key
        )
    
    def transform_response(
        self,
        user_question: str,
        standard_response: str,
        personality: str,
        memory: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Transform a standard response into a personality-matched response.
        
        Args:
            user_question: The original user question
            standard_response: The neutral/standard AI response
            personality: Personality key (e.g., "calm_mentor", "witty_friend")
            memory: Optional extracted memory dictionary
            
        Returns:
            Transformed response with personality and memory integration
        """
        if personality not in self.PERSONALITIES:
            personality = "neutral"
        
        personality_info = self.PERSONALITIES[personality]
        
        # Format memory context if available
        memory_context = ""
        if memory:
            memory_parts = []
            if memory.get("preferences"):
                memory_parts.append(f"User preferences: {', '.join(memory['preferences'][:3])}")
            if memory.get("emotional_patterns"):
                memory_parts.append(f"Emotional patterns: {memory['emotional_patterns']}")
            if memory.get("facts"):
                memory_parts.append(f"Key facts: {', '.join(memory['facts'][:3])}")
            
            if memory_parts:
                memory_context = "\n\nUser Context (use this to personalize your response):\n" + "\n".join(memory_parts)
        
        # Design prompt for personality transformation
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are transforming a standard AI response into a {personality_info['name']} style response.

Your personality traits: {personality_info['traits']}

Your task:
1. Keep the core information and accuracy of the original response
2. Transform the tone, style, and delivery to match the {personality_info['name']} personality
3. Use the user's memory context to personalize the response (reference their preferences, acknowledge their emotional state, mention relevant facts)
4. Make it feel natural and authentic to the personality style

DO NOT change the factual content, only the delivery style and personalization."""),
            ("user", """Transform this response:

**Original User Question:**
{user_question}

**Standard Response:**
{standard_response}
{memory_context}

**Your Task:**
Rewrite the response in the {personality_name} style, incorporating the user context naturally. 
Make it feel personalized and authentic to both the personality and the user's situation.""")
        ])
        
        chain = prompt | self.llm
        
        try:
            result = chain.invoke({
                "user_question": user_question,
                "standard_response": standard_response,
                "memory_context": memory_context,
                "personality_name": personality_info["name"]
            })
            
            return result.content
            
        except Exception as e:
            return f"Error transforming response: {str(e)}"
    
    def get_standard_response(
        self,
        user_question: str,
        api_key: str
    ) -> str:
        """
        Generate a standard, neutral AI response (for before/after comparison).
        
        Args:
            user_question: The user's question
            api_key: OpenAI API key
            
        Returns:
            Neutral, standard response
        """
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            api_key=api_key
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful, neutral AI assistant. Provide clear, informative responses without any particular personality style."),
            ("user", "{question}")
        ])
        
        chain = prompt | llm
        
        try:
            result = chain.invoke({"question": user_question})
            return result.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

