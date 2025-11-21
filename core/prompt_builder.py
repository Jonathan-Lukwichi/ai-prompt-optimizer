"""
Advanced Prompt Builder - Guided prompt construction using proven frameworks
Implements: 6-Step Framework + CRAFT Formula
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import google.generativeai as genai
from core.config import Config
import base64
from PIL import Image
import io


@dataclass
class PromptComponents:
    """Container for prompt components"""
    # 6-Step Framework
    role: str = ""
    context: str = ""
    task: str = ""
    format: str = ""
    rules: str = ""
    examples: str = ""

    # CRAFT Formula (alternative)
    craft_context: str = ""
    craft_role: str = ""
    craft_action: str = ""
    craft_format: str = ""
    craft_thinking_mode: str = ""

    # Additional context
    uploaded_context: Optional[str] = None  # Text from uploaded files/images


class PromptBuilder:
    """
    Advanced prompt builder with multiple frameworks

    Frameworks:
    1. 6-Step Framework: Role → Context → Task → Format → Rules → Examples
    2. CRAFT Formula: Contexte, Rôle, Action, Format, Thinking mode
    """

    def __init__(self):
        """Initialize prompt builder"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def build_from_6_step(self, components: PromptComponents) -> str:
        """
        Build prompt using 6-Step Framework

        Args:
            components: PromptComponents with 6-step fields filled

        Returns:
            Constructed prompt string
        """
        parts = []

        # Role
        if components.role:
            parts.append(f"Role: {components.role}")

        # Context
        if components.context:
            parts.append(f"\nContext: {components.context}")

        # Uploaded context (from images/documents)
        if components.uploaded_context:
            parts.append(f"\nAdditional Context (from uploaded file):\n{components.uploaded_context}")

        # Task
        if components.task:
            parts.append(f"\nTask: {components.task}")

        # Format
        if components.format:
            parts.append(f"\nFormat: {components.format}")

        # Rules
        if components.rules:
            parts.append(f"\nRules/Constraints:\n{components.rules}")

        # Examples
        if components.examples:
            parts.append(f"\nExamples/References:\n{components.examples}")

        return "\n".join(parts)

    def build_from_craft(self, components: PromptComponents) -> str:
        """
        Build prompt using CRAFT Formula

        CRAFT = Contexte, Rôle, Action, Format, Thinking mode

        Args:
            components: PromptComponents with CRAFT fields filled

        Returns:
            Constructed prompt string
        """
        parts = []

        # Contexte
        if components.craft_context:
            parts.append(f"Contexte: {components.craft_context}")

        # Uploaded context
        if components.uploaded_context:
            parts.append(f"\nContexte supplémentaire (fichier téléchargé):\n{components.uploaded_context}")

        # Rôle
        if components.craft_role:
            parts.append(f"\nRôle: {components.craft_role}")

        # Action
        if components.craft_action:
            parts.append(f"\nAction: {components.craft_action}")

        # Format
        if components.craft_format:
            parts.append(f"\nFormat: {components.craft_format}")

        # Thinking mode
        if components.craft_thinking_mode:
            parts.append(f"\nMode de réflexion: {components.craft_thinking_mode}")

        return "\n".join(parts)

    def extract_context_from_image(self, image_bytes: bytes, user_query: str = "") -> str:
        """
        Extract context from uploaded image using Gemini Vision

        Args:
            image_bytes: Image file bytes
            user_query: Optional specific query about the image

        Returns:
            Extracted context text
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes))

            # Create prompt for context extraction
            prompt = f"""Analyze this image and extract relevant context that could be useful for creating a prompt.

Focus on:
- What is shown in the image
- Key information, data, or text visible
- Relevant details that could inform a task or question
- Any specific elements worth mentioning

{f'User specifically wants to know: {user_query}' if user_query else ''}

Provide a clear, structured description of the context from this image."""

            # Use Gemini Vision
            response = self.model.generate_content([prompt, image])

            return response.text

        except Exception as e:
            return f"Error extracting context from image: {str(e)}"

    def extract_context_from_document(self, text_content: str, user_query: str = "") -> str:
        """
        Extract key context from uploaded document

        Args:
            text_content: Document text content
            user_query: Optional specific query about the document

        Returns:
            Extracted context summary
        """
        try:
            prompt = f"""Analyze this document and extract the most relevant context for creating a prompt.

Document content:
{text_content[:4000]}  # Limit to avoid token overflow

{f'User specifically wants to know: {user_query}' if user_query else ''}

Provide:
1. Main topic/subject
2. Key points or findings
3. Relevant data or statistics
4. Important context for understanding the content

