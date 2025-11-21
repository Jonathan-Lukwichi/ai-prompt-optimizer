"""
Core Prompt Engineering Engine
The brain of the AI Prompt Optimizer
Universal Technical & Academic Edition - Supporting 10 Domains
"""
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import openai
import google.generativeai as genai
from .config import Config


@dataclass
class PromptAnalysis:
    """Analysis results for a prompt"""
    intent: str
    risks: List[str]
    missing_info: List[str]
    clarity_score: int  # 0-100
    safety_score: int   # 0-100
    suggestions: List[str]
    domain: str = "academic"  # New: track which domain this is for


class OptimizedPromptSet:
    """
    Set of optimized prompt versions - now domain-aware!
    Dynamically generates versions based on domain
    """

    def __init__(self, domain: str, versions: Dict[str, str], analysis: PromptAnalysis):
        """
        Initialize with domain-specific versions

        Args:
            domain: The domain (academic, ml_ds, python_code, etc.)
            versions: Dict mapping version label to optimized prompt
            analysis: PromptAnalysis object
        """
        self.domain = domain
        self.versions = versions
        self.analysis = analysis

        # For backward compatibility with academic mode
        if domain == "academic":
            self.basic = versions.get("basic", "")
            self.critical_thinking = versions.get("critical", "")
            self.tutor = versions.get("tutor", "")
            self.safe = versions.get("safe", "")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "domain": self.domain,
            "versions": self.versions,
            "analysis": asdict(self.analysis)
        }

    def get_version(self, label: str) -> str:
        """Get a specific version by label"""
        return self.versions.get(label, "")


class PromptEngine:
    """
    Universal Prompt Engineering Engine
    Supports 10 technical & academic domains with domain-specific optimization
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o", provider: Optional[str] = None):
        """
        Initialize the prompt engine

        Args:
            api_key: API key (uses Config based on provider if not provided)
            model: Model to use for optimization
            provider: LLM provider ('openai', 'gemini', or 'anthropic') - uses Config.LLM_PROVIDER if not provided
        """
        self.provider = provider or Config.LLM_PROVIDER

        if self.provider == "gemini":
            self.api_key = api_key or Config.GEMINI_API_KEY
            self.model = Config.GEMINI_MODEL
            genai.configure(api_key=self.api_key)
        else:  # Default to OpenAI
            self.api_key = api_key or Config.OPENAI_API_KEY
            self.model = model
            openai.api_key = self.api_key

    def analyze_prompt(
        self,
        raw_prompt: str,
        role: str,
        task_type: str,
        domain: str = "academic",
        field: Optional[str] = None
    ) -> PromptAnalysis:
        """
        Analyze a prompt for quality, risks, and missing information

        Args:
            raw_prompt: The user's original prompt
            role: User role (academic or professional)
            task_type: Type of task
            domain: Domain (academic, ml_ds, python_code, etc.)
            field: Specific field/discipline within domain

        Returns:
            PromptAnalysis object with scores and recommendations
        """
        # Domain-aware heuristic analysis
        risks = self._detect_risks(raw_prompt, role, task_type, domain)
        missing = self._detect_missing_info(raw_prompt, role, task_type, domain, field)
        suggestions = self._generate_suggestions(raw_prompt, role, task_type, domain)

        # Calculate scores
        clarity_score = self._calculate_clarity_score(raw_prompt)
        safety_score = self._calculate_safety_score(raw_prompt, risks)

        # Determine intent
        intent = self._classify_intent(raw_prompt, task_type, domain)

        return PromptAnalysis(
            intent=intent,
            risks=risks,
            missing_info=missing,
            clarity_score=clarity_score,
            safety_score=safety_score,
            suggestions=suggestions,
            domain=domain
        )

    def optimize_prompt(
        self,
        raw_prompt: str,
        analysis: PromptAnalysis,
        role: str,
        task_type: str,
        domain: str = "academic",
        field: Optional[str] = None
    ) -> OptimizedPromptSet:
        """
        Generate domain-specific optimized versions of a prompt

        Args:
            raw_prompt: Original prompt
            analysis: PromptAnalysis from analyze_prompt()
            role: User role
            task_type: Task type
            domain: Domain (academic, ml_ds, python_code, etc.)
            field: Specific field within domain

        Returns:
            OptimizedPromptSet with domain-specific versions
        """
        # Get domain-specific version labels
        version_labels = Config.get_version_labels(domain)

        # Build context
        context = self._build_context(role, task_type, domain, field)

        # Get role name
        all_roles = Config.get_all_roles()
        role_name = all_roles.get(role, role)

        # Get task name
        task_name = Config.TASK_TYPES.get(task_type, task_type)

        # Get domain name
        domain_name = Config.DOMAINS.get(domain, {}).get("name", domain)

        # Build domain-specific system prompt
        system_prompt = self._build_system_prompt(
            domain, domain_name, role_name, task_name, field, analysis, version_labels
        )

        try:
            if self.provider == "gemini":
                # Use Google Gemini API
                model = genai.GenerativeModel(self.model)

                # Combine system prompt and user message for Gemini
                full_prompt = f"""{system_prompt}

