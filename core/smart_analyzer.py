"""
Smart Analyzer - AI-powered prompt analysis
Automatically detects domain, role, and task from raw prompts using Gemini
"""
import json
import google.generativeai as genai
from core.config import Config
from typing import Dict, Optional


class SmartAnalyzer:
    """Uses Gemini to auto-detect prompt context and characteristics"""

    def __init__(self):
        """Initialize Gemini"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def analyze_prompt(self, raw_prompt: str) -> Dict[str, any]:
        """
        Analyze a raw prompt and detect its characteristics

        Args:
            raw_prompt: The user's original prompt

        Returns:
            Dictionary with detected domain, role, task, and confidence
        """
        if not raw_prompt or len(raw_prompt.strip()) < 5:
            # Default to general if prompt is too short
            return {
                'domain': 'academic',
                'role': 'student',
                'task': 'learning',
                'confidence': 0.5,
                'detected': False
            }

        try:
            # Craft analysis prompt
            analysis_request = f"""Analyze this user prompt and return ONLY valid JSON (no markdown, no code blocks, no explanation).

Prompt: "{raw_prompt}"

Analyze and determine:
1. domain: Choose ONE from ["academic", "ml-data-science", "python-development"]
2. role: Infer user's role (e.g., student, researcher, developer, data-scientist, professional)
3. task: What they're trying to do (e.g., learning, research, debugging, analysis, writing)
4. confidence: Your confidence level 0.0-1.0 based on clarity of the prompt

Rules:
- Return ONLY the JSON object
- No markdown formatting
- No code blocks
- No explanations
- Must be valid JSON

Return format:
{{"domain": "academic", "role": "student", "task": "learning", "confidence": 0.9}}"""

            # Get response from Gemini
            response = self.model.generate_content(analysis_request)
            response_text = response.text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                # Extract JSON from code block
                lines = response_text.split('\n')
                json_lines = [line for line in lines if line and not line.startswith('```')]
                response_text = '\n'.join(json_lines)

            # Parse JSON
            analysis = json.loads(response_text)

            # Validate domain
            valid_domains = ['academic', 'ml-data-science', 'python-development']
            if analysis.get('domain') not in valid_domains:
                # Default to academic if invalid
                analysis['domain'] = 'academic'

            # Add detected flag
            analysis['detected'] = True

            return analysis

        except json.JSONDecodeError as e:
            # Fallback to keyword-based detection
            return self._fallback_analysis(raw_prompt)
        except Exception as e:
            # Fallback on any error
            return self._fallback_analysis(raw_prompt)

    def _fallback_analysis(self, raw_prompt: str) -> Dict[str, any]:
        """
        Fallback keyword-based analysis when Gemini fails

        Args:
            raw_prompt: The user's prompt

        Returns:
            Dictionary with detected characteristics
        """
        prompt_lower = raw_prompt.lower()

        # Keyword-based domain detection
        ml_keywords = ['machine learning', 'neural network', 'model', 'dataset', 'training',
                      'algorithm', 'prediction', 'classification', 'regression', 'data science',
                      'pandas', 'numpy', 'sklearn', 'tensorflow', 'pytorch']

        python_keywords = ['python', 'code', 'function', 'class', 'debug', 'error', 'script',
                          'variable', 'loop', 'import', 'module', 'programming']

        academic_keywords = ['research', 'paper', 'study', 'thesis', 'dissertation', 'literature',
                           'review', 'citation', 'analysis', 'explain', 'understand', 'learn']

        # Count keyword matches
        ml_score = sum(1 for kw in ml_keywords if kw in prompt_lower)
        python_score = sum(1 for kw in python_keywords if kw in prompt_lower)
        academic_score = sum(1 for kw in academic_keywords if kw in prompt_lower)

        # Determine domain
        scores = {
            'ml-data-science': ml_score,
            'python-development': python_score,
            'academic': academic_score
        }
        domain = max(scores, key=scores.get)
        confidence = min(scores[domain] * 0.2, 0.9)  # Cap at 0.9

        # Determine role based on prompt characteristics
        if any(word in prompt_lower for word in ['learn', 'understand', 'explain', 'what is']):
            role = 'student'
            task = 'learning'
        elif any(word in prompt_lower for word in ['research', 'analyze', 'investigate']):
            role = 'researcher'
            task = 'research'
        elif any(word in prompt_lower for word in ['code', 'develop', 'build', 'create']):
            role = 'developer'
            task = 'coding'
        else:
            role = 'professional'
            task = 'analysis'

        return {
            'domain': domain,
            'role': role,
            'task': task,
            'confidence': confidence,
            'detected': True
        }

    def get_best_version_type(self, analysis: Dict[str, any]) -> str:
        """
        Determine which version type is best based on analysis

        Args:
            analysis: Analysis results from analyze_prompt

        Returns:
            Version type ('basic', 'critical', 'tutor', 'safe')
        """
        task = analysis.get('task', 'learning').lower()
        role = analysis.get('role', 'student').lower()

        # Decision logic
        if 'student' in role or 'learn' in task:
            return 'tutor'  # Learning-focused
        elif 'research' in task or 'researcher' in role:
            return 'critical'  # Critical thinking
        elif 'citation' in task or 'factual' in task:
            return 'safe'  # Accuracy-focused
        else:
            return 'basic'  # Default
