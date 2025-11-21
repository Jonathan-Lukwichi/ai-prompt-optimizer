"""
User Preferences - Smart learning from user behavior
Tracks preferences and provides smart defaults based on usage patterns
"""
from typing import Dict, Optional, List
from collections import Counter
from datetime import datetime, timedelta
import json


class UserPreferences:
    """
    Tracks and learns from user behavior to provide smart defaults

    Tracks:
    - Preferred version types (basic, critical, tutor, safe)
    - Common domain/role/task combinations
    - Copy/usage patterns
    - Time-based patterns
    """

    def __init__(self, db_manager=None):
        """
        Initialize preferences tracker

        Args:
            db_manager: Optional DatabaseManager instance for persistence
        """
        self.db = db_manager
        self._cache = {
            'version_usage': Counter(),
            'domain_usage': Counter(),
            'role_usage': Counter(),
            'task_usage': Counter(),
            'combinations': Counter(),  # (domain, role, task) tuples
            'last_updated': None
        }

    def track_optimization(
        self,
        domain: str,
        role: str,
        task_type: str,
        selected_version: Optional[str] = None
    ):
        """
        Track an optimization event

        Args:
            domain: Domain used (academic, ml-data-science, python-development)
            role: Role selected
            task_type: Task type selected
            selected_version: Which version was copied/used (if known)
        """
        # Update counters
        self._cache['domain_usage'][domain] += 1
        self._cache['role_usage'][role] += 1
        self._cache['task_usage'][task_type] += 1
        self._cache['combinations'][(domain, role, task_type)] += 1

        if selected_version:
            self._cache['version_usage'][selected_version] += 1

        self._cache['last_updated'] = datetime.now()

        # Persist to database if available
        if self.db:
            self._save_to_db()

    def track_version_usage(self, version_type: str, action: str = 'copy'):
        """
        Track when a specific version is used

        Args:
            version_type: Version used (basic, critical, tutor, safe)
            action: Type of action (copy, view, test)
        """
        self._cache['version_usage'][version_type] += 1
        self._cache['last_updated'] = datetime.now()

        if self.db:
            self._save_to_db()

    def get_preferred_version(self) -> Optional[str]:
        """
        Get the user's most-used version type

        Returns:
            Most common version type, or None if no data
        """
        if not self._cache['version_usage']:
            return None

        return self._cache['version_usage'].most_common(1)[0][0]

    def get_preferred_domain(self) -> Optional[str]:
        """
        Get the user's most-used domain

        Returns:
            Most common domain, or None if no data
        """
        if not self._cache['domain_usage']:
            return None

        return self._cache['domain_usage'].most_common(1)[0][0]

    def get_preferred_role(self, domain: Optional[str] = None) -> Optional[str]:
        """
        Get the user's most-used role (optionally filtered by domain)

        Args:
            domain: Optional domain to filter by

        Returns:
            Most common role, or None if no data
        """
        if domain:
            # Filter combinations by domain
            domain_roles = [
                role for (d, role, _), count in self._cache['combinations'].items()
                if d == domain
            ]
            if not domain_roles:
                return None
            return Counter(domain_roles).most_common(1)[0][0]

        if not self._cache['role_usage']:
            return None

        return self._cache['role_usage'].most_common(1)[0][0]

    def get_preferred_task(
        self,
        domain: Optional[str] = None,
        role: Optional[str] = None
    ) -> Optional[str]:
        """
        Get the user's most-used task type (optionally filtered)

        Args:
            domain: Optional domain to filter by
            role: Optional role to filter by

        Returns:
            Most common task type, or None if no data
        """
        if domain or role:
            # Filter combinations
            filtered_tasks = [
                task for (d, r, task), count in self._cache['combinations'].items()
                if (domain is None or d == domain) and (role is None or r == role)
            ]
            if not filtered_tasks:
                return None
            return Counter(filtered_tasks).most_common(1)[0][0]

        if not self._cache['task_usage']:
            return None

        return self._cache['task_usage'].most_common(1)[0][0]

    def get_smart_defaults(self) -> Dict[str, Optional[str]]:
        """
        Get smart defaults for all settings based on usage history

        Returns:
            Dictionary with recommended domain, role, task, version
        """
        preferred_domain = self.get_preferred_domain()
        preferred_role = self.get_preferred_role(preferred_domain)
        preferred_task = self.get_preferred_task(preferred_domain, preferred_role)
        preferred_version = self.get_preferred_version()

        return {
            'domain': preferred_domain,
            'role': preferred_role,
            'task_type': preferred_task,
            'version': preferred_version
        }

    def get_usage_stats(self) -> Dict:
        """
        Get comprehensive usage statistics

        Returns:
            Dictionary with usage patterns and statistics
        """
        total_optimizations = sum(self._cache['domain_usage'].values())

        stats = {
            'total_optimizations': total_optimizations,
            'domains': dict(self._cache['domain_usage']),
            'roles': dict(self._cache['role_usage']),
            'tasks': dict(self._cache['task_usage']),
            'versions': dict(self._cache['version_usage']),
            'top_combinations': [
                {
                    'domain': domain,
                    'role': role,
                    'task': task,
                    'count': count
                }
                for (domain, role, task), count in self._cache['combinations'].most_common(5)
            ],
            'last_updated': self._cache['last_updated'].isoformat() if self._cache['last_updated'] else None
        }

        # Calculate percentages
        if total_optimizations > 0:
            stats['domain_percentages'] = {
                domain: (count / total_optimizations) * 100
                for domain, count in self._cache['domain_usage'].items()
            }

            stats['version_percentages'] = {
                version: (count / sum(self._cache['version_usage'].values())) * 100
                for version, count in self._cache['version_usage'].items()
            } if self._cache['version_usage'] else {}

        return stats

    def should_suggest_template(self, raw_prompt: str) -> bool:
        """
        Determine if we should suggest a template based on prompt similarity

        Args:
            raw_prompt: The user's raw prompt

        Returns:
            True if template suggestion would be helpful
        """
        # Simple heuristic: suggest template if prompt is short or vague
        word_count = len(raw_prompt.split())

        # Suggest if:
        # 1. Very short prompt (< 10 words)
        # 2. Common patterns detected
        if word_count < 10:
            return True

        # Check for common beginner patterns
        beginner_patterns = ['help me', 'how do i', 'what is', 'explain', 'tell me about']
        prompt_lower = raw_prompt.lower()

        if any(pattern in prompt_lower for pattern in beginner_patterns):
            # User might benefit from template
            return True

        return False

    def get_template_suggestions(
        self,
        domain: str,
        task_type: str
    ) -> List[str]:
        """
        Get suggested template types based on domain and task

        Args:
            domain: Current domain
            task_type: Current task type

        Returns:
            List of suggested template categories
        """
        suggestions = []

        # Domain-specific suggestions
        if domain == 'academic':
            if task_type in ['research', 'literature_review']:
                suggestions.extend(['Literature Review', 'Research Question'])
            elif task_type in ['writing', 'paper']:
                suggestions.extend(['Thesis Statement', 'Abstract Writing'])
            elif task_type == 'learning':
                suggestions.extend(['Concept Explanation', 'Study Guide'])

        elif domain == 'ml-data-science':
            if task_type in ['analysis', 'research']:
                suggestions.extend(['Data Analysis', 'Model Evaluation'])
            elif task_type == 'coding':
                suggestions.extend(['Algorithm Implementation', 'Code Review'])

        elif domain == 'python-development':
            if task_type == 'debugging':
                suggestions.extend(['Debug Help', 'Error Analysis'])
            elif task_type == 'coding':
                suggestions.extend(['Function Design', 'Code Optimization'])

        return suggestions

    def _save_to_db(self):
        """Save preferences to database"""
        # TODO: Implement database persistence
        # This will be implemented when we add the database schema
        pass

    def _load_from_db(self):
        """Load preferences from database"""
        # TODO: Implement database loading
        pass

    def reset_preferences(self):
        """Clear all preference data"""
        self._cache = {
            'version_usage': Counter(),
            'domain_usage': Counter(),
            'role_usage': Counter(),
            'task_usage': Counter(),
            'combinations': Counter(),
            'last_updated': None
        }

    def export_preferences(self) -> str:
        """
        Export preferences as JSON string

        Returns:
            JSON string with all preference data
        """
        data = {
            'version_usage': dict(self._cache['version_usage']),
            'domain_usage': dict(self._cache['domain_usage']),
            'role_usage': dict(self._cache['role_usage']),
            'task_usage': dict(self._cache['task_usage']),
            'combinations': {
                f"{d}|{r}|{t}": count
                for (d, r, t), count in self._cache['combinations'].items()
            },
            'last_updated': self._cache['last_updated'].isoformat() if self._cache['last_updated'] else None
        }

        return json.dumps(data, indent=2)

    def import_preferences(self, json_str: str):
        """
        Import preferences from JSON string

        Args:
            json_str: JSON string with preference data
        """
        data = json.loads(json_str)

        self._cache['version_usage'] = Counter(data.get('version_usage', {}))
        self._cache['domain_usage'] = Counter(data.get('domain_usage', {}))
        self._cache['role_usage'] = Counter(data.get('role_usage', {}))
        self._cache['task_usage'] = Counter(data.get('task_usage', {}))

        # Reconstruct combinations
        combinations = {}
        for key, count in data.get('combinations', {}).items():
            domain, role, task = key.split('|')
            combinations[(domain, role, task)] = count
        self._cache['combinations'] = Counter(combinations)

        if data.get('last_updated'):
            self._cache['last_updated'] = datetime.fromisoformat(data['last_updated'])


# Global instance for session-based preferences
_session_preferences = None


def get_preferences() -> UserPreferences:
    """
    Get or create the global preferences instance

    Returns:
        UserPreferences instance
    """
    global _session_preferences

    if _session_preferences is None:
        _session_preferences = UserPreferences()

    return _session_preferences


def reset_session_preferences():
    """Reset the global preferences instance"""
    global _session_preferences
    _session_preferences = None
