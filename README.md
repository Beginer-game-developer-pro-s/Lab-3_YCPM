# CSE703095 - Software Requirements (Lab 03)
## MedBook: Requirements Specification & Living Document System

This project implements an automated Software Requirements Specification (SRS) generation system following the **ISO/IEC/IEEE 29148:2018** standard for **MedBook** -- an Online Medical Appointment Booking System.

---

### 1. Project Directory Structure

```text
Lab 3_YCPM/
├── README.md                          # Project documentation and instructions
├── code/
│   ├── srs_generator.py               # Main Python generator script with extensions
│   ├── SRS_MedBook_generated.md       # Auto-generated SRS document (Markdown)
│   └── SRS_MedBook_generated.tex      # Auto-generated SRS document (LaTeX)
└── report/
    └── lab03_report.doc               # Lab 03 report document (Word/DOC format)
```

---

### 2. Features & Extended Capabilities

1. **Automated SRS Generation (Living Document):**
   - Synthesizes structured data (Functional Requirements, Non-Functional Requirements, Stakeholders) into a standardized IEEE 29148 document.
   - Ensures continuous synchronization between requirement datasets and formal documentation.

2. **Automated Glossary Extraction (`section_glossary`):**
   - Automatically scans all requirement statements using regular expressions (`\b[A-Z]{2,5}\b`) to identify domain acronyms (`FR`, `NFR`, `RBAC`, `SRS`, `OTP`, `SMS`, `API`, `BHYT`, `ICD`, etc.).
   - Maps acronyms to standardized definitions in healthcare and software engineering domains.

3. **Multi-format CLI Output via `argparse`:**
   - Supports `--format markdown` (default) to generate GitHub-flavored Markdown (`SRS_MedBook_generated.md`).
   - Supports `--format latex` to generate fully compilable LaTeX code (`SRS_MedBook_generated.tex`) with proper escaping, tables, and section structures.

4. **Integrated Design Constraints (Section 5):**
   - Incorporates Technical Constraints (RESTful microservices, responsive mobile $\ge 360$px, HL7/FHIR release 4).
   - Incorporates Legal & Regulatory Constraints (Vietnam Decree 13/2023/ND-CP, local data centers, AES-256 / TLS 1.3 encryption).
   - Incorporates Timeline & Budget Constraints (4-month MVP deadline, phase 1 annual cloud budget $\le 150$M VND).

---

### 3. Usage & Execution Instructions

From the `code/` directory, execute:

```bash
# Generate Markdown specification (default)
python srs_generator.py

# Explicitly specify Markdown output
python srs_generator.py --format markdown

# Generate LaTeX specification (.tex)
python srs_generator.py --format latex
```

---

### 4. Deliverables Summary

- **Report Document:** Located in `report/lab03_report.doc` with comprehensive EARS analysis, Karl Wiegers 6-attribute evaluation, automation vs. human analysis, and full self-assessment (10.0/10.0).
- **Generated Specifications:** Located in `code/SRS_MedBook_generated.md` and `code/SRS_MedBook_generated.tex`.
- **Source Code:** Located in `code/srs_generator.py`.