"""
Database models and operations for AI Prompt Optimizer
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
from typing import List, Optional, Dict
from contextlib import contextmanager
from .config import Config

# Create engine and base
engine = create_engine(Config.DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


# ==================== MODELS ====================

class User(Base):
    """User model for authentication and personalization"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    role = Column(String(32))  # Academic role
    field = Column(String(100))  # Academic field
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sessions = relationship("PromptSession", back_populates="user", cascade="all, delete-orphan")
    templates = relationship("PromptTemplate", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"


class PromptTemplate(Base):
    """Reusable prompt templates"""
    __tablename__ = 'prompt_templates'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    role = Column(String(32))  # Target academic role
    task_type = Column(String(32))  # Type of task
    field = Column(String(100))  # Academic field
    base_prompt = Column(Text, nullable=False)
    tags = Column(JSON)  # List of tags for search
    is_public = Column(Boolean, default=False)
    uses_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="templates")

    def __repr__(self):
        return f"<PromptTemplate(name='{self.name}', task='{self.task_type}')>"


class PromptSession(Base):
    """A prompt optimization session"""
    __tablename__ = 'prompt_sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    role = Column(String(32), nullable=False)
    task_type = Column(String(32), nullable=False)
    field = Column(String(100))
    raw_prompt = Column(Text, nullable=False)

    # Analysis results
    intent = Column(String(100))
    clarity_score = Column(Integer)
    safety_score = Column(Integer)
    risks = Column(JSON)  # List of risks
    missing_info = Column(JSON)  # List of missing information
    suggestions = Column(JSON)  # List of suggestions

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="sessions")
    versions = relationship("PromptVersion", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PromptSession(id={self.id}, task='{self.task_type}', created='{self.created_at}')>"


class PromptVersion(Base):
    """Optimized version of a prompt"""
    __tablename__ = 'prompt_versions'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('prompt_sessions.id'), nullable=False)
    label = Column(String(64), nullable=False)  # basic, critical_thinking, tutor, safe
    optimized_prompt = Column(Text, nullable=False)
    was_copied = Column(Boolean, default=False)
    was_rated = Column(Boolean, default=False)
    rating = Column(Integer)  # 1-5 stars
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("PromptSession", back_populates="versions")

    def __repr__(self):
        return f"<PromptVersion(label='{self.label}', session_id={self.session_id})>"


class Workflow(Base):
    """Multi-step academic workflow"""
    __tablename__ = 'workflows'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    workflow_type = Column(String(64))  # lit_review, paper_writing, etc.
    role = Column(String(32))
    field = Column(String(100))
    steps = Column(JSON)  # List of workflow steps
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Workflow(name='{self.name}', type='{self.workflow_type}')>"


# ==================== DATABASE OPERATIONS ====================

