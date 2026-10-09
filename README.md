\# Sickle Cell Computational Modelling



\### Exploring Oxygen-Dependent HbS Polymerisation and the Potential Role of Fetal Haemoglobin



\## 1. Project Overview



Sickle cell disease is a genetic blood disorder associated with the polymerisation of haemoglobin S (HbS), particularly under conditions of reduced oxygen availability.



This project explores how computational modelling can be used to investigate relationships between oxygen pressure, haemoglobin oxygen binding, HbS fibre formation, and solubility.



The project uses Python to implement mathematical models, perform numerical calculations, compare calculated results with approximate experimental data, and generate scientific visualisations.



\*\*Current status:\*\* Educational and exploratory computational research. The solubility model and its reference parameters require further verification and experimental validation.



\## 2. Research Objectives



The project investigates the following questions:



1\. How does oxygen partial pressure influence haemoglobin oxygen saturation?

2\. How does oxygen binding differ between free haemoglobin and haemoglobin fibres?

3\. How can mathematical equations be used to investigate oxygen-dependent HbS solubility?

4\. How can calculated results be compared with published experimental observations?

5\. What additional modelling and validation would be required to investigate the potential influence of fetal haemoglobin (HbF)?



\## 3. Scientific Foundation



The primary reference informing the project is:



Henry et al. (2020).



\*Allosteric control of hemoglobin S fiber formation by oxygen and its relation to the pathophysiology of sickle cell disease.\*



\*\*Journal:\*\* Proceedings of the National Academy of Sciences (PNAS)



\*\*DOI:\*\* 10.1073/pnas.1922004117



\*\*Full text:\*\* https://pmc.ncbi.nlm.nih.gov/articles/PMC7334536/



The publication investigates relationships between oxygen binding and the thermodynamic stability of HbS fibres.



This repository implements selected mathematical components informed by the research. It is not a complete or independently validated reproduction of the original study.



\## 4. Computational Methodology



\### 4.1 Oxygen Binding by Free Haemoglobin



The project implements the Monod–Wyman–Changeux (MWC) model to represent cooperative oxygen binding by haemoglobin.



\*\*Implementation:\*\* `mwc\_binding.py`



The model calculates fractional oxygen saturation across a range of oxygen partial pressures.



\### 4.2 Oxygen Binding by Haemoglobin Fibres



A separate mathematical relationship represents oxygen binding by haemoglobin fibres.



\*\*Implementation:\*\* `fiber\_binding.py`



The resulting predictions can be compared with the free-haemoglobin binding model.



\### 4.3 Binding Model Comparison



\*\*Implementation:\*\* `binding\_comparison.py`



\*\*Output:\*\* `binding\_comparison.png`



This component visualises differences between the calculated oxygen-binding behaviour of free haemoglobin and haemoglobin fibres.



\### 4.4 Numerical Integration



\*\*Implementation:\*\* `solubility\_integration.py`



SciPy provides numerical integration tools for evaluating mathematical relationships that may not have convenient analytical solutions.



Numerical integration can produce a result without establishing that the underlying equation, parameters, or biological assumptions are correct.



\### 4.5 HbS Solubility Modelling



\*\*Implementation:\*\* `complete\_solubility\_model.py`



This component numerically integrates a differential form of the HbS solubility relationship informed by Henry et al. (2020).



The implementation includes:



\- Published model parameters used by the calculation.

\- Free-haemoglobin oxygen saturation.

\- Haemoglobin fibre oxygen saturation.

\- A hard-sphere activity-coefficient derivative.

\- Numerical integration using SciPy.

\- CSV export of calculated values.

\- Graph generation.

\- Numerical failure and concentration-boundary checks.



\*\*Generated outputs:\*\*



\- `complete\_solubility\_results.csv`

\- `complete\_solubility\_curve.png`



The current implementation uses a provisional zero-oxygen reference concentration of 0.178375 g/mL.



This reference value and the resulting predictions require verification against appropriate original experimental data.



A successful numerical integration does not establish scientific validity.



\### 4.6 Experimental Comparison



\*\*Implementation:\*\* `experimental\_comparison.py`



This component compares the calculated solubility results with approximate values digitised from a graph.



\*\*Input files:\*\*



\- `figure3\_approximate\_data.csv`

\- `complete\_solubility\_results.csv`



\*\*Generated outputs:\*\*



\- `figure3\_experimental\_comparison.png`

\- `experimental\_comparison\_results.csv`

\- `experimental\_comparison\_report.txt`



The comparison script:



1\. Loads the experimental and calculated datasets.

2\. Identifies the oxygen-saturation and solubility columns.

3\. Converts solubility values into consistent units.

4\. Interpolates model predictions at experimental oxygen-saturation values.

5\. Calculates differences between predicted and approximate experimental values.

6\. Calculates mean absolute error (MAE).

7\. Calculates root mean square error (RMSE).

8\. Exports the comparison data, graph, and report.



The comparison is preliminary because the experimental points are approximate digitised estimates rather than verified raw measurements.



The calculated error metrics describe agreement with these approximate points only.



They must not be interpreted as definitive evidence of model accuracy.



