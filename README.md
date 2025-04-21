# <p align="justify">The Crisis of Proteomics Reproducibility - A Bioinformatics Perspective<p>

## Abstract
<p align="justify">The lack of reproducibility in proteomics analyses, when viewed from a bioinformatics perspective, is a multifaceted issue stemming from several related challenges. A primary challenge is the inherent complexity and variability in proteomic datasets. Furthermore, the absence of standardized protocols and analysis pipelines across different laboratories and research groups compounds this problem, resulting in inconsistent practices and results. This review sets out to identify the primary obstacles and underlying causes contributing to the reproducibility crisis in proteomics analyses from a bioinformatics standpoint, while also exploring potential solutions. The review introduces a novel approach to assessing the reproducibility of proteomics data analysis tools. It involves evaluating key factors like documentation, version control, maintenance and community engagement employed by these tools and rating them on a scale of one to three, with three showing the greatest reproducibility. By scrutinizing these elements, developers can pinpoint areas requiring improvement and implement best practices to enhance reproducibility. Alternatively, users can select tools that are more likely to be reproducible for their analyses. This will hopefully facilitate the development of community-driven standards and guidelines for proteomics data analysis. Overall, we show that there is a reproducibility crisis in protein bioinformatics analyses, however, there are several solutions in play to improve this and the field will continue to develop. As it develops, it is essential to prioritize reproducibility and work towards establishing standardized protocols and guidelines for proteomics data analysis.<p>

### **Filtering criteria for proteomics tools extracted from Bio.tools registry**

![Filtering results](https://github.com/omicscodeathon/reproteomics/blob/main/figures/reproproteo_filter_April2025.png)

### How to reproduce this study

**Steps:**

1. Fetch the bio.tools metadata using keyword/s of interest using fetch_biotools.py (V1 or V2). If using multiple terms, separate each term by a comma e.g. protein,peptide,PPI etc. The Python script saves the file in json format.

2. Convert the json file to a tsv file using json2tsv.py (V1 or V2)

3. Filter the tsv file using filter_biotools.R (V1 or V2). You can adjust any of the filtering steps for your specific use.

4. Manually go through your tools and score each one using the criteria (reproteomics/output
/scoring_criteria.pdf). Use the exact descriptions given in the table to ensure that there are no issue with the scoring.

5. Score the filtered tool table using scoring_tools.R. These scores are based on the ten criteria associated with reproducibility.

### Differences between version 1 vs. version 2 of scripts

1. fetch_biotools.py: V1 does not extract citation information. V2 extracts citation information based on publications listed in bio.tools. 

2. json2tsv.py: V1 does not include citation information. V2 does include citation information.

3. filter_biotools.py: V1 does not filter the citations whereas V2 does. 

### **Team members:**

Coetzer, K.C(1), Aidoo, A.S(2), Adomako N.A(1,4), Ajiboye, I.O(5,6), Nortey H.(3), Okello, O.I(7), and Awe, O.I(8)

1. Department Biomedical Sciences, Division of Molecular Biology and Human Genetics, Stellenbosch University, Cape Town, South Africa

2. Department of Virology, Noguchi Memorial Institute for Medical Research, College of Health Sciences, University of Ghana, Legon, Accra, Ghana.

3. Department of Clinical Pathology, Noguchi Memorial Institute for Medical Research, College of Health Sciences, University of Ghana, Legon, Accra, Ghana.

4. Department of Molecular Medicine, School of Medicine and Dentistry, Kwame Nkrumah   University of Science and Technology, Kumasi, Ghana. 

5. Covenant Applied Informatics and Communication Africa Centre of Excellence (CApIC-ACE), Covenant University, Ota, Nigeria.

6. Department of Computer and Information Sciences, College of Science and Technology, Covenant University, Ota, Nigeria.

7. Department of Immunology and Molecular Biology, College of Health Sciences, School of Biomedical Sciences, Makerere University, Kampala, Uganda.

8. African Society for Bioinformatics and Computational Biology, Cape Town, South Africa.
