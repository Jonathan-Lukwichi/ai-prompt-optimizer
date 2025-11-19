"""
Configuration management for AI Prompt Optimizer
Universal Technical & Academic Edition
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
    APP_NAME = os.getenv("APP_NAME", "AI Prompt Optimizer - Universal Edition")
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
            "description": "ML models, data analysis, and AI development"
        },
        "engineering": {
            "name": "Engineering & Design",
            "icon": "⚙️",
            "color": "#10B981",
            "description": "CAD, FEA, design optimization, and validation"
        },
        "industrial": {
            "name": "Industrial Engineering",
            "icon": "🏭",
            "color": "#F59E0B",
            "description": "Process optimization, lean, six sigma, manufacturing"
        },
        "supply_chain": {
            "name": "Supply Chain & Operations",
            "icon": "📦",
            "color": "#EC4899",
            "description": "Logistics, inventory, demand forecasting, network design"
        },
        "web_dev": {
            "name": "Web & Software Development",
            "icon": "💻",
            "color": "#06B6D4",
            "description": "Web design, frontend, backend, full-stack development"
        },
        "python_code": {
            "name": "Python & Programming",
            "icon": "🐍",
            "color": "#EF4444",
            "description": "Python development, debugging, testing, optimization"
        },
        "robotics": {
            "name": "Robotics & Mechatronics",
            "icon": "🤖",
            "color": "#8B5CF6",
            "description": "Control systems, sensors, automation, ROS"
        },
        "timeseries": {
            "name": "Time Series & Forecasting",
            "icon": "📈",
            "color": "#10B981",
            "description": "Forecasting, ARIMA, LSTM, seasonality analysis"
        },
        "process_opt": {
            "name": "Process Optimization",
            "icon": "⚡",
            "color": "#F59E0B",
            "description": "OR, linear programming, optimization algorithms"
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
        "data_analyst": "Data Analyst",
        "software_dev": "Software Developer",
        "web_designer": "Web Designer/Developer",
        "industrial_eng": "Industrial Engineer",
        "process_eng": "Process Engineer",
        "supply_chain_mgr": "Supply Chain Manager",
        "operations_mgr": "Operations Manager",
        "robotics_eng": "Robotics Engineer",
        "mechatronics_eng": "Mechatronics Engineer",
        "design_eng": "Design Engineer",
        "quality_eng": "Quality Engineer",
        "consultant": "Technical Consultant",
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
            "data_pipeline": "Data Pipeline Design"
        },
        "engineering": {
            "cad_design": "CAD/3D Modeling",
            "fea_analysis": "FEA/Simulation",
            "design_opt": "Design Optimization",
            "validation": "Design Validation & Testing",
            "material_select": "Material Selection",
            "dfm_dfa": "DFM/DFA Analysis",
            "tolerance_analysis": "Tolerance Analysis"
        },
        "industrial": {
            "process_opt": "Process Optimization",
            "lean_mfg": "Lean Manufacturing",
            "six_sigma": "Six Sigma Project",
            "capacity_plan": "Capacity Planning",
            "layout_design": "Facility Layout Design",
            "quality_control": "Quality Control System",
            "workflow_design": "Workflow Design"
        },
        "supply_chain": {
            "inventory_opt": "Inventory Optimization",
            "demand_forecast": "Demand Forecasting",
            "network_design": "Network Design",
            "logistics_opt": "Logistics Optimization",
            "supplier_mgmt": "Supplier Management",
            "risk_mgmt": "Risk Management",
            "s_and_op": "S&OP Planning"
        },
        "web_dev": {
            "ui_ux_design": "UI/UX Design",
            "frontend_dev": "Frontend Development",
            "backend_dev": "Backend Development",
            "api_design": "API Design",
            "responsive_design": "Responsive Design",
            "performance_opt": "Performance Optimization",
            "accessibility": "Accessibility (a11y)",
            "seo": "SEO Optimization"
        },
        "python_code": {
            "debugging": "Debugging",
            "refactoring": "Code Refactoring",
            "testing": "Unit Testing",
            "documentation": "Documentation",
            "code_review": "Code Review",
            "performance": "Performance Optimization",
            "architecture": "Software Architecture"
        },
        "robotics": {
            "control_systems": "Control System Design",
            "path_planning": "Path Planning",
            "sensor_fusion": "Sensor Fusion",
            "ros_dev": "ROS Development",
            "kinematics": "Kinematics & Dynamics",
            "vision": "Computer Vision Integration",
            "hardware_int": "Hardware Integration"
        },
        "timeseries": {
            "forecast_setup": "Forecasting Setup",
            "model_select": "Model Selection (ARIMA/LSTM)",
            "seasonality": "Seasonality Analysis",
            "anomaly_detect": "Anomaly Detection",
            "trend_analysis": "Trend Analysis",
            "multivariate": "Multivariate Forecasting"
        },
        "process_opt": {
            "linear_prog": "Linear Programming",
            "integer_prog": "Integer Programming",
            "constraint_opt": "Constraint Optimization",
            "simulation": "Simulation Modeling",
            "heuristics": "Heuristic Algorithms",
            "multi_objective": "Multi-Objective Optimization"
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
        "engineering": {
            "standards": {
                "name": "Standards-Compliant",
                "icon": "📐",
                "description": "Follow engineering codes, safety factors",
                "color": "#3B82F6"
            },
            "validation": {
                "name": "Validation-Focused",
                "icon": "🔍",
                "description": "Emphasize verification, testing",
                "color": "#10B981"
            },
            "innovative": {
                "name": "Innovative",
                "icon": "💡",
                "description": "Explore creative solutions",
                "color": "#8B5CF6"
            },
            "cost_opt": {
                "name": "Cost-Optimized",
                "icon": "💰",
                "description": "Focus on manufacturability, cost reduction",
                "color": "#F59E0B"
            }
        },
        "industrial": {
            "lean": {
                "name": "Lean-Focused",
                "icon": "🎯",
                "description": "Eliminate waste, maximize value",
                "color": "#10B981"
            },
            "quality": {
                "name": "Quality-Driven",
                "icon": "⭐",
                "description": "Six Sigma, defect reduction",
                "color": "#8B5CF6"
            },
            "throughput": {
                "name": "Throughput-Optimized",
                "icon": "⚡",
                "description": "Maximize production rate",
                "color": "#EF4444"
            },
            "safety": {
                "name": "Safety-First",
                "icon": "🛡️",
                "description": "Prioritize worker safety, compliance",
                "color": "#EC4899"
            }
        },
        "supply_chain": {
            "data_driven": {
                "name": "Data-Driven",
                "icon": "📊",
                "description": "Emphasize analytics, KPIs",
                "color": "#3B82F6"
            },
            "risk_aware": {
                "name": "Risk-Aware",
                "icon": "⚠️",
                "description": "Consider disruptions, contingencies",
                "color": "#EF4444"
            },
            "sustainable": {
                "name": "Sustainable",
                "icon": "💚",
                "description": "Green supply chain, ESG focus",
                "color": "#10B981"
            },
            "cost_effective": {
                "name": "Cost-Effective",
                "icon": "💵",
                "description": "Minimize total cost of ownership",
                "color": "#F59E0B"
            }
        },
        "web_dev": {
            "modern": {
                "name": "Modern Stack",
                "icon": "✨",
                "description": "Latest frameworks, best practices",
                "color": "#8B5CF6"
            },
            "accessible": {
                "name": "Accessible",
                "icon": "♿",
                "description": "WCAG compliance, a11y first",
                "color": "#10B981"
            },
            "performant": {
                "name": "Performant",
                "icon": "⚡",
                "description": "Optimize load time, Core Web Vitals",
                "color": "#EF4444"
            },
            "responsive": {
                "name": "Responsive",
                "icon": "📱",
                "description": "Mobile-first, cross-device",
                "color": "#06B6D4"
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
        },
        "robotics": {
            "realtime": {
                "name": "Real-Time",
                "icon": "⏱️",
                "description": "Low latency, deterministic",
                "color": "#EF4444"
            },
            "robust": {
                "name": "Robust",
                "icon": "🛡️",
                "description": "Fault tolerance, error recovery",
                "color": "#10B981"
            },
            "modular": {
                "name": "Modular",
                "icon": "🧩",
                "description": "ROS nodes, reusable components",
                "color": "#8B5CF6"
            },
            "safety": {
                "name": "Safety-Critical",
                "icon": "🚨",
                "description": "Failsafe mechanisms, validation",
                "color": "#EC4899"
            }
        },
        "timeseries": {
            "accurate": {
                "name": "Accuracy-Focused",
                "icon": "🎯",
                "description": "Minimize forecast error, validation",
                "color": "#10B981"
            },
            "interpretable": {
                "name": "Interpretable",
                "icon": "📊",
                "description": "Explainable models, clear insights",
                "color": "#3B82F6"
            },
            "robust": {
                "name": "Robust",
                "icon": "🛡️",
                "description": "Handle outliers, missing data",
                "color": "#8B5CF6"
            },
            "automated": {
                "name": "Automated",
                "icon": "🤖",
                "description": "Auto-tuning, continuous retraining",
                "color": "#F59E0B"
            }
        },
        "process_opt": {
            "optimal": {
                "name": "Globally Optimal",
                "icon": "🎯",
                "description": "Exact methods, proven optimality",
                "color": "#10B981"
            },
            "fast": {
                "name": "Fast & Scalable",
                "icon": "⚡",
                "description": "Heuristics, near-optimal solutions",
                "color": "#EF4444"
            },
            "practical": {
                "name": "Practical",
                "icon": "🔧",
                "description": "Implementable, real-world constraints",
                "color": "#3B82F6"
            },
            "robust": {
                "name": "Robust",
                "icon": "🛡️",
                "description": "Uncertainty handling, sensitivity",
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
