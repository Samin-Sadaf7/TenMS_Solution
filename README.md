# Bangla QA RAG Pipeline

This project implements a Retrieval-Augmented Generation (RAG) system for question answering on Bangla educational content using PDF documents as knowledge sources.

## Features
- Bangla PDF text extraction with OCR preprocessing
- Hybrid retrieval (semantic + keyword search)
- Multilingual embedding support
- Context-aware question answering
- Conversation memory
- REST API endpoints

## Setup Guide

### Prerequisites
- Python 3.8+
- Tesseract OCR (with Bangla support)
- Poppler (for PDF conversion)

### Installation
```bash
# Clone repository
git clone https://github.com/Samin-Sadaf7/TenMS_Solution.git
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export COHERE_API_KEY="your_cohere_key"
export OPENAI_API_KEY="your_openai_key"
export HF_TOKEN="your_huggingface_token"
```

### Run FastAPI Server
```bash
uvicorn app.main:app --reload
```

## Implementation Details

### Text Extraction
- **Library**: PyTesseract with PDF2Image
- **Reason**: PyMuPDF failed with complex Bangla PDF layouts
- **Challenges**: 
  - Text corruption in original PDF
  - Non-standard fonts and formatting
  - Mixed Bangla/English content
- **Solution**:
  - Convert PDF pages to images (300 DPI)
  - Preprocess images (grayscale, contrast enhancement)
  - OCR with Tesseract (`ben` language)
  - Text cleaning (remove special chars, normalize punctuation)

### Chunking Strategy
- **Approach**: 150-word chunks with 50-word overlap
- **Benefits**:
  - Preserves contextual coherence
  - Handles long answers spanning multiple paragraphs
  - Maintains relationship between questions and answers
- **Optimization**: Overlap ensures no context loss at boundaries

### Embedding Model
- **Primary Model**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Alternative**: Cohere `embed-multilingual-v3.0`
- **Selection Criteria**:
  - Strong multilingual performance
  - Efficient semantic representation
  - Compatibility with Bangla morphology
- **Vector Size**: 384 dimensions (HuggingFace), 1024 dimensions (Cohere)

### Similarity Search
- **Architecture**: Hybrid retrieval pipeline
  1. FAISS semantic search (top 10 candidates)
  2. BM25 keyword filtering
  3. Cohere reranking (top 3 contexts)
- **Advantages**:
  - Combines semantic understanding with keyword matching
  - Handles vague queries effectively
  - Adapts to Bangla synonym variations
- **Storage**: FAISS index with HNSW algorithm

### Query Handling
- **Vague Query Solution**:
  - Expand query using conversation memory
  - Return multiple context candidates
  - Request clarification when needed
- **Context Comparison**:
  - Sentence-boundary aware matching
  - Cross-lingual alignment (Bangla-English)
  - Proximity-based scoring

## API Documentation

### Endpoints
- **POST /query** - Submit a question
  ```json
  {
    "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"
  }
  ```
  
- **GET /last-messages** - Get conversation history
  ```json
  [
    {"role": "human", "content": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"},
    {"role": "ai", "content": "১৫ বছর"}
  ]
  ```

- **POST /relevant-contexts** - Retrieve relevant contexts
  ```json
  {
    "query": "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"
  }
  ```

## Sample Queries & Outputs

### Bangla Queries
```bash
Query: "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"
Answer: "১৫ বছর"

Query: "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"
Answer: "শুম্ভুনাথ"

Query: "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?"
Answer: "মামা"
```

### English Queries
```bash
Query: "What was Kalyanee's real age at marriage?"
Answer: "15 years"

Query: "Who is called handsome in Anupam's words?"
Answer: "Mama (uncle)"
```


### Response Quality
- **Strengths**:
  - Not Precise factual answers
  - Context-aware interpretations
  - Effective handling of PDF artifacts
  
- **Limitations**:
  - Struggles with implied context
  - Inconsistent with numerical responses
  - OCR errors affect retrieval quality

## Future Improvements
1. Implement Bangla-specific tokenization
2. Add domain-adaptive fine-tuning
3. Integrate spelling correction module
4. Develop custom OCR model for educational PDFs
5. Add multi-document support

## Contributors
- Syed Samin Sadaf

---

**Implementation Q&A**

**Q: What method/library was used for text extraction?**  
A: Used PyTesseract with PDF2Image after PyMuPDF failed with Bangla PDF formatting. OCR preprocessing addressed text corruption and font issues.

**Q: What chunking strategy was chosen?**  
A: 150-word chunks with 50-word overlap preserves question-answer relationships while maintaining context continuity.

**Q: Which embedding model was selected?**  
A: `paraphrase-multilingual-MiniLM-L12-v2` for its Bangla compatibility and efficient semantic representation.

### **Q: How are queries compared to chunks?**  
**Hybrid Retrieval Pipeline**:  

1. **FAISS (Semantic Search)**  
   - Uses multilingual embeddings (`paraphrase-multilingual-MiniLM-L12-v2`) to handle **mixed Bangla-English queries**.  
   - Matches intent even if terms are partially in English (e.g., *"অনুপমের age বিয়ের সময়"* → "অনুপমের বয়স").  

2. **BM25 (Keyword Matching)**  
   - Tokenizes and normalizes **both Bangla and English terms** (e.g., *"ভাগ্য deity"* → "ভাগ্য দেবতা").  
   - Filters FAISS results by exact keyword overlap.  

3. **Cohere Reranker (Contextual Boost)**  
   - Resolves **cross-lingual synonyms** (e.g., *"সুপুরুষ vs. gentleman"*).  
   - Prioritizes chunks with **balanced Bangla-English context** for mixed queries.  

### **Q: Are results relevant?**  
**Key Strengths**:  
✅ **Mixed-Language Queries**:  
   - Handles hybrid phrases like *"কল্যাণীর real age"* by aligning English terms to Bangla context.  
✅ **Direct Facts**:  
   - Accurate for explicit answers (e.g., *"অনুপমের পেশা কী?"* → "Profession").  

**Limitations**:  
❌ **Partial Translations**:  
   - Struggles with **non-literal translations** (e.g., *"ভাগ্য দেবতা"* → "fate deity" in English queries).  
❌ **OCR-Dependent Terms**:  
   - Misreads **digits/compound letters** (e.g., "১৫" → "18" in English contexts).  

---

### **Handling Mixed Bangla-English Queries**  
1. **Query Normalization**:  
   - Transliterates English terms to Bangla (e.g., *"age"* → "বয়স") using a **bilingual dictionary**.  
2. **Cross-Lingual Embeddings**:  
   - Uses **multilingual Cohere embeddings** to map mixed terms to a shared semantic space.  
3. **Dynamic Keyword Expansion**:  
   - Auto-adds **Bangla synonyms** for English terms (e.g., *"gentleman"* → ["সুপুরুষ", "ভদ্রলোক"]).  

**Example**:  
- Query: *"Who is called সুপুরুষ in অনুপমের words?"*  
- Normalized: "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"  
- Retrieval: Correctly maps to "শুম্ভুনাথ".  

**Note**: For best results, **fully Bangla queries** yield higher accuracy than mixed ones.  
