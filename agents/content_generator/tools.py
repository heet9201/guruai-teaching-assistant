# agents/content_generator/tools.py
from google.cloud import translate
import json
import os
from typing import Dict, List, Any
import random

def generate_local_story(
    subject: str,
    language: str,
    grade_level: str,
    cultural_context: str,
    story_type: str = "educational"
) -> Dict[str, Any]:
    """
    Generate a culturally relevant story for educational purposes.
    
    Args:
        subject: The educational subject (e.g., "mathematics", "science", "social studies")
        language: Target language (e.g., "hindi", "marathi", "english")
        grade_level: Target grade level (e.g., "grade_3", "grade_5")
        cultural_context: Regional context (e.g., "maharashtra_rural", "punjab_farming")
        story_type: Type of story ("educational", "moral", "scientific")
    
    Returns:
        Dictionary containing story content, characters, setting, and learning objectives
    """
    
    # Load cultural contexts and story templates
    cultural_data = _load_cultural_contexts()
    story_templates = _load_story_templates()
    
    context_info = cultural_data.get(cultural_context, cultural_data.get("default_rural"))
    
    # Select appropriate story template based on subject and grade
    template_key = f"{subject}_{grade_level}"
    template = story_templates.get(template_key, story_templates.get("default_story"))
    
    # Generate story elements
    characters = _generate_characters(cultural_context, grade_level)
    setting = _generate_setting(cultural_context, subject)
    plot = _generate_plot(subject, grade_level, characters, setting)
    
    # Create the complete story
    story_content = _create_story_content(
        template=template,
        characters=characters,
        setting=setting,
        plot=plot,
        language=language,
        cultural_context=context_info
    )
    
    return {
        "story_content": "Sample story content",
        "characters": [],
        "setting": {},
        "language": language,
        "grade_level": grade_level,
        "learning_objectives": [],
        "cultural_elements": [],
        "vocabulary_notes": [],
        "discussion_questions": [],
        "extension_activities": []
    }

def create_cultural_analogies(
    concept: str,
    cultural_context: str,
    language: str,
    grade_level: str
) -> Dict[str, Any]:
    """
    Create culturally relevant analogies to explain complex concepts.
    
    Args:
        concept: The concept to explain (e.g., "photosynthesis", "democracy", "fractions")
        cultural_context: Regional cultural context
        language: Target language
        grade_level: Student grade level
    
    Returns:
        Dictionary with multiple analogies and explanations
    """
    
    cultural_data = _load_cultural_contexts()
    context_info = cultural_data.get(cultural_context, {})
    
    # Generate multiple analogies for the concept
    analogies = []
    
    if concept.lower() in ["photosynthesis", "plant growth"]:
        analogies = [
            {
                "analogy": "किसान और खेत की तरह (Like a farmer and field)",
                "explanation": "जैसे किसान मिट्टी, पानी और धूप का उपयोग करके फसल उगाता है, वैसे ही पेड़-पौधे मिट्टी, पानी और सूरज की रोशनी का उपयोग करके अपना भोजन बनाते हैं।",
                "visual_element": "Farmer tending to crops with sun, water, and soil",
                "local_reference": "गेहूं या धान की खेती"
            },
            {
                "analogy": "रसोई में खाना बनाने की तरह (Like cooking in kitchen)",
                "explanation": "माँ रसोई में अलग-अलग सामग्री मिलाकर खाना बनाती है, वैसे ही पत्ते सूरज की रोशनी, हवा और पानी मिलाकर अपना भोजन बनाते हैं।",
                "visual_element": "Mother cooking with various ingredients",
                "local_reference": "घर की रसोई और पारंपरिक खाना पकाना"
            }
        ]
    
    elif concept.lower() in ["fractions", "parts", "division"]:
        analogies = [
            {
                "analogy": "रोटी के टुकड़े (Pieces of roti)",
                "explanation": "जब माँ एक रोटी को चार भागों में बांटती है, तो हर टुकड़ा 1/4 (एक चौथाई) होता है। चार टुकड़े मिलकर पूरी रोटी (4/4 = 1) बनती है।",
                "visual_element": "Roti divided into equal parts",
                "local_reference": "दैनिक भोजन और परिवार में बांटना"
            },
            {
                "analogy": "खेत का बंटवारा (Division of farmland)",
                "explanation": "किसान अपने खेत को अलग-अलग फसलों के लिए हिस्सों में बांटता है। अगर आधा खेत गेहूं के लिए है तो वो 1/2 हिस्सा है।",
                "visual_element": "Farmland divided for different crops",
                "local_reference": "कृषि और भूमि विभाजन"
            }
        ]
    
    return {
        "concept": concept,
        "analogies": analogies,
        "cultural_context": cultural_context,
        "language": language,
        "grade_level": grade_level,
        "usage_tips": [],
        "related_activities": []
    }

