# agents/worksheet_processor/tools.py
from google.cloud import vision
from PIL import Image
import base64
import io
import json
import re
from typing import Dict, List, Any, Optional, Tuple
import os

def process_textbook_image(
    image_base64: str,
    grade_levels: List[str],
    subject_hint: str = "auto",
    language_preference: str = "hindi_english"
) -> Dict[str, Any]:
    """
    Process a textbook image and generate differentiated worksheets for multiple grade levels.
    
    Args:
        image_base64: Base64 encoded image of textbook page
        grade_levels: List of target grade levels (e.g., ["grade_3", "grade_4", "grade_5"])
        subject_hint: Subject area hint ("mathematics", "science", "social_studies", "language", "auto")
        language_preference: Preferred language for output ("hindi", "english", "hindi_english")
    
    Returns:
        Dictionary containing processed content and differentiated worksheets
    """
    
    try:
        # Step 1: Extract and analyze content from image
        extracted_content = extract_text_from_image(image_base64)
        
        if not extracted_content or extracted_content.get('error'):
            return {"error": "Failed to extract text from image", "details": extracted_content}
        
        # Step 2: Analyze content complexity and subject
        content_analysis = analyze_content_complexity(
            extracted_content['text'],
            subject_hint
        )
        
        # Step 3: Generate differentiated worksheets
        worksheets = generate_differentiated_worksheets(
            content=extracted_content['text'],
            content_analysis=content_analysis,
            grade_levels=grade_levels,
            language_preference=language_preference
        )
        
        # Step 4: Generate visual elements that can be recreated
        visual_elements = _extract_visual_elements(image_base64, content_analysis['subject'])
        
        return {
            "status": "success",
            "original_content": {
                "extracted_text": extracted_content['text'],
                "detected_language": extracted_content.get('language', 'mixed'),
                "confidence": extracted_content.get('confidence', 0.0)
            },
            "content_analysis": content_analysis,
            "worksheets": worksheets,
            "visual_elements": visual_elements,
            "teacher_notes": _generate_teacher_notes(content_analysis, worksheets),
            "implementation_guide": _create_implementation_guide(worksheets, grade_levels),
            "assessment_rubrics": _create_assessment_rubrics(content_analysis, grade_levels)
        }
        
    except Exception as e:
        return {
            "error": f"Image processing failed: {str(e)}",
            "status": "failed"
        }

def extract_text_from_image(image_base64: str) -> Dict[str, Any]:
    """
    Extract text from image using Google Cloud Vision API.
    
    Args:
        image_base64: Base64 encoded image data
    
    Returns:
        Dictionary containing extracted text and metadata
    """
    
    try:
        # Initialize Vision API client
        client = vision.ImageAnnotatorClient()
        
        # Decode base64 image
        image_data = base64.b64decode(image_base64)
        image = vision.Image(content=image_data)
        
        # Perform text detection
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if response.error.message:
            raise Exception(f'Vision API error: {response.error.message}')
        
        if not texts:
            return {"error": "No text detected in image"}
        
        # Extract full text (first annotation contains all detected text)
        full_text = texts[0].description if texts else ""
        
        # Detect language
        detected_language = _detect_language(full_text)
        
        # Clean and process text
        processed_text = _clean_extracted_text(full_text)
        
        # Extract structured information
        structured_content = _extract_structured_content(processed_text)
        
        return {
            "text": processed_text,
            "raw_text": full_text,
            "language": detected_language,
            "confidence": _calculate_extraction_confidence(texts),
            "structured_content": structured_content,
            "text_regions": [
                {
                    "text": annotation.description,
                    "bounds": _format_bounds(annotation.bounding_poly)
                }
                for annotation in texts[1:]  # Skip first element (full text)
            ]
        }
        
    except Exception as e:
        return {"error": f"Text extraction failed: {str(e)}"}

