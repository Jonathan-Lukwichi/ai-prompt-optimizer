"""
Advanced Prompt Enhancer - Competitive features from industry leaders
Implements: Quick Enhance, Iterative Refinement, Educational Feedback
"""
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai
from core.config import Config
from dataclasses import dataclass


@dataclass
class Enhancement:
    """Container for enhancement results"""
    original: str
    enhanced: str
    changes: List[Dict[str, str]]
    score_before: int
    score_after: int
    explanation: str


@dataclass
class RefinementStage:
    """Container for iterative refinement stage"""
    stage_number: int
    prompt: str
    analysis: Dict[str, any]
    questions: List[str]
    suggestions: List[str]
    score: int


class PromptEnhancer:
    """
    Advanced prompt enhancement system inspired by industry leaders

    Features:
    1. Quick Enhance - One-shot optimization (like CustomGPT)
    2. Iterative Refinement - Multi-stage improvement (like MaxAI)
    3. Educational Feedback - Explain why changes improve prompts
    """

    def __init__(self):
        """Initialize enhancer with Gemini"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def quick_enhance(self, raw_prompt: str) -> Enhancement:
        """
        One-shot prompt enhancement using best practices

        Inspired by: CustomGPT's "Improve My Prompt"
        Applies OpenAI's prompt engineering best practices automatically

        Args:
            raw_prompt: Original prompt to enhance

        Returns:
            Enhancement object with improved prompt and explanations
        """
        try:
            prompt = f"""You are an expert prompt engineer. Enhance this prompt using industry best practices.

Original Prompt:
{raw_prompt}

Apply these best practices:
1. **Clarity**: Make instructions crystal clear and unambiguous
2. **Specificity**: Add specific details about desired output
3. **Context**: Provide relevant background information
4. **Structure**: Organize information logically
5. **Constraints**: Add helpful constraints or requirements
6. **Examples**: Include examples when beneficial

Provide your response in this exact format:

ENHANCED PROMPT:
[Your improved version of the prompt]

SCORE_BEFORE: [Rate original 0-100]

SCORE_AFTER: [Rate enhanced 0-100]

CHANGES:
- Change 1: [What changed] | Why: [Explanation]
- Change 2: [What changed] | Why: [Explanation]
- Change 3: [What changed] | Why: [Explanation]

OVERALL EXPLANATION:
[Brief explanation of how these changes improve the prompt]"""

            response = self.model.generate_content(prompt)
            result_text = response.text

            # Parse response
            enhanced_prompt = self._extract_section(result_text, "ENHANCED PROMPT:", "SCORE_BEFORE:")
            score_before = self._extract_score(result_text, "SCORE_BEFORE:")
            score_after = self._extract_score(result_text, "SCORE_AFTER:")
            changes = self._extract_changes(result_text)
            explanation = self._extract_section(result_text, "OVERALL EXPLANATION:", None)

            return Enhancement(
                original=raw_prompt,
                enhanced=enhanced_prompt,
                changes=changes,
                score_before=score_before,
                score_after=score_after,
                explanation=explanation
            )

        except Exception as e:
            # Fallback: simple enhancement
            return Enhancement(
                original=raw_prompt,
                enhanced=f"As an expert, {raw_prompt}. Please provide a detailed response.",
                changes=[{
                    'change': 'Added role and detail request',
                    'why': 'Improves clarity and output quality'
                }],
                score_before=60,
                score_after=75,
                explanation=f"Applied basic enhancements. Error: {str(e)}"
            )

    def start_iterative_refinement(self, raw_prompt: str) -> RefinementStage:
        """
        Start iterative refinement process (Stage 1)

        Inspired by: MaxAI's multi-stage refinement

        Args:
            raw_prompt: Initial prompt to refine

        Returns:
            RefinementStage with analysis and questions
        """
        try:
            prompt = f"""You are an expert prompt engineer. Analyze this prompt and start an iterative refinement process.

Prompt to Analyze:
{raw_prompt}

Provide your analysis in this format:

SCORE: [Rate the prompt 0-100]

STRENGTHS:
- [Strength 1]
- [Strength 2]

WEAKNESSES:
- [Weakness 1]
- [Weakness 2]
- [Weakness 3]