class DatabaseManager:
    """Manages database operations"""

    @staticmethod
    @contextmanager
    def get_session() -> Session:
        """Context manager for database sessions"""
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def init_db():
        """Initialize database tables"""
        Base.metadata.create_all(engine)

    @staticmethod
    def create_user(username: str, email: Optional[str] = None, role: Optional[str] = None, field: Optional[str] = None) -> User:
        """Create a new user"""
        with DatabaseManager.get_session() as session:
            user = User(username=username, email=email, role=role, field=field)
            session.add(user)
            session.flush()
            return user

    @staticmethod
    def get_user(username: str) -> Optional[User]:
        """Get user by username"""
        with DatabaseManager.get_session() as session:
            return session.query(User).filter_by(username=username).first()

    @staticmethod
    def create_session(
        user_id: Optional[int],
        role: str,
        task_type: str,
        raw_prompt: str,
        field: Optional[str] = None,
        analysis: Optional[Dict] = None
    ) -> PromptSession:
        """Create a prompt session"""
        with DatabaseManager.get_session() as session:
            prompt_session = PromptSession(
                user_id=user_id,
                role=role,
                task_type=task_type,
                field=field,
                raw_prompt=raw_prompt,
                intent=analysis.get('intent') if analysis else None,
                clarity_score=analysis.get('clarity_score') if analysis else None,
                safety_score=analysis.get('safety_score') if analysis else None,
                risks=analysis.get('risks') if analysis else None,
                missing_info=analysis.get('missing_info') if analysis else None,
                suggestions=analysis.get('suggestions') if analysis else None
            )
            session.add(prompt_session)
            session.flush()
            return prompt_session

    @staticmethod
    def create_version(session_id: int, label: str, optimized_prompt: str) -> PromptVersion:
        """Create a prompt version"""
        with DatabaseManager.get_session() as session:
            version = PromptVersion(
                session_id=session_id,
                label=label,
                optimized_prompt=optimized_prompt
            )
            session.add(version)
            session.flush()
            return version

    @staticmethod
    def get_user_sessions(user_id: int, limit: int = 10) -> List[PromptSession]:
        """Get recent sessions for a user"""
        with DatabaseManager.get_session() as session:
            return session.query(PromptSession)\
                .filter_by(user_id=user_id)\
                .order_by(PromptSession.created_at.desc())\
                .limit(limit)\
                .all()

    @staticmethod
    def get_templates(role: Optional[str] = None, task_type: Optional[str] = None, is_public: bool = True) -> List[PromptTemplate]:
        """Get templates with optional filtering"""
        with DatabaseManager.get_session() as session:
            query = session.query(PromptTemplate).filter_by(is_public=is_public)

            if role:
                query = query.filter_by(role=role)
            if task_type:
                query = query.filter_by(task_type=task_type)

            templates = query.order_by(PromptTemplate.uses_count.desc()).all()

            # Expunge objects from session so they can be used after session closes
            for template in templates:
                session.expunge(template)

            return templates

    @staticmethod
    def create_template(
        name: str,
        description: str,
        role: str,
        task_type: str,
        base_prompt: str,
        field: Optional[str] = None,
        owner_id: Optional[int] = None,
        is_public: bool = True,
        tags: Optional[List[str]] = None
    ) -> PromptTemplate:
        """Create a prompt template"""
        with DatabaseManager.get_session() as session:
            template = PromptTemplate(
                name=name,
                description=description,
                role=role,
                task_type=task_type,
                field=field,
                base_prompt=base_prompt,
                owner_id=owner_id,
                is_public=is_public,
                tags=tags or []
            )
            session.add(template)
            session.flush()
            return template

    @staticmethod
    def get_workflows(workflow_type: Optional[str] = None) -> List[Workflow]:
        """Get workflows"""
        with DatabaseManager.get_session() as session:
            query = session.query(Workflow).filter_by(is_public=True)

            if workflow_type:
                query = query.filter_by(workflow_type=workflow_type)

            return query.all()


# Initialize database on import
DatabaseManager.init_db()


# ==================== SEED DATA ====================

