
## 📘 ChemRxivQuest

**ChemRxivQuest** is a curated, domain-specific dataset for natural language processing (NLP) in chemistry. It contains **970 high-quality question–answer (QA) pairs** extracted from **155 ChemRxiv preprints** spanning **17 subfields** of chemistry. Each QA pair is explicitly linked to its source text segment, ensuring scientific traceability and contextual accuracy.

---

### 🧪 Project Highlights

* **Broad Coverage**: QA pairs span organic, inorganic, materials, physical chemistry, and more.
* **LLM-Generated QA**: Questions and answers generated using **GPT-4o** with structured prompts.
* **Rigorous Validation**: QA verified using **fuzzy matching** (≥80% similarity threshold).
* **Structured for Use** in:

  * Retrieval-based QA systems
  * Fine-tuning chemistry-specific LLMs
  * Educational tools and semantic search

---

### 🗂️ Repository Structure

```
chemrxivquest/
├── data/
│   ├── chemrxivquest.json           # Final curated QA dataset (970 pairs)
│   ├── metadata.csv                 # Metadata for all 155 preprints
│   └── raw_pdfs/                    # (Optional) Original ChemRxiv PDFs
│
├── src/
│   ├── extract_text.py              # OCR + preprocessing pipeline
│   ├── generate_qa.py               # GPT-based QA generation
│   ├── verify_answers.py            # Fuzzy matching + validation
│   └── utils.py                     # Helper functions (regex, config, etc.)
│
├── notebooks/
│   ├── dataset_analysis.ipynb       # QA type distribution, subfield stats
│   └── model_eval_examples.ipynb    # Sample evaluation of LLMs on dataset
│
├── models/                          # (Optional) Fine-tuned model checkpoints
│
├── evaluation/
│   ├── benchmark_metrics.py         # ROUGE, BLEU, EM calculations
│   └── retrieval_benchmark.py       # Embedding-based R@k and nDCG tests
│
├── README.md
├── LICENSE
└── requirements.txt
```

---

### 📦 Dataset Details

* **Total QA Pairs**: 970
* **Source**: ChemRxiv preprints (CC-BY license)
* **QA Types**:

  * Conceptual (23.7%)
  * Mechanistic (24.9%)
  * Applied (25.5%)
  * Experimental/Synthetic (25.7%)
* **Formats**: JSON, CSV

---

### 🚀 Getting Started

#### Installation

```bash
git clone https://github.com/your-org/chemrxivquest.git
cd chemrxivquest
pip install -r requirements.txt
```

#### Run the QA Pipeline

```bash
python src/extract_text.py --input data/raw_pdfs/
python src/generate_qa.py --input data/preprocessed/
python src/verify_answers.py --input data/qa_candidates.json
```

---

### 🧪 Example Use Cases

* **Fine-tune LLMs** on chemistry-specific Q\&A tasks
* **Evaluate embeddings** for semantic chemical retrieval (e.g., SciBERT, E5)
* **Train RAG systems** for chemistry
* **Create educational tools** or chemistry quiz generators

---

### ⚠️ Limitations

* Based on **preprints**, which may contain unverified information.
* Some QA pairs may contain **LLM hallucinations** despite fuzzy validation.
* Domain imbalance—e.g., **Organic Chemistry** is overrepresented.

---

### 🛠️ Future Work

* Add **expert human validation** for improved quality
* Expand to **peer-reviewed journals**
* Include **semantic verification using transformers**
* Release **benchmark leaderboards**

---

### 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

### 🙌 Acknowledgments

Developed by [Mahmoud Amiri](https://github.com/mahmoud-amiri) and [Thomas Bocklitz](https://www.ipht-jena.de), Leibniz Institute of Photonic Technology and Friedrich Schiller University Jena.

-
