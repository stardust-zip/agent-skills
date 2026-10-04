# Evidence Registry and Traceability

Load this file only when auditing sources, changing or adding to the standard, or explaining the evidence behind a rule. The normal research flow uses the rule IDs in `standard.md` without loading the source list.

Use only primary sources: official guidance, tool documentation or original research.

## Evidence registry

| ID | Source | What it supports |
|---|---|---|
| E01 | [Google Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) | objective and metric first, a reliable pipeline, a simple first model |
| E02 | [Sandve et al., Ten Simple Rules for Reproducible Computational Research](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1003285) | tracing claims to data, code, parameters and results |
| E03 | [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) | validity, reliability, transparency, safety and risk governance |
| E04 | [Gebru et al., Datasheets for Datasets](https://doi.org/10.48550/ARXIV.1803.09010) | dataset provenance, composition, collection process and limitations |
| E05 | [Scikit-learn: Cross-validation and TimeSeriesSplit](https://scikit-learn.org/stable/modules/cross_validation.html#time-series-split) | splitting by time and evaluating on the future |
| E06 | [Scikit-learn: Common pitfalls and data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage) | split before preprocessing; fit transformations on train only |
| E07 | [Google: Implementing a model](https://developers.google.com/machine-learning/problem-framing/implement-model) | a simple pipeline and baseline before a complex model |
| E08 | [Hyndman & Athanasopoulos, Forecasting: Principles and Practice](https://otexts.com/fpp2/simple-methods.html) | mean, naive and seasonal-naive forecasting baselines |
| E09 | [Schmidl et al., Anomaly Detection in Time Series: A Comprehensive Evaluation](https://www.vldb.org/pvldb/vol15/p1779-wenig.pdf) | comparing anomaly-detector families on effectiveness, efficiency and robustness |
| E10 | [Breck et al., The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) | feature, data, model and serving tests and monitoring for production readiness |
| E11 | [Mitchell et al., Model Cards for Model Reporting](https://research.google/pubs/model-cards-for-model-reporting/) | intended use, limitations, data and metrics by group |
| E12 | [Rule et al., Ten Simple Rules for Reproducible Research in Jupyter Notebooks](https://arxiv.org/abs/1810.08055) | dependencies, execution order and rerunnable notebooks; telling the reader a story and recording the process, not just the results |
| E13 | [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking) | a reference implementation for logging runs, code version, dataset, parameters, metrics and artifacts |
| E14 | [Tatbul et al., Precision and Recall for Time Series](https://papers.nips.cc/paper_files/paper/2018/hash/8f468c873a32bb0619eaeb2050ba45d1-Abstract.html) | evaluating range or event anomalies instead of single points only |
| E15 | [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist) | assumptions, error bars, compute, reproducibility and the limits of claims |
| E16 | [Sculley et al., Hidden Technical Debt in ML Systems](https://papers.neurips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf) | data dependencies, feedback loops, configuration and pipeline debt |
| E17 | [Saito & Rehmsmeier, Precision-Recall for imbalanced classification](https://doi.org/10.1371/journal.pone.0118432) | PR curves reflect positive predictions better than ROC under strong class imbalance |
| E18 | [Gneiting & Raftery, Strictly Proper Scoring Rules](https://doi.org/10.1198/016214506000001437) | Brier and log scores for probabilistic forecasts |
| E19 | [Taschuk & Wilson, Robust Research Software](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1005412) | research code that runs outside the author's machine |

## Traceability matrix

| Standard | Evidence |
|---|---|
| S01 Repository structure | E02, E12, E13, E19 |
| S02 Task selection | E01, E03, E05, E08, E14 |
| S03 Stage gates | E01, E02, E03, E10, E15 |
| S04 Problem Card | E01, E03 |
| S05 Data Contract | E04, E10, E16 |
| S06 Dataset manifest | E02, E04, E13 |
| S07 Data-quality report | E04, E10 |
| S08 Data format, scale and security | E02, E04, E16, E19 |
| S09 Split | E05, E06 |
| S10 Baselines | E07, E08, E09 |
| S11 Metrics | E03, E08, E14, E17, E18 |
| S12 Uncertainty/slices | E03, E11, E15 |
| S13 Baseline execution | E01, E07, E08, E09 |
| S14 Experiment tracking | E02, E13, E15 |
| S15 Locked test | E03, E10, E11, E15 |
| S16 Robustness | E03, E10, E16 |
| S17 Notebook | E02, E12, E19 |
| S18 Research log/claims | E02, E15 |
| S19 Handoff | E03, E10, E11, E13, E16 |
| S20 Definition of Done | E02, E03, E10, E11, E15 |
| S21 Anti-patterns | E01, E02, E06, E10, E15, E16 |