def seed_templates():
    """Seed initial templates for 4 priority domains"""
    templates = [
        # ==================== ACADEMIC & RESEARCH ====================
        {
            "name": "Literature Review Starter",
            "description": "Comprehensive template for beginning a literature review",
            "role": "phd",
            "task_type": "lit_review",
            "field": "Computer Science",
            "base_prompt": """I need to conduct a literature review on [TOPIC] in the field of [FIELD].

Please help me:
1. Identify key research questions and themes
2. Suggest search strategies and keywords
3. Outline a framework for organizing the findings
4. Highlight recent influential papers (last 5 years)

Context: I am a [ROLE] with [BACKGROUND KNOWLEDGE LEVEL] in this area.
Target audience: [AUDIENCE]
Scope: [TIME PERIOD / GEOGRAPHIC / THEMATIC SCOPE]""",
            "tags": ["literature review", "research", "academic"]
        },
        {
            "name": "Paper Summary Template",
            "description": "Structured template for summarizing academic papers",
            "role": "masters",
            "task_type": "summary",
            "field": "General",
            "base_prompt": """Please provide a structured summary of the paper: [PAPER TITLE/DOI]

Include:
1. Main research question and objectives
2. Methodology used
3. Key findings and results
4. Implications and contributions
5. Limitations acknowledged by authors
6. Potential areas for future research

Target length: [WORD COUNT]
Audience: [AUDIENCE LEVEL]""",
            "tags": ["summary", "paper", "analysis"]
        },
        {
            "name": "Reviewer Response Helper",
            "description": "Template for responding to peer reviewer comments",
            "role": "postdoc",
            "task_type": "reviewer_reply",
            "field": "General",
            "base_prompt": """I received the following reviewer comment:

[PASTE REVIEWER COMMENT]

My current response approach: [YOUR INITIAL THOUGHTS]

Please help me:
1. Understand what the reviewer is truly asking for
2. Craft a professional, respectful response
3. Identify what changes (if any) are needed in the manuscript
4. Ensure I address all parts of the comment

Context: [PAPER TOPIC], [JOURNAL/CONFERENCE]""",
            "tags": ["peer review", "response", "publishing"]
        },

        # ==================== MACHINE LEARNING & DATA SCIENCE ====================
        {
            "name": "ML Model Selection Guide",
            "description": "Comprehensive template for selecting the right ML model",
            "role": "ml_engineer",
            "task_type": "model_selection",
            "field": "Machine Learning",
            "base_prompt": """I need to select an appropriate machine learning model for the following problem:

Problem Type: [CLASSIFICATION / REGRESSION / CLUSTERING / etc.]
Dataset Size: [NUMBER OF SAMPLES]
Number of Features: [NUMBER]
Data Characteristics: [BALANCED/IMBALANCED, CONTINUOUS/CATEGORICAL, etc.]

Requirements:
- Performance Goal: [ACCURACY/F1/RMSE TARGET]
- Interpretability: [HIGH/MEDIUM/LOW]
- Latency Constraints: [REAL-TIME / BATCH]
- Training Time Constraints: [IF ANY]

Please recommend:
1. Top 3 model architectures to consider
2. Pros/cons of each for my specific case
3. Baseline model to start with
4. Key hyperparameters to tune
5. Evaluation strategy""",
            "tags": ["ml", "model selection", "data science"]
        },
        {
            "name": "Feature Engineering Assistant",
            "description": "Template for systematic feature engineering",
            "role": "data_scientist",
            "task_type": "feature_eng",
            "field": "Data Science",
            "base_prompt": """I need help with feature engineering for a [PROBLEM TYPE] problem.

Current Features:
[LIST YOUR CURRENT FEATURES]

Target Variable: [DESCRIBE TARGET]

Domain Context: [DESCRIBE THE DOMAIN - e.g., finance, healthcare, etc.]

Please suggest:
1. Feature transformations (scaling, encoding, etc.)
2. Feature interactions to explore
3. Domain-specific features based on the context
4. Feature selection strategies
5. How to handle missing values and outliers
6. Dimensionality reduction techniques if applicable""",
            "tags": ["feature engineering", "ml", "data preprocessing"]
        },
        {
            "name": "Hyperparameter Tuning Strategy",
            "description": "Template for efficient hyperparameter optimization",
            "role": "ml_engineer",
            "task_type": "hyperparameter",
            "field": "Machine Learning",
            "base_prompt": """I need to tune hyperparameters for a [MODEL NAME] model.

Current Setup:
- Model: [MODEL TYPE]
- Dataset Size: [NUMBER OF SAMPLES]
- Compute Resources: [GPU/CPU, TIME CONSTRAINTS]
- Current Performance: [BASELINE METRICS]

Please help me:
1. Identify the most important hyperparameters to tune
2. Suggest reasonable search ranges for each
3. Recommend search strategy (Grid/Random/Bayesian)
4. Design cross-validation approach
5. Propose a tuning budget (iterations/time)
6. Suggest stopping criteria""",
            "tags": ["hyperparameter tuning", "optimization", "ml"]
        },
        {
            "name": "Model Deployment Checklist",
            "description": "Production deployment readiness template",
            "role": "ml_engineer",
            "task_type": "model_deploy",
            "field": "MLOps",
            "base_prompt": """I'm preparing to deploy a [MODEL TYPE] model to production.

Deployment Context:
- Expected Traffic: [REQUESTS PER SECOND]
- Latency Requirement: [MS]
- Infrastructure: [CLOUD PROVIDER / ON-PREM]
- Serving Pattern: [BATCH / REAL-TIME / STREAMING]

Please provide:
1. Pre-deployment checklist (testing, validation, etc.)
2. Model serving recommendations (TF Serving, FastAPI, etc.)
3. Monitoring strategy (metrics to track, alerts)
4. Rollback plan and A/B testing approach
5. Data drift detection setup
6. Performance optimization tips
7. Documentation requirements""",
            "tags": ["deployment", "mlops", "production"]
        },
        {
            "name": "Exploratory Data Analysis (EDA) Framework",
            "description": "Systematic approach to EDA",
            "role": "data_analyst",
            "task_type": "eda",
            "field": "Data Analysis",
            "base_prompt": """I need to perform EDA on a dataset for a [PROJECT TYPE] project.

Dataset Info:
- Size: [ROWS × COLUMNS]
- Target Variable: [IF SUPERVISED LEARNING]
- Data Types: [NUMERICAL, CATEGORICAL, TEXT, etc.]
- Known Issues: [MISSING DATA, OUTLIERS, etc.]

Please guide me through:
1. Initial data quality checks
2. Univariate analysis (distributions, summary stats)
3. Bivariate/multivariate analysis
4. Correlation analysis
5. Outlier detection strategies
6. Missing data patterns
7. Key visualizations to create
8. Insights to look for specific to [DOMAIN]""",
            "tags": ["eda", "data analysis", "visualization"]
        },

        # ==================== PYTHON & PROGRAMMING ====================
        {
            "name": "Python Function with Best Practices",
            "description": "Template for writing production-quality Python functions",
            "role": "software_dev",
            "task_type": "refactoring",
            "field": "Python",
            "base_prompt": """I need to write a Python function that [DESCRIBE FUNCTIONALITY].

Requirements:
- Input: [DESCRIBE INPUTS WITH TYPES]
- Output: [DESCRIBE EXPECTED OUTPUT]
- Edge Cases: [LIST ANY KNOWN EDGE CASES]
- Python Version: [3.8, 3.9, 3.10, etc.]

Please provide:
1. Clean, well-documented function with type hints
2. Comprehensive docstring (Google or NumPy style)
3. Error handling for edge cases
4. Example usage
5. Suggested unit tests (pytest format)
6. Any performance considerations""",
            "tags": ["python", "clean code", "best practices"]
        },
        {
            "name": "Debug Python Code",
            "description": "Systematic debugging template",
            "role": "software_dev",
            "task_type": "debugging",
            "field": "Python",
            "base_prompt": """I'm encountering a bug in my Python code.

Error/Issue:
[PASTE ERROR MESSAGE OR DESCRIBE THE PROBLEM]

Code:
```python
[PASTE YOUR CODE HERE]
```

Expected Behavior: [WHAT SHOULD HAPPEN]
Actual Behavior: [WHAT ACTUALLY HAPPENS]
Python Version: [VERSION]
Dependencies: [LIST RELEVANT PACKAGES]

Please help me:
1. Identify the root cause of the issue
2. Explain why the error occurs
3. Provide a fix with explanation
4. Suggest how to prevent similar issues
5. Recommend debugging strategies for future""",
            "tags": ["debugging", "python", "troubleshooting"]
        },
        {
            "name": "Code Refactoring Guide",
            "description": "Template for refactoring legacy Python code",
            "role": "software_dev",
            "task_type": "refactoring",
            "field": "Software Engineering",
            "base_prompt": """I need to refactor the following Python code:

```python
[PASTE CODE TO REFACTOR]
```

Refactoring Goals:
- [ ] Improve readability
- [ ] Better performance
- [ ] Add type hints
- [ ] Follow PEP 8
- [ ] Improve error handling
- [ ] Better naming conventions

Please provide:
1. Refactored version with explanations
2. Key improvements made
3. Performance comparison (if applicable)
4. Tests to ensure functionality is preserved
5. Migration strategy if breaking changes""",
            "tags": ["refactoring", "clean code", "python"]
        },
        {
            "name": "Python Testing Strategy",
            "description": "Comprehensive testing approach template",
            "role": "software_dev",
            "task_type": "testing",
            "field": "Software Testing",
            "base_prompt": """I need to create a testing strategy for [DESCRIBE YOUR CODE/MODULE].

Code Context:
- Module Purpose: [DESCRIPTION]
- Key Functions/Classes: [LIST MAIN COMPONENTS]
- Dependencies: [EXTERNAL LIBRARIES]
- Complexity: [SIMPLE / MODERATE / COMPLEX]

Please help me design:
1. Unit test structure (pytest)
2. Test cases to cover (happy path, edge cases, errors)
3. Mocking strategy for external dependencies
4. Fixtures and test data setup
5. Coverage goals and how to achieve them
6. Integration test approach
7. CI/CD integration recommendations""",
            "tags": ["testing", "pytest", "quality assurance"]
        },
        {
            "name": "Performance Optimization Guide",
            "description": "Template for optimizing slow Python code",
            "role": "software_dev",
            "task_type": "performance",
            "field": "Performance Optimization",
            "base_prompt": """I need to optimize the performance of this Python code:

```python
[PASTE CODE HERE]
```

Performance Issues:
- Current Runtime: [TIME]
- Expected Runtime: [TARGET TIME]
- Dataset Size: [IF APPLICABLE]
- Bottleneck: [IF KNOWN]

Please analyze and suggest:
1. Profiling approach (cProfile, line_profiler)
2. Algorithmic improvements
3. Data structure optimizations
4. Vectorization opportunities (NumPy/Pandas)
5. Caching strategies
6. Parallelization possibilities
7. Memory optimization tips""",
            "tags": ["performance", "optimization", "python"]
        },

        # ==================== TIME SERIES & FORECASTING ====================
        {
            "name": "Time Series Forecasting Setup",
            "description": "Complete template for starting a forecasting project",
            "role": "data_scientist",
            "task_type": "forecast_setup",
            "field": "Time Series",
            "base_prompt": """I need to forecast [WHAT YOU'RE FORECASTING] using time series analysis.

Data Characteristics:
- Frequency: [HOURLY / DAILY / WEEKLY / MONTHLY / etc.]
- History Length: [NUMBER OF PERIODS]
- Patterns Observed: [TREND / SEASONALITY / CYCLES]
- Forecast Horizon: [HOW FAR AHEAD]
- Update Frequency: [HOW OFTEN TO RETRAIN]

Please guide me through:
1. Data preparation and cleaning steps
2. Stationarity testing and transformation
3. Train/validation/test split strategy
4. Baseline model selection
5. Feature engineering for time series
6. Evaluation metrics appropriate for my use case
7. Cross-validation approach for time series""",
            "tags": ["forecasting", "time series", "prediction"]
        },
        {
            "name": "ARIMA vs LSTM Model Selection",
            "description": "Choosing between classical and deep learning approaches",
            "role": "data_scientist",
            "task_type": "model_select",
            "field": "Forecasting",
            "base_prompt": """I'm deciding between ARIMA and LSTM for my forecasting problem.

Problem Details:
- Data Frequency: [FREQUENCY]
- History Length: [NUMBER OF POINTS]
- Forecast Horizon: [STEPS AHEAD]
- Data Patterns: [LINEAR/NON-LINEAR, SEASONAL, etc.]
- Computational Resources: [LIMITED / MODERATE / AMPLE]
- Interpretability Need: [HIGH / MEDIUM / LOW]

Please help me:
1. Compare ARIMA and LSTM for my specific case
2. Recommend which to try first
3. Outline implementation steps for recommended model
4. Suggest hybrid approaches if applicable
5. Identify when to use each model type
6. Provide evaluation strategy""",
            "tags": ["arima", "lstm", "model selection"]
        },
        {
            "name": "Seasonality Decomposition Guide",
            "description": "Template for analyzing seasonal patterns",
            "role": "data_analyst",
            "task_type": "seasonality",
            "field": "Time Series Analysis",
            "base_prompt": """I need to analyze and handle seasonality in my time series data.

Data Info:
- Series: [WHAT YOU'RE MEASURING]
- Frequency: [DATA FREQUENCY]
- Suspected Seasonality: [DAILY / WEEKLY / MONTHLY / YEARLY]
- Data Span: [TIME PERIOD]

Please help me:
1. Decompose the series (additive vs multiplicative)
2. Identify seasonal patterns and strength
3. Extract seasonal components
4. Remove seasonality for modeling (if needed)
5. Visualize seasonal patterns
6. Handle multiple seasonal patterns if present
7. Validate seasonality statistically""",
            "tags": ["seasonality", "decomposition", "time series"]
        },
        {
            "name": "Anomaly Detection in Time Series",
            "description": "Template for detecting outliers and anomalies",
            "role": "data_scientist",
            "task_type": "anomaly_detect",
            "field": "Anomaly Detection",
            "base_prompt": """I need to detect anomalies in my time series data.

Context:
- Data Type: [WHAT YOU'RE MONITORING]
- Frequency: [DATA FREQUENCY]
- Anomaly Types Expected: [SPIKES / DROPS / LEVEL SHIFTS / etc.]
- Real-time vs Batch: [DETECTION MODE]
- False Positive Tolerance: [HIGH / MEDIUM / LOW]

Please guide me on:
1. Appropriate anomaly detection methods
2. Statistical vs ML-based approaches
3. Threshold setting strategies
4. Handling seasonality in detection
5. Distinguishing anomalies from changepoints
6. Evaluation metrics for anomaly detection
7. Alert system design""",
            "tags": ["anomaly detection", "outliers", "monitoring"]
        },
        {
            "name": "Multivariate Forecasting Template",
            "description": "Template for forecasting with multiple variables",
            "role": "data_scientist",
            "task_type": "multivariate",
            "field": "Advanced Forecasting",
            "base_prompt": """I need to forecast [TARGET VARIABLE] using multiple input variables.

Variables:
- Target: [TARGET VARIABLE]
- Exogenous Variables: [LIST PREDICTOR VARIABLES]
- Relationships: [KNOWN CORRELATIONS OR DEPENDENCIES]
- Data Frequency: [FREQUENCY]
- Forecast Horizon: [STEPS AHEAD]

Please help me with:
1. Exploratory analysis of variable relationships
2. Causality testing (Granger causality)
3. Model selection (VAR, VARMAX, Prophet with regressors, ML models)
4. Feature engineering for multivariate series
5. Handling different variable frequencies
6. Cross-validation approach
7. Interpreting variable contributions""",
            "tags": ["multivariate", "forecasting", "exogenous variables"]
        }
    ]

    for template_data in templates:
        try:
            DatabaseManager.create_template(**template_data)
        except Exception:
            pass  # Template might already exist


