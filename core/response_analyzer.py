"""
Response Quality Analyzer
Analyzes and scores AI responses to prove optimized prompts work better
"""
from dataclasses import dataclass
from typing import List


@dataclass
class ResponseQuality:
    """Quality metrics for an AI response"""
    completeness_score: int  # 0-100
    clarity_score: int  # 0-100
    specificity_score: int  # 0-100
    actionability_score: int  # 0-100
    overall_score: int  # 0-100
    strengths: List[str]
    weaknesses: List[str]


class ResponseAnalyzer:
    """Analyzes AI responses to compare quality"""

    @staticmethod
    def analyze_response(response_text: str, prompt: str) -> ResponseQuality:
        """
        Analyze the quality of an AI response

        Args:
            response_text: The AI's response
            prompt: The prompt that generated this response

        Returns:
            ResponseQuality with scores and analysis
        """
        # Calculate individual scores
        completeness = ResponseAnalyzer._calculate_completeness(response_text, prompt)
        clarity = ResponseAnalyzer._calculate_clarity(response_text)
        specificity = ResponseAnalyzer._calculate_specificity(response_text)
        actionability = ResponseAnalyzer._calculate_actionability(response_text)

        # Overall score (weighted average)
        overall = int(
            completeness * 0.3 +
            clarity * 0.25 +
            specificity * 0.25 +
            actionability * 0.2
        )

        # Identify strengths and weaknesses
        strengths, weaknesses = ResponseAnalyzer._identify_qualities(
            response_text, completeness, clarity, specificity, actionability
        )

        return ResponseQuality(
            completeness_score=completeness,
            clarity_score=clarity,
            specificity_score=specificity,
            actionability_score=actionability,
            overall_score=overall,
            strengths=strengths,
            weaknesses=weaknesses
        )

    @staticmethod
    def _calculate_completeness(response: str, prompt: str) -> int:
        """Calculate how complete/thorough the response is"""
        score = 50  # Base score

        # Length indicates thoroughness (within reason)
        word_count = len(response.split())
        if 100 <= word_count <= 500:
            score += 25
        elif 50 <= word_count < 100:
            score += 15
        elif word_count > 500:
            score += 20

        # Structure indicators
        if any(marker in response.lower() for marker in ['1.', '2.', '3.', '-', '•']):
            score += 10  # Has structured points

        # Multiple paragraphs indicate depth
        paragraphs = response.count('\n\n') + 1
        if paragraphs >= 3:
            score += 10
        elif paragraphs >= 2:
            score += 5

        # Examples/evidence
        example_indicators = ['for example', 'such as', 'for instance', 'e.g.', 'specifically']
        if any(indicator in response.lower() for indicator in example_indicators):
            score += 5

        return min(100, score)

    @staticmethod
    def _calculate_clarity(response: str) -> int:
        """Calculate how clear and readable the response is"""
        score = 50  # Base score

        words = response.split()
        word_count = len(words)

        if word_count == 0:
            return 0

        # Average sentence length (not too long, not too short)
        sentences = response.count('.') + response.count('!') + response.count('?')
        if sentences > 0:
            avg_words_per_sentence = word_count / sentences
            if 15 <= avg_words_per_sentence <= 25:
                score += 15  # Good range
            elif 10 <= avg_words_per_sentence < 15 or 25 < avg_words_per_sentence <= 30:
                score += 10  # Acceptable

        # Clear structure
        if response.count('\n') >= 2:
            score += 10  # Has paragraph breaks

        # Transition words indicate clear flow
        transitions = ['however', 'therefore', 'additionally', 'furthermore', 'moreover', 'first', 'second', 'finally']
        if any(word in response.lower() for word in transitions):
            score += 10

        # Avoiding jargon/complex words (simplified check)
        avg_word_length = sum(len(word) for word in words) / word_count
        if avg_word_length <= 6:
            score += 15  # Clear, simple language
        elif avg_word_length <= 8:
            score += 10

        return min(100, score)

    @staticmethod
    def _calculate_specificity(response: str) -> int:
        """Calculate how specific and detailed the response is"""
        score = 50  # Base score

        response_lower = response.lower()

        # Numbers indicate specificity
        import re
        numbers = re.findall(r'\d+', response)
        if len(numbers) >= 5:
            score += 15
        elif len(numbers) >= 3:
            score += 10
        elif len(numbers) >= 1:
            score += 5

        # Technical/specific terms
        specific_indicators = ['specifically', 'precisely', 'exactly', 'particular', 'detailed']
        if any(word in response_lower for word in specific_indicators):
            score += 10

        # Citations/references
        citation_markers = ['according to', 'research shows', 'studies indicate', 'source:', 'reference']
        if any(marker in response_lower for marker in citation_markers):
            score += 10

        # Examples and illustrations
        if 'example' in response_lower or 'instance' in response_lower:
            score += 10

        # Avoiding vague language
        vague_words = ['maybe', 'perhaps', 'might', 'could', 'possibly', 'generally']
        vague_count = sum(1 for word in vague_words if word in response_lower)
        if vague_count == 0:
            score += 5
        elif vague_count <= 2:
            score += 2

        return min(100, score)

    @staticmethod
    def _calculate_actionability(response: str) -> int:
        """Calculate how actionable/useful the response is"""
        score = 50  # Base score

        response_lower = response.lower()

        # Action verbs
        action_verbs = ['use', 'apply', 'implement', 'create', 'develop', 'follow', 'try', 'start', 'begin', 'practice']
        action_count = sum(1 for verb in action_verbs if verb in response_lower)
        score += min(action_count * 3, 15)

        # Step-by-step instructions
        step_markers = ['step 1', 'step 2', 'first,', 'second,', 'next,', 'then,', 'finally']
        if any(marker in response_lower for marker in step_markers):
            score += 15

        # Practical examples
        if 'example:' in response_lower or 'for instance:' in response_lower:
            score += 10

        # Recommendations/suggestions
        recommendation_words = ['recommend', 'suggest', 'should', 'consider', 'try']
        if any(word in response_lower for word in recommendation_words):
            score += 10

        return min(100, score)

    @staticmethod
    def _identify_qualities(response: str, completeness: int, clarity: int, specificity: int, actionability: int) -> tuple:
        """Identify strengths and weaknesses"""
        strengths = []
        weaknesses = []

        # Completeness
        if completeness >= 80:
            strengths.append("✓ Comprehensive and thorough coverage")
        elif completeness < 50:
            weaknesses.append("✗ Lacks depth and completeness")

        # Clarity
        if clarity >= 80:
            strengths.append("✓ Clear and easy to understand")
        elif clarity < 50:
            weaknesses.append("✗ Could be clearer and more concise")

        # Specificity
        if specificity >= 80:
            strengths.append("✓ Specific and detailed information")
        elif specificity < 50:
            weaknesses.append("✗ Too vague or general")

        # Actionability
        if actionability >= 80:
            strengths.append("✓ Practical and actionable advice")
        elif actionability < 50:
            weaknesses.append("✗ Lacks practical next steps")

        # Content analysis
        if len(response) > 300:
            if '\n\n' in response or '\n' in response:
                strengths.append("✓ Well-structured with clear sections")

        if any(marker in response for marker in ['1.', '2.', '3.']):
            strengths.append("✓ Organized with numbered points")

        # If no weaknesses found, add positive note
        if not weaknesses:
            weaknesses.append("Minor improvements could enhance readability")

        return strengths, weaknesses

    @staticmethod
    def compare_responses(original_response: ResponseQuality, optimized_response: ResponseQuality) -> dict:
        """
        Compare two responses and show improvement

        Returns:
            Dictionary with comparison metrics
        """
        return {
            'completeness_improvement': optimized_response.completeness_score - original_response.completeness_score,
            'clarity_improvement': optimized_response.clarity_score - original_response.clarity_score,
            'specificity_improvement': optimized_response.specificity_score - original_response.specificity_score,
            'actionability_improvement': optimized_response.actionability_score - original_response.actionability_score,
            'overall_improvement': optimized_response.overall_score - original_response.overall_score,
            'winner': 'optimized' if optimized_response.overall_score > original_response.overall_score else 'original'
        }
