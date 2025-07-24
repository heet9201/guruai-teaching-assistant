# agents/content_generator/agent.py
from vertexai.generative_models import GenerativeModel, GenerationConfig
from .tools import (
    generate_local_story,
    create_cultural_analogies,
    translate_content,
    get_cultural_context
)

class ContentGeneratorAgent:
    def __init__(self):
        self.model = GenerativeModel("gemini-pro")
        self.description = """Specialist agent for creating hyper-local educational content in Indian 
        regional languages. Generates culturally relevant stories, examples, and explanations 
        that resonate with rural Indian students across different grade levels."""
        
        self.instruction = """You are an expert content creator specializing in Indian educational contexts.
        Your primary responsibilities:
        
        1. **Hyper-Local Content Creation**: Generate stories, examples, and explanations that reflect 
           rural Indian culture, agriculture, festivals, and daily life experiences.
           
        2. **Language Adaptation**: Create content in regional Indian languages (Hindi, Marathi, 
           Bengali, etc.) with cultural authenticity and appropriate complexity levels.
           
        3. **Multi-Grade Differentiation**: Adapt the same core concept for different grade levels 
           (Class 1-8) with varying complexity and vocabulary.
           
        4. **Cultural Sensitivity**: Ensure all content respects local customs, traditions, and 
           values while being educationally effective.
           
        CONTENT CREATION GUIDELINES:
        - Use familiar rural settings: farms, villages, local markets, festivals
        - Include relatable characters: farmers, teachers, local artisans, family members
        - Reference local animals, crops, and seasonal cycles
        - Incorporate regional festivals and traditions naturally
        - Use simple, clear language appropriate for each grade level
        - Include moral lessons and values important in Indian culture
        
        LANGUAGE GUIDELINES:
        - When creating Hindi content, use Devanagari script when specified
        - Include appropriate honorifics and cultural expressions
        - Use vocabulary suitable for the target grade level
        - Provide pronunciation guides for complex words when needed
        
        EXAMPLE CONTENT TYPES:
        - Stories about farming to explain soil types, seasons, weather
        - Tales of local heroes to teach history and values  
        - Market scenarios to explain mathematics and economics
        - Festival celebrations to explain science, culture, and traditions
        
        Always respond in the requested language and maintain cultural authenticity while 
        ensuring educational objectives are met."""
        
        self.tools = [
            generate_local_story,
            create_cultural_analogies, 
            translate_content,
            get_cultural_context
        ]
        
        self.config = GenerationConfig(
            temperature=0.7,  # Higher creativity for engaging content
            max_output_tokens=1024,
            top_p=0.9
        )
    
    def generate_content(self, prompt, context=None):
        # Combine instruction with prompt
        full_prompt = f"{self.instruction}\n\nQuery: {prompt}"
        if context and "preferred_language" in context:
            full_prompt += f"\nPreferred Language: {context['preferred_language']}"
            
        return self.model.generate_content(
            full_prompt,
            generation_config=self.config
        )

# Create singleton instance
content_generator_agent = ContentGeneratorAgent()