def analyze_content_complexity(
    text_content: str,
    subject_hint: str = "auto"
) -> Dict[str, Any]:
    """
    Analyze the complexity and educational characteristics of extracted content.
    
    Args:
        text_content: Extracted text content
        subject_hint: Subject area hint
    
    Returns:
        Analysis results including complexity, subject, and educational level
    """
    
    # Determine subject if not specified
    if subject_hint == "auto":
        detected_subject = _detect_subject_area(text_content)
    else:
        detected_subject = subject_hint
    
    # Analyze text complexity
    complexity_metrics = _calculate_text_complexity(text_content)
    
    # Identify key concepts
    key_concepts = _extract_key_concepts(text_content, detected_subject)
    
    # Determine appropriate grade levels
    suggested_grades = _determine_grade_levels(complexity_metrics, detected_subject)
    
    # Identify question types present
    existing_question_types = _identify_question_types(text_content)
    
    # Extract learning objectives
    learning_objectives = _extract_learning_objectives(text_content, detected_subject)
    
    return {
        "subject": detected_subject,
        "complexity_level": complexity_metrics['overall_level'],
        "complexity_metrics": complexity_metrics,
        "key_concepts": key_concepts,
        "suggested_grade_levels": suggested_grades,
        "learning_objectives": learning_objectives,
        "existing_question_types": existing_question_types,
        "language_complexity": _analyze_language_complexity(text_content),
        "prerequisites": _identify_prerequisites(key_concepts, detected_subject),
        "extension_opportunities": _identify_extension_opportunities(key_concepts, detected_subject)
    }

def generate_differentiated_worksheets(
    content: str,
    content_analysis: Dict[str, Any],
    grade_levels: List[str],
    language_preference: str = "hindi_english"
) -> Dict[str, Any]:
    """
    Generate differentiated worksheets for multiple grade levels.
    
    Args:
        content: Original text content
        content_analysis: Analysis results from analyze_content_complexity
        grade_levels: Target grade levels
        language_preference: Language preference for worksheets
    
    Returns:
        Dictionary containing worksheets for each grade level
    """
    
    worksheets = {}
    subject = content_analysis['subject']
    key_concepts = content_analysis['key_concepts']
    
    for grade_level in grade_levels:
        grade_num = int(grade_level.replace('grade_', ''))
        
        worksheet = {
            "grade_level": grade_level,
            "title": _generate_worksheet_title(subject, key_concepts[0] if key_concepts else "General", grade_num),
            "learning_objectives": _adapt_learning_objectives(
                content_analysis['learning_objectives'], 
                grade_num
            ),
            "sections": []
        }
        
        # Generate different sections based on grade level
        if grade_num <= 2:  # Early primary
            worksheet["sections"] = _create_early_primary_sections(content, key_concepts, subject)
        elif grade_num <= 5:  # Primary
            worksheet["sections"] = _create_primary_sections(content, key_concepts, subject)
        else:  # Upper primary
            worksheet["sections"] = _create_upper_primary_sections(content, key_concepts, subject)
        
        # Add language-specific content
        if language_preference == "hindi" or language_preference == "hindi_english":
            worksheet["hindi_version"] = _translate_worksheet_to_hindi(worksheet)
        
        # Add assessment criteria
        worksheet["assessment"] = _create_grade_appropriate_assessment(grade_num, subject)
        
        # Add material requirements
        worksheet["materials_needed"] = _list_required_materials(worksheet["sections"], grade_num)
        
        # Add time estimates
        worksheet["estimated_time"] = _estimate_completion_time(worksheet["sections"], grade_num)
        
        worksheets[grade_level] = worksheet
    
    return worksheets

# Helper Functions

def _extract_visual_elements(image_base64: str, subject: str) -> Dict[str, Any]:
    """Extract and describe visual elements that can be recreated on blackboard."""
    # This would use image analysis to identify diagrams, charts, etc.
    return {
        "diagrams": [],
        "charts": [],
        "illustrations": [],
        "recreatable_visuals": [
            {
                "type": "simple_diagram",
                "description": "Basic diagram that can be drawn on blackboard",
                "materials": ["chalk", "ruler"],
                "instructions": "Step-by-step drawing instructions"
            }
        ]
    }

def _detect_language(text: str) -> str:
    """Detect the primary language of the text."""
    # Simple detection based on script
    hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    if hindi_chars > english_chars:
        return "hindi"
    elif english_chars > 0:
        return "english" 
    else:
        return "mixed"