def seed_workflows():
    """Seed domain-specific workflows for 4 priority domains"""
    from sqlalchemy.orm import Session

    workflows = [
        # ==================== ACADEMIC WORKFLOWS ====================
        {
            "name": "Complete Literature Review",
            "description": "Step-by-step workflow for conducting a comprehensive literature review",
            "workflow_type": "lit_review",
            "role": "phd",
            "field": "General",
            "steps": [
                {
                    "step": 1,
                    "name": "Define Research Questions",
                    "prompt_template": "Help me formulate clear research questions for a literature review on [TOPIC]"
                },
                {
                    "step": 2,
                    "name": "Develop Search Strategy",
                    "prompt_template": "Create a comprehensive search strategy including keywords, databases, and Boolean operators for [RESEARCH QUESTIONS]"
                },
                {
                    "step": 3,
                    "name": "Screen and Select Papers",
                    "prompt_template": "Help me develop inclusion/exclusion criteria for screening papers on [TOPIC]"
                },
                {
                    "step": 4,
                    "name": "Extract Key Information",
                    "prompt_template": "What information should I extract from each paper for my review on [TOPIC]? Suggest a data extraction template."
                },
                {
                    "step": 5,
                    "name": "Synthesize Findings",
                    "prompt_template": "Help me synthesize findings from [NUMBER] papers on [TOPIC]. Key themes: [THEMES]"
                }
            ]
        },

        # ==================== ML/DS WORKFLOWS ====================
        {
            "name": "End-to-End ML Project",
            "description": "Complete workflow for building and deploying an ML model",
            "workflow_type": "ml_project",
            "role": "data_scientist",
            "field": "Machine Learning",
            "steps": [
                {
                    "step": 1,
                    "name": "Problem Definition & Data Understanding",
                    "prompt_template": "Help me define the ML problem: [BUSINESS PROBLEM]. What type of ML task is this? What data do I need?"
                },
                {
                    "step": 2,
                    "name": "Exploratory Data Analysis",
                    "prompt_template": "Guide me through EDA for this dataset: [DESCRIBE DATASET]. What should I look for?"
                },
                {
                    "step": 3,
                    "name": "Feature Engineering",
                    "prompt_template": "Suggest feature engineering strategies for: [DESCRIBE DATA AND TARGET]. What features should I create?"
                },
                {
                    "step": 4,
                    "name": "Model Selection & Training",
                    "prompt_template": "Recommend 3 models to try for [PROBLEM TYPE] with [DATA CHARACTERISTICS]. Help me set up training pipeline."
                },
                {
                    "step": 5,
                    "name": "Hyperparameter Tuning",
                    "prompt_template": "Guide me through hyperparameter tuning for [MODEL]. What parameters should I tune and what ranges?"
                },
                {
                    "step": 6,
                    "name": "Model Evaluation & Validation",
                    "prompt_template": "Help me evaluate [MODEL] for [PROBLEM]. What metrics should I use? How to validate properly?"
                },
                {
                    "step": 7,
                    "name": "Deployment Preparation",
                    "prompt_template": "Guide me through deployment prep: model serving, monitoring, documentation for [MODEL]"
                }
            ]
        },
        {
            "name": "Data Science Investigation",
            "description": "Workflow for exploratory data analysis and insights discovery",
            "workflow_type": "data_analysis",
            "role": "data_analyst",
            "field": "Data Science",
            "steps": [
                {
                    "step": 1,
                    "name": "Business Question Framing",
                    "prompt_template": "Help me translate this business question into data analysis tasks: [BUSINESS QUESTION]"
                },
                {
                    "step": 2,
                    "name": "Data Collection & Cleaning",
                    "prompt_template": "Guide me through data cleaning for: [DESCRIBE DATA AND QUALITY ISSUES]"
                },
                {
                    "step": 3,
                    "name": "Statistical Analysis",
                    "prompt_template": "What statistical tests should I run to answer: [QUESTION]? Guide me through the analysis."
                },
                {
                    "step": 4,
                    "name": "Visualization Strategy",
                    "prompt_template": "Suggest visualizations to communicate [FINDINGS] to [AUDIENCE]"
                },
                {
                    "step": 5,
                    "name": "Insight Synthesis",
                    "prompt_template": "Help me synthesize insights from this analysis: [SUMMARIZE FINDINGS]"
                }
            ]
        },

        # ==================== PYTHON WORKFLOWS ====================
        {
            "name": "Python Package Development",
            "description": "Complete workflow for creating a production-ready Python package",
            "workflow_type": "package_dev",
            "role": "software_dev",
            "field": "Python",
            "steps": [
                {
                    "step": 1,
                    "name": "Project Setup & Structure",
                    "prompt_template": "Help me set up a Python package structure for: [PACKAGE PURPOSE]. Include setup.py, directory structure, etc."
                },
                {
                    "step": 2,
                    "name": "Core Implementation",
                    "prompt_template": "Guide me through implementing [CORE FUNCTIONALITY] with clean code practices"
                },
                {
                    "step": 3,
                    "name": "Testing Strategy",
                    "prompt_template": "Create comprehensive testing strategy for [PACKAGE]. Include unit tests, integration tests, fixtures."
                },
                {
                    "step": 4,
                    "name": "Documentation",
                    "prompt_template": "Help me create documentation: README, API docs, examples for [PACKAGE]"
                },
                {
                    "step": 5,
                    "name": "CI/CD Setup",
                    "prompt_template": "Guide me through CI/CD setup: GitHub Actions, testing, linting, coverage for Python package"
                },
                {
                    "step": 6,
                    "name": "Package Distribution",
                    "prompt_template": "Help me prepare for PyPI distribution: versioning, build, upload process"
                }
            ]
        },
        {
            "name": "Code Refactoring Project",
            "description": "Systematic workflow for refactoring legacy Python code",
            "workflow_type": "refactoring",
            "role": "software_dev",
            "field": "Software Engineering",
            "steps": [
                {
                    "step": 1,
                    "name": "Code Assessment",
                    "prompt_template": "Analyze this code and identify refactoring opportunities: [CODE]"
                },
                {
                    "step": 2,
                    "name": "Write Tests First",
                    "prompt_template": "Help me write comprehensive tests for existing behavior before refactoring: [CODE]"
                },
                {
                    "step": 3,
                    "name": "Incremental Refactoring",
                    "prompt_template": "Guide me through refactoring [COMPONENT]. What should I refactor first?"
                },
                {
                    "step": 4,
                    "name": "Add Type Hints",
                    "prompt_template": "Help me add type hints to this code: [CODE]"
                },
                {
                    "step": 5,
                    "name": "Performance Optimization",
                    "prompt_template": "Identify and fix performance bottlenecks in: [CODE]"
                },
                {
                    "step": 6,
                    "name": "Documentation Update",
                    "prompt_template": "Update documentation to reflect refactored code: [CHANGES MADE]"
                }
            ]
        },

        # ==================== TIME SERIES WORKFLOWS ====================
        {
            "name": "Time Series Forecasting Project",
            "description": "Complete workflow for building a forecasting model",
            "workflow_type": "forecasting",
            "role": "data_scientist",
            "field": "Time Series",
            "steps": [
                {
                    "step": 1,
                    "name": "Problem & Data Understanding",
                    "prompt_template": "Help me understand my forecasting problem: [WHAT TO FORECAST], frequency: [FREQUENCY], horizon: [HORIZON]"
                },
                {
                    "step": 2,
                    "name": "Data Preprocessing",
                    "prompt_template": "Guide me through time series preprocessing: handling missing data, outliers for [DATA DESCRIPTION]"
                },
                {
                    "step": 3,
                    "name": "Exploratory Time Series Analysis",
                    "prompt_template": "Help me analyze: trend, seasonality, stationarity for [TIME SERIES]"
                },
                {
                    "step": 4,
                    "name": "Feature Engineering for Time Series",
                    "prompt_template": "Suggest time series features: lags, rolling stats, seasonal indicators for [PROBLEM]"
                },
                {
                    "step": 5,
                    "name": "Model Selection & Training",
                    "prompt_template": "Recommend forecasting models for [DATA CHARACTERISTICS]. Compare ARIMA, Prophet, LSTM, etc."
                },
                {
                    "step": 6,
                    "name": "Cross-Validation",
                    "prompt_template": "Design time series cross-validation strategy for [MODEL] with [DATA LENGTH]"
                },
                {
                    "step": 7,
                    "name": "Evaluation & Diagnostics",
                    "prompt_template": "Help me evaluate forecast quality: metrics, residual analysis for [MODEL]"
                },
                {
                    "step": 8,
                    "name": "Production Forecasting",
                    "prompt_template": "Guide me through production setup: retraining schedule, monitoring, drift detection for [FORECAST]"
                }
            ]
        },
        {
            "name": "Anomaly Detection System",
            "description": "Workflow for building a time series anomaly detection system",
            "workflow_type": "anomaly_detection",
            "role": "data_scientist",
            "field": "Anomaly Detection",
            "steps": [
                {
                    "step": 1,
                    "name": "Define Normal Behavior",
                    "prompt_template": "Help me characterize normal behavior in [TIME SERIES]. What patterns are expected?"
                },
                {
                    "step": 2,
                    "name": "Anomaly Type Identification",
                    "prompt_template": "What types of anomalies should I detect in [CONTEXT]? Point anomalies, contextual, collective?"
                },
                {
                    "step": 3,
                    "name": "Method Selection",
                    "prompt_template": "Recommend anomaly detection methods for [TIME SERIES TYPE]. Statistical vs ML approaches?"
                },
                {
                    "step": 4,
                    "name": "Threshold Tuning",
                    "prompt_template": "Guide me through threshold selection to balance false positives/negatives for [USE CASE]"
                },
                {
                    "step": 5,
                    "name": "Validation Strategy",
                    "prompt_template": "How to validate anomaly detection without labeled data for [SCENARIO]?"
                },
                {
                    "step": 6,
                    "name": "Alert System Design",
                    "prompt_template": "Design alert system: severity levels, notification strategy for [MONITORING CONTEXT]"
                }
            ]
        }
    ]

    with SessionLocal() as session:
        for workflow_data in workflows:
            existing = session.query(Workflow).filter_by(name=workflow_data["name"]).first()
            if not existing:
                workflow = Workflow(**workflow_data)
                session.add(workflow)
        session.commit()


# Seed on first run
try:
    seed_templates()
    seed_workflows()
except Exception:
    pass  # Tables might not exist yet