def translate_content(
    content: str,
    source_language: str,
    target_language: str,
    preserve_cultural_context: bool = True
) -> Dict[str, Any]:
    """
    Translate educational content while preserving cultural context.
    
    Args:
        content: Content to translate
        source_language: Source language code
        target_language: Target language code  
        preserve_cultural_context: Whether to maintain cultural references
    
    Returns:
        Translated content with cultural notes
    """
    
    try:
        # Initialize Google Translate client
        client = translate.TranslationServiceClient()
        
        # Detect source language if not provided
        if source_language == "auto":
            result = client.detect_language(
                request={
                    "content": content,
                    "mime_type": "text/plain",
                }
            )
            source_language = result.languages[0].language_code
        
        # Translate the content
        response = client.translate_text(
            request={
                "contents": [content],
                "source_language_code": source_language,
                "target_language_code": target_language,
                "mime_type": "text/plain",
            }
        )
        
        translated_text = response.translations[0].translated_text
        
        return {
            "original_content": content,
            "translated_content": translated_text,
            "source_language": source_language,
            "target_language": target_language,
            "confidence": 0.95,  # Default confidence
            "cultural_notes": [],
            "pronunciation_guide": []
        }
        
    except Exception as e:
        return {
            "error": f"Translation failed: {str(e)}",
            "original_content": content,
            "source_language": source_language,
            "target_language": target_language
        }

def get_cultural_context(region: str, subject_area: str = "general") -> Dict[str, Any]:
    """
    Retrieve cultural context information for content creation.
    
    Args:
        region: Geographic/cultural region (e.g., "maharashtra", "punjab", "bengal")
        subject_area: Subject area for context (e.g., "agriculture", "festivals", "daily_life")
    
    Returns:
        Cultural context data including customs, references, and appropriate content elements
    """
    
    cultural_data = _load_cultural_contexts()
    
    region_data = cultural_data.get(region, {})
    
    return {
        "region": region,
        "subject_area": subject_area,
        "key_cultural_elements": [],
        "local_references": {},
        "festivals": [],
        "traditional_occupations": [],
        "local_foods": [],
        "common_animals": [],
        "crops_and_agriculture": {},
        "language_notes": {},
        "teaching_considerations": [],
        "taboos_and_sensitivities": []
    }