def _clean_extracted_text(text: str) -> str:
    """Clean and normalize extracted text."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters that interfere with processing
    text = re.sub(r'[^\w\s\u0900-\u097F.,;:!?()-]', '', text)
    return text.strip()

def _extract_structured_content(text: str) -> Dict[str, List[str]]:
    """Extract structured elements like questions, answers, definitions."""
    structure = {
        "questions": [],
        "definitions": [],
        "examples": [],
        "key_points": []
    }
    
    # Simple pattern matching for questions
    questions = re.findall(r'[.?।]\s*([^.?।]*[?।][^.?।]*)', text)
    structure["questions"] = [q.strip() for q in questions if len(q.strip()) > 10]
    
    return structure

def _format_bounds(bounding_poly):
    """Format bounding polygon coordinates."""
    vertices = []
    for vertex in bounding_poly.vertices:
        vertices.append({"x": vertex.x, "y": vertex.y})
    return vertices

def _calculate_extraction_confidence(texts) -> float:
    """Calculate confidence score for text extraction."""
    if not texts or len(texts) < 2:
        return 0.0
    
    # Calculate based on number of detected text regions and their sizes
    total_chars = sum(len(annotation.description) for annotation in texts[1:])
    avg_confidence = min(1.0, total_chars / 100)  # Simple heuristic
    
    return round(avg_confidence, 2)

def _detect_subject_area(text: str) -> str:
    """Detect subject area based on content keywords."""
    text_lower = text.lower()
    
    math_keywords = ['addition', 'subtraction', 'multiply', 'divide', 'equation', 'number', '=', '+', '-', '×', '÷']
    science_keywords = ['experiment', 'observation', 'hypothesis', 'plant', 'animal', 'water', 'air', 'energy']
    social_keywords = ['history', 'geography', 'community', 'government', 'culture', 'society', 'map']
    
    math_score = sum(1 for keyword in math_keywords if keyword in text_lower)
    science_score = sum(1 for keyword in science_keywords if keyword in text_lower)
    social_score = sum(1 for keyword in social_keywords if keyword in text_lower)
    
    if math_score >= max(science_score, social_score):
        return "mathematics"
    elif science_score >= social_score:
        return "science"
    elif social_score > 0:
        return "social_studies"
    else:
        return "general"

def _calculate_text_complexity(text: str) -> Dict[str, Any]:
    """Calculate various complexity metrics for the text."""
    sentences = re.split(r'[.!?।]', text)
    words = text.split()
    
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    unique_words = len(set(words))
    vocabulary_diversity = unique_words / len(words) if words else 0
    
    # Simple complexity scoring
    if avg_sentence_length <= 8:
        sentence_complexity = "simple"
    elif avg_sentence_length <= 15:
        sentence_complexity = "moderate"
    else:
        sentence_complexity = "complex"
    
    return {
        "overall_level": sentence_complexity,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "vocabulary_diversity": round(vocabulary_diversity, 2),
        "total_words": len(words),
        "unique_words": unique_words
    }

def _extract_key_concepts(text: str, subject: str) -> List[str]:
    """Extract key educational concepts from the text."""
    # This would use more sophisticated NLP to extract concepts
    # For now, a simple implementation
    concepts = []
    
    if subject == "mathematics":
        math_concepts = ["addition", "subtraction", "multiplication", "division", "fractions", "geometry"]
        concepts = [concept for concept in math_concepts if concept.lower() in text.lower()]
    elif subject == "science":
        science_concepts = ["plants", "animals", "water cycle", "weather", "seasons", "food chains"]
        concepts = [concept for concept in science_concepts if concept.lower() in text.lower()]
    
    return concepts[:5]  # Limit to top 5 concepts

def _determine_grade_levels(complexity_metrics: Dict, subject: str) -> List[str]:
    """Determine appropriate grade levels based on complexity."""
    complexity = complexity_metrics['overall_level']
    
    if complexity == "simple":
        return ["grade_1", "grade_2", "grade_3"]
    elif complexity == "moderate":
        return ["grade_3", "grade_4", "grade_5"]
    else:
        return ["grade_5", "grade_6", "grade_7", "grade_8"]

def _identify_question_types(text: str) -> List[str]:
    """Identify types of questions present in the text."""
    question_types = []
    
    if re.search(r'what|क्या|कौन', text, re.IGNORECASE):
        question_types.append("factual")
    if re.search(r'why|क्यों|कैसे', text, re.IGNORECASE):
        question_types.append("analytical")
    if re.search(r'how|कैसे', text, re.IGNORECASE):
        question_types.append("procedural")
    
    return question_types

def _extract_learning_objectives(text: str, subject: str) -> List[str]:
    """Extract or infer learning objectives from content."""
    # This would be more sophisticated in a real implementation
    base_objectives = {
        "mathematics": [
            "Understand basic mathematical concepts",
            "Apply problem-solving skills",
            "Use mathematical reasoning"
        ],
        "science": [
            "Observe natural phenomena", 
            "Understand scientific concepts",
            "Develop inquiry skills"
        ],
        "general": [
            "Comprehend written content",
            "Apply knowledge to new situations",
            "Develop critical thinking"
        ]
    }
    
    return base_objectives.get(subject, base_objectives["general"])

def _analyze_language_complexity(text: str) -> Dict[str, Any]:
    """Analyze language complexity including multilingual aspects."""
    hindi_ratio = len(re.findall(r'[\u0900-\u097F]', text)) / len(text) if text else 0
    english_ratio = len(re.findall(r'[a-zA-Z]', text)) / len(text) if text else 0
    
    return {
        "multilingual": hindi_ratio > 0.1 and english_ratio > 0.1,
        "hindi_ratio": round(hindi_ratio, 2),
        "english_ratio": round(english_ratio, 2),
        "complexity_level": "appropriate_for_multilingual_learners"
    }

def _identify_prerequisites(concepts: List[str], subject: str) -> List[str]:
    """Identify prerequisite knowledge for the concepts."""
    prerequisites = {
        "multiplication": ["addition", "counting"],
        "fractions": ["division", "parts_and_wholes"],
        "plant_growth": ["living_vs_nonliving", "basic_needs"]
    }
    
    result = []
    for concept in concepts:
        if concept.lower() in prerequisites:
            result.extend(prerequisites[concept.lower()])
    
    return list(set(result))

def _identify_extension_opportunities(concepts: List[str], subject: str) -> List[str]:
    """Identify opportunities for extending learning."""
    extensions = {
        "addition": ["word_problems", "multi_digit_addition"],
        "plants": ["plant_classification", "ecosystem_studies"],
        "community": ["local_government", "civic_responsibility"]
    }
    
    result = []
    for concept in concepts:
        if concept.lower() in extensions:
            result.extend(extensions[concept.lower()])
    
    return list(set(result))

def _generate_worksheet_title(subject: str, concept: str, grade: int) -> str:
    """Generate appropriate worksheet title."""
    titles = {
        "mathematics": f"गणित अभ्यास - {concept} (कक्षा {grade})",
        "science": f"विज्ञान अन्वेषण - {concept} (कक्षा {grade})",
        "social_studies": f"सामाजिक अध्ययन - {concept} (कक्षा {grade})",
        "general": f"अध्ययन पत्रक - {concept} (कक्षा {grade})"
    }
    
    return titles.get(subject, titles["general"])

def _adapt_learning_objectives(objectives: List[str], grade_num: int) -> List[str]:
    """Adapt learning objectives for specific grade level."""
    adapted = []
    for objective in objectives:
        if grade_num <= 2:
            adapted.append(f"Basic: {objective}")
        elif grade_num <= 5:
            adapted.append(f"Intermediate: {objective}")
        else:
            adapted.append(f"Advanced: {objective}")
    
    return adapted

def _create_early_primary_sections(content: str, concepts: List[str], subject: str) -> List[Dict]:
    """Create worksheet sections for early primary grades (1-2)."""
    sections = [
        {
            "title": "देखो और बताओ (Look and Tell)",
            "type": "observation",
            "activities": [
                {
                    "instruction": "चित्र को देखकर सवालों के जवाब दो",
                    "questions": ["यह क्या है?", "इसका रंग कैसा है?", "यह कहाँ मिलता है?"],
                    "format": "oral_response"
                }
            ],
            "time_estimate": "10 minutes"
        },
        {
            "title": "मिलान करो (Match)",
            "type": "matching",
            "activities": [
                {
                    "instruction": "सही जोड़े बनाओ",
                    "format": "drawing_lines"
                }
            ],
            "time_estimate": "15 minutes"
        }
    ]
    return sections

def _create_primary_sections(content: str, concepts: List[str], subject: str) -> List[Dict]:
    """Create worksheet sections for primary grades (3-5)."""
    sections = [
        {
            "title": "समझो और लिखो (Understand and Write)",
            "type": "comprehension",
            "activities": [
                {
                    "instruction": "पैराग्राफ पढ़कर सवालों के जवाब लिखो",
                    "questions": ["मुख्य विषय क्या है?", "कोई तीन मुख्य बातें लिखो"],
                    "format": "written_response"
                }
            ],
            "time_estimate": "20 minutes"
        },
        {
            "title": "अभ्यास करो (Practice)",
            "type": "application",
            "activities": [
                {
                    "instruction": "दिए गए उदाहरणों को हल करो",
                    "format": "problem_solving"
                }
            ],
            "time_estimate": "25 minutes"
        }
    ]
    return sections

def _create_upper_primary_sections(content: str, concepts: List[str], subject: str) -> List[Dict]:
    """Create worksheet sections for upper primary grades (6-8)."""
    sections = [
        {
            "title": "विश्लेषण करो (Analyze)",
            "type": "analysis",
            "activities": [
                {
                    "instruction": "गहराई से सोचकर जवाब दो",
                    "questions": ["कारण और परिणाम क्या हैं?", "अपनी राय दो"],
                    "format": "detailed_written_response"
                }
            ],
            "time_estimate": "25 minutes"
        },
        {
            "title": "लागू करो (Apply)",
            "type": "application",
            "activities": [
                {
                    "instruction": "वास्तविक जीवन में इसका उपयोग कैसे करोगे?",
                    "format": "project_based"
                }
            ],
            "time_estimate": "30 minutes"
        }
    ]
    return sections

def _translate_worksheet_to_hindi(worksheet: Dict) -> Dict:
    """Translate worksheet content to Hindi."""
    # This would use the translation service
    # For now, returning a placeholder
    return {
        "title_hindi": worksheet["title"],
        "instructions_hindi": "Hindi instructions would go here",
        "notes": "Complete Hindi version available"
    }

def _create_grade_appropriate_assessment(grade_num: int, subject: str) -> Dict:
    """Create assessment criteria appropriate for grade level."""
    if grade_num <= 2:
        return {
            "type": "observational",
            "criteria": ["Participation", "Understanding", "Effort"],
            "scale": "Excellent/Good/Needs Improvement"
        }
    else:
        return {
            "type": "rubric_based",
            "criteria": ["Content Knowledge", "Application", "Communication"],
            "scale": "4-point scale"
        }

def _list_required_materials(sections: List[Dict], grade_num: int) -> List[str]:
    """List materials required for worksheet activities."""
    basic_materials = ["paper", "pencil", "eraser"]
    
    if grade_num <= 2:
        return basic_materials + ["crayons", "pictures"]
    else:
        return basic_materials + ["ruler", "colored pencils"]

def _estimate_completion_time(sections: List[Dict], grade_num: int) -> str:
    """Estimate time needed to complete worksheet."""
    total_minutes = sum(int(section.get("time_estimate", "20 minutes").split()[0]) for section in sections)
    
    if grade_num <= 2:
        total_minutes = int(total_minutes * 1.5)  # Younger students need more time
    
    return f"{total_minutes} minutes"

def _generate_teacher_notes(content_analysis: Dict, worksheets: Dict) -> Dict:
    """Generate comprehensive teacher notes."""
    return {
        "preparation_tips": [
            "Review key concepts before class",
            "Prepare visual aids from local materials",
            "Plan for different learning paces"
        ],
        "implementation_strategies": [
            "Start with group discussion",
            "Use peer learning for mixed abilities",
            "Provide individual support as needed"
        ],
        "common_challenges": [
            "Students may struggle with language",
            "Different grade levels need different support",
            "Limited resources require creativity"
        ],
        "extension_ideas": [
            "Connect to local community examples",
            "Create hands-on activities",
            "Encourage student presentations"
        ]
    }

def _create_implementation_guide(worksheets: Dict, grade_levels: List[str]) -> Dict:
    """Create step-by-step implementation guide."""
    return {
        "before_class": [
            "Print or write worksheets on blackboard",
            "Gather required materials",
            "Review content and anticipate questions"
        ],
        "during_class": [
            "Introduce topic with familiar examples",
            "Distribute worksheets by grade level",
            "Circulate and provide individual support",
            "Facilitate peer learning"
        ],
        "after_class": [
            "Review completed work",
            "Identify students needing extra help",
            "Plan follow-up activities"
        ],
        "differentiation_tips": {
            "for_struggling_students": [
                "Provide additional examples",
                "Allow pair work",
                "Break tasks into smaller steps"
            ],
            "for_advanced_students": [
                "Provide extension questions",
                "Encourage helping others",
                "Assign leadership roles"
            ]
        }
    }

def _create_assessment_rubrics(content_analysis: Dict, grade_levels: List[str]) -> Dict:
    """Create assessment rubrics for different grade levels."""
    rubrics = {}
    
    for grade_level in grade_levels:
        grade_num = int(grade_level.replace('grade_', ''))
        
        if grade_num <= 2:
            rubrics[grade_level] = {
                "participation": {"excellent": "Active participation", "good": "Some participation", "needs_improvement": "Limited participation"},
                "understanding": {"excellent": "Shows clear understanding", "good": "Shows basic understanding", "needs_improvement": "Needs support"}
            }
        else:
            rubrics[grade_level] = {
                "content_knowledge": {"4": "Excellent", "3": "Good", "2": "Satisfactory", "1": "Needs Improvement"},
                "application": {"4": "Applies independently", "3": "Applies with guidance", "2": "Limited application", "1": "Cannot apply"},
                "communication": {"4": "Clear and detailed", "3": "Clear and adequate", "2": "Unclear but present", "1": "Minimal or unclear"}
            }
    
    return rubrics
