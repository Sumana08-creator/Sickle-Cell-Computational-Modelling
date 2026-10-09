\# Sickle Cell Computational Modelling

\### Exploring Oxygen-Dependent HbS Polymerisation and the Potential Role of Fetal Haemoglobin



\## 1. Project Overview



Sickle cell disease is a genetic blood disorder associated with the polymerisation of haemoglobin S (HbS) under conditions of reduced oxygen availability. This polymerisation contributes to red blood cell deformation and the complications associated with the disease.



This project explores how computational modelling can be used to investigate the relationships between oxygen availability, haemoglobin oxygen binding, HbS fibre formation, and fetal haemoglobin (HbF).



Using Python, mathematical models, numerical integration, and scientific visualisation, the project investigates selected relationships described in published research.



The long-term objective is to develop a reproducible computational framework that can help explore the physical and biochemical processes involved in HbS polymerisation.



\*\*Project status:\*\* Educational and exploratory computational modelling. The current solubility calculations require further scientific verification and validation against published experimental measurements.



\## 2. Research Motivation



HbS polymerisation is influenced by oxygenation and the thermodynamic properties of haemoglobin fibres. Fetal haemoglobin is also relevant to sickle cell research because its presence can influence HbS polymerisation.



Understanding these relationships requires consideration of multiple interacting factors rather than treating oxygen availability as an isolated variable.



Computational modelling provides a way to represent selected relationships mathematically, explore their behaviour under different conditions, and visualise the resulting calculations.



This project was initiated to explore how published mathematical relationships can be translated into Python implementations and how computational experiments can support further investigation of sickle cell disease.



\## 3. Research Questions



The project is organised around the following exploratory questions:



1\. How does oxygen partial pressure influence haemoglobin oxygen saturation in mathematical binding models?

2\. How does the predicted oxygen-binding behaviour of free haemoglobin compare with that of haemoglobin fibres?

3\. How can mathematical models be used to investigate relationships between oxygen saturation and HbS solubility?

4\. How could fetal haemoglobin be incorporated into a computational framework investigating HbS polymerisation?

5\. What additional experimental data and model validation would be required before these calculations could support reliable scientific predictions?



These questions guide the current implementations and provide a foundation for further model development.



\## 4. Scientific Foundation



The project is informed by the following publication:



Henry et al. (2020).



\*Allosteric control of hemoglobin S fiber formation by oxygen and its relation to the pathophysiology of sickle cell disease.\*



\*\*Journal:\*\* Proceedings of the National Academy of Sciences (PNAS)



\*\*DOI:\*\* 10.1073/pnas.1922004117



\*\*Full text:\*\* https://pmc.ncbi.nlm.nih.gov/articles/PMC7334536/



The publication investigates the relationship between oxygen binding and the thermodynamic stability of HbS fibres. It provides a scientific basis for exploring oxygen-binding behaviour and HbS solubility through mathematical modelling.



The current project implements selected computational components informed by this research. The implementations should not be interpreted as a complete or independently validated reproduction of every model in the publication.



\## 5. Computational Approach



The project uses Python to implement mathematical relationships, perform calculations, export numerical results, and generate graphs.



\### 5.1 Haemoglobin Oxygen Binding



The project includes an implementation of the Monod–Wyman–Changeux (MWC) model, which represents cooperative oxygen binding through an allosteric equilibrium between haemoglobin conformational states.



\*\*Implementation:\*\* `mwc\_binding.py`



The model allows oxygen-binding behaviour to be calculated across a range of oxygen partial pressures.



\### 5.2 Haemoglobin Fibre Binding



A separate implementation represents oxygen binding by haemoglobin fibres using a noncooperative binding relationship.



\*\*Implementation:\*\* `fiber\_binding.py`



The resulting calculations can be compared with those from the free-haemoglobin model.



\### 5.3 Model Comparison



The project combines the oxygen-binding calculations in a visual comparison.



\*\*Implementation:\*\* `binding\_comparison.py`



\*\*Output:\*\* `binding\_comparison.png`



The graph presents the calculated oxygen saturation of free haemoglobin and haemoglobin fibres across a range of oxygen partial pressures.



The comparison illustrates differences between the implemented mathematical relationships. Its scientific interpretation depends on the validity of the equations, parameters, and assumptions used.



\### 5.4 Numerical Integration



SciPy is used to perform numerical integration in an exploratory investigation of the relationship between oxygen binding and HbS solubility.



\*\*Implementation:\*\* `solubility\_integration.py`



Numerical integration provides a computational method for evaluating an integral when an analytical solution is unavailable or inconvenient.



The successful completion of a numerical calculation establishes that the integration procedure ran for the selected inputs; it does not independently establish that the underlying scientific model is correct.



\### 5.5 Exploratory HbS Solubility Calculations



The project contains implementations exploring mathematical relationships between oxygen conditions and HbS solubility.



Relevant files include:



\- `solubility\_model.py`

\- `solubility\_integration.py`

\- `complete\_solubility\_model.py`

\- `empirical\_solubility\_model.py`



The empirical implementation calculates solubility estimates across 101 fractional oxygen-saturation values at a specified temperature of 25°C.



\*\*Generated outputs:\*\*

\- `empirical\_solubility\_results.csv`

\- `empirical\_solubility\_curve\_new.png`



The CSV contains calculated estimates, while the graph visualises the relationship represented by the implemented equation.