\### 4.7 Empirical Solubility Model



\*\*Implementation:\*\* `empirical\_solubility\_model.py`



This component explores a separate empirical relationship for calculating solubility estimates across fractional oxygen saturation values.



\*\*Generated outputs:\*\*



\- `empirical\_solubility\_results.csv`

\- `empirical\_solubility\_curve\_new.png`



The equation and reference values require verification against their original sources before the estimates can be interpreted scientifically.



\## 5. Current Computational Results



The current solubility implementation completed numerical integration across 101 pressure points, from 0 to 100 torr.



The experimental comparison script also completed successfully using 11 approximate experimental points.



The reported preliminary comparison metrics were:



| Metric | Preliminary result |

|---|---:|

| Approximate experimental points | 11 |

| Calculated model points | 101 |

| Points compared | 11 |

| Mean absolute error (MAE) | 8.3544 mg/mL |

| Root mean square error (RMSE) | 14.9793 mg/mL |



These figures describe the output of the current implementation and comparison procedure.



They do not establish that the model accurately reproduces experimental biology.



The experimental dataset is approximate, and the zero-oxygen reference concentration remains provisional. Further equation verification, parameter verification, and comparison with reliable experimental measurements are required.



\## 6. Scientific Interpretation



The project demonstrates a computational workflow for translating selected mathematical relationships into Python, solving numerical equations, exporting data, and generating graphs.



The binding models provide a framework for exploring calculated oxygen-saturation behaviour.



The solubility implementation extends this workflow to a more complex relationship involving oxygen binding and concentration-dependent activity.



The experimental comparison provides an initial method for examining differences between calculated outputs and approximate observations.



However, a graph that visually follows approximate data does not independently establish that the underlying scientific model is correct.



The present work should therefore be regarded as exploratory computational modelling rather than a validated predictive model of sickle cell disease.



\## 7. Limitations



\### 7.1 Reference Concentration



The zero-oxygen reference concentration is provisional and requires verification against the original experimental source.



\### 7.2 Equation Verification



The implemented equations must be checked against the original publication, including mathematical notation, units, parameter definitions, and assumptions.



\### 7.3 Approximate Experimental Data



The current comparison uses approximate values digitised from a graph. These values may differ from the original experimental measurements.



\### 7.4 Numerical Stability



The solubility equation can approach a numerical boundary as concentration approaches the polymer concentration. Solver behaviour and sensitivity near this boundary require further investigation.



\### 7.5 Model Validation



Agreement with a small set of approximate points is insufficient to establish model validity. Reliable experimental measurements and a documented validation procedure are required.



\### 7.6 Fetal Haemoglobin



Although HbF is part of the research motivation, a quantitatively defined and validated implementation of its influence on HbS polymerisation remains future work.



\### 7.7 Clinical Interpretation



The current calculations do not provide patient-specific predictions, clinical recommendations, or treatment guidance.



\## 8. Future Development



Planned research directions include:



1\. Verify the mathematical equations against the original publication.

2\. Confirm the reference concentration and all parameter values.

3\. Obtain reliable experimental measurements for comparison.

4\. Improve the provenance and reproducibility of the experimental dataset.

5\. Evaluate numerical stability across the intended pressure and concentration ranges.

6\. Perform parameter-sensitivity analysis.

7\. Document model assumptions and units consistently.

8\. Develop and test a quantitative representation of HbF's potential influence on HbS polymerisation.

9\. Separate exploratory components from components that have been independently validated.

10\. Develop automated tests for mathematical functions, numerical outputs, and data processing.



\## 9. Repository Structure



| File | Purpose |

|---|---|

| `main.py` | Introductory computational demonstration |

| `model.py` | Basic computational model |

| `experiment.py` | Exploratory experiment |

| `mwc\_binding.py` | MWC oxygen-binding model |

| `fiber\_binding.py` | Haemoglobin fibre-binding model |

| `oxygen\_binding\_graph.py` | Oxygen-binding visualisation |

| `binding\_comparison.py` | Comparison of oxygen-binding models |

| `integrated\_model.py` | Integrated modelling experiment |

| `solubility\_model.py` | Solubility-related calculations |

| `solubility\_integration.py` | Numerical integration experiment |

| `complete\_solubility\_model.py` | Differential-equation solubility implementation |

| `empirical\_solubility\_model.py` | Exploratory empirical solubility calculation |

| `experimental\_comparison.py` | Comparison of calculated and approximate experimental results |

| `figure3\_approximate\_data.csv` | Approximate digitised experimental values |

| `complete\_solubility\_results.csv` | Calculated solubility results |

| `complete\_solubility\_curve.png` | Calculated solubility graph |

| `figure3\_experimental\_comparison.png` | Experimental comparison graph |

| `experimental\_comparison\_results.csv` | Point-by-point comparison results |

| `experimental\_comparison\_report.txt` | Comparison metrics and limitations |

| `requirements.txt` | Python package dependencies |



Other CSV and PNG files in the repository contain outputs from the exploratory experiments.



\## 10. Running the Project



Install the required Python dependencies:



```bash

pip install -r requirements.txt

