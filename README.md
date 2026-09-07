# ⚡ Multi-Agent AI Career Research Assistant

A **Hybrid Multi-Agent + LCEL Career Research Assistant** built using **LangChain, Google Gemini/Groq, Tavily Search, BeautifulSoup, and Streamlit**.

The system performs live career and job-market research based on a user's **target role, experience, skills, and location**. It searches the web, reads relevant sources, generates a structured career intelligence report, and automatically audits the report for quality and completeness.

---

## 🚀 What This Project Does

The application works like an AI-powered career research team:

```text
                                                            User Input
                                                                 │
                                                                 ▼
                                                      ┌─────────────────────┐
                                                      │  Search Agent 🔎    │
                                                      │  Find information   │
                                                      └──────────┬──────────┘
                                                                 │
                                                                 ▼
                                                      ┌─────────────────────┐
                                                      │  Reader Agent 📖    │
                                                      │  Read web pages     │
                                                      └──────────┬──────────┘
                                                                 │
                                                                 ▼
                                                      ┌─────────────────────┐
                                                      │  Writer Chain ✍️    │
                                                      │  Create report      │
                                                      └──────────┬──────────┘
                                                                 │
                                                                 ▼
                                                      ┌─────────────────────┐
                                                      │  Critic Chain 🧐    │
                                                      │  Audit the report   │
                                                      └──────────┬──────────┘
                                                                 │
                                                                 ▼
                                                      ┌─────────────────────┐
                                                      │ Final Report 📊     │
                                                      │ + Quality Score     │
                                                      └─────────────────────┘
```

### In simple terms:

> **Search → Read → Write → Critic → Final Report**

---

# 🏗️ Architecture

The project follows a **hybrid architecture** combining Agents and LangChain Expression Language (LCEL) Chains.

<img width="1312" height="1199" alt="architecture" src="https://github.com/user-attachments/assets/c8727171-cf7e-4de8-9cc6-04df08bd8e48" />

---

# 🤖 Why Hybrid Agents + Chains?

The project intentionally uses **Agents for dynamic tasks** and **LCEL Chains for predictable tasks**.

| Component       | Type       | Purpose                                 |
| --------------- | ---------- | --------------------------------------- |
| 🔎 Search Agent | Agent      | Dynamically searches the web            |
| 📖 Reader Agent | Agent      | Selects and extracts useful web content |
| ✍️ Writer Chain | LCEL Chain | Generates the career report             |
| 🧐 Critic Chain | LCEL Chain | Evaluates the generated report          |

### Agents

Agents are useful when the LLM needs to **make decisions and interact with tools**.

For example:

```text
Should I search?
     ↓
Search Tavily
     ↓
Are the results useful?
     ↓
Search again / Continue
```

### Chains

Chains are useful when the processing flow is already known.

For example:

```text
Input
  ↓
Prompt
  ↓
LLM
  ↓
Output Parser
  ↓
Result
```

This makes the system more predictable and efficient.

---

# 🔗 What is LCEL?

**LCEL stands for LangChain Expression Language.**

LCEL provides a simple way to connect LangChain components together using the pipe (`|`) operator.

For example:

```python
chain = prompt | llm | output_parser
```

This represents:

```text
Prompt
   │
   ▼
 LLM
   │
   ▼
Output Parser
   │
   ▼
Final Result
```

In this project, LCEL is primarily used for the **Writer Chain** and **Critic Chain**.

### Writer Chain

```text
Research Data
     │
     ▼
Prompt Template
     │
     ▼
LLM
     │
     ▼
Output Parser
     │
     ▼
Career Report
```

### Critic Chain

```text
Career Report + Research
            │
            ▼
       Audit Prompt
            │
            ▼
           LLM
            │
            ▼
      Output Parser
            │
            ▼
    Score + Feedback
```

---

# 🔎 1. Search Agent

The Search Agent is responsible for finding relevant career information from the internet.

### Input

The agent receives:

* Target Role
* Experience Level
* Current Skills
* Location

### Tool

**Tavily Search API**

### Example Searches

