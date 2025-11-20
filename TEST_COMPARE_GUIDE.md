# Test & Compare Feature Guide

## What is it?

The **Test & Compare** feature proves that your optimized prompts work better by testing both versions with the same AI model and comparing the results with objective metrics.

## How to Use

### Option 1: Automatic Mode (Recommended) ✨

1. **Go to Prompt Lab** first and optimize your prompt
2. **Navigate** to "Test & Compare" page (5th page with 🔬 icon)
3. **Prompts Auto-Load**: Your original and optimized prompts are automatically loaded!
4. **Choose Version** (if multiple versions exist):
   - Use the dropdown to select which optimized version to test
   - Options: 📝 Basic, 🧠 Critical, 👨‍🏫 Tutor, 🛡️ Safe
5. **Click "Test Both Prompts"**:
   - Both prompts are sent to Gemini AI
   - Responses are analyzed for quality
   - Results are displayed with visualizations

### Option 2: Manual Mode

1. **Navigate** to the "Test & Compare" page directly
2. **Enter Your Prompts** manually:
   - Left column: Your original prompt
   - Right column: Your optimized prompt
3. **Click "Test Both Prompts"** to run the comparison

## What Gets Analyzed

### 4 Quality Dimensions (0-100 score each):

1. **Completeness (30% weight)**
   - Thoroughness of the response
   - Presence of examples and structure
   - Overall depth

2. **Clarity (25% weight)**
   - Readability and sentence structure
   - Use of transitions
   - Word complexity

3. **Specificity (25% weight)**
   - Detail level and concrete examples
   - Use of numbers and technical terms
   - Avoidance of vague language

4. **Actionability (20% weight)**
   - Practical usefulness
   - Action verbs and steps
   - Implementable recommendations

### Overall Score
Weighted average of all 4 dimensions

## Visual Results

### 1. Winner Announcement
- Celebrates if optimized prompt wins
- Shows point improvement
- Suggests next steps if original wins

### 2. Score Comparison Cards
- 5 cards showing: Overall, Completeness, Clarity, Specificity, Actionability
- Color-coded improvements (green = better, red = worse)
- Shows score changes (original → optimized)

### 3. Interactive Charts
- **Radar Chart**: Multi-dimensional comparison across all metrics
- **Bar Chart**: Improvement scores (positive or negative)
- Both charts use dark theme with neon accents (bolt.new style)

### 4. Side-by-Side Responses
- Full AI responses from both prompts
- Strengths and weaknesses for each
- Color-coded sections for easy comparison

## Design Highlights

Inspired by **bolt.new**, the page features:
- ✨ Glassmorphism effects
- 🎨 Gradient backgrounds and text
- 📊 Interactive Plotly charts
- 🌈 Neon color accents (#8B5CF6, #10B981, #EF4444)
- 💫 Modern dark theme with high contrast
- 🎯 Clear visual hierarchy

## Seamless Workflow 🔄

The auto-load feature creates a seamless workflow:

1. **Prompt Lab** → Optimize your prompt and get 4 versions
2. **Test & Compare** → Prompts automatically load (no copy/paste!)
3. **Select Version** → Choose which optimized version to test
4. **Run Test** → See objective proof of improvement
5. **Iterate** → Go back to Prompt Lab if needed

**Pro Tip**: The selected version is remembered! Switch between versions with the dropdown to compare different optimization styles.

## Tips for Best Results

1. **Test all versions** - Each version (Basic, Critical, Tutor, Safe) optimizes differently
2. **Keep prompts similar in intent** - Test the same goal with different approaches
3. **Use realistic scenarios** - Test with actual use cases from your work
4. **Review weaknesses** - Even winning prompts have areas to improve
5. **Compare metrics** - Look beyond overall score - some versions excel in specific dimensions
6. **Iterate** - Use insights to create even better prompts

## Example Use Case

**Original**: "Explain machine learning"

**Optimized**: "As a data scientist, explain machine learning concepts including supervised, unsupervised, and reinforcement learning, with practical examples from industry applications. Focus on key algorithms and their real-world use cases."

**Expected Result**: The optimized prompt should score higher on:
- Completeness (requests specific topics)
- Specificity (asks for examples and use cases)
- Actionability (practical industry applications)

---

**Ready to prove your prompts are better?** Run `streamlit run home.py` and navigate to Test & Compare! 🚀
