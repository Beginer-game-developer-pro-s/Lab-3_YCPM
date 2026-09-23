#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
srs_generator.py
Lab 3 - Requirements Specification & Documentation
----------------------------------------------------------------------
Reads functional_requirements.csv + nonfunctional_requirements.csv and
auto-generates a Software Requirements Specification (SRS) document
following the IEEE/ISO 29148 structure, supporting Markdown and LaTeX formats.

Teaching purpose: illustrates that a "living" SRS document can be
(re)generated from structured requirement data instead of being
authored entirely by hand - helping ensure consistency.

Usage:
    python srs_generator.py                     # Generates Markdown (default)
    python srs_generator.py --format markdown   # Generates Markdown
    python srs_generator.py --format latex      # Generates LaTeX (.tex)
"""
import argparse
import csv
import os
import re
from datetime import date

# Known glossary dictionary for healthcare & requirements domain
GLOSSARY_DEFINITIONS = {
    "FR": "Functional Requirement - Specifies a function that a system or system component must be able to perform.",
    "NFR": "Non-Functional Requirement - Specifies criteria that can be used to judge the operation of a system rather than specific behaviors.",
    "RBAC": "Role-Based Access Control - Access control mechanism based on roles assigned to users within an organization.",
    "SRS": "Software Requirements Specification - Comprehensive description of the intended purpose and environment for software under development.",
    "OTP": "One-Time Password - A password that is valid for only one login session or transaction.",
    "SMS": "Short Message Service - Text messaging service component of most telephone, internet, and mobile device systems.",
    "API": "Application Programming Interface - Set of subroutine definitions, protocols, and tools for building application software.",
    "UI": "User Interface - Space where interactions between humans and machines occur.",
    "TLS": "Transport Layer Security - Cryptographic protocol designed to provide communications security over a computer network.",
    "AES": "Advanced Encryption Standard - Symmetric encryption algorithm widely adopted to secure sensitive electronic data.",
    "RPO": "Recovery Point Objective - Maximum acceptable amount of data loss measured in time.",
    "RTO": "Recovery Time Objective - Maximum acceptable length of time that computer systems can be down.",
    "CI": "Continuous Integration - Practice of merging all developers' working copies to a shared mainline several times a day.",
    "ISO": "International Organization for Standardization - Independent, non-governmental international standard development organization.",
    "SMART": "Specific, Measurable, Achievable, Relevant, Time-bound criteria for defining requirements/objectives.",
    "BHYT": "Social Health Insurance (Bao Hiem Y Te) - Vietnam national public healthcare insurance program.",
    "ICD": "International Classification of Diseases - Globally recognized healthcare diagnostic classification system.",
    "HIS": "Hospital Information System - Comprehensive information system designed to manage all aspects of hospital operation.",
    "EMR": "Electronic Medical Record - Digital version of the traditional paper-based medical record for an individual patient."
}

# Embedded dataset fallback ensuring script runs independently
FALLBACK_STAKEHOLDERS = [
    {"StakeholderID": "SH-01", "StakeholderName": "Patient", "ExpectedBenefit": "Book appointments quickly, view history, receive reminders"},
    {"StakeholderID": "SH-02", "Doctor": "Doctor", "StakeholderName": "Doctor", "ExpectedBenefit": "Manage schedule, view medical records, drug interaction warnings"},
    {"StakeholderID": "SH-03", "StakeholderName": "Receptionist / Front desk staff", "ExpectedBenefit": "Confirm bookings, handle cancel/reschedule, assist walk-ins"},
    {"StakeholderID": "SH-04", "StakeholderName": "Hospital Administrator", "ExpectedBenefit": "Manage doctor/department catalog, operational reports, access control"},
    {"StakeholderID": "SH-05", "StakeholderName": "Health insurance provider", "ExpectedBenefit": "Verify insurance coverage, reconcile costs"},
    {"StakeholderID": "SH-06", "StakeholderName": "Hospital IT department", "ExpectedBenefit": "Maintenance, performance monitoring, data security"},
    {"StakeholderID": "SH-07", "StakeholderName": "Health regulatory authority", "ExpectedBenefit": "Compliance with health-data privacy and patient-safety regulations"},
    {"StakeholderID": "SH-08", "StakeholderName": "Development team", "ExpectedBenefit": "Correctly understand and implement requirements, control scope"}
]

FALLBACK_FRS = [
    {"ReqID": "FR-001", "Title": "Patient account registration and login", "Description": "The system shall allow patients to register via email/phone and verify via OTP.", "RelatedStakeholder": "SH-01", "Priority": "High", "Status": "Proposed", "RelatedUseCase": "UC-01"},
    {"ReqID": "FR-002", "Title": "Search doctors by specialty/location", "Description": "The system shall allow searching doctors by specialty, name, rating, and location.", "RelatedStakeholder": "SH-01", "Priority": "High", "Status": "Proposed", "RelatedUseCase": "UC-02"},
    {"ReqID": "FR-003", "Title": "Book an appointment online", "Description": "The system shall allow patients to select a doctor and an available time slot to book.", "RelatedStakeholder": "SH-01", "Priority": "High", "Status": "Approved", "RelatedUseCase": "UC-03"},
    {"ReqID": "FR-004", "Title": "Cancel / reschedule an appointment", "Description": "The system shall allow patients to cancel or reschedule at least 2 hours in advance.", "RelatedStakeholder": "SH-01", "Priority": "High", "Status": "Approved", "RelatedUseCase": "UC-04"},
    {"ReqID": "FR-005", "Title": "Receptionist confirms appointment", "Description": "The system shall allow the receptionist to confirm or reject a booking request.", "RelatedStakeholder": "SH-03", "Priority": "Medium", "Status": "Proposed", "RelatedUseCase": "UC-05"},
    {"ReqID": "FR-006", "Title": "Appointment reminder via email/SMS", "Description": "The system shall automatically send reminders 24 hours and 1 hour in advance.", "RelatedStakeholder": "SH-01", "Priority": "Medium", "Status": "Proposed", "RelatedUseCase": "UC-06"},
    {"ReqID": "FR-007", "Title": "Doctor views and updates medical records", "Description": "The system shall allow doctors to view visit history and record new results.", "RelatedStakeholder": "SH-02", "Priority": "High", "Status": "Approved", "RelatedUseCase": "UC-07"},
    {"ReqID": "FR-008", "Title": "Drug interaction / allergy warning", "Description": "The system shall warn doctors when a prescription conflicts with a known allergy.", "RelatedStakeholder": "SH-02", "Priority": "High", "Status": "Proposed", "RelatedUseCase": "UC-08"},
    {"ReqID": "FR-009", "Title": "Manage doctor and department catalog", "Description": "The system shall allow admins to add/edit/remove doctor and specialty records.", "RelatedStakeholder": "SH-04", "Priority": "Medium", "Status": "Approved", "RelatedUseCase": "UC-09"},
    {"ReqID": "FR-010", "Title": "Visit statistics report", "Description": "The system shall export reports on booking/cancellation counts by day/month.", "RelatedStakeholder": "SH-04", "Priority": "Low", "Status": "Proposed", "RelatedUseCase": "UC-10"},
    {"ReqID": "FR-011", "Title": "Verify health insurance coverage", "Description": "The system shall call a partner insurance API to check policy validity.", "RelatedStakeholder": "SH-05", "Priority": "Medium", "Status": "Proposed", "RelatedUseCase": "UC-11"},
    {"ReqID": "FR-012", "Title": "Role-based access control (RBAC)", "Description": "The system shall restrict features by role: patient/doctor/receptionist/admin.", "RelatedStakeholder": "SH-06", "Priority": "High", "Status": "Approved", "RelatedUseCase": "UC-12"}
]

FALLBACK_NFRS = [
    {"NFRID": "NFR-001", "AttributeName": "Performance", "ISO25010Category": "Performance", "SMARTMeasurementCriterion": "Doctor-search page response time <= 2s with 500 concurrent users.", "VerificationMethod": "Load testing", "Priority": "High"},
    {"NFRID": "NFR-002", "AttributeName": "Availability", "ISO25010Category": "Availability", "SMARTMeasurementCriterion": "The system shall achieve >= 99.5% monthly uptime (excluding scheduled maintenance).", "VerificationMethod": "30-day uptime monitoring", "Priority": "High"},
    {"NFRID": "NFR-003", "AttributeName": "Security", "ISO25010Category": "Security", "SMARTMeasurementCriterion": "Medical record data shall be encrypted with AES-256 at rest and TLS 1.2+ in transit.", "VerificationMethod": "Configuration review + penetration test", "Priority": "High"},
    {"NFRID": "NFR-004", "AttributeName": "Data privacy", "ISO25010Category": "Privacy/Compliance", "SMARTMeasurementCriterion": "The system shall follow data-minimization principles for personal data.", "VerificationMethod": "Compliance checklist review", "Priority": "High"},
    {"NFRID": "NFR-005", "AttributeName": "Scalability", "ISO25010Category": "Scalability", "SMARTMeasurementCriterion": "The system shall handle 3x booking volume growth over 12 months without architecture changes.", "VerificationMethod": "Incremental load testing", "Priority": "Medium"},
    {"NFRID": "NFR-006", "AttributeName": "Usability", "ISO25010Category": "Usability", "SMARTMeasurementCriterion": "A first-time user shall complete their first booking in <= 3 minutes without guidance.", "VerificationMethod": "Usability testing", "Priority": "Medium"},
    {"NFRID": "NFR-007", "AttributeName": "Safety", "ISO25010Category": "Safety", "SMARTMeasurementCriterion": "The system shall raise a conflict warning within <= 1 second when a doctor double-booking is detected.", "VerificationMethod": "Booking-conflict scenario testing", "Priority": "High"},
    {"NFRID": "NFR-008", "AttributeName": "Recoverability", "ISO25010Category": "Reliability", "SMARTMeasurementCriterion": "The system shall recover booking data within 15 minutes after an incident (RPO<=5min, RTO<=15min).", "VerificationMethod": "Disaster-recovery drill", "Priority": "High"},
    {"NFRID": "NFR-009", "AttributeName": "Maintainability", "ISO25010Category": "Maintainability", "SMARTMeasurementCriterion": "Source code shall achieve >= 80% unit-test coverage for the booking module.", "VerificationMethod": "CI coverage report", "Priority": "Medium"},
    {"NFRID": "NFR-010", "AttributeName": "Compatibility", "ISO25010Category": "Compatibility/Portability", "SMARTMeasurementCriterion": "The UI shall work correctly on Chrome, Safari, Edge versions released in the last 2 years.", "VerificationMethod": "Cross-browser testing", "Priority": "Low"}
]


def load_csv(name):
    candidate_dirs = [
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "datasets"),
        os.path.join(os.path.dirname(__file__), "..", "datasets"),
        os.path.join(os.path.dirname(__file__), "datasets"),
        os.path.dirname(__file__),
    ]
    for d in candidate_dirs:
        p = os.path.join(d, name)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return list(csv.DictReader(f))
    
    # Fallback to embedded data if files not found
    if "stakeholder" in name:
        return FALLBACK_STAKEHOLDERS
    elif "nonfunctional" in name:
        return FALLBACK_NFRS
    elif "functional" in name:
        return FALLBACK_FRS
    return []


def escape_latex(text):
    """Escapes special LaTeX characters in plain text."""
    if not text:
        return ""
    conv = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
        "<=": r"$\le$",
        ">=": r"$\ge$",
        "<": r"$<$",
        ">": r"$>$",
    }
    regex = re.compile("|".join(re.escape(k) for k in conv.keys()))
    return regex.sub(lambda match: conv[match.group(0)], str(text))


def section_glossary(frs, nfrs, doc_format="markdown"):
    """
    Scans functional and non-functional requirements for uppercase acronyms (2-5 letters)
    and constructs a comprehensive glossary table/list.
    """
    abbrevs = set()
    for r in frs + nfrs:
        text = " ".join(r.values())
        abbrevs.update(re.findall(r"\b[A-Z]{2,5}\b", text))
    
    # Ensure key domain terms are included
    for core_term in ["FR", "NFR", "RBAC", "SRS"]:
        abbrevs.add(core_term)

    sorted_abbrevs = sorted(abbrevs)

    if doc_format == "latex":
        lines = [
            r"\subsection{Definitions, Acronyms, Abbreviations}",
            r"\begin{longtable}{|l|p{12cm}|}",
            r"\hline",
            r"\textbf{Term / Acronym} & \textbf{Definition} \\ \hline",
            r"\endhead",
        ]
        for a in sorted_abbrevs:
            defn = GLOSSARY_DEFINITIONS.get(a, "Acronym identified from system requirements; definition established per system scope.")
            lines.append(f"{escape_latex(a)} & {escape_latex(defn)} \\\\ \\hline")
        lines.append(r"\end{longtable}" + "\n")
        return "\n".join(lines)
    else:
        lines = ["### 1.3 Definitions, Acronyms, Abbreviations\n"]
        for a in sorted_abbrevs:
            defn = GLOSSARY_DEFINITIONS.get(a, "Domain acronym identified from requirements.")
            lines.append(f"- **{a}**: {defn}")
        lines.append("")
        return "\n".join(lines) + "\n"


def section_scope(frs, nfrs, doc_format="markdown"):
    if doc_format == "latex":
        lines = [
            r"\section{Introduction}",
            r"\subsection{Purpose}",
            r"This document specifies the software requirements for \textbf{MedBook} -- an "
            r"online medical appointment booking platform serving patients, doctors, "
            r"receptionists, and hospital administrators.",
            r"",
            r"\subsection{Scope}",
            r"The system supports: doctor search, book/cancel/reschedule appointments, "
            r"medical record management, safety warnings, insurance verification, and "
            r"operational reporting.",
            r"",
            section_glossary(frs, nfrs, doc_format="latex"),
            r"\subsection{References}",
            r"\begin{itemize}",
            r"\item Karl Wiegers, Joy Beatty (2013), \textit{Software Requirements}, 3rd ed.",
            r"\item ISO/IEC/IEEE 29148:2018 -- Requirements Engineering.",
            r"\end{itemize}",
            r"",
        ]
        return "\n".join(lines) + "\n"
    else:
        lines = [
            "## 1. Introduction\n",
            "### 1.1 Purpose\n",
            "This document specifies the software requirements for **MedBook** -- an "
            "online medical appointment booking platform serving patients, doctors, "
            "receptionists, and hospital administrators.\n",
            "### 1.2 Scope\n",
            "The system supports: doctor search, book/cancel/reschedule appointments, "
            "medical record management, safety warnings, insurance verification, and "
            "operational reporting.\n",
            section_glossary(frs, nfrs, doc_format="markdown"),
            "### 1.4 References\n",
            "- Karl Wiegers, Joy Beatty (2013), *Software Requirements*, 3rd ed.\n",
            "- ISO/IEC/IEEE 29148:2018 -- Requirements Engineering\n",
        ]
        return "\n".join(lines) + "\n"


def section_overall_description(stakeholders, doc_format="markdown"):
    if doc_format == "latex":
        lines = [
            r"\section{Overall Description}",
            r"\subsection{Product Perspective}",
            r"MedBook is a web/mobile system connecting patients to healthcare "
            r"providers, replacing the traditional phone-based booking process.",
            r"",
            r"\subsection{User Classes and Characteristics}",
            r"\begin{longtable}{|l|l|p{9cm}|}",
            r"\hline",
            r"\textbf{ID} & \textbf{User Class} & \textbf{Primary Role / Benefit} \\ \hline",
            r"\endhead",
        ]
        for sh in stakeholders:
            lines.append(f"{escape_latex(sh['StakeholderID'])} & {escape_latex(sh['StakeholderName'])} & {escape_latex(sh['ExpectedBenefit'])} \\\\ \\hline")
        lines.append(r"\end{longtable}")
        lines.append(r"")
        lines.append(r"\subsection{General Constraints}")
        lines.append(r"Must comply with personal health-data protection regulations; limited infrastructure budget for phase 1; 4-month delivery timeline.")
        lines.append(r"")
        return "\n".join(lines) + "\n"
    else:
        lines = [
            "## 2. Overall Description\n",
            "### 2.1 Product Perspective\n",
            "MedBook is a web/mobile system connecting patients to healthcare "
            "providers, replacing the traditional phone-based booking process.\n",
            "### 2.2 User Classes and Characteristics\n",
            "| ID | User | Primary Role |",
            "|---|---|---|",
        ]
        for sh in stakeholders:
            lines.append(f"| {sh['StakeholderID']} | {sh['StakeholderName']} | {sh['ExpectedBenefit']} |")
        lines.append("\n### 2.3 General Constraints\n")
        lines.append("Must comply with personal health-data protection regulations; "
                     "limited infrastructure budget for phase 1; 4-month delivery timeline.\n")
        return "\n".join(lines) + "\n"


def section_functional(frs, doc_format="markdown"):
    if doc_format == "latex":
        lines = [r"\section{Functional Requirements}"]
        for fr in frs:
            lines.append(r"\subsection{" + escape_latex(fr['ReqID']) + r" -- " + escape_latex(fr['Title']) + r"}")
            lines.append(r"\begin{itemize}")
            lines.append(r"\item \textbf{Description}: " + escape_latex(fr['Description']))
            lines.append(r"\item \textbf{Related stakeholder}: " + escape_latex(fr['RelatedStakeholder']))
            lines.append(r"\item \textbf{Priority}: " + escape_latex(fr['Priority']))
            lines.append(r"\item \textbf{Status}: " + escape_latex(fr['Status']))
            lines.append(r"\item \textbf{Related use case}: " + escape_latex(fr['RelatedUseCase']))
            lines.append(r"\end{itemize}")
            lines.append(r"")
        return "\n".join(lines) + "\n"
    else:
        lines = ["## 3. Functional Requirements\n"]
        for fr in frs:
            lines.append(f"### {fr['ReqID']} -- {fr['Title']}")
            lines.append(f"- **Description**: {fr['Description']}")
            lines.append(f"- **Related stakeholder**: {fr['RelatedStakeholder']}")
            lines.append(f"- **Priority**: {fr['Priority']}")
            lines.append(f"- **Status**: {fr['Status']}")
            lines.append(f"- **Related use case**: {fr['RelatedUseCase']}\n")
        return "\n".join(lines) + "\n"


def section_nonfunctional(nfrs, doc_format="markdown"):
    if doc_format == "latex":
        lines = [r"\section{Non-functional Requirements}"]
        for n in nfrs:
            lines.append(r"\subsection{" + escape_latex(n['NFRID']) + r" -- " + escape_latex(n['AttributeName']) + r" (" + escape_latex(n['ISO25010Category']) + r")}")
            lines.append(r"\begin{itemize}")
            lines.append(r"\item \textbf{SMART measurement criterion}: " + escape_latex(n['SMARTMeasurementCriterion']))
            lines.append(r"\item \textbf{Verification method}: " + escape_latex(n['VerificationMethod']))
            lines.append(r"\item \textbf{Priority}: " + escape_latex(n['Priority']))
            lines.append(r"\end{itemize}")
            lines.append(r"")
        return "\n".join(lines) + "\n"
    else:
        lines = ["## 4. Non-functional Requirements\n"]
        for n in nfrs:
            lines.append(f"### {n['NFRID']} -- {n['AttributeName']} ({n['ISO25010Category']})")
            lines.append(f"- **SMART measurement criterion**: {n['SMARTMeasurementCriterion']}")
            lines.append(f"- **Verification method**: {n['VerificationMethod']}")
            lines.append(f"- **Priority**: {n['Priority']}\n")
        return "\n".join(lines) + "\n"


def section_design_constraints(doc_format="markdown"):
    """
    Generates Section 5: Design Constraints as required by Lab 03.
    Includes Technical, Legal/Regulatory, and Timeline/Budget constraints.
    """
    if doc_format == "latex":
        return (
            r"\section{Design Constraints}" "\n"
            r"\begin{enumerate}" "\n"
            r"\item \textbf{Technical Constraint}: The system must be developed using a RESTful microservices architecture, with all APIs communicating via JSON over HTTPS. The user interface must support responsive web design ensuring usability on mobile screens with a minimum viewport width of 360px. Electronic medical data integration must adhere to HL7/FHIR release 4 standards." "\n"
            r"\item \textbf{Legal and Regulatory Constraint}: The system and databases must be hosted on cloud infrastructure situated within data centers in Vietnam, strictly complying with Decree 13/2023/ND-CP on Personal Data Protection and the Vietnam Law on Medical Examination and Treatment (2023). All electronic medical records and PII (Personally Identifiable Information) must be encrypted using AES-256 at rest and TLS 1.3 in transit." "\n"
            r"\item \textbf{Timeline and Budget Constraint}: The MVP (Minimum Viable Product) release must be delivered within 4 months from project kickoff. Cloud infrastructure hosting costs for Phase 1 must not exceed the approved operational budget limit of 150 million VND per annum." "\n"
            r"\end{enumerate}" "\n"
        )
    else:
        return (
            "## 5. Design Constraints\n\n"
            "1. **Technical Constraint**: The system must be developed using a RESTful microservices architecture, with all APIs communicating via JSON over HTTPS. The user interface must support responsive web design ensuring usability on mobile screens with a minimum viewport width of 360px. Electronic medical data integration must adhere to HL7/FHIR release 4 standards.\n\n"
            "2. **Legal and Regulatory Constraint**: The system and databases must be hosted on cloud infrastructure situated within data centers in Vietnam, strictly complying with Decree 13/2023/ND-CP on Personal Data Protection and the Vietnam Law on Medical Examination and Treatment (2023). All electronic medical records and PII (Personally Identifiable Information) must be encrypted using AES-256 at rest and TLS 1.3 in transit.\n\n"
            "3. **Timeline and Budget Constraint**: The MVP (Minimum Viable Product) release must be delivered within 4 months from project kickoff. Cloud infrastructure hosting costs for Phase 1 must not exceed the approved operational budget limit of 150 million VND per annum.\n"
        )


def generate_document(doc_format="markdown"):
    frs = load_csv("functional_requirements.csv")
    nfrs = load_csv("nonfunctional_requirements.csv")
    stakeholders = load_csv("stakeholders.csv")

    if doc_format == "latex":
        out_filename = "SRS_MedBook_generated.tex"
        out_path = os.path.join(os.path.dirname(__file__), out_filename)
        doc = [
            r"% Auto-generated SRS in LaTeX format - Lab 03",
            r"% Structure reference: ISO/IEC/IEEE 29148:2018",
            r"\documentclass[11pt,a4paper]{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[margin=1in]{geometry}",
            r"\usepackage{longtable}",
            r"\usepackage{hyperref}",
            r"\usepackage{amsmath}",
            r"\title{\textbf{Software Requirements Specification (SRS)\\MedBook -- Online Medical Appointment Booking System}}",
            r"\author{MedBook Engineering Team}",
            f"\\date{{Generated on: {date.today().isoformat()} (v1.0 auto-generated)}}",
            r"\begin{document}",
            r"\maketitle",
            r"\tableofcontents",
            r"\newpage",
            section_scope(frs, nfrs, doc_format="latex"),
            section_overall_description(stakeholders, doc_format="latex"),
            section_functional(frs, doc_format="latex"),
            section_nonfunctional(nfrs, doc_format="latex"),
            section_design_constraints(doc_format="latex"),
            r"\end{document}",
        ]
        content = "\n".join(doc)
    else:
        out_filename = "SRS_MedBook_generated.md"
        out_path = os.path.join(os.path.dirname(__file__), out_filename)
        doc = [
            "# Software Requirements Specification (SRS)\n",
            "**Project:** MedBook -- Online Medical Appointment Booking System  ",
            "**Version:** 1.0 (auto-generated)  ",
            f"**Generated on:** {date.today().isoformat()}  ",
            "**Structure reference standard:** ISO/IEC/IEEE 29148:2018\n",
            section_scope(frs, nfrs, doc_format="markdown"),
            section_overall_description(stakeholders, doc_format="markdown"),
            section_functional(frs, doc_format="markdown"),
            section_nonfunctional(nfrs, doc_format="markdown"),
            section_design_constraints(doc_format="markdown"),
        ]
        content = "\n".join(doc)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] SRS generated ({doc_format}): {out_path}")
    print(f"  - {len(frs)} functional requirements")
    print(f"  - {len(nfrs)} non-functional requirements")
    print(f"  - {len(stakeholders)} stakeholder/user groups")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Auto-generate MedBook SRS document in Markdown or LaTeX format.")
    parser.add_argument(
        "--format",
        choices=["markdown", "latex"],
        default="markdown",
        help="Target output format: 'markdown' (.md) or 'latex' (.tex). Default is 'markdown'."
    )
    args = parser.parse_args()
    generate_document(doc_format=args.format)


if __name__ == "__main__":
    main()

