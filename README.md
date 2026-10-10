\# Computational Modelling of Sickle Cell Disease: HbS Solubility



\## 1. Project Overview



This project implements a numerical model to investigate the relationship between oxygen binding and the solubility of sickle haemoglobin (HbS), based on Henry et al. (2020), published in the \*Proceedings of the National Academy of Sciences (PNAS)\*.



The project uses Python, NumPy, SciPy, and Matplotlib to solve a differential equation and compare alternative assumptions about oxygen binding in haemoglobin fibres.



The project includes:

\- Numerical implementation of the solubility model.

\- Comparison of three fibre-binding formulations.

\- Starting-concentration sensitivity analysis.

\- Numerical integration robustness testing.

\- Automated software tests.

\- GitHub Actions continuous integration.

\- CSV outputs and visualisations.



\*\*Scientific limitation:\*\* Numerical completion, automated tests, and numerical convergence do not establish biological accuracy. The initial solubility concentration remains provisional, and experimental validation is outstanding.



\## 2. Scientific Reference



Henry et al. (2020).



\*Allosteric control of hemoglobin S fiber formation by oxygen and its relation to the pathophysiology of sickle cell disease.\*



Proceedings of the National Academy of Sciences.



Publication: https://pmc.ncbi.nlm.nih.gov/articles/PMC7334536/



The publication reports that underlying data not included in the article or supplementary information can be requested from the authors.



\## 3. Research Objectives



The project aims to:



1\. Implement the published HbS solubility equation numerically.

2\. Model oxygen saturation of free haemoglobin using the Monod–Wyman–Changeux (MWC) framework.

3\. Compare alternative assumptions for oxygen binding in haemoglobin fibres.

4\. Explore the effect of oxygen saturation on calculated HbS solubility.

5\. Investigate sensitivity to the provisional initial concentration.

6\. Evaluate numerical integration robustness.

7\. Establish a reproducible computational workflow.

8\. Prepare the model for comparison with verified experimental measurements.



\## 4. Models Implemented



\### 4.1 Noncooperative Fibre-Binding Model



This model uses a noncooperative fibre-binding parameter:



\- `K\_P = 0.0059 torr⁻¹`



\### 4.2 MWC Fibre-Binding Comparison



This formulation uses:



\- `K\_T = 0.016 torr⁻¹`



\### 4.3 TTS Fibre-Binding Model



The current implementation uses:



\- `K\_t = 0.0036 torr⁻¹`

\- `K\_r = 3.7 torr⁻¹`

\- `l\_T = 840`



These are computational comparisons. Their equations, parameterisation, and applicability must be verified against the original publication before scientific accuracy can be claimed.



\## 5. Computational Methods



The project uses:



| Component | Purpose |

|---|---|

| Python | Implementation |

| NumPy | Numerical arrays and calculations |

| SciPy | Differential-equation integration |

| Radau solver | Numerical integration |

| Matplotlib | Visualisation |

| CSV | Numerical result storage |

| Pytest | Automated testing |

| GitHub Actions | Continuous integration |



The main model calculates predicted solubility over an oxygen-pressure range and exports numerical results and comparison plots.



The reference solubility is currently:



`0.178375 g/mL`



\*\*This value is provisional and has not been independently verified for this implementation.\*\*



\## 6. Repository Structure



```text

Sickle-Cell-Computational-Modelling/

├── .github/

│   └── workflows/

│       └── tests.yml

├── complete\_solubility\_model.py

├── sensitivity\_analysis.py

├── sensitivity\_analysis\_results.csv

├── numerical\_robustness.py

├── numerical\_robustness\_results.csv

├── test\_solubility\_model.py

├── README.md

└── requirements.txt

```



The repository also contains supporting model implementations, comparison scripts, generated figures, and historical outputs.



Generated files and supplementary scripts may change as the project develops. The actual repository contents should be checked against this list.



\## 7. Starting-Concentration Sensitivity Analysis



\### 7.1 Method



The starting concentration was varied by ±10% around the provisional baseline of `0.178375 g/mL`.



The three tested values were approximately:



\- `0.160537 g/mL`

\- `0.178375 g/mL`

\- `0.196213 g/mL`



All three fibre-binding formulations were evaluated at a maximum oxygen pressure of 100 torr.



\### 7.2 Results



| Model | Initial Concentration (g/mL) | Predicted Solubility at 100 torr (g/mL) | Change from Baseline |

|---|---:|---:|---:|

| Measured fibre binding | 0.160537 | 0.597928 | -3.01% |

| Measured fibre binding | 0.178375 | 0.616462 | 0.00% |

| Measured fibre binding | 0.196213 | 0.638196 | +3.53% |

| MWC fibre binding | 0.160537 | 0.484420 | -2.84% |

| MWC fibre binding | 0.178375 | 0.498586 | 0.00% |

| MWC fibre binding | 0.196213 | 0.512625 | +2.82% |

| TTS fibre binding | 0.160537 | 0.566760 | -2.72% |

| TTS fibre binding | 0.178375 | 0.582596 | 0.00% |

| TTS fibre binding | 0.196213 | 0.599310 | +2.87% |



\### 7.3 Interpretation



All three models respond to changes in the initial concentration.



Changing the initial value by ±10% changes the predicted final solubility by approximately 3%, with some differences between models and directions of change.



This demonstrates that the initial condition affects the numerical predictions.



However, this analysis does not establish whether the baseline concentration is biologically correct. Independent justification of the initial value remains necessary.



\*\*Output:\*\* `sensitivity\_analysis\_results.csv`



\## 8. Numerical Integration Robustness



\### 8.1 Method



Numerical robustness was assessed by running all three models with progressively tighter relative and absolute integration tolerances.



| Run | Relative Tolerance | Absolute Tolerance |

|---|---:|---:|

| 1 | 1e-6 | 1e-8 |

| 2 | 1e-8 | 1e-10 |

| 3 | 1e-10 | 1e-12 |



The analysis used:

\- The Radau integration method.

\- A maximum pressure of 100 torr.

\- The same initial concentration for all runs.

\- A maximum integration step of 0.1 torr.



\### 8.2 Results



| Model | Final Solubility at 100 torr (g/mL) | Largest Relative Difference from First Run |

|---|---:|---:|

| Measured fibre binding | 0.6164622987 | Approximately 1.12e-12% |

| MWC fibre binding | 0.4985863992 | Approximately 1.24e-12% |

| TTS fibre binding | 0.5825957336 | Approximately 7.62e-13% |



All nine integrations completed successfully.



The final predictions were effectively unchanged when the solver tolerances were tightened. This supports numerical convergence for the tested configurations.



It does not demonstrate that the equations or parameters reproduce experimental measurements. It also does not establish robustness to every possible modelling assumption or parameter choice.



\*\*Output:\*\* `numerical\_robustness\_results.csv`



\## 9. Automated Testing and Continuous Integration



The project includes a Pytest suite checking:



\- Required project files.

\- Python syntax and model compilation.

\- Expected model-output structure.

\- Finite numerical outputs.

\- Presence of all three model formulations.

\- Comparison graph generation, when applicable.

\- Explicit identification of the provisional reference solubility.



The latest reported local test result was:



`7 passed`



GitHub Actions also reported a successful run for the numerical robustness analysis.



These tests check software behaviour and selected numerical properties. They are not tests of experimental predictive accuracy.



\## 10. Scientific Validation Status



\### Completed



\- Implemented three fibre-binding model formulations.

\- Generated numerical solubility predictions.

\- Compared sensitivity to the starting concentration.

\- Tested numerical integration using tighter tolerances.

\- Added automated tests.

\- Configured GitHub Actions.

\- Documented important scientific limitations.



\### Outstanding



\- Independently verify the initial reference solubility.

\- Obtain or digitise trustworthy experimental measurements.

\- Record experimental data provenance and uncertainty.

\- Compare predictions with independent measurements.

\- Calculate MAE, RMSE, or other appropriate error metrics only when verified reference data are available.

\- Investigate discrepancies between predictions and experimental results.



No experimental error metrics are currently reported because verified numerical measurements have not yet been supplied for comparison.



The model must therefore be described as \*\*numerically implemented and tested, but not yet experimentally validated\*\*.



\## 11. Reproducibility



Run these commands from the project directory.



\### Generate the main model outputs



```bash

python complete\_solubility\_model.py

```



\### Run the starting-concentration sensitivity analysis



```bash

python sensitivity\_analysis.py

```



\### Run the numerical robustness analysis



```bash

python numerical\_robustness.py

```



\### Run automated tests



```bash

python -m pytest -v

```



The analysis scripts produce CSV result files. The main model also generates its comparison outputs.



\## 12. Future Work



The next stages are to:



1\. Obtain the underlying experimental measurements from the original study or digitise published figures with documented uncertainty.

2\. Verify the initial concentration and all model parameters.

3\. Compare numerical predictions with independent measurements.

4\. Quantify predictive errors and uncertainty.

5\. Evaluate how sensitive conclusions are to parameter uncertainty.

6\. Extend the automated tests to cover individual equations and numerical boundary conditions.

7\. Update the scientific conclusions after experimental validation.



\## 13. Conclusion



This project provides a reproducible computational framework for exploring alternative oxygen-binding assumptions in HbS solubility modelling.



The current implementation demonstrates successful numerical integration, sensitivity to the provisional initial concentration, and strong convergence under the tested solver tolerances.



These are useful computational checks, but they do not establish biological accuracy. Experimental validation and independent verification of the initial condition remain essential before the predicted curves can be treated as scientifically validated results.

