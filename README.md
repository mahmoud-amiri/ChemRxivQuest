## ChemRxivQuest

**ChemRxivQuest** is a curated, domain-specific dataset for natural language processing (NLP) in chemistry. It contains **970 high-quality question–answer (QA) pairs** extracted from **155 ChemRxiv preprints** spanning **17 subfields** of chemistry. Each QA pair is explicitly linked to its source text segment, ensuring scientific traceability and contextual accuracy.

---

### Project Highlights

* **Broad Coverage**: QA pairs span organic, inorganic, materials, physical chemistry, and more.
* **LLM-Generated QA**: Questions and answers generated using **GPT-4o** with structured prompts.
* **Rigorous Validation**: QA verified using **fuzzy matching** (≥80% similarity threshold).
* **Structured for Use** in:
  * Retrieval-based QA systems
  * Fine-tuning chemistry-specific LLMs
  * Educational tools and semantic search

---

### Dataset Details

* **Total QA Pairs**: 970
* **Source**: ChemRxiv preprints (CC BY 4.0 license)
* **QA Types**:
  * Conceptual (23.7%)
  * Mechanistic (24.9%)
  * Applied (25.5%)
  * Experimental/Synthetic (25.7%)
* **Formats**: JSON, CSV
* **Preprint Metadata**: See `sources.tsv` for complete citation list of all 155 preprints.

---

### Getting Started

#### Installation

```bash
git clone https://github.com/mahmoud-amiri/ChemRxivQuest.git
cd ChemRxivQuest
pip install -r requirements.txt
````

---

### Example Use Cases

* Fine-tune LLMs on chemistry-specific Q\&A tasks
* Evaluate embeddings for semantic chemical retrieval (e.g., SciBERT, E5)
* Train RAG systems for chemistry
* Create educational tools or chemistry quiz generators

---

### Limitations

* Based on **preprints**, which may contain unverified or preliminary findings.
* Some QA pairs may include **hallucinations** from the LLM despite fuzzy matching validation.
* Domain imbalance — **Organic Chemistry** is overrepresented.

---

### Future Work

* Add **expert human validation** for improved quality
* Expand coverage to **peer-reviewed journals**
* Introduce **semantic verification with transformers**
* Release **leaderboards** for benchmarking QA models

---

### Licensing and Legal

* 📚 The **dataset** (ChemRxivQuest) is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). See the `LICENSE` file.
* 💻 The **code** in this repository is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE_CODE` file.

**Attribution Requirements**
If you use this dataset, please cite:

> ChemRxivQuest: A Curated Chemistry Question-Answer Database Extracted from ChemRxiv Preprints by Mahmoud Amiri and Thomas Bocklitz
> Source: [https://arxiv.org/abs/2505.05232](https://arxiv.org/abs/2505.05232)
> License: CC BY 4.0

Include proper attribution for all reused content. See `sources.tsv` for citation of each ChemRxiv preprint used in this dataset.

**Liability and Disclaimer**
This dataset is provided **"as is"**, without warranty of any kind. The authors and licensors assume no responsibility for any damages resulting from its use, to the extent permitted by §§ 521–524 BGB (German Civil Code).
This dataset contains **no personal data** as defined under Article 4 of the GDPR.

**Database Rights**
Any sui generis database rights under § 87a UrhG and Directive 96/9/EC are licensed under CC BY 4.0.

---

### 🙌 Acknowledgments

Developed by [Mahmoud Amiri](https://github.com/mahmoud-amiri) and [Thomas Bocklitz](https://www.ipht-jena.de), at the Leibniz Institute of Photonic Technology and Friedrich Schiller University Jena.

---
If you use this dataset, please cite it.
```
@misc{amiri2025chemrxivquestcuratedchemistryquestionanswer,
      title={ChemRxivQuest: A Curated Chemistry Question-Answer Database Extracted from ChemRxiv Preprints}, 
      author={Mahmoud Amiri and Thomas Bocklitz},
      year={2025},
      eprint={2505.05232},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2505.05232}, 
}
```