```text
Data Scientist jobs in Hyderabad
Data Scientist skills required
Data Scientist salary trends
Generative AI skills for Data Scientists
Data Scientist career roadmap
```

The Agent dynamically determines appropriate searches based on the user's requirements.

### Why an Agent?

Search is an unpredictable task. The system may need to determine:

* What to search
* Which search results are relevant
* Whether additional searches are required

Therefore, an Agent is more suitable than a fixed chain.

---

# 📖 2. Reader Agent

The Reader Agent converts search results into useful textual information.

### Flow

```text
Search Results
      │
      ▼
Relevant URLs
      │
      ▼
Web Scraper
      │
      ▼
HTML Content
      │
      ▼
Clean Text
```

### Tools

* BeautifulSoup4
* Requests
* Custom `scrape_url` tool

The scraper removes unnecessary HTML elements such as:

* Scripts
* Navigation
* Headers
* Footers
* Other webpage noise

and extracts the useful page content.

### Why an Agent?

Websites have different structures and content quality. The Reader Agent can dynamically determine which available URLs should be processed.

---

# ✍️ 3. Writer Chain

After research and web extraction are completed, the Writer Chain generates the final career intelligence report.

### Input

The Writer Chain receives:

```text
User Profile
+
Search Results
+
Scraped Web Content
```

### Processing

```text
Research Context
       │
       ▼
Prompt Template
       │
       ▼
Gemini / Groq LLM
       │
       ▼
Output Parser
       │
       ▼
Career Intelligence Report
```

### Report Sections

The generated report can include:

* Market Overview
* Current Skill Analysis
* Skill Gaps
* In-Demand Technologies
* Learning Roadmap
* Career Recommendations
* Action Items

### Why a Chain?

At this stage, the required information has already been collected.

The system does not need another tool-selection or reasoning loop.

Therefore, a predictable **LCEL chain** is more appropriate.

---

# 🧐 4. Critic Chain

The Critic Chain acts as an automated quality reviewer.

It evaluates the generated report against the collected research.

### Evaluation Areas

* Accuracy
* Completeness
* Relevance
* Consistency
* Actionability
* Quality of recommendations

### Flow

```text
Generated Report
       +
Research Context
       │
       ▼
   Audit Prompt
       │
       ▼
      LLM
       │
       ▼
  Audit Result
       │
       ▼
Score + Feedback
```

Example:

```text
Overall Score: 8.5/10

Strengths:
- Good skill analysis
- Relevant recommendations

Areas for Improvement:
- Add more cloud-related skills
- Provide a more detailed learning roadmap
```

---

# ⚙️ Pipeline Orchestrator

The `pipeline.py` module acts as the **central manager** of the application.

It controls the execution order:

```text
Search
  ↓
Reader
  ↓
Writer
  ↓
Critic
```

It also manages intermediate results and sends execution status updates to the Streamlit frontend.

---

# 🔄 Generator-Based Streaming

The pipeline uses Python's **Generator pattern** with `yield`.

Instead of waiting for the entire pipeline to finish, the application can receive progress updates after each stage.

```text
Pipeline Started 🔄
       │
       ▼
Search Completed ✅
       │
       ▼
Reader Completed ✅
       │
       ▼
Report Generated ✅
       │
       ▼
Quality Audit Completed ✅
       │
       ▼
Final Result 📊
```

This allows the Streamlit interface to display real-time execution progress.

---

# 🖥️ Streamlit Frontend

The Streamlit application provides the user interface for the system.

Users provide:

```text
Target Role
Experience Level
Current Skills
Location
```

The dashboard then displays:

* Pipeline execution status
* Search results
* Scraped content
* Generated career report
* Critic score
* Critic feedback

The UI uses custom CSS to provide a modern dashboard experience.

---

# 📂 Project Structure

