# agents/worksheet_processor/models/grade_differentiation.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class GradeLevel(Enum):
    GRADE_1 = "grade_1"
    GRADE_2 = "grade_2" 
    GRADE_3 = "grade_3"
    GRADE_4 = "grade_4"
    GRADE_5 = "grade_5"
    GRADE_6 = "grade_6"
    GRADE_7 = "grade_7"
    GRADE_8 = "grade_8"

class ComplexityLevel(Enum):
    VERY_SIMPLE = "very_simple"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

class ActivityType(Enum):
    OBSERVATION = "observation"
    MATCHING = "matching"
    FILL_IN_BLANKS = "fill_in_blanks"
    SHORT_ANSWER = "short_answer"
    LONG_ANSWER = "long_answer"
    PROBLEM_SOLVING = "problem_solving"
    CREATIVE = "creative"
    HANDS_ON = "hands_on"

@dataclass
class GradeCharacteristics:
    """Characteristics and capabilities for each grade level."""
    grade_level: GradeLevel
    age_range: tuple
    attention_span_minutes: int
    vocabulary_level: ComplexityLevel
    reading_level: ComplexityLevel
    writing_ability: ComplexityLevel
    abstract_thinking: bool
    preferred_activities: List[ActivityType]
    learning_characteristics: List[str]

@dataclass
class ContentDifferentiation:
    """Rules for differentiating content across grade levels."""
    concept: str
    grade_adaptations: Dict[GradeLevel, Dict[str, Any]]
    
