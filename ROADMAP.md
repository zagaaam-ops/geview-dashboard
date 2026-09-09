# 📡 Project Plus — Telecom Infrastructure PMO Roadmap

**Project Lead:** Rana Muhammad Zagham (PMP®)  
**System Architecture:** Enterprise Telecom Civil Works, BOQ, EW Governance & Subcontractor Platform  
**Last Updated:** September 2026  

---

## 🚦 Master Progress Tracker

| Phase | Description | Status | Target Deliverables |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Core Framework & Access Control** | 🟢 **COMPLETED** | RBAC Login, Project Plus Preloader, Multi-module Router, Layout Architecture |
| **Phase 2** | **Site Survey & Dynamic BOQ Engine** | 🟡 **IN PROGRESS** | Master Price Book, Site Survey Forms, Automated Site BOQ Generation |
| **Phase 3** | **Extra Works (EW) & Workflow Governance** | ⚪ **PLANNED** | Out-of-Scope EW Upload, Photo Evidence Logs, Multi-tier Approval Chain |
| **Phase 4** | **Vendor Portal & EVM Analytics** | ⚪ **PLANNED** | Subcontractor PO Tracking, Milestone Completion, SPI/CPI Earned Value Metrics, GIS |

---

## 📝 Phase Breakdown & Feature Backlog

### 🟢 Phase 1: Foundation & RBAC Governance [DONE]
- [x] **Project Plus Preloader:** Fullpage animated telecom tower and signal preloader with copyright footer.
- [x] **Enterprise Authentication:** Login portal supporting role-based perspectives (PM, Civil Lead, Vendor, Finance, HR).
- [x] **Dynamic Module Router:** `runpy` execution pipeline preventing app crashes across all 22 sub-modules.
- [x] **Repository Environment:** GitHub & Streamlit Cloud integration setup.

---

### 🟡 Phase 2: Site Survey & Dynamic BOQ Engine [CURRENT FOCUS]
- [ ] **Master Price Book:** Database of standardized telecom civil works items, units, and base rates.
- [ ] **Site Survey Input Forms:** Field input module capturing tower type, foundation volume, soil conditions, fencing, and power requirements.
- [ ] **Automated Site BOQ Generator:** Algorithmic compilation of site-specific Bills of Quantities mapped to client contracts.
- [ ] **BOQ Export Module:** Exporting generated BOQ to structured PDF/Excel for client submission.

---

### ⚪ Phase 3: Extra Works (EW) & Workflow Governance [NEXT]
- [ ] **Extra Work (EW) Request Portal:** Civil lead interface to request out-of-scope site variations with photographic proof.
- [ ] **Sequential Approval Engine:**
  $$\text{Field/Civil Engineer} \longrightarrow \text{Project Manager Verification} \longrightarrow \text{Finance Budget Sign-Off}$$
- [ ] **Audit Trail & Logs:** Immutable, time-stamped history of changes, approvals, and rejections per site.

---

### ⚪ Phase 4: Subcontractor Portal, EVM & GIS [UPCOMING]
- [ ] **Vendor Portal:** Subcontractor dashboard for assigned POs, site civil completion sign-offs, and invoice tracking.
- [ ] **Earned Value Management (EVM):** Automated calculation of project performance:
  - $\text{SPI} = \frac{\text{EV}}{\text{PV}}$
  - $\text{CPI} = \frac{\text{EV}}{\text{AC}}$
- [ ] **GIS Site Mapping:** Interactive spatial map showing live civil construction statuses across tower locations.

---

> *Note: This roadmap is maintained automatically. Any addition, modification, or completion of tasks will be updated here to keep software development strictly aligned with PMO standards.*