```text
multi-agent-system-using-langchain/
│
├── agents/
│   ├── __init__.py
│   └── agent.py
|
├── pipeline/
│   ├── __init__.py
│   └── pipeline.py
│
├── tools/
│   ├── __init__.py
│   ├── tools.py
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

### Main Files

| File               | Responsibility                              |
| ------------------ | ------------------------------------------- |
| `app.py`           | Streamlit UI and application entry point    |
| `pipeline.py`      | Pipeline orchestration and state management |
| `tool.py`          | Tavily search/Webpage scraping integration  |
| `agent.py`         | LLM, Agents,LCEL chains defined             |
| `requirements.txt` | Python dependencies                         |
| `.env.example`     | Environment variable template               |

---

# 🛠️ Tech Stack

### Programming Language

* Python 3.10+

### AI / LLM

* LangChain
* Google Gemini
* Groq
* Llama models

### Agent & Chain Framework

* LangChain Agents
* LangChain Expression Language (LCEL)
* Prompt Templates
* Output Parsers

### Search

* Tavily Search API

### Web Scraping

* BeautifulSoup4
* Requests

### Frontend

* Streamlit
* Custom CSS

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Venkatesh0610/multi-agent-system-using-langchain.git

cd multi-agent-system-using-langchain
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

## 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

If BeautifulSoup is missing, install it with:

```bash
python -m pip install beautifulsoup4
```

The package is installed as **`beautifulsoup4`** but imported in Python as:

```python
from bs4 import BeautifulSoup
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_google_gemini_api_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Do not commit your `.env` file to GitHub.

Make sure `.gitignore` contains:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# 🚀 Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# 🔄 Complete Execution Flow

The complete system can be summarized as:

```text
                    USER
                     │
                     ▼
             User Requirements
                     │
                     ▼
             ┌───────────────┐
             │ Search Agent  │
             │               │
             │ Tavily Search │
             └───────┬───────┘
                     │
                     ▼
              Search Results
                     │
                     ▼
             ┌───────────────┐
             │ Reader Agent  │
             │               │
             │ Web Scraper   │
             └───────┬───────┘
                     │
                     ▼
               Web Context
                     │
                     ▼
             ┌───────────────┐
             │ Writer Chain  │
             │               │
             │ Prompt → LLM  │
             │      → Parser │
             └───────┬───────┘
                     │
                     ▼
              Career Report
                     │
                     ▼
             ┌───────────────┐
             │ Critic Chain  │
             │               │
             │ Prompt → LLM  │
             │      → Parser │
             └───────┬───────┘
                     │
                     ▼
              Audit Score
               + Feedback
                     │
                     ▼
              ┌─────────────┐
              │ Streamlit UI│
              └─────────────┘
```

---

# 💡 Key Design Decisions

### Why Agents?

Agents are used where the system needs:

* Dynamic decision-making
* Tool interaction
* Web searching
* URL selection
* Handling unpredictable external content

### Why LCEL Chains?

LCEL Chains are used where the workflow is predictable:

```text
Prompt → LLM → Output
```

This makes the system:

* Easier to maintain
* More structured
* More predictable
* Efficient
* Less dependent on unnecessary agent reasoning loops

---

# 🎯 Key Features

* ✅ Hybrid Multi-Agent + Chain architecture
* ✅ Dynamic web research
* ✅ Tavily-powered search
* ✅ Webpage content extraction
* ✅ Gemini / Groq LLM support
* ✅ LCEL-based report generation
* ✅ Automated report quality audit
* ✅ Quality score and feedback
* ✅ Generator-based pipeline execution
* ✅ Real-time Streamlit status updates
* ✅ Modular project structure

---

# 🔮 Future Improvements

Potential enhancements include:

* [ ] Parallel search execution
* [ ] Persistent research history
* [ ] Vector database integration
* [ ] RAG-based career recommendations
* [ ] Job matching and ranking
* [ ] Resume-to-job comparison
* [ ] Salary trend visualization
* [ ] PDF report generation
* [ ] LangGraph-based stateful orchestration
* [ ] Multi-user authentication
* [ ] Deployment using Docker / Cloud

---

# 📜 License

This project is distributed under the **MIT License**.

See the `LICENSE` file for more information.

---

# 👨‍💻 Author

**A. Venkatesh**

AI/ML | Generative AI | Python Backend | LangChain | Agentic AI

---

## ⭐ If you find this project useful

Consider giving the repository a ⭐ on GitHub and sharing it with others interested in **AI Agents, LangChain, Generative AI, and Agentic AI systems**.
