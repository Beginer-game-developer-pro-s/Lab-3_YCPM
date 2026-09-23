# Software Requirements Specification (SRS)

**Project:** MedBook -- Online Medical Appointment Booking System  
**Version:** 1.0 (auto-generated)  
**Generated on:** 2026-09-23  
**Structure reference standard:** ISO/IEC/IEEE 29148:2018

## 1. Introduction

### 1.1 Purpose

This document specifies the software requirements for **MedBook** -- an online medical appointment booking platform serving patients, doctors, receptionists, and hospital administrators.

### 1.2 Scope

The system supports: doctor search, book/cancel/reschedule appointments, medical record management, safety warnings, insurance verification, and operational reporting.

### 1.3 Definitions, Acronyms, Abbreviations

- **AES**: Advanced Encryption Standard - Symmetric encryption algorithm widely adopted to secure sensitive electronic data.
- **API**: Application Programming Interface - Set of subroutine definitions, protocols, and tools for building application software.
- **CI**: Continuous Integration - Practice of merging all developers' working copies to a shared mainline several times a day.
- **FR**: Functional Requirement - Specifies a function that a system or system component must be able to perform.
- **NFR**: Non-Functional Requirement - Specifies criteria that can be used to judge the operation of a system rather than specific behaviors.
- **OTP**: One-Time Password - A password that is valid for only one login session or transaction.
- **RBAC**: Role-Based Access Control - Access control mechanism based on roles assigned to users within an organization.
- **RPO**: Recovery Point Objective - Maximum acceptable amount of data loss measured in time.
- **RTO**: Recovery Time Objective - Maximum acceptable length of time that computer systems can be down.
- **SH**: Domain acronym identified from requirements.
- **SMS**: Short Message Service - Text messaging service component of most telephone, internet, and mobile device systems.
- **SRS**: Software Requirements Specification - Comprehensive description of the intended purpose and environment for software under development.
- **TLS**: Transport Layer Security - Cryptographic protocol designed to provide communications security over a computer network.
- **UC**: Domain acronym identified from requirements.
- **UI**: User Interface - Space where interactions between humans and machines occur.


### 1.4 References

- Karl Wiegers, Joy Beatty (2013), *Software Requirements*, 3rd ed.

- ISO/IEC/IEEE 29148:2018 -- Requirements Engineering


## 2. Overall Description

### 2.1 Product Perspective

MedBook is a web/mobile system connecting patients to healthcare providers, replacing the traditional phone-based booking process.

### 2.2 User Classes and Characteristics

| ID | User | Primary Role |
|---|---|---|
| SH-01 | Patient | Book appointments quickly, view history, receive reminders |
| SH-02 | Doctor | Manage schedule, view medical records, drug interaction warnings |
| SH-03 | Receptionist / Front desk staff | Confirm bookings, handle cancel/reschedule, assist walk-ins |
| SH-04 | Hospital Administrator | Manage doctor/department catalog, operational reports, access control |
| SH-05 | Health insurance provider | Verify insurance coverage, reconcile costs |
| SH-06 | Hospital IT department | Maintenance, performance monitoring, data security |
| SH-07 | Health regulatory authority | Compliance with health-data privacy and patient-safety regulations |
| SH-08 | Development team | Correctly understand and implement requirements, control scope |

### 2.3 General Constraints

Must comply with personal health-data protection regulations; limited infrastructure budget for phase 1; 4-month delivery timeline.


## 3. Functional Requirements

### FR-001 -- Patient account registration and login
- **Description**: The system shall allow patients to register via email/phone and verify via OTP.
- **Related stakeholder**: SH-01
- **Priority**: High
- **Status**: Proposed
- **Related use case**: UC-01

### FR-002 -- Search doctors by specialty/location
- **Description**: The system shall allow searching doctors by specialty, name, rating, and location.
- **Related stakeholder**: SH-01
- **Priority**: High
- **Status**: Proposed
- **Related use case**: UC-02

### FR-003 -- Book an appointment online
- **Description**: The system shall allow patients to select a doctor and an available time slot to book.
- **Related stakeholder**: SH-01
- **Priority**: High
- **Status**: Approved
- **Related use case**: UC-03

### FR-004 -- Cancel / reschedule an appointment
- **Description**: The system shall allow patients to cancel or reschedule at least 2 hours in advance.
- **Related stakeholder**: SH-01
- **Priority**: High
- **Status**: Approved
- **Related use case**: UC-04

### FR-005 -- Receptionist confirms appointment
- **Description**: The system shall allow the receptionist to confirm or reject a booking request.
- **Related stakeholder**: SH-03
- **Priority**: Medium
- **Status**: Proposed
- **Related use case**: UC-05

### FR-006 -- Appointment reminder via email/SMS
- **Description**: The system shall automatically send reminders 24 hours and 1 hour in advance.
- **Related stakeholder**: SH-01
- **Priority**: Medium
- **Status**: Proposed
- **Related use case**: UC-06