Original prompt to optimize:

{raw_prompt}

Please respond with a JSON object containing the optimized versions."""

                response = model.generate_content(
                    full_prompt,
                    generation_config={
                        'temperature': 0.7,
                        'max_output_tokens': 2000,
                    }
                )

                # Extract JSON from response
                response_text = response.text.strip()

                # Remove markdown code blocks if present
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.startswith('```'):
                    response_text = response_text[3:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]

                result = json.loads(response_text.strip())

            else:
                # Use OpenAI API
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Original prompt to optimize:\n\n{raw_prompt}"}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7,
                    max_tokens=2000
                )

                result = json.loads(response.choices[0].message.content)

            # Extract versions dynamically based on domain
            versions = {}
            for label_key in version_labels.keys():
                versions[label_key] = result.get(label_key, "")

            return OptimizedPromptSet(
                domain=domain,
                versions=versions,
                analysis=analysis
            )

        except Exception as e:
            # Fallback to rule-based optimization
            return self._fallback_optimization(raw_prompt, analysis, role, task_type, domain)

    def smart_optimize(self, raw_prompt: str) -> Dict:
        """
        Quick optimization with auto-detection
        Analyzes and optimizes in one shot - perfect for Quick Mode!

        Args:
            raw_prompt: The user's original prompt

        Returns:
            Dictionary with analysis, best version, all versions, and metadata
        """
        # Import here to avoid circular dependency
        from core.smart_analyzer import SmartAnalyzer

        # Step 1: Auto-detect context
        analyzer = SmartAnalyzer()
        detection = analyzer.analyze_prompt(raw_prompt)

        # Step 2: Analyze with detected context
        analysis = self.analyze_prompt(
            raw_prompt=raw_prompt,
            role=detection['role'],
            task_type=detection['task'],
            domain=detection['domain']
        )

        # Step 3: Optimize
        optimized = self.optimize_prompt(
            raw_prompt=raw_prompt,
            analysis=analysis,
            role=detection['role'],
            task_type=detection['task'],
            domain=detection['domain']
        )

        # Step 4: Pick best version automatically
        best_version_key = analyzer.get_best_version_type(detection)
        best_version_text = optimized.versions.get(best_version_key, "")

        # If best version is empty, fallback to first available
        if not best_version_text and optimized.versions:
            best_version_key = list(optimized.versions.keys())[0]
            best_version_text = optimized.versions[best_version_key]

        # Calculate improvement (compare scores)
        original_score = analysis.clarity_score
        # Estimate optimized score (heuristic: typically 15-30 points improvement)
        estimated_improvement = min(30, 100 - original_score)
        optimized_score = min(100, original_score + estimated_improvement)

        return {
            'raw_prompt': raw_prompt,
            'detection': detection,
            'analysis': analysis,
            'optimized': optimized,
            'best_version_key': best_version_key,
            'best_version': best_version_text,
            'improvement': optimized_score - original_score,
            'original_score': original_score,
            'optimized_score': optimized_score,
            'all_versions': optimized.versions
        }

    # ==================== PRIVATE HELPER METHODS ====================

    def _build_system_prompt(
        self,
        domain: str,
        domain_name: str,
        role_name: str,
        task_name: str,
        field: Optional[str],
        analysis: PromptAnalysis,
        version_labels: Dict
    ) -> str:
        """Build domain-specific system prompt for optimization"""

        # Build version descriptions
        version_desc = []
        for label_key, label_data in version_labels.items():
            version_desc.append(
                f'{label_key.upper()}: {label_data["name"]} {label_data["icon"]}\n'
                f'   {label_data["description"]}'
            )

        version_instructions = '\n\n'.join(version_desc)

        # Domain-specific expertise statements
        expertise_map = {
            "academic": "You are an expert prompt engineer specializing in academic research and education.",
            "ml_ds": "You are an expert prompt engineer specializing in machine learning, data science, and AI development.",
            "python_code": "You are an expert prompt engineer specializing in Python programming, software development, and code quality.",
            "timeseries": "You are an expert prompt engineer specializing in time series analysis, forecasting, and temporal data.",
            "engineering": "You are an expert prompt engineer specializing in engineering design, CAD, FEA, and product development.",
            "industrial": "You are an expert prompt engineer specializing in industrial engineering, lean manufacturing, and process optimization.",
            "supply_chain": "You are an expert prompt engineer specializing in supply chain management, logistics, and operations.",
            "web_dev": "You are an expert prompt engineer specializing in web development, UI/UX design, and frontend/backend systems.",
            "robotics": "You are an expert prompt engineer specializing in robotics, mechatronics, control systems, and automation.",
            "process_opt": "You are an expert prompt engineer specializing in optimization, operations research, and mathematical modeling."
        }

        expertise = expertise_map.get(domain, expertise_map["academic"])

        return f"""{expertise}

