"""
AI Prompt Agent - The Brain of the Chatbot
Automatically analyzes input, detects domain, selects templates, and generates optimized prompts
Specialized for Research and Programming/Coding
"""
import json
import re
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import google.generativeai as genai
from core.config import Config


class Domain(Enum):
    RESEARCH = "research"
    CODING = "coding"
    DATA_SCIENCE = "data_science"
    GENERAL = "general"


class TaskType(Enum):
    # Research tasks
    LITERATURE_REVIEW = "literature_review"
    PAPER_WRITING = "paper_writing"
    DATA_ANALYSIS = "data_analysis"
    METHODOLOGY = "methodology"
    EXPLANATION = "explanation"

    # Coding tasks
    CODE_GENERATION = "code_generation"
    DEBUGGING = "debugging"
    CODE_REVIEW = "code_review"
    ARCHITECTURE = "architecture"
    DOCUMENTATION = "documentation"
    API_DESIGN = "api_design"

    # General
    GENERAL_QUERY = "general_query"


@dataclass
class AnalysisResult:
    """Result of analyzing user input"""
    domain: Domain
    task_type: TaskType
    complexity: str  # low, medium, high
    key_topics: List[str]
    detected_language: Optional[str]  # For code
    confidence: float
    context_summary: str


@dataclass
class PromptResult:
    """Final optimized prompt result"""
    optimized_prompt: str
    quality_score: int  # 0-100
    domain: str
    task_type: str
    template_used: str
    suggestions: List[str]
    metadata: Dict


