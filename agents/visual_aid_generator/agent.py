"""
Visual Aid Generator Agent
Creates simple line drawings and diagrams for blackboard reproduction
"""
from typing import Dict, Any, Optional
from vertexai.generative_models import GenerativeModel, GenerationConfig
from google.cloud import vision
import base64
from PIL import Image
from io import BytesIO
from .tools import (
    generate_line_drawing,
    create_simple_diagram,
    optimize_for_blackboard,
    add_labels_in_language
)

class VisualAidGeneratorAgent:
    def __init__(self):
        self.model = GenerativeModel("gemini-pro-vision")
        self.vision_client = vision.ImageAnnotatorClient()
        
        self.instruction = """You are an expert in creating simple, clear visual aids for 
        education. Your drawings should be:

        1. Easy to reproduce on a blackboard
        2. Clear and uncluttered
        3. Properly labeled with key components
        4. Appropriate for the grade level

        Focus on:
        - Scientific diagrams
        - Mathematical visualizations
        - Process flows
        - Geographic illustrations
        - Simple charts and graphs
        """
        
        self.config = GenerationConfig(
            temperature=0.2,  # Lower for more consistent outputs
            top_p=0.8,
            top_k=40
        )
    
    async def create_diagram(
        self,
        concept: str,
        language: str,
        grade_level: str,
        diagram_type: str = 'line_drawing'
    ) -> Dict[str, Any]:
        """Generate a simple diagram or drawing"""
        try:
            # Generate base diagram
            if diagram_type == 'line_drawing':
                image_data = await generate_line_drawing(
                    concept=concept,
                    grade_level=grade_level,
                    model=self.model,
                    config=self.config
                )
            else:
                image_data = await create_simple_diagram(
                    concept=concept,
                    diagram_type=diagram_type,
                    grade_level=grade_level,
                    model=self.model,
                    config=self.config
                )
            
            # Optimize for blackboard reproduction
            optimized_image = await optimize_for_blackboard(
                image_data=image_data
            )
            
            # Add labels in specified language
            if language.lower() != 'english':
                final_image = await add_labels_in_language(
                    image=optimized_image,
                    language=language,
                    labels=self._extract_labels(optimized_image)
                )
            else:
                final_image = optimized_image
            
            # Convert to base64 for response
            buffered = BytesIO()
            final_image.save(buffered, format="PNG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'image_data': image_base64,
                'concept': concept,
                'language': language,
                'grade_level': grade_level,
                'diagram_type': diagram_type
            }
        
        except Exception as e:
            raise Exception(f"Error generating diagram: {str(e)}")
    
    async def create_chart(
        self,
        data: Dict[str, Any],
        chart_type: str,
        language: str,
        grade_level: str
    ) -> Dict[str, Any]:
        """Generate a simple chart or graph"""
        try:
            # Generate chart based on data
            chart_image = await self._generate_chart(
                data=data,
                chart_type=chart_type,
                grade_level=grade_level
            )
            
            # Optimize for blackboard
            optimized_chart = await optimize_for_blackboard(
                image_data=chart_image
            )
            
            # Add labels in specified language
            if language.lower() != 'english':
                final_chart = await add_labels_in_language(
                    image=optimized_chart,
                    language=language,
                    labels=self._extract_labels(optimized_chart)
                )
            else:
                final_chart = optimized_chart
            
            # Convert to base64
            buffered = BytesIO()
            final_chart.save(buffered, format="PNG")
            chart_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'image_data': chart_base64,
                'chart_type': chart_type,
                'language': language,
                'grade_level': grade_level,
                'data': data
            }
        
        except Exception as e:
            raise Exception(f"Error generating chart: {str(e)}")
    
    def _extract_labels(self, image: Image) -> list:
        """Extract text labels from image using Vision API"""
        try:
            # Convert image to bytes
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            content = buffered.getvalue()
            
            # Detect text
            image = vision.Image(content=content)
            response = self.vision_client.text_detection(image=image)
            texts = response.text_annotations
            
            # Extract unique text elements
            labels = []
            if texts:
                labels = [text.description for text in texts[1:]]  # Skip first which is all text
            
            return labels
        
        except Exception as e:
            print(f"Warning: Error extracting labels: {str(e)}")
            return []
    
    async def _generate_chart(
        self,
        data: Dict[str, Any],
        chart_type: str,
        grade_level: str
    ) -> Image:
        """Generate a chart based on data and type"""
        # Implementation would use appropriate charting library
        # This is a placeholder for the actual implementation
        pass 