Keep it concise but informative."""

            response = self.model.generate_content(prompt)

            return response.text

        except Exception as e:
            return f"Error extracting context from document: {str(e)}"

    def suggest_improvements(self, partial_prompt: str, framework: str = "6-step") -> Dict[str, List[str]]:
        """
        Suggest improvements for partially constructed prompt

        Args:
            partial_prompt: Current prompt text
            framework: "6-step" or "craft"

        Returns:
            Dictionary with suggestions for each component
        """
        try:
            if framework == "6-step":
                prompt = f"""Analyze this partially constructed prompt and suggest improvements for each component:

Current prompt:
{partial_prompt}

For each of the 6 components, provide 2-3 suggestions:
1. Role - Who should the AI act as?
2. Context - What background information is needed?
3. Task - What specific action should be performed?
4. Format - How should the output be structured?
5. Rules - What constraints or requirements?
6. Examples - What samples or references would help?

Respond in JSON format:
{{
  "role": ["suggestion 1", "suggestion 2"],
  "context": ["suggestion 1", "suggestion 2"],
  ...
}}"""
            else:  # CRAFT
                prompt = f"""Analyze this partially constructed prompt and suggest improvements for each CRAFT component:

Current prompt:
{partial_prompt}

For each CRAFT component, provide 2-3 suggestions:
1. Contexte - What is the situation/background?
2. Rôle - Who should the AI be?
3. Action - What precise action is expected?
4. Format - What type of output?
5. Thinking mode - What reasoning approach?

Respond in JSON format:
{{
  "contexte": ["suggestion 1", "suggestion 2"],
  "role": ["suggestion 1", "suggestion 2"],
  ...
}}"""

            response = self.model.generate_content(prompt)

            # Try to parse JSON (basic parsing, can be improved)
            import json
            import re

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response.text)
            if json_match:
                suggestions = json.loads(json_match.group(0))
                return suggestions
            else:
                # Fallback: return raw text
                return {"suggestions": [response.text]}

        except Exception as e:
            return {"error": [f"Error generating suggestions: {str(e)}"]}

    def get_template_suggestions(
        self,
        components: PromptComponents,
        user_preferences: Optional[Dict] = None
    ) -> List[Dict[str, str]]:
        """
        Get AI-powered template suggestions based on components and preferences

        Args:
            components: Current prompt components
            user_preferences: User's usage history and preferences

        Returns:
            List of suggested templates with name, description, content
        """
        try:
            # Build context from components
            context_parts = []

            if components.role or components.craft_role:
                context_parts.append(f"Role: {components.role or components.craft_role}")

            if components.task or components.craft_action:
                context_parts.append(f"Task: {components.task or components.craft_action}")

            if user_preferences:
                domain = user_preferences.get('preferred_domain', '')
                if domain:
                    context_parts.append(f"Domain: {domain}")

            context_str = "\n".join(context_parts)

            prompt = f"""Based on this user's needs, suggest 3 relevant prompt templates:

User context:
{context_str}

For each template, provide:
1. Name - A catchy template name
2. Description - When to use this template
3. Template - The actual prompt template with [placeholders]

Respond in this format for each template:
---
NAME: [Template Name]
DESCRIPTION: [When to use]
TEMPLATE:
[The template with [placeholders]]
---"""

            response = self.model.generate_content(prompt)

            # Parse response into templates
            templates = []
            template_blocks = response.text.split('---')

            for block in template_blocks:
                if 'NAME:' in block:
                    lines = block.strip().split('\n')
                    template_data = {'name': '', 'description': '', 'content': ''}

                    current_section = None
                    for line in lines:
                        if line.startswith('NAME:'):
                            template_data['name'] = line.replace('NAME:', '').strip()
                        elif line.startswith('DESCRIPTION:'):
                            template_data['description'] = line.replace('DESCRIPTION:', '').strip()
                        elif line.startswith('TEMPLATE:'):
                            current_section = 'content'
                        elif current_section == 'content':
                            template_data['content'] += line + '\n'

                    if template_data['name']:
                        templates.append(template_data)

            return templates[:3]  # Return top 3

        except Exception as e:
            return [{'name': 'Error', 'description': str(e), 'content': ''}]

    def validate_prompt(self, prompt: str) -> Dict[str, any]:
        """
        Validate a constructed prompt and provide quality score

        Args:
            prompt: The complete prompt to validate

        Returns:
            Dictionary with score, strengths, weaknesses, recommendations
        """
        try:
            validation_prompt = f"""Evaluate this prompt's quality and provide feedback:

Prompt to evaluate:
{prompt}

Provide:
1. Quality Score (0-100)
2. Strengths (2-3 points)
3. Weaknesses (2-3 points)
4. Recommendations for improvement

