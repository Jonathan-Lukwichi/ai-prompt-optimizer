"""
Configuration management for AI Prompt Optimizer
Academic & Technical Edition
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # App Settings
    APP_NAME = os.getenv("APP_NAME", "AI Prompt Optimizer")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # Database
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATABASE_PATH = BASE_DIR / "data" / "prompts.db"
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

    # LLM Settings
    DEFAULT_MODEL = "gpt-4o"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 2000

    # ==================== DOMAINS ====================

    DOMAINS = {
        "academic": {
            "name": "Academic & Research",
            "icon": "🎓",
            "color": "#8B5CF6",
            "description": "Academic research, teaching, and scholarly work"
        },
        "ml_ds": {
            "name": "Machine Learning & Data Science",
            "icon": "🤖",
            "color": "#3B82F6",
            "description": "ML models, AI projects, data analysis, and analytics"
        },
        "python_code": {
            "name": "Python Development",
            "icon": "🐍",
            "color": "#10B981",
            "description": "Python programming, software development, debugging, testing"
        }
    }

    # ==================== ACADEMIC ROLES ====================

    ACADEMIC_ROLES = {
        "undergrad": "Undergraduate Student",
        "masters": "Master's Student",
        "phd": "PhD Candidate",
        "postdoc": "Postdoctoral Researcher",
        "professor": "Professor/Faculty"
    }

    # ==================== PROFESSIONAL ROLES ====================

    PROFESSIONAL_ROLES = {
        "data_scientist": "Data Scientist",
        "ml_engineer": "ML Engineer",
        "ai_researcher": "AI Researcher",
        "data_analyst": "Data Analyst",
        "data_engineer": "Data Engineer",
        "software_dev": "Software Developer",
        "python_dev": "Python Developer",
        "backend_dev": "Backend Developer",
        "researcher": "R&D Researcher"
    }

    # Combined roles for UI
    @classmethod
    def get_all_roles(cls):
        """Get all roles (academic + professional)"""
        return {**cls.ACADEMIC_ROLES, **cls.PROFESSIONAL_ROLES}

    # ==================== TASK TYPES BY DOMAIN ====================

    TASK_TYPES_BY_DOMAIN = {
        "academic": {
            "lit_review": "Literature Review",
            "summary": "Paper Summary",
            "methods": "Methodology Design",
            "drafting": "Academic Writing",
            "reviewer_reply": "Reviewer Response",
            "teaching": "Teaching Material",
            "grant_writing": "Grant Writing"
        },
        "ml_ds": {
            "model_selection": "Model Selection & Architecture",
            "feature_eng": "Feature Engineering",
            "hyperparameter": "Hyperparameter Tuning",
            "model_deploy": "Model Deployment",
            "mlops": "MLOps & Monitoring",
            "eda": "Exploratory Data Analysis",
            "model_eval": "Model Evaluation & Validation",
            "data_pipeline": "Data Pipeline Design",
            "data_viz": "Data Visualization",
            "ai_research": "AI Research & Development"
        },
        "python_code": {
            "debugging": "Debugging",
            "refactoring": "Code Refactoring",
            "testing": "Unit Testing",
            "documentation": "Documentation",
            "code_review": "Code Review",
            "performance": "Performance Optimization",
            "architecture": "Software Architecture",
            "api_dev": "API Development"
        }
    }

    # Legacy support - all task types combined
    TASK_TYPES = {}
    for domain_tasks in TASK_TYPES_BY_DOMAIN.values():
        TASK_TYPES.update(domain_tasks)

    # ==================== VERSION LABELS BY DOMAIN ====================

    VERSION_LABELS_BY_DOMAIN = {
        "academic": {
            "basic": {
                "name": "Basic",
                "icon": "📝",
                "description": "Clear, structured version for general use",
                "color": "#3B82F6"
            },
            "critical": {
                "name": "Critical Thinking",
                "icon": "🧠",
                "description": "Forces deeper analysis and questioning",
                "color": "#8B5CF6"
            },
            "tutor": {
                "name": "Tutor Mode",
                "icon": "👨‍🏫",
                "description": "Socratic method - teaches rather than tells",
                "color": "#10B981"
            },
            "safe": {
                "name": "Safe Mode",
                "icon": "🛡️",
                "description": "Minimizes hallucinations, emphasizes uncertainty",
                "color": "#EC4899"
            }
        },
        "ml_ds": {
            "production": {
                "name": "Production-Ready",
                "icon": "🚀",
                "description": "Focus on robustness, monitoring, error handling",
                "color": "#10B981"
            },
            "research": {
                "name": "Research-Grade",
                "icon": "🔬",
                "description": "Emphasize experimentation, reproducibility",
                "color": "#8B5CF6"
            },
            "explainable": {
                "name": "Explainable",
                "icon": "💡",
                "description": "Force model interpretability, SHAP values",
                "color": "#F59E0B"
            },
            "performance": {
                "name": "Performance-Optimized",
                "icon": "⚡",
                "description": "Focus on speed, efficiency, scalability",
                "color": "#EF4444"
            }
        },
        "python_code": {
            "clean": {
                "name": "Clean Code",
                "icon": "✨",
                "description": "PEP 8, readable, maintainable",
                "color": "#10B981"
            },
            "tested": {
                "name": "Well-Tested",
                "icon": "✅",
                "description": "TDD, high coverage, robust",
                "color": "#3B82F6"
            },
            "performant": {
                "name": "Performant",
                "icon": "⚡",
                "description": "Optimized for speed, memory",
                "color": "#EF4444"
            },
            "production": {
                "name": "Production-Ready",
                "icon": "🚀",
                "description": "Error handling, logging, monitoring",
                "color": "#8B5CF6"
            }
        }
    }

    # Default version labels (for backward compatibility)
    VERSION_LABELS = VERSION_LABELS_BY_DOMAIN["academic"]

    @classmethod
    def get_version_labels(cls, domain="academic"):
        """Get version labels for a specific domain"""
        return cls.VERSION_LABELS_BY_DOMAIN.get(domain, cls.VERSION_LABELS_BY_DOMAIN["academic"])

    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []

        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            errors.append("No API keys configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file")

        if not cls.DATABASE_PATH.parent.exists():
            cls.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

        return errors

# Validate on import
config_errors = Config.validate()
if config_errors and Config.ENVIRONMENT != "test":
    import warnings
    for error in config_errors:
        warnings.warn(error)
