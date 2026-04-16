# Literature Review: Space Debris Collision Avoidance

## Team Details
* Mayank Goyal (Team Leader), Roll No: 24293916114, Email: mayankgoyal18052005@ce.du.ac.in
* Abeer bartaria, Roll No: 23293916061, Email: abeerbartaria@ce.du.ac.in
* Ansh Kumar, Roll No: 24293916052, Email: Anshk3671@gmail.com
* Vansh Saharawat, Roll No: 24293916089, Email: vanshsahara@ce.du.ac.in

## Scope
This review covers conjunction assessment and collision avoidance in Earth orbit, aligned with our EDA domain.

## Literature Collection (5 Works)

### 1) Chan (2000)
Source: Journal of Guidance, Control, and Dynamics
DOI: https://doi.org/10.2514/2.4611
* Problem statement: How to compute collision risk rigorously for close approaches.
* Dataset used: Cataloged space objects and encounter uncertainty states.
* Methods applied: Analytical probability of collision using encounter geometry and covariance.
* Key findings: Probability-based thresholds are better than simple geometric screening rules.

### 2) Newman et al. (2009)
Source: Acta Astronautica
DOI: https://doi.org/10.1016/j.actaastro.2009.10.005
* Problem statement: How to run robotic mission conjunction assessment in operations.
* Dataset used: U.S. tracking catalog conjunction products plus mission trajectory data.
* Methods applied: Multi-stage screening, escalation, analyst review, and maneuver planning.
* Key findings: Layered pipelines reduce false alerts and support practical mission decisions.

### 3) Flohrer et al. (2009)
Source: Advances in Space Research
DOI: https://doi.org/10.1016/j.asr.2009.04.012
* Problem statement: How to identify and assess high-risk conjunction events for ESA missions.
* Dataset used: Daily screenings of tracked objects with orbit prediction and uncertainty data.
* Methods applied: Automated filtering, manual refinement, trend checks, and decision gates.
* Key findings: Staged assessment improves safety while limiting unnecessary maneuvers.

### 4) Braun et al. (2016)
Source: CEAS Space Journal
DOI: https://doi.org/10.1007/s12567-016-0119-3
* Problem statement: How to scale operational collision support across many missions.
* Dataset used: Operational conjunction streams, OD updates, and mission constraints.
* Methods applied: Standardized support workflow and mission-tailored risk handling.
* Key findings: Institutional support improves consistency, but upstream uncertainty remains a major limiter.

### 5) Weigel et al. (2024)
Source: Journal of Guidance, Control, and Dynamics
DOI: https://doi.org/10.2514/1.G008245
* Problem statement: How to make covariance models realistic enough for robust CA decisions.
* Dataset used: Historical mission orbit-estimation and covariance behavior data.
* Methods applied: Consider-covariance calibration and comparative risk-ranking experiments.
* Key findings: Better covariance realism improves event ranking and maneuver timing quality.

## Comparative Analysis with Our EDA

### Our EDA snapshot
* SATCAT cleaned: 68,330 objects.
* UCS cleaned: 7,563 satellites.
* Kelvins labels: 100 records, with long trajectory subsets (deb_train, deb_test, sat).
* UCS analysis shows LEO-heavy distribution and Communications-dominant mission purpose.
* Launch trend rises sharply in recent years, especially around 2020 to 2022.

### Similarities with literature
* Literature and our EDA both indicate strong growth in orbital traffic and conjunction burden.
* LEO concentration in our UCS data matches operational studies where LEO dominates conjunction workload.
* Data quality and uncertainty are central in both; our cleaning steps already show mixed formats and missingness that impact downstream risk scoring.

### Differences from literature
* Literature mostly uses mission-grade conjunction products (for example CDMs and refined covariance chains), while our current datasets are catalog-level and benchmark-oriented.
* Literature includes maneuver authority and mission constraints; our current pipeline is pre-decision and analytics-focused.
* Recent covariance-optimization methods require historical orbit-determination streams not present in our current data bundle.

## Research Gaps and Future Work

### Gap 1: Public end-to-end CA benchmarks are limited
Most strong systems are agency internal. Reproducible public benchmarks that cover screening, ranking, and maneuver recommendation are still limited.

### Gap 2: Screening and maneuver planning are often disconnected
Many workflows optimize each stage separately. A unified objective from first filter to final maneuver can reduce inconsistency.

### Gap 3: Uncertainty treatment is still uneven
Catalog-level studies often under-model covariance realism. Operational papers show uncertainty quality strongly changes decisions.

### Proposed next steps for our project
1. Build a two-stage CA pipeline on top of our processed SATCAT and UCS artifacts: fast screening plus refined probability scoring.
2. Add uncertainty-aware modeling inspired by modern covariance calibration work.
3. Evaluate with operationally meaningful metrics: false alert rate, unnecessary maneuver rate, and missed-danger events.
4. Publish a reproducible benchmark protocol with fixed scenario splits and reporting templates.

## References
1. Chan, F. K. (2000). Probability of Collision Between Space Objects. Journal of Guidance, Control, and Dynamics. https://doi.org/10.2514/2.4611
2. Newman, L. K., et al. (2009). The NASA robotic conjunction assessment process: Overview and operational experiences. Acta Astronautica. https://doi.org/10.1016/j.actaastro.2009.10.005
3. Flohrer, T., Krag, H., and Klinkrad, H. (2009). ESA’s process for the identification and assessment of high-risk conjunction events. Advances in Space Research. https://doi.org/10.1016/j.asr.2009.04.012
4. Braun, V., et al. (2016). Operational support to collision avoidance activities by ESA’s space debris office. CEAS Space Journal. https://doi.org/10.1007/s12567-016-0119-3
5. Weigel, M., et al. (2024). Optimizing Consider-Covariance Models for Realistic Orbit Errors and Application to Collision Avoidance. Journal of Guidance, Control, and Dynamics. https://doi.org/10.2514/1.G008245