class GradeDifferentiationModel:
    """Model for handling grade-level differentiation of educational content."""
    
    def __init__(self):
        self.grade_characteristics = self._initialize_grade_characteristics()
        self.differentiation_rules = self._initialize_differentiation_rules()
    
    def _initialize_grade_characteristics(self) -> Dict[GradeLevel, GradeCharacteristics]:
        """Initialize characteristics for each grade level based on Indian educational context."""
        return {
            GradeLevel.GRADE_1: GradeCharacteristics(
                grade_level=GradeLevel.GRADE_1,
                age_range=(6, 7),
                attention_span_minutes=10,
                vocabulary_level=ComplexityLevel.VERY_SIMPLE,
                reading_level=ComplexityLevel.VERY_SIMPLE,
                writing_ability=ComplexityLevel.VERY_SIMPLE,
                abstract_thinking=False,
                preferred_activities=[
                    ActivityType.OBSERVATION,
                    ActivityType.MATCHING,
                    ActivityType.HANDS_ON
                ],
                learning_characteristics=[
                    "Learn through play and games",
                    "Need concrete examples",
                    "Short attention spans",
                    "Learn through repetition",
                    "Prefer visual and tactile learning"
                ]
            ),
            
            GradeLevel.GRADE_2: GradeCharacteristics(
                grade_level=GradeLevel.GRADE_2,
                age_range=(7, 8),
                attention_span_minutes=15,
                vocabulary_level=ComplexityLevel.SIMPLE,
                reading_level=ComplexityLevel.SIMPLE,
                writing_ability=ComplexityLevel.SIMPLE,
                abstract_thinking=False,
                preferred_activities=[
                    ActivityType.OBSERVATION,
                    ActivityType.MATCHING,
                    ActivityType.FILL_IN_BLANKS,
                    ActivityType.HANDS_ON
                ],
                learning_characteristics=[
                    "Beginning to read simple sentences",
                    "Can write simple words",
                    "Still need concrete examples",
                    "Enjoy stories and songs",
                    "Learn well in groups"
                ]
            ),
            
            GradeLevel.GRADE_3: GradeCharacteristics(
                grade_level=GradeLevel.GRADE_3,
                age_range=(8, 9),
                attention_span_minutes=20,
                vocabulary_level=ComplexityLevel.SIMPLE,
                reading_level=ComplexityLevel.SIMPLE,
                writing_ability=ComplexityLevel.SIMPLE,
                abstract_thinking=False,
                preferred_activities=[
                    ActivityType.SHORT_ANSWER,
                    ActivityType.MATCHING,
                    ActivityType.FILL_IN_BLANKS,
                    ActivityType.HANDS_ON,
                    ActivityType.CREATIVE
                ],
                learning_characteristics=[
                    "Can read simple paragraphs",
                    "Beginning paragraph writing",
                    "Starting to think logically",
                    "Curious and ask many questions",
                    "Learn through exploration"
                ]
            ),
            
            GradeLevel.GRADE_4: GradeCharacteristics(
                grade_level=GradeLevel.GRADE_4,
                age_range=(9, 10),
                attention_span_minutes=25,
                vocabulary_level=ComplexityLevel.MODERATE,
                reading_level=ComplexityLevel.MODERATE,
                writing_ability=ComplexityLevel.SIMPLE,
                abstract_thinking=False,
                preferred_activities=[
                    ActivityType.SHORT_ANSWER,
                    ActivityType.PROBLEM_SOLVING,
                    ActivityType.CREATIVE,
                    ActivityType.HANDS_ON
                ],
                learning_characteristics=[
                    "Can read longer texts",
                    "Writing skills developing",
                    "Beginning analytical thinking",
                    "Enjoy collaborative work",
                    "Can follow multi-step instructions"
                ]
            ),
            
            GradeLevel.GRADE_5: GradeCharacteristics(
                grade_level=GradeLevel.GRADE_5,
                age_range=(10, 11),
                attention_span_minutes=30,
                vocabulary_level=ComplexityLevel.MODERATE,
                reading_level=ComplexityLevel.MODERATE,
                writing_ability=ComplexityLevel.MODERATE,
                abstract_thinking=True,
                preferred_activities=[
                    ActivityType.SHORT_ANSWER,
                    ActivityType.LONG_ANSWER,
                    ActivityType.PROBLEM_SOLVING,
                    ActivityType.CREATIVE
                ],
                learning_characteristics=[
                    "Can understand complex texts",
                    "Developing writing skills",
                    "Beginning abstract reasoning",
                    "Can work independently",
                    "Understand cause and effect"
                ]
            ),
            
            GradeLevel.GRADE_6: GradeCharacteristics(
                grade_level=GradeLevel.GRADE_6,
                age_range=(11, 12),
                attention_span_minutes=35,
                vocabulary_level=ComplexityLevel.MODERATE,
                reading_level=ComplexityLevel.COMPLEX,
                writing_ability=ComplexityLevel.MODERATE,
                abstract_thinking=True,
                preferred_activities=[
                    ActivityType.LONG_ANSWER,
                    ActivityType.PROBLEM_SOLVING,
                    ActivityType.CREATIVE
                ],
                learning_characteristics=[
                    "Can analyze and synthesize information",
                    "Developing critical thinking",
                    "Can handle abstract concepts",
                    "Prefer challenging tasks",
                    "Beginning to form personal opinions"
                ]
            ),
            
            GradeLevel.GRADE_7: GradeCharacteristics(
                grade_level=GradeLevel.GRADE_7,
                age_range=(12, 13),
                attention_span_minutes=40,
                vocabulary_level=ComplexityLevel.COMPLEX,
                reading_level=ComplexityLevel.COMPLEX,
                writing_ability=ComplexityLevel.COMPLEX,
                abstract_thinking=True,
                preferred_activities=[
                    ActivityType.LONG_ANSWER,
                    ActivityType.PROBLEM_SOLVING,
                    ActivityType.CREATIVE
                ],
                learning_characteristics=[
                    "Strong analytical abilities",
                    "Can handle complex concepts",
                    "Developing research skills",
                    "Can work on long-term projects",
                    "Beginning metacognitive awareness"
                ]
            ),
            
            GradeLevel.GRADE_8: GradeCharacteristics(
                grade_level=GradeLevel.GRADE_8,
                age_range=(13, 14),
                attention_span_minutes=45,
                vocabulary_level=ComplexityLevel.COMPLEX,
                reading_level=ComplexityLevel.VERY_COMPLEX,
                writing_ability=ComplexityLevel.COMPLEX,
                abstract_thinking=True,
                preferred_activities=[
                    ActivityType.LONG_ANSWER,
                    ActivityType.PROBLEM_SOLVING,
                    ActivityType.CREATIVE
                ],
                learning_characteristics=[
                    "Advanced critical thinking",
                    "Can handle highly abstract concepts", 
                    "Strong research and analysis skills",
                    "Can create original work",
                    "Developing personal learning strategies"
                ]
            )
        }
    
    def _initialize_differentiation_rules(self) -> Dict[str, ContentDifferentiation]:
        """Initialize differentiation rules for common concepts."""
        return {
            "addition": ContentDifferentiation(
                concept="addition",
                grade_adaptations={
                    GradeLevel.GRADE_1: {
                        "approach": "concrete_objects",
                        "range": "1-10",
                        "format": "pictures_and_symbols",
                        "examples": "counting toys, fruits"
                    },
                    GradeLevel.GRADE_2: {
                        "approach": "visual_representation",
                        "range": "1-20",
                        "format": "number_line",
                        "examples": "adding school supplies"
                    },
                    GradeLevel.GRADE_3: {
                        "approach": "abstract_numbers",
                        "range": "1-100",
                        "format": "vertical_addition",
                        "examples": "money problems"
                    }
                }
            ),
            
            "photosynthesis": ContentDifferentiation(
                concept="photosynthesis",
                grade_adaptations={
                    GradeLevel.GRADE_2: {
                        "approach": "plants_need_sunlight",
                        "vocabulary": "simple_words",
                        "activities": "observation_drawing"
                    },
                    GradeLevel.GRADE_4: {
                        "approach": "plants_make_food",
                        "vocabulary": "basic_scientific_terms",
                        "activities": "simple_experiments"
                    },
                    GradeLevel.GRADE_6: {
                        "approach": "chemical_process",
                        "vocabulary": "scientific_terminology",
                        "activities": "detailed_experiments"
                    }
                }
            )
        }
    
    def get_grade_characteristics(self, grade_level: GradeLevel) -> GradeCharacteristics:
        """Get characteristics for a specific grade level."""
        return self.grade_characteristics[grade_level]
    
    def adapt_content_for_grade(self, content: str, concept: str, grade_level: GradeLevel) -> Dict[str, Any]:
        """Adapt content for a specific grade level."""
        characteristics = self.get_grade_characteristics(grade_level)
        
        # Get differentiation rules if available
        differentiation = self.differentiation_rules.get(concept)
        specific_adaptations = {}
        if differentiation and grade_level in differentiation.grade_adaptations:
            specific_adaptations = differentiation.grade_adaptations[grade_level]
        
        return {
            "adapted_content": self._simplify_language(content, characteristics.vocabulary_level),
            "recommended_activities": [activity.value for activity in characteristics.preferred_activities],
            "time_estimate": characteristics.attention_span_minutes,
            "teaching_approach": self._get_teaching_approach(characteristics),
            "assessment_method": self._get_assessment_method(characteristics),
            "specific_adaptations": specific_adaptations,
            "learning_characteristics": characteristics.learning_characteristics
        }
    
    def _simplify_language(self, content: str, vocabulary_level: ComplexityLevel) -> str:
        """Simplify language based on vocabulary level."""
        # This would implement actual language simplification
        # For now, returning based on complexity level
        if vocabulary_level == ComplexityLevel.VERY_SIMPLE:
            return self._make_very_simple(content)
        elif vocabulary_level == ComplexityLevel.SIMPLE:
            return self._make_simple(content)
        elif vocabulary_level == ComplexityLevel.MODERATE:
            return self._make_moderate(content)
        else:
            return content
    
    def _make_very_simple(self, content: str) -> str:
        """Make content very simple for early grades."""
        # Replace complex words with simple ones
        replacements = {
            "photosynthesis": "plants making food",
            "multiplication": "adding many times",
            "environment": "the place around us"
        }
        
        simplified = content
        for complex_word, simple_word in replacements.items():
            simplified = simplified.replace(complex_word, simple_word)
        
        return simplified
    
    def _make_simple(self, content: str) -> str:
        """Make content simple."""
        # Add explanations for difficult concepts
        return content  # Simplified implementation
    
    def _make_moderate(self, content: str) -> str:
        """Make content moderately complex."""
        return content  # Could add some complexity management
    
    def _get_teaching_approach(self, characteristics: GradeCharacteristics) -> str:
        """Get recommended teaching approach."""
        if not characteristics.abstract_thinking:
            return "concrete_hands_on"
        elif characteristics.grade_level.value in ["grade_3", "grade_4", "grade_5"]:
            return "visual_conceptual"
        else:
            return "abstract_analytical"
    
    def _get_assessment_method(self, characteristics: GradeCharacteristics) -> str:
        """Get recommended assessment method."""
        if characteristics.grade_level.value in ["grade_1", "grade_2"]:
            return "observation_based"
        elif characteristics.grade_level.value in ["grade_3", "grade_4"]:
            return "simple_written_tasks"
        else:
            return "comprehensive_assessment"
    
    def get_multi_grade_adaptations(self, content: str, concept: str, grade_levels: List[GradeLevel]) -> Dict[GradeLevel, Dict[str, Any]]:
        """Get adaptations for multiple grade levels simultaneously."""
        adaptations = {}
        
        for grade_level in grade_levels:
            adaptations[grade_level] = self.adapt_content_for_grade(content, concept, grade_level)
        
        return adaptations
    
    def suggest_cross_grade_activities(self, concept: str, grade_levels: List[GradeLevel]) -> List[Dict[str, Any]]:
        """Suggest activities that work across multiple grade levels."""
        activities = []
        
        # Activities that can be differentiated by complexity
        base_activities = [
            {
                "name": "Group Discussion",
                "description": "Discuss the concept with grade-appropriate questions",
                "differentiation": "question_complexity"
            },
            {
                "name": "Drawing Activity", 
                "description": "Visual representation of the concept",
                "differentiation": "detail_level"
            },
            {
                "name": "Hands-on Exploration",
                "description": "Physical manipulation and exploration",
                "differentiation": "complexity_of_materials"
            }
        ]
        
        for activity in base_activities:
            activity["grade_adaptations"] = {}
            for grade_level in grade_levels:
                characteristics = self.get_grade_characteristics(grade_level)
                activity["grade_adaptations"][grade_level.value] = {
                    "time": characteristics.attention_span_minutes,
                    "complexity": characteristics.vocabulary_level.value,
                    "support_needed": "high" if not characteristics.abstract_thinking else "low"
                }
            activities.append(activity)
        
        return activities