Format your response as:
SCORE: [number]
STRENGTHS:
- [strength 1]
- [strength 2]
WEAKNESSES:
- [weakness 1]
- [weakness 2]
RECOMMENDATIONS:
- [recommendation 1]
- [recommendation 2]"""

            response = self.model.generate_content(validation_prompt)

            # Parse response
            result = {
                'score': 75,  # Default
                'strengths': [],
                'weaknesses': [],
                'recommendations': []
            }

            lines = response.text.split('\n')
            current_section = None

            for line in lines:
                if 'SCORE:' in line:
                    try:
                        result['score'] = int(''.join(filter(str.isdigit, line)))
                    except:
                        pass
                elif 'STRENGTHS:' in line:
                    current_section = 'strengths'
                elif 'WEAKNESSES:' in line:
                    current_section = 'weaknesses'
                elif 'RECOMMENDATIONS:' in line:
                    current_section = 'recommendations'
                elif line.strip().startswith('-') and current_section:
                    result[current_section].append(line.strip()[1:].strip())

            return result

        except Exception as e:
            return {
                'score': 0,
                'strengths': [],
                'weaknesses': [],
                'recommendations': [f"Error validating prompt: {str(e)}"]
            }


# Framework examples and guides
FRAMEWORK_EXAMPLES = {
    "6-step": {
        "name": "6-Step Framework",
        "description": "Comprehensive prompt construction in 6 steps",
        "steps": [
            {
                "name": "Role",
                "description": "Define who the AI should be",
                "example": "You are an expert data scientist with 10 years of experience in machine learning",
                "tips": [
                    "Be specific about expertise level",
                    "Include relevant background",
                    "Mention specific skills if needed"
                ]
            },
            {
                "name": "Context",
                "description": "Explain the situation and background",
                "example": "I'm working on a project to predict customer churn for a SaaS company with 50,000 users",
                "tips": [
                    "Provide relevant background information",
                    "Include important constraints or limitations",
                    "Mention the broader goal or purpose"
                ]
            },
            {
                "name": "Task",
                "description": "State precisely what you expect",
                "example": "Help me select the most appropriate machine learning algorithm and explain why it would work best for this use case",
                "tips": [
                    "Be very specific about the desired action",
                    "Break down complex tasks into steps",
                    "Use action verbs (analyze, create, explain, etc.)"
                ]
            },
            {
                "name": "Format",
                "description": "Specify the type of output you want",
                "example": "Provide a structured comparison table with algorithm name, pros, cons, and suitability score (1-10)",
                "tips": [
                    "Specify structure (list, table, paragraph, etc.)",
                    "Indicate desired length",
                    "Mention any special formatting needs"
                ]
            },
            {
                "name": "Rules",
                "description": "Indicate any constraints or requirements",
                "example": "Focus only on algorithms suitable for datasets with 100K+ rows. Avoid algorithms requiring extensive feature engineering.",
                "tips": [
                    "List must-have requirements",
                    "Specify things to avoid",
                    "Mention any constraints (time, complexity, etc.)"
                ]
            },
            {
                "name": "Examples",
                "description": "Provide models, samples, or references",
                "example": "Similar to how you'd evaluate Random Forest vs XGBoost for classification tasks",
                "tips": [
                    "Show examples of desired output",
                    "Reference similar successful cases",
                    "Include sample data if relevant"
                ]
            }
        ]
    },
    "craft": {
        "name": "CRAFT Formula",
        "description": "French framework: Contexte, Rôle, Action, Format, Thinking mode",
        "steps": [
            {
                "name": "Contexte",
                "description": "La situation et le contexte",
                "example": "Je prépare une présentation pour un client sur l'IA dans le retail",
                "tips": [
                    "Décrivez la situation actuelle",
                    "Mentionnez les enjeux",
                    "Précisez les contraintes"
                ]
            },
            {
                "name": "Rôle",
                "description": "Qui doit être l'IA",
                "example": "Tu es un consultant en transformation digitale spécialisé dans le retail",
                "tips": [
                    "Définissez l'expertise requise",
                    "Mentionnez le niveau d'expérience",
                    "Précisez les compétences clés"
                ]
            },
            {
                "name": "Action",
                "description": "L'action précise attendue",
                "example": "Crée un plan de présentation avec 5 slides clés sur les bénéfices de l'IA",
                "tips": [
                    "Utilisez des verbes d'action",
                    "Soyez très précis",
                    "Décomposez si nécessaire"
                ]
            },
            {
                "name": "Format",
                "description": "Le type de sortie souhaité",
                "example": "Format: Liste numérotée avec titre de slide + 3 points clés par slide",
                "tips": [
                    "Spécifiez la structure",
                    "Indiquez la longueur",
                    "Mentionnez le style si important"
                ]
            },
            {
                "name": "Thinking mode",
                "description": "Le mode de réflexion à adopter",
                "example": "Réfléchis de manière stratégique en priorisant le ROI et les quick wins",
                "tips": [
                    "Analytique, créatif, stratégique?",
                    "Quels critères prioriser?",
                    "Quel niveau de détail?"
                ]
            }
        ]
    }
}


def get_framework_guide(framework: str = "6-step") -> Dict:
    """Get the guide for a specific framework"""
    return FRAMEWORK_EXAMPLES.get(framework, FRAMEWORK_EXAMPLES["6-step"])