class PromptAgent:
    """
    AI Agent that automatically generates optimized prompts
    No user configuration needed - everything is detected automatically
    """

    def __init__(self):
        """Initialize the Prompt Agent with Gemini"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

        # Prompt templates for different scenarios
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load optimized prompt templates"""
        return {
            # Research Templates
            "literature_review": """You are an expert academic researcher specializing in {topic}.

**Task:** {user_request}

**Instructions:**
1. Provide a comprehensive, well-structured response
2. Cite relevant concepts and methodologies (do NOT invent citations)
3. Identify key themes, gaps, and future directions
4. Use academic language appropriate for scholarly work
5. If you're uncertain about specific facts, clearly state your uncertainty

**Context:** {context}

**Format:** Structure your response with clear headings, bullet points where appropriate, and a summary of key findings.""",

            "paper_writing": """You are an expert academic writer with extensive experience in {topic}.

**Task:** {user_request}

**Instructions:**
1. Write in clear, professional academic prose
2. Follow standard academic structure and conventions
3. Support arguments with logical reasoning
4. Maintain objectivity and critical analysis
5. Do NOT fabricate references or data

**Context:** {context}

**Deliverable:** Provide well-structured content that can be directly used or adapted for academic purposes.""",

            "methodology": """You are a research methodology expert specializing in {topic}.

**Task:** {user_request}

**Instructions:**
1. Recommend appropriate research methods
2. Explain the rationale for each recommendation
3. Address potential limitations and how to mitigate them
4. Consider ethical implications
5. Provide practical implementation steps

**Context:** {context}

**Output:** A detailed methodology recommendation with justification.""",

            "data_analysis": """You are a data analysis expert with deep knowledge in {topic}.

**Task:** {user_request}

**Instructions:**
1. Suggest appropriate analytical approaches
2. Explain statistical/analytical methods clearly
3. Address assumptions and limitations
4. Recommend visualization strategies
5. Provide interpretation guidelines

**Context:** {context}

**Deliverable:** Comprehensive data analysis guidance with practical steps.""",

            # Coding Templates
            "code_generation": """You are an expert {language} developer with deep knowledge of best practices and design patterns.

**Task:** {user_request}

**Requirements:**
1. Write clean, efficient, and well-documented code
2. Follow {language} best practices and conventions
3. Include error handling and edge cases
4. Add clear comments explaining complex logic
5. Consider performance and scalability

**Context:** {context}

**Output Format:**
- Complete, runnable code
- Brief explanation of the approach
- Usage examples if applicable""",

            "debugging": """You are an expert debugger and code analyst specializing in {language}.

**Problem:** {user_request}

**Debugging Approach:**
1. Analyze the issue systematically
2. Identify the root cause, not just symptoms
3. Explain why the bug occurs
4. Provide a clear fix with explanation
5. Suggest preventive measures for the future

**Context:** {context}

**Output:**
- Root cause analysis
- Step-by-step fix
- Improved code with explanation""",

            "code_review": """You are a senior software engineer conducting a thorough code review.

**Code/Request:** {user_request}

**Review Criteria:**
1. Code quality and readability
2. Performance and efficiency
3. Security vulnerabilities
4. Best practices adherence
5. Potential bugs or edge cases
6. Suggestions for improvement

**Context:** {context}

**Output:** Detailed code review with specific, actionable feedback.""",

            "architecture": """You are a software architect with expertise in {topic} systems.

**Request:** {user_request}

**Design Considerations:**
1. Scalability and performance
2. Maintainability and modularity
3. Security best practices
4. Technology stack recommendations
5. Trade-offs and alternatives

**Context:** {context}

**Deliverable:**
- Architecture overview
- Component diagram description
- Implementation roadmap
- Key decisions and rationale""",

            "api_design": """You are an API design expert specializing in RESTful and modern API architectures.

**Request:** {user_request}

**Design Principles:**
1. RESTful conventions and best practices
2. Clear and consistent naming
3. Proper HTTP methods and status codes
4. Authentication and authorization
5. Error handling and validation
6. Documentation standards

**Context:** {context}

**Output:**
- API endpoint specifications
- Request/Response schemas
- Authentication flow
- Example usage""",

            "documentation": """You are a technical writer specializing in software documentation.

**Request:** {user_request}

**Documentation Standards:**
1. Clear, concise language
2. Appropriate technical depth
3. Code examples where relevant
4. Proper structure and formatting
5. Consider the target audience

**Context:** {context}

**Output:** Professional documentation ready for use.""",

            # General/Explanation
            "explanation": """You are an expert educator in {topic}.

**Request:** {user_request}

**Teaching Approach:**
1. Start with fundamentals, build to complexity
2. Use clear examples and analogies
3. Address common misconceptions
4. Provide practical applications
5. Encourage deeper exploration

**Context:** {context}

**Output:** Clear, comprehensive explanation suitable for learning.""",

            "general_query": """You are a knowledgeable assistant specializing in {topic}.

**Request:** {user_request}

**Guidelines:**
1. Provide accurate, helpful information
2. Be clear and well-organized
3. Acknowledge limitations in your knowledge
4. Suggest follow-up resources if relevant

**Context:** {context}

**Output:** Comprehensive, helpful response."""
        }

    async def process_input(self,
                           user_input: str,
                           file_content: Optional[str] = None,
                           file_type: Optional[str] = None) -> PromptResult:
        """
        Main entry point - process user input and generate optimized prompt

        Args:
            user_input: Text from user (could be from voice transcription)
            file_content: Optional content extracted from uploaded file
            file_type: Type of file (pdf, image, code, etc.)

        Returns:
            PromptResult with optimized prompt and hidden metrics
        """
        # Combine inputs
        full_context = self._build_context(user_input, file_content, file_type)

        # Step 1: Analyze the input
        analysis = await self._analyze_input(full_context)

        # Step 2: Select best template
        template_key = self._select_template(analysis)

        # Step 3: Generate optimized prompt
        optimized_prompt = self._generate_prompt(analysis, template_key, user_input, full_context)

        # Step 4: Score the prompt (hidden from user by default)
        quality_score, suggestions = await self._evaluate_prompt(optimized_prompt, analysis)

        return PromptResult(
            optimized_prompt=optimized_prompt,
            quality_score=quality_score,
            domain=analysis.domain.value,
            task_type=analysis.task_type.value,
            template_used=template_key,
            suggestions=suggestions,
            metadata={
                "complexity": analysis.complexity,
                "confidence": analysis.confidence,
                "key_topics": analysis.key_topics,
                "detected_language": analysis.detected_language
            }
        )

    def process_input_sync(self,
                          user_input: str,
                          file_content: Optional[str] = None,
                          file_type: Optional[str] = None) -> PromptResult:
        """Synchronous version of process_input for Streamlit compatibility"""
        # Combine inputs
        full_context = self._build_context(user_input, file_content, file_type)

        # Step 1: Analyze the input
        analysis = self._analyze_input_sync(full_context)

        # Step 2: Select best template
        template_key = self._select_template(analysis)

        # Step 3: Generate optimized prompt
        optimized_prompt = self._generate_prompt(analysis, template_key, user_input, full_context)

        # Step 4: Score the prompt (hidden from user by default)
        quality_score, suggestions = self._evaluate_prompt_sync(optimized_prompt, analysis)

        return PromptResult(
            optimized_prompt=optimized_prompt,
            quality_score=quality_score,
            domain=analysis.domain.value,
            task_type=analysis.task_type.value,
            template_used=template_key,
            suggestions=suggestions,
            metadata={
                "complexity": analysis.complexity,
                "confidence": analysis.confidence,
                "key_topics": analysis.key_topics,
                "detected_language": analysis.detected_language
            }
        )

    def _build_context(self, user_input: str, file_content: Optional[str], file_type: Optional[str]) -> str:
        """Build full context from all inputs"""
        context_parts = [user_input]

        if file_content:
            if file_type == "code":
                context_parts.append(f"\n\n[Attached Code]:\n```\n{file_content}\n```")
            elif file_type == "document":
                context_parts.append(f"\n\n[Document Content]:\n{file_content}")
            elif file_type == "image":
                context_parts.append(f"\n\n[Image Analysis]:\n{file_content}")
            else:
                context_parts.append(f"\n\n[Additional Content]:\n{file_content}")

        return "\n".join(context_parts)

    def _analyze_input_sync(self, full_context: str) -> AnalysisResult:
        """Analyze user input to detect domain, task type, and complexity"""

        analysis_prompt = f"""Analyze this user request and return ONLY valid JSON (no markdown, no explanation).

User Request: "{full_context[:2000]}"

Analyze and determine:
1. domain: "research", "coding", "data_science", or "general"
2. task_type: One of:
   - Research: "literature_review", "paper_writing", "data_analysis", "methodology", "explanation"
   - Coding: "code_generation", "debugging", "code_review", "architecture", "api_design", "documentation"
   - General: "general_query"
3. complexity: "low", "medium", or "high"
4. key_topics: Array of 2-4 main topics/keywords
5. detected_language: Programming language if coding (null otherwise)
6. confidence: 0.0-1.0 how confident you are
7. context_summary: One sentence summary of what user wants

Return ONLY this JSON:
{{"domain": "...", "task_type": "...", "complexity": "...", "key_topics": [...], "detected_language": null, "confidence": 0.9, "context_summary": "..."}}"""

        try:
            response = self.model.generate_content(analysis_prompt)
            response_text = response.text.strip()

            # Clean response
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                json_lines = [l for l in lines if l and not l.startswith('```')]
                response_text = '\n'.join(json_lines)

            data = json.loads(response_text)

            return AnalysisResult(
                domain=Domain(data.get("domain", "general")),
                task_type=TaskType(data.get("task_type", "general_query")),
                complexity=data.get("complexity", "medium"),
                key_topics=data.get("key_topics", []),
                detected_language=data.get("detected_language"),
                confidence=data.get("confidence", 0.8),
                context_summary=data.get("context_summary", "")
            )
        except Exception as e:
            # Fallback to keyword-based detection
            return self._fallback_analysis(full_context)

    async def _analyze_input(self, full_context: str) -> AnalysisResult:
        """Async version of analysis"""
        return self._analyze_input_sync(full_context)

    def _fallback_analysis(self, text: str) -> AnalysisResult:
        """Fallback keyword-based analysis when AI fails"""
        text_lower = text.lower()

        # Detect domain
        coding_keywords = ['code', 'python', 'javascript', 'function', 'class', 'api', 'debug',
                          'error', 'bug', 'programming', 'develop', 'build', 'implement',
                          'java', 'rust', 'go', 'typescript', 'react', 'sql', 'database']
        research_keywords = ['research', 'paper', 'study', 'literature', 'methodology',
                           'hypothesis', 'analysis', 'academic', 'thesis', 'dissertation']
        data_keywords = ['data', 'dataset', 'machine learning', 'ml', 'ai', 'model',
                        'training', 'neural', 'statistics', 'visualization']

        coding_score = sum(1 for k in coding_keywords if k in text_lower)
        research_score = sum(1 for k in research_keywords if k in text_lower)
        data_score = sum(1 for k in data_keywords if k in text_lower)

        if coding_score > research_score and coding_score > data_score:
            domain = Domain.CODING
            task_type = TaskType.CODE_GENERATION
        elif research_score > coding_score:
            domain = Domain.RESEARCH
            task_type = TaskType.EXPLANATION
        elif data_score > 0:
            domain = Domain.DATA_SCIENCE
            task_type = TaskType.DATA_ANALYSIS
        else:
            domain = Domain.GENERAL
            task_type = TaskType.GENERAL_QUERY

        # Detect programming language
        languages = {
            'python': ['python', '.py', 'pip', 'pandas', 'numpy'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue'],
            'typescript': ['typescript', 'ts', 'angular'],
            'java': ['java', 'spring', 'maven'],
            'rust': ['rust', 'cargo'],
            'go': ['golang', ' go '],
            'sql': ['sql', 'query', 'database', 'select', 'insert']
        }

        detected_lang = None
        for lang, keywords in languages.items():
            if any(k in text_lower for k in keywords):
                detected_lang = lang
                break

        return AnalysisResult(
            domain=domain,
            task_type=task_type,
            complexity="medium",
            key_topics=[],
            detected_language=detected_lang,
            confidence=0.6,
            context_summary="User request"
        )

    def _select_template(self, analysis: AnalysisResult) -> str:
        """Select the best template based on analysis"""
        task_to_template = {
            TaskType.LITERATURE_REVIEW: "literature_review",
            TaskType.PAPER_WRITING: "paper_writing",
            TaskType.DATA_ANALYSIS: "data_analysis",
            TaskType.METHODOLOGY: "methodology",
            TaskType.EXPLANATION: "explanation",
            TaskType.CODE_GENERATION: "code_generation",
            TaskType.DEBUGGING: "debugging",
            TaskType.CODE_REVIEW: "code_review",
            TaskType.ARCHITECTURE: "architecture",
            TaskType.API_DESIGN: "api_design",
            TaskType.DOCUMENTATION: "documentation",
            TaskType.GENERAL_QUERY: "general_query"
        }

        return task_to_template.get(analysis.task_type, "general_query")

    def _generate_prompt(self, analysis: AnalysisResult, template_key: str,
                        user_input: str, full_context: str) -> str:
        """Generate the optimized prompt using selected template"""
        template = self.templates.get(template_key, self.templates["general_query"])

        # Determine topic
        topic = ", ".join(analysis.key_topics) if analysis.key_topics else "the requested subject"

        # Determine language for coding
        language = analysis.detected_language or "the appropriate programming language"

        # Build the optimized prompt
        optimized = template.format(
            topic=topic,
            language=language,
            user_request=user_input,
            context=analysis.context_summary or "No additional context provided."
        )

        return optimized

    def _evaluate_prompt_sync(self, prompt: str, analysis: AnalysisResult) -> Tuple[int, List[str]]:
        """Evaluate prompt quality and generate suggestions"""

        eval_prompt = f"""Rate this prompt on a scale of 0-100 and provide 2-3 brief improvement suggestions.

Prompt to evaluate:
"{prompt[:1500]}"

Evaluation criteria:
1. Clarity (is the request clear?)
2. Specificity (is it specific enough?)
3. Structure (is it well-organized?)
4. Completeness (does it have all needed info?)
5. Professional tone

Return ONLY this JSON:
{{"score": 85, "suggestions": ["suggestion 1", "suggestion 2"]}}"""

        try:
            response = self.model.generate_content(eval_prompt)
            response_text = response.text.strip()

            # Clean response
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                json_lines = [l for l in lines if l and not l.startswith('```')]
                response_text = '\n'.join(json_lines)

            data = json.loads(response_text)
            score = min(100, max(0, int(data.get("score", 75))))
            suggestions = data.get("suggestions", [])

            return score, suggestions
        except Exception:
            # Fallback scoring based on heuristics
            score = 75
            suggestions = []

            if len(prompt) > 500:
                score += 10
            if "instructions" in prompt.lower():
                score += 5
            if analysis.confidence > 0.8:
                score += 5

            return min(100, score), suggestions

    async def _evaluate_prompt(self, prompt: str, analysis: AnalysisResult) -> Tuple[int, List[str]]:
        """Async version of evaluation"""
        return self._evaluate_prompt_sync(prompt, analysis)