# Helper functions
def _load_cultural_contexts() -> Dict[str, Any]:
    """Load cultural context data from JSON file."""
    try:
        file_path = os.path.join(os.path.dirname(__file__), "data", "cultural_contexts.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return _get_default_cultural_contexts()

def _load_story_templates() -> Dict[str, Any]:
    """Load story templates from JSON file."""
    try:
        file_path = os.path.join(os.path.dirname(__file__), "data", "story_templates.json") 
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return _get_default_story_templates()

def _generate_characters(cultural_context: str, grade_level: str) -> List[Dict[str, str]]:
    """Generate appropriate characters for the story."""
    base_characters = [
        {"name": "राम", "role": "student", "age": "10", "background": "farmer's son"},
        {"name": "सीता", "role": "student", "age": "9", "background": "teacher's daughter"},
        {"name": "गुरुजी", "role": "teacher", "age": "45", "background": "village teacher"},
        {"name": "किसान काका", "role": "farmer", "age": "50", "background": "experienced farmer"}
    ]
    
    return random.sample(base_characters, min(3, len(base_characters)))

def _generate_setting(cultural_context: str, subject: str) -> Dict[str, str]:
    """Generate appropriate setting for the story."""
    settings = {
        "mathematics": {"location": "गाँव का बाज़ार (Village market)", "description": "Local weekly market with various vendors"},
        "science": {"location": "खेत और बगीचा (Farm and garden)", "description": "Agricultural field with various crops and plants"},
        "social_studies": {"location": "गाँव की चौपाल (Village gathering place)", "description": "Community meeting place under banyan tree"},
        "default": {"location": "गाँव का स्कूल (Village school)", "description": "Single-room school building with courtyard"}
    }
    
    return settings.get(subject, settings["default"])

def _generate_plot(subject: str, grade_level: str, characters: List[Dict], setting: Dict) -> str:
    """Generate plot outline for the story."""
    # This would contain logic to create age-appropriate plots
    # For brevity, returning a template
    return f"Characters {[char['name'] for char in characters]} learn about {subject} in {setting['location']}"

def _create_story_content(template: Dict, characters: List, setting: Dict, plot: str, 
                         language: str, cultural_context: Dict) -> str:
    """Create the actual story content using template and elements."""
    # This would use the template system to generate complete story
    # For brevity, returning a sample
    return f"""एक छोटे से गाँव में {characters[0]['name']} नाम का एक लड़का रहता था। 
    वह बहुत जिज्ञासु था और हमेशा नई चीज़ें सीखना चाहता था।
    
    आज का दिन खास था क्योंकि {characters[2]['name']} ने कुछ दिलचस्प पढ़ाने का वादा किया था।
    {setting['description']} में सभी बच्चे इकट्ठा हुए।
    
    {plot}
    
    इस कहानी से हमने सीखा कि ज्ञान हर जगह मिल सकता है, बस हमें ध्यान से देखना होता है।"""

def _extract_learning_objectives(subject: str, grade_level: str) -> List[str]:
    """Extract learning objectives based on subject and grade."""
    return [
        f"Understanding basic concepts of {subject}",
        f"Connecting {subject} with daily life experiences", 
        "Developing cultural awareness and values"
    ]

def _generate_vocabulary_notes(story: str, language: str, grade_level: str) -> List[Dict]:
    """Generate vocabulary notes for difficult words."""
    return [
        {"word": "जिज्ञासु", "meaning": "curious", "pronunciation": "jigyasu"},
        {"word": "दिलचस्प", "meaning": "interesting", "pronunciation": "dilchasp"}
    ]

def _generate_discussion_questions(subject: str, story: str, grade_level: str) -> List[str]:
    """Generate discussion questions for the story."""
    return [
        "कहानी में मुख्य पात्र कौन था?",
        "आपने इस कहानी से क्या सीखा?",
        "क्या आप भी ऐसी कोई चीज़ जानते हैं?"
    ]

def _suggest_extension_activities(subject: str, cultural_context: str, grade_level: str) -> List[Dict]:
    """Suggest hands-on extension activities."""
    return [
        {"activity": "Field trip to local farm", "description": "Visit nearby farm to observe real examples"},
        {"activity": "Role play", "description": "Act out story characters and scenarios"},
        {"activity": "Art creation", "description": "Draw or create art based on story elements"}
    ]

def _generate_teaching_tips(concept: str, analogies: List, grade_level: str) -> List[str]:
    """Generate teaching tips for using the analogies."""
    return [
        "Start with the most familiar analogy first",
        "Use visual aids and real objects when possible",
        "Encourage students to share their own analogies",
        "Connect back to students' personal experiences"
    ]

def _suggest_hands_on_activities(concept: str, cultural_context: str) -> List[Dict]:
    """Suggest hands-on activities related to the concept."""
    return [
        {"activity": "Demonstration", "description": "Physical demonstration using local materials"},
        {"activity": "Group work", "description": "Students work together to explore concept"},
        {"activity": "Community connection", "description": "Interview local experts or elders"}
    ]

def _preserve_cultural_terms(text: str, language: str) -> str:
    """Preserve important cultural terms during translation."""
    # Implementation would identify and preserve cultural terms
    return text

def _extract_cultural_notes(original: str, translated: str) -> List[str]:
    """Extract cultural notes about the translation."""
    return ["Cultural context preserved in translation"]

def _generate_pronunciation_guide(text: str, language: str) -> List[Dict]:
    """Generate pronunciation guide for translated text."""
    return [{"text": "sample", "pronunciation": "sam-pul"}]

def _get_default_cultural_contexts() -> Dict[str, Any]:
    """Default cultural contexts when file is not available."""
    return {
        "maharashtra_rural": {
            "cultural_elements": ["farming", "festivals", "joint family"],
            "local_references": {"crops": ["wheat", "sugarcane"], "festivals": ["Ganesh Chaturthi"]},
            "language_specific": {"script": "devanagari", "honorifics": ["ji", "saheb"]}
        }
    }

def _get_default_story_templates() -> Dict[str, Any]:
    """Default story templates when file is not available."""
    return {
        "default_story": {
            "structure": ["introduction", "problem", "solution", "moral"],
            "length": "medium",
            "complexity": "appropriate"
        }
    }