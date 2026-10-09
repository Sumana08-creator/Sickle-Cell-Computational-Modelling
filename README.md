\# Computational Modelling of Sickle Cell Disease: HbS Solubility



\## Project Overview



This project implements a numerical model to investigate the relationship between oxygen binding and the solubility of sickle haemoglobin (HbS), based on the study by Henry et al. (2020), published in PNAS.



The project uses Python, SciPy, NumPy and Matplotlib to solve a differential equation and compare alternative assumptions about oxygen binding in haemoglobin fibres.



\*\*Important:\*\* Numerical completion and automated software tests do not establish scientific validity. The initial solubility concentration is provisional, and experimental validation remains outstanding.



\## Scientific Reference



Henry et al. (2020).



\*Allosteric control of hemoglobin S fiber formation by oxygen and its relation to the pathophysiology of sickle cell disease.\*



Proceedings of the National Academy of Sciences (PNAS).



https://pmc.ncbi.nlm.nih.gov/articles/PMC7334536/



\## Research Objectives



\- Implement the published HbS solubility equation numerically.

\- Model oxygen saturation of free haemoglobin using the MWC framework.

\- Compare alternative assumptions for oxygen binding in haemoglobin fibres.

\- Explore the effect of oxygen saturation on calculated HbS solubility.

\- Develop reproducible computational workflows and automated tests.

\- Establish a framework for future comparison with published experimental measurements.



\## Models Implemented



\### 1. Noncooperative Fibre-Binding Model



Uses the fibre oxygen-binding parameter:



\- `K\_P = 0.0059 torr⁻¹`



\### 2. MWC Fibre-Binding Comparison



Uses:



\- `K\_T = 0.016 torr⁻¹`



\### 3. TTS Fibre-Binding Model



Uses the current implementation's parameters:



\- `K\_t = 0.0036 torr⁻¹`

\- `K\_r = 3.7 torr⁻¹`

\- `l\_T = 840`



These implementations are computational comparisons. Their equations and parameterisation must be checked against the original publication before their scientific accuracy can be claimed.



\## Computational Methods



The main model uses:



\- Python

\- NumPy

\- SciPy's `solve\_ivp`

\- The Radau numerical integration method

\- Matplotlib for figures

\- CSV files for numerical output

\- Pytest for automated tests

\- GitHub Actions for continuous integration



The numerical solver calculates solubility over an oxygen-pressure range and exports the calculated curves.



\## Repository Structure



```text

Sickle-Cell-Computational-Modelling/

│

├── complete\_solubility\_model.py

├── compare\_model\_error.py

├── experimental\_comparison.py

├── figure3\_approximate\_data.csv

├── test\_solubility\_model.py

├── README.md

└── .github/

&#x20;   └── workflows/

&#x20;       └── tests.yml



\## Scientific Validation Status



The model currently compares three fibre oxygen-binding assumptions:

\- Measured noncooperative fibre binding

\- MWC fibre binding

\- TTS fibre binding



The initial reference solubility (0.178375 g/mL) remains provisional.



The generated curves are model predictions, not experimental measurements.

The model has not yet been scientifically validated against digitised

experimental data from Henry et al. (2020).



\### Next Validation Steps

1\. Verify the initial reference solubility against the original study.

2\. Obtain reliable experimental data from the authors or published figures.

3\. Compare model predictions with verified measurements.

4\. Calculate MAE and RMSE only after obtaining trustworthy data.

5\. Document assumptions, limitations, and reproducibility.