\*\*Important limitation:\*\* The empirical equation and reference values require verification against their original sources. The resulting estimates have not been validated against published experimental measurements and must not be presented as established biological findings.



\## 6. Results and Visualisations



The current project generates numerical outputs and graphs that allow the behaviour of the implemented mathematical relationships to be inspected.



\### 6.1 Oxygen-Binding Behaviour



\*\*Output:\*\* `oxygen\_binding\_curve.png`



The oxygen-binding graph displays calculated haemoglobin oxygen saturation across a range of oxygen partial pressures.



The curve provides a visual representation of the behaviour predicted by the oxygen-binding function implemented in the code.



\### 6.2 Comparison of Binding Models



\*\*Output:\*\* `binding\_comparison.png`



The comparison graph displays the calculated oxygen-binding behaviour of free haemoglobin and haemoglobin fibres.



It provides a visual means of comparing the two mathematical relationships under the parameters specified in the implementation.



\### 6.3 HbS Solubility Estimates



\*\*Output:\*\* `empirical\_solubility\_curve\_new.png`



The empirical solubility experiment produces 101 calculated points at 25°C, spanning fractional oxygen saturation values from 0 to 1.



The current implementation calculates:



\- Solubility at 0% fractional oxygen saturation: 0.178375 g/mL.

\- Solubility at 100% fractional oxygen saturation: 0.603775 g/mL.



These values are outputs of the currently implemented equation. They are not experimental measurements, and their scientific accuracy has not been established.



\### 6.4 Numerical Data Export



The project exports selected calculated results to CSV files.



\- `experiment\_results.csv`

\- `empirical\_solubility\_results.csv`



This allows numerical outputs to be inspected separately from the Python scripts and graphs.



The files provide a starting point for subsequent analysis and comparison with appropriate published datasets.



\## 7. Scientific Interpretation



The current implementations demonstrate how mathematical relationships can be translated into computational models and visualised using Python.



The oxygen-binding models provide a framework for comparing calculated binding behaviour. The solubility experiments demonstrate a computational workflow involving mathematical functions, numerical calculations, data export, and graphical representation.



However, generating a curve or obtaining a numerical result is not sufficient to establish a biological conclusion.



In particular, the current solubility calculations should be regarded as exploratory because their equations, reference values, assumptions, and outputs require further verification.



The project therefore represents an initial computational investigation rather than a validated predictive model of sickle cell disease.



\## 8. Limitations



Several limitations remain.



\### Equation and Parameter Verification



The equations and parameter values must be checked against the original scientific sources, including their units, assumptions, and experimental conditions.



\### Experimental Validation



Calculated outputs must be compared with suitable published experimental measurements before model accuracy can be evaluated.



\### Numerical Stability



The solubility implementations require further investigation of numerical stability, parameter sensitivity, and behaviour across the intended range of conditions.



\### Fetal Haemoglobin Modelling



Although HbF is part of the project's research motivation, further work is required to establish and validate a quantitative implementation of its influence on HbS polymerisation.



\### Scope of Interpretation



The present results do not establish clinical predictions, patient-specific outcomes, or treatment recommendations.



\## 9. Future Research Directions



Future development will focus on:



1\. Verifying the mathematical equations and parameters against the original publication.

2\. Obtaining suitable published experimental data for model comparison.

3\. Quantifying differences between calculated and experimental values.

4\. Evaluating numerical stability and sensitivity to parameter changes.

5\. Developing a clearly defined and testable representation of the potential influence of HbF on HbS polymerisation.

6\. Improving reproducibility through documented assumptions, parameter sources, and computational experiments.

7\. Separating validated model components from exploratory implementations.



These steps would help establish whether the framework can progress from educational modelling towards a scientifically evaluated computational model.



\## 10. Conclusion



This project explores the use of Python to investigate selected mathematical relationships associated with haemoglobin oxygen binding and HbS polymerisation.



It brings together oxygen-binding models, numerical integration, exploratory solubility calculations, CSV data export, and scientific visualisation.



The main contribution at this stage is the development of a computational framework for investigating these relationships and identifying the additional verification and validation required for further scientific work.



The project provides a foundation for continued exploration of oxygen-dependent HbS polymerisation and the potential role of fetal haemoglobin.



\## 11. Repository Structure



| File | Purpose |

|---|---|

| `main.py` | Introductory computational demonstration |

| `model.py` | Basic computational model |

| `experiment.py` | Exploratory experiment |

| `oxygen\_binding.py` | Oxygen-binding calculations |

| `oxygen\_binding\_graph.py` | Oxygen-binding visualisation |

| `mwc\_binding.py` | MWC oxygen-binding model |

| `fiber\_binding.py` | Haemoglobin fibre-binding model |

| `integrated\_model.py` | Integrated modelling experiment |

| `binding\_comparison.py` | Comparison of oxygen-binding models |

| `solubility\_model.py` | Activity-coefficient calculations |

| `solubility\_integration.py` | Numerical integration experiment |

| `complete\_solubility\_model.py` | Exploratory solubility implementation |

| `empirical\_solubility\_model.py` | Empirical solubility calculation |

| `experiment\_results.csv` | Exploratory experiment output |

| `empirical\_solubility\_results.csv` | Calculated solubility estimates |

| `research\_data.csv` | Research data template |

| `requirements.txt` | Python package dependencies |



The PNG files contain graphs generated by the project scripts.



\---



\*This repository is an educational and exploratory computational research project. Its outputs require appropriate scientific verification and validation before being used to support biological conclusions.\*