USER CONTEXT:
- Domain: {domain_name}
- Role: {role_name}
- Task: {task_name}
- Field: {field or 'General'}

ANALYSIS INSIGHTS:
- Intent: {analysis.intent}
- Clarity Score: {analysis.clarity_score}/100
- Safety Score: {analysis.safety_score}/100
- Identified Risks: {', '.join(analysis.risks) if analysis.risks else 'None'}
- Missing Information: {', '.join(analysis.missing_info) if analysis.missing_info else 'None'}

YOUR TASK:
Generate {len(version_labels)} optimized versions of the user's prompt. Each version serves a different purpose:

{version_instructions}

GUIDELINES:
- Maintain professional integrity and best practices for {domain_name}
- Be specific and actionable
- Include relevant constraints (requirements, format, style)
- Address the identified risks and missing information
- Use clear, professional language appropriate for the domain
- For technical domains, include relevant technical specifications and best practices

Return a JSON object with keys: {', '.join(version_labels.keys())}"""

    def _detect_risks(self, prompt: str, role: str, task_type: str, domain: str = "academic") -> List[str]:
        """Detect potential risks in the prompt - domain-aware!"""
        risks = []
        prompt_lower = prompt.lower()

        # Universal risks
        if len(prompt.split()) < 10:
            risks.append("📉 Too vague - lacks sufficient detail and context")

        # Domain-specific risk detection
        if domain == "academic":
            # Hallucination risks
            if any(word in prompt_lower for word in ['citation', 'reference', 'paper', 'study', 'research']):
                if 'specific' not in prompt_lower and 'about' not in prompt_lower:
                    risks.append("⚠️ High risk of hallucinated citations - no specific papers mentioned")

            # Academic integrity risks
            ghostwriting_phrases = ['write my', 'do my', 'complete my', 'finish my']
            if any(phrase in prompt_lower for phrase in ghostwriting_phrases):
                risks.append("🚨 Academic integrity concern - sounds like ghostwriting rather than assistance")

            # Complexity mismatch
            if role in ['undergrad', 'masters'] and any(word in prompt_lower for word in ['complex', 'advanced', 'sophisticated']):
                risks.append("⚡ Complexity mismatch - may receive overly technical responses")

        elif domain == "ml_ds":
            # ML-specific risks
            if 'dataset' in prompt_lower and 'train' in prompt_lower:
                if 'validation' not in prompt_lower and 'test' not in prompt_lower:
                    risks.append("⚠️ No mention of validation/test sets - risk of overfitting")

            if 'model' in prompt_lower or 'algorithm' in prompt_lower:
                if 'bias' not in prompt_lower and 'fair' not in prompt_lower:
                    risks.append("⚖️ No consideration of model bias or fairness")

            if 'feature' in prompt_lower and 'target' in prompt_lower:
                if 'leakage' not in prompt_lower:
                    risks.append("🚨 No mention of data leakage prevention")

            if 'production' in prompt_lower or 'deploy' in prompt_lower:
                if 'monitor' not in prompt_lower and 'drift' not in prompt_lower:
                    risks.append("📊 Production deployment without monitoring/drift detection")

        elif domain == "python_code":
            # Python code risks
            if 'function' in prompt_lower or 'class' in prompt_lower or 'code' in prompt_lower:
                if 'test' not in prompt_lower and 'testing' not in prompt_lower:
                    risks.append("✅ No mention of testing - code quality risk")

                if 'error' not in prompt_lower and 'exception' not in prompt_lower:
                    risks.append("⚠️ No error handling considerations mentioned")

                if 'type' not in prompt_lower and 'typing' not in prompt_lower:
                    risks.append("📝 No type hints mentioned - maintainability risk")

        return risks

    def _detect_missing_info(self, prompt: str, role: str, task_type: str, domain: str, field: Optional[str]) -> List[str]:
        """Detect missing information that would improve the prompt - domain-aware!"""
        missing = []
        prompt_lower = prompt.lower()

        if not field:
            missing.append("Specific field/discipline within domain")

        # Domain-specific missing info detection
        if domain == "academic":
            if task_type in ['lit_review', 'summary'] and 'scope' not in prompt_lower:
                missing.append("Scope or timeframe (e.g., 'last 5 years', '2020-2024')")

            if 'audience' not in prompt_lower and 'level' not in prompt_lower:
                missing.append("Target audience or knowledge level")

            if task_type == 'drafting' and 'length' not in prompt_lower:
                missing.append("Desired length or word count")

            if task_type == 'methods' and 'data' not in prompt_lower:
                missing.append("Data type or research context")

        elif domain == "ml_ds":
            if 'data' not in prompt_lower and 'dataset' not in prompt_lower:
                missing.append("Dataset information (size, type, characteristics)")

            if 'metric' not in prompt_lower and 'accuracy' not in prompt_lower:
                missing.append("Success metrics or evaluation criteria")

            if 'constraint' not in prompt_lower:
                missing.append("Constraints (compute, latency, interpretability)")

            if task_type in ['model_selection', 'model_eval']:
                if 'baseline' not in prompt_lower:
                    missing.append("Baseline model for comparison")

        elif domain == "python_code":
            if 'version' not in prompt_lower and 'python' not in prompt_lower:
                missing.append("Python version and dependency requirements")

            if 'input' not in prompt_lower and 'output' not in prompt_lower:
                missing.append("Expected inputs and outputs")

            if 'edge case' not in prompt_lower and 'error' not in prompt_lower:
                missing.append("Edge cases and error handling requirements")

        return missing

    def _generate_suggestions(self, prompt: str, role: str, task_type: str, domain: str) -> List[str]:
        """Generate improvement suggestions - domain-aware!"""
        suggestions = []

        if len(prompt.split()) < 15:
            suggestions.append("Add more context about your specific goal")

        if '?' not in prompt:
            suggestions.append("Frame as a clear question or explicit request")

        # Domain-specific suggestions
        if domain == "academic":
            if task_type in ['lit_review', 'summary']:
                suggestions.append("Specify key themes or questions you want to explore")

            if role in ['undergrad', 'masters']:
                suggestions.append("Mention your current understanding level")

        elif domain == "ml_ds":
            suggestions.append("Specify your data characteristics (size, features, imbalance)")
            suggestions.append("Mention performance goals and constraints")

        elif domain == "python_code":
            suggestions.append("Describe expected behavior with example inputs/outputs")
            suggestions.append("Mention any specific libraries or patterns to use/avoid")

        return suggestions

    def _calculate_clarity_score(self, prompt: str) -> int:
        """Calculate clarity score (0-100)"""
        score = 50  # Base score

        # Length factor
        word_count = len(prompt.split())
        if 20 <= word_count <= 100:
            score += 20
        elif 10 <= word_count < 20:
            score += 10
        elif word_count > 100:
            score += 10

        # Specificity indicators
        specific_words = ['specific', 'particular', 'focus on', 'in the context of', 'related to']
        if any(word in prompt.lower() for word in specific_words):
            score += 15

        # Question format
        if '?' in prompt:
            score += 10

        # Has constraints
        constraint_words = ['length', 'format', 'style', 'include', 'avoid']
        if any(word in prompt.lower() for word in constraint_words):
            score += 5

        return min(100, max(0, score))

    def _calculate_safety_score(self, prompt: str, risks: List[str]) -> int:
        """Calculate safety score (0-100)"""
        score = 100 - (len(risks) * 15)

        # Bonus for safety-conscious language
        safety_words = ['cite', 'source', 'verify', 'accurate', 'reliable']
        if any(word in prompt.lower() for word in safety_words):
            score += 10

        return min(100, max(0, score))

    def _classify_intent(self, prompt: str, task_type: str, domain: str) -> str:
        """Classify the user's intent - domain-aware!"""
        prompt_lower = prompt.lower()

        # Get task name from config
        task_name = Config.TASK_TYPES.get(task_type, "")

        # If we have a clear task name, use it
        if task_name:
            return task_name

        # Fallback to keyword-based classification
        if 'explain' in prompt_lower or 'understand' in prompt_lower:
            return "Learning/Understanding"
        elif 'write' in prompt_lower or 'draft' in prompt_lower or 'create' in prompt_lower:
            return "Content Generation"
        elif 'analyze' in prompt_lower or 'analysis' in prompt_lower:
            return "Analysis"
        elif 'optimize' in prompt_lower or 'improve' in prompt_lower:
            return "Optimization"
        elif 'debug' in prompt_lower or 'fix' in prompt_lower:
            return "Debugging/Troubleshooting"
        elif 'design' in prompt_lower:
            return "Design"
        elif 'forecast' in prompt_lower or 'predict' in prompt_lower:
            return "Forecasting/Prediction"
        else:
            return f"General {Config.DOMAINS.get(domain, {}).get('name', domain)} Task"

    def _build_context(self, role: str, task_type: str, domain: str, field: Optional[str]) -> str:
        """Build context string for optimization"""
        all_roles = Config.get_all_roles()
        role_name = all_roles.get(role, role)
        task_name = Config.TASK_TYPES.get(task_type, task_type)
        domain_name = Config.DOMAINS.get(domain, {}).get("name", domain)

        context = f"{role_name} working on {task_name} in {domain_name}"
        if field:
            context += f" ({field})"
        return context

    def _fallback_optimization(
        self,
        raw_prompt: str,
        analysis: PromptAnalysis,
        role: str,
        task_type: str,
        domain: str = "academic"
    ) -> OptimizedPromptSet:
        """Fallback optimization using domain-specific templates when API fails"""

        # Get domain-specific version labels
        version_labels = Config.get_version_labels(domain)
        all_roles = Config.get_all_roles()
        role_name = all_roles.get(role, role)
        task_name = Config.TASK_TYPES.get(task_type, task_type)

        # Build domain-specific fallback versions
        versions = {}

        # For academic domain - use original templates
        if domain == "academic":
            versions["basic"] = f"""Please help me with the following task:

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Please provide a clear, well-structured response."""

            versions["critical"] = f"""I need critical analysis on this topic:

{raw_prompt}

Please:
1. Question the underlying assumptions
2. Consider alternative perspectives
3. Identify potential limitations or weaknesses
4. Suggest areas that need further investigation

Be thorough and intellectually rigorous in your analysis."""

            versions["tutor"] = f"""I'm trying to learn about this topic:

{raw_prompt}

Instead of directly giving me the answer, please:
1. Ask me clarifying questions about what I already know
2. Guide me through the reasoning process
3. Help me discover the insights myself
4. Point out where my thinking might be incomplete

Act as a Socratic tutor, not a lecturer."""

            versions["safe"] = f"""Please assist with the following, being careful about accuracy:

{raw_prompt}

Important instructions:
- Clearly state when you're uncertain about something
- Do NOT make up citations, references, or data
- Distinguish clearly between established facts and your interpretations
- If you need more information to give an accurate answer, ask for it
- Acknowledge the limitations of your knowledge

Academic integrity and accuracy are paramount."""

        # For ML/DS domain
        elif domain == "ml_ds":
            versions["production"] = f"""Production-Ready ML Solution:

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Please provide a solution that emphasizes:
- Robust error handling and edge cases
- Monitoring and logging
- Model validation and testing
- Scalability and efficiency
- Production best practices"""

            versions["research"] = f"""Research-Grade ML Approach:

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Please provide a solution that emphasizes:
- Experimental rigor and reproducibility
- Multiple approaches to compare
- Statistical significance testing
- Ablation studies and sensitivity analysis
- Clear documentation of methodology"""

            versions["explainable"] = f"""Explainable ML Solution:

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Please provide a solution that emphasizes:
- Model interpretability (SHAP, LIME, feature importance)
- Explainable predictions
- Feature contribution analysis
- Decision transparency
- Stakeholder-friendly explanations"""

            versions["performance"] = f"""Performance-Optimized ML Solution:

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Please provide a solution that emphasizes:
- Speed and latency optimization
- Memory efficiency
- Scalability to large datasets
- Parallel processing where applicable
- Benchmark comparisons"""

        # For Python domain
        elif domain == "python_code":
            versions["clean"] = f"""Clean Python Code:

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Please provide code that follows:
- PEP 8 style guidelines
- Clear variable and function names
- Comprehensive docstrings
- Type hints
- Modular, maintainable structure"""

            versions["tested"] = f"""Well-Tested Python Code:

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Please provide:
- Production-quality code
- Comprehensive unit tests (pytest)
- Edge case handling
- Test coverage considerations
- Example test cases"""

            versions["performant"] = f"""Performance-Optimized Python Code:

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Please provide code that:
- Optimizes for speed and memory
- Uses efficient algorithms and data structures
- Includes profiling considerations
- Handles large-scale data efficiently
- Documents complexity (Big O)"""

            versions["production"] = f"""Production-Ready Python Code:

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Please provide code with:
- Comprehensive error handling
- Logging and monitoring
- Configuration management
- Input validation
- Clear documentation"""

        # Generic fallback for any other domains
        else:
            for label_key, label_data in version_labels.items():
                versions[label_key] = f"""{label_data['name']} {label_data['icon']}

{raw_prompt}

Context: I am a {role_name} working on {task_name}.

Focus: {label_data['description']}

Please provide a comprehensive solution aligned with this focus."""

        return OptimizedPromptSet(
            domain=domain,
            versions=versions,
            analysis=analysis
        )