### FR-007 -- Doctor views and updates medical records
- **Description**: The system shall allow doctors to view visit history and record new results.
- **Related stakeholder**: SH-02
- **Priority**: High
- **Status**: Approved
- **Related use case**: UC-07

### FR-008 -- Drug interaction / allergy warning
- **Description**: The system shall warn doctors when a prescription conflicts with a known allergy.
- **Related stakeholder**: SH-02
- **Priority**: High
- **Status**: Proposed
- **Related use case**: UC-08

### FR-009 -- Manage doctor and department catalog
- **Description**: The system shall allow admins to add/edit/remove doctor and specialty records.
- **Related stakeholder**: SH-04
- **Priority**: Medium
- **Status**: Approved
- **Related use case**: UC-09

### FR-010 -- Visit statistics report
- **Description**: The system shall export reports on booking/cancellation counts by day/month.
- **Related stakeholder**: SH-04
- **Priority**: Low
- **Status**: Proposed
- **Related use case**: UC-10

### FR-011 -- Verify health insurance coverage
- **Description**: The system shall call a partner insurance API to check policy validity.
- **Related stakeholder**: SH-05
- **Priority**: Medium
- **Status**: Proposed
- **Related use case**: UC-11

### FR-012 -- Role-based access control (RBAC)
- **Description**: The system shall restrict features by role: patient/doctor/receptionist/admin.
- **Related stakeholder**: SH-06
- **Priority**: High
- **Status**: Approved
- **Related use case**: UC-12


## 4. Non-functional Requirements

### NFR-001 -- Performance (Performance)
- **SMART measurement criterion**: Doctor-search page response time <= 2s with 500 concurrent users.
- **Verification method**: Load testing
- **Priority**: High

### NFR-002 -- Availability (Availability)
- **SMART measurement criterion**: The system shall achieve >= 99.5% monthly uptime (excluding scheduled maintenance).
- **Verification method**: 30-day uptime monitoring
- **Priority**: High

### NFR-003 -- Security (Security)
- **SMART measurement criterion**: Medical record data shall be encrypted with AES-256 at rest and TLS 1.2+ in transit.
- **Verification method**: Configuration review + penetration test
- **Priority**: High

### NFR-004 -- Data privacy (Privacy/Compliance)
- **SMART measurement criterion**: The system shall follow data-minimization principles for personal data.
- **Verification method**: Compliance checklist review
- **Priority**: High

### NFR-005 -- Scalability (Scalability)
- **SMART measurement criterion**: The system shall handle 3x booking volume growth over 12 months without architecture changes.
- **Verification method**: Incremental load testing
- **Priority**: Medium

### NFR-006 -- Usability (Usability)
- **SMART measurement criterion**: A first-time user shall complete their first booking in <= 3 minutes without guidance.
- **Verification method**: Usability testing
- **Priority**: Medium

### NFR-007 -- Safety (Safety)
- **SMART measurement criterion**: The system shall raise a conflict warning within <= 1 second when a doctor double-booking is detected.
- **Verification method**: Booking-conflict scenario testing
- **Priority**: High

### NFR-008 -- Recoverability (Reliability)
- **SMART measurement criterion**: The system shall recover booking data within 15 minutes after an incident (RPO<=5min, RTO<=15min).
- **Verification method**: Disaster-recovery drill
- **Priority**: High

### NFR-009 -- Maintainability (Maintainability)
- **SMART measurement criterion**: Source code shall achieve >= 80% unit-test coverage for the booking module.
- **Verification method**: CI coverage report
- **Priority**: Medium

### NFR-010 -- Compatibility (Compatibility/Portability)
- **SMART measurement criterion**: The UI shall work correctly on Chrome, Safari, Edge versions released in the last 2 years.
- **Verification method**: Cross-browser testing
- **Priority**: Low


## 5. Design Constraints

1. **Technical Constraint**: The system must be developed using a RESTful microservices architecture, with all APIs communicating via JSON over HTTPS. The user interface must support responsive web design ensuring usability on mobile screens with a minimum viewport width of 360px. Electronic medical data integration must adhere to HL7/FHIR release 4 standards.

2. **Legal and Regulatory Constraint**: The system and databases must be hosted on cloud infrastructure situated within data centers in Vietnam, strictly complying with Decree 13/2023/ND-CP on Personal Data Protection and the Vietnam Law on Medical Examination and Treatment (2023). All electronic medical records and PII (Personally Identifiable Information) must be encrypted using AES-256 at rest and TLS 1.3 in transit.

3. **Timeline and Budget Constraint**: The MVP (Minimum Viable Product) release must be delivered within 4 months from project kickoff. Cloud infrastructure hosting costs for Phase 1 must not exceed the approved operational budget limit of 150 million VND per annum.