CLARIFYING QUESTIONS:
1. [Question to understand user's needs better]
2. [Question about desired output format]
3. [Question about context or constraints]

SUGGESTIONS:
- [Specific improvement 1]
- [Specific improvement 2]
- [Specific improvement 3]"""

            response = self.model.generate_content(prompt)
            result_text = response.text

            # Parse response
            score = self._extract_score(result_text, "SCORE:")
            strengths = self._extract_list(result_text, "STRENGTHS:", "WEAKNESSES:")
            weaknesses = self._extract_list(result_text, "WEAKNESSES:", "CLARIFYING QUESTIONS:")
            questions = self._extract_numbered_list(result_text, "CLARIFYING QUESTIONS:")
            suggestions = self._extract_list(result_text, "SUGGESTIONS:", None)

            analysis = {
                'score': score,
                'strengths': strengths,
                'weaknesses': weaknesses
            }

            return RefinementStage(
                stage_number=1,
                prompt=raw_prompt,
                analysis=analysis,
                questions=questions,
                suggestions=suggestions,
                score=score
            )

        except Exception as e:
            # Fallback
            return RefinementStage(
                stage_number=1,
                prompt=raw_prompt,
                analysis={'score': 60, 'strengths': [], 'weaknesses': ['Needs improvement']},
                questions=["What is your main goal with this prompt?"],
                suggestions=["Add more context", "Be more specific"],
                score=60
            )

    def refine_with_answers(
        self,
        current_prompt: str,
        questions: List[str],
        answers: List[str],
        stage_number: int
    ) -> RefinementStage:
        """
        Continue refinement with user answers

        Args:
            current_prompt: Current version of prompt
            questions: Questions that were asked
            answers: User's answers to questions
            stage_number: Current stage number

        Returns:
            Next RefinementStage with improved prompt
        """
        try:
            qa_pairs = "\n".join([
                f"Q: {q}\nA: {a}"
                for q, a in zip(questions, answers)
            ])

            prompt = f"""You are an expert prompt engineer. Refine this prompt based on the user's answers.

Current Prompt:
{current_prompt}

User Answers:
{qa_pairs}

Now refine the prompt incorporating the user's feedback. Provide:

REFINED PROMPT:
[Your improved version]

SCORE: [Rate 0-100]

CHANGES MADE:
- [Change 1] | Why: [Explanation]
- [Change 2] | Why: [Explanation]

NEXT QUESTIONS:
1. [Follow-up question if needed, or "None - prompt is ready" if complete]

SUGGESTIONS:
- [Any final suggestions, or "None - prompt is optimal"]"""

            response = self.model.generate_content(prompt)
            result_text = response.text

            # Parse response
            refined_prompt = self._extract_section(result_text, "REFINED PROMPT:", "SCORE:")
            score = self._extract_score(result_text, "SCORE:")
            next_questions = self._extract_numbered_list(result_text, "NEXT QUESTIONS:")
            suggestions = self._extract_list(result_text, "SUGGESTIONS:", None)

            # Check if refinement is complete
            is_complete = (
                "none" in str(next_questions).lower() or
                "ready" in str(next_questions).lower() or
                score >= 90
            )

            return RefinementStage(
                stage_number=stage_number + 1,
                prompt=refined_prompt if refined_prompt else current_prompt,
                analysis={'complete': is_complete},
                questions=[] if is_complete else next_questions,
                suggestions=suggestions,
                score=score
            )

        except Exception as e:
            # Fallback: return current with no questions
            return RefinementStage(
                stage_number=stage_number + 1,
                prompt=current_prompt,
                analysis={'complete': True, 'error': str(e)},
                questions=[],
                suggestions=[],
                score=75
            )

    def explain_improvement(self, original: str, enhanced: str) -> Dict[str, any]:
        """
        Explain how the enhanced prompt is better

        Educational feature to help users learn

        Args:
            original: Original prompt
            enhanced: Enhanced prompt

        Returns:
            Dictionary with detailed explanation
        """
        try:
            prompt = f"""You are a prompt engineering teacher. Explain how the enhanced prompt is better.

Original:
{original}

Enhanced:
{enhanced}

Provide a clear educational explanation:

KEY IMPROVEMENTS:
1. [Improvement 1] - [Why it matters]
2. [Improvement 2] - [Why it matters]
3. [Improvement 3] - [Why it matters]

TECHNIQUES USED:
- [Technique 1]: [Explanation]
- [Technique 2]: [Explanation]

EXPECTED IMPACT:
[How these changes will improve AI responses]

LEARNING TAKEAWAY:
[One key lesson the user can apply to future prompts]"""

            response = self.model.generate_content(prompt)
            result_text = response.text

            improvements = self._extract_numbered_list(result_text, "KEY IMPROVEMENTS:")
            techniques = self._extract_list(result_text, "TECHNIQUES USED:", "EXPECTED IMPACT:")
            impact = self._extract_section(result_text, "EXPECTED IMPACT:", "LEARNING TAKEAWAY:")
            takeaway = self._extract_section(result_text, "LEARNING TAKEAWAY:", None)

            return {
                'improvements': improvements,
                'techniques': techniques,
                'impact': impact,
                'takeaway': takeaway
            }

        except Exception as e:
            return {
                'improvements': ['Enhanced clarity', 'Added structure', 'Improved specificity'],
                'techniques': ['Added role definition', 'Included constraints'],
                'impact': 'These changes should result in more accurate and relevant responses.',
                'takeaway': 'Always be specific and provide context in your prompts.'
            }

    # Helper methods for parsing AI responses

    def _extract_section(self, text: str, start_marker: str, end_marker: Optional[str]) -> str:
        """Extract text between markers"""
        try:
            start_idx = text.find(start_marker)
            if start_idx == -1:
                return ""

            start_idx += len(start_marker)

            if end_marker:
                end_idx = text.find(end_marker, start_idx)
                if end_idx == -1:
                    return text[start_idx:].strip()
                return text[start_idx:end_idx].strip()
            else:
                return text[start_idx:].strip()

        except:
            return ""

    def _extract_score(self, text: str, marker: str) -> int:
        """Extract numerical score"""
        try:
            section = self._extract_section(text, marker, "\n")
            # Extract first number found
            import re
            numbers = re.findall(r'\d+', section)
            if numbers:
                score = int(numbers[0])
                return min(100, max(0, score))
            return 70
        except:
            return 70

    def _extract_list(self, text: str, start_marker: str, end_marker: Optional[str]) -> List[str]:
        """Extract bullet point list"""
        try:
            section = self._extract_section(text, start_marker, end_marker)
            lines = section.split('\n')
            items = []
            for line in lines:
                line = line.strip()
                if line.startswith('-') or line.startswith('•'):
                    items.append(line[1:].strip())
            return items
        except:
            return []

    def _extract_numbered_list(self, text: str, marker: str) -> List[str]:
        """Extract numbered list"""
        try:
            # Find section after marker
            start_idx = text.find(marker)
            if start_idx == -1:
                return []

            start_idx += len(marker)
            remaining_text = text[start_idx:]

            # Extract lines that start with numbers
            lines = remaining_text.split('\n')
            items = []
            import re

            for line in lines:
                line = line.strip()
                # Match patterns like "1.", "1)", "1 -", etc.
                match = re.match(r'^\d+[\.\)\-\:]?\s*(.+)', line)
                if match:
                    items.append(match.group(1).strip())
                elif not line or line[0].isupper():
                    # Stop at empty line or new section
                    if items:  # Only break if we've found some items
                        break

            return items
        except:
            return []

    def _extract_changes(self, text: str) -> List[Dict[str, str]]:
        """Extract changes with explanations"""
        try:
            section = self._extract_section(text, "CHANGES:", "OVERALL EXPLANATION:")
            lines = section.split('\n')
            changes = []

            for line in lines:
                line = line.strip()
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 2:
                        change = parts[0].strip().lstrip('-').strip()
                        why = parts[1].strip().replace('Why:', '').strip()
                        changes.append({'change': change, 'why': why})
                elif line.startswith('-'):
                    changes.append({'change': line[1:].strip(), 'why': 'Improves prompt quality'})

            return changes
        except:
            return []


# Global instance
_enhancer_instance = None


def get_enhancer() -> PromptEnhancer:
    """Get global enhancer instance"""
    global _enhancer_instance
    if _enhancer_instance is None:
        _enhancer_instance = PromptEnhancer()
    return _enhancer_instance
