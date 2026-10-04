# Evidence Registry and Traceability

File này chỉ được tải khi audit nguồn, sửa/thêm standard hoặc giải thích cơ sở bằng chứng. Luồng nghiên cứu thông thường dùng rule ID trong `standard.md` mà không tải danh sách nguồn.

Chỉ dùng nguồn gốc chính thức, tài liệu của công cụ hoặc nghiên cứu gốc.

## Evidence registry

| ID | Nguồn | Phạm vi bằng chứng |
|---|---|---|
| E01 | [Google Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml) | objective/metric trước, pipeline đáng tin cậy, model đầu tiên đơn giản |
| E02 | [Sandve et al., Ten Simple Rules for Reproducible Computational Research](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1003285) | truy vết claim tới dữ liệu, code, tham số và kết quả |
| E03 | [NIST AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) | tính hợp lệ, tin cậy, minh bạch, an toàn và quản trị rủi ro |
| E04 | [Gebru et al., Datasheets for Datasets](https://doi.org/10.48550/ARXIV.1803.09010) | nguồn gốc, thành phần, quá trình tạo và giới hạn dataset |
| E05 | [Scikit-learn: Cross-validation và TimeSeriesSplit](https://scikit-learn.org/stable/modules/cross_validation.html#time-series-split) | split theo thời gian và đánh giá trên tương lai |
| E06 | [Scikit-learn: Common pitfalls và data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage) | split trước preprocessing; fit transformation chỉ trên train |
| E07 | [Google: Implementing a model](https://developers.google.com/machine-learning/problem-framing/implement-model) | pipeline và baseline đơn giản trước model phức tạp |
| E08 | [Hyndman & Athanasopoulos, Forecasting: Principles and Practice](https://otexts.com/fpp2/simple-methods.html) | mean, naive và seasonal-naive forecasting baseline |
| E09 | [Schmidl et al., Anomaly Detection in Time Series: A Comprehensive Evaluation](https://www.vldb.org/pvldb/vol15/p1779-wenig.pdf) | so sánh nhiều họ anomaly detector về effectiveness, efficiency và robustness |
| E10 | [Breck et al., The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) | test feature/data/model/serving và monitoring cho production readiness |
| E11 | [Mitchell et al., Model Cards for Model Reporting](https://research.google/pubs/model-cards-for-model-reporting/) | intended use, giới hạn, dữ liệu và metric theo nhóm |
| E12 | [Rule et al., Ten Simple Rules for Reproducible Research in Jupyter Notebooks](https://arxiv.org/abs/1810.08055) | dependency, thứ tự thực thi, khả năng chạy lại notebook; kể câu chuyện cho người đọc và ghi lại quá trình, không chỉ kết quả |
| E13 | [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking) | một implementation tham chiếu cho việc log run, code version, dataset, parameter, metric và artifact |
| E14 | [Tatbul et al., Precision and Recall for Time Series](https://papers.nips.cc/paper_files/paper/2018/hash/8f468c873a32bb0619eaeb2050ba45d1-Abstract.html) | đánh giá anomaly dạng khoảng/sự kiện thay vì chỉ từng điểm |
| E15 | [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist) | assumptions, error bars, compute, reproducibility và giới hạn claim |
| E16 | [Sculley et al., Hidden Technical Debt in ML Systems](https://papers.neurips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf) | data dependency, feedback loop, configuration và pipeline debt |
| E17 | [Saito & Rehmsmeier, Precision-Recall for imbalanced classification](https://doi.org/10.1371/journal.pone.0118432) | PR curve phản ánh positive prediction tốt hơn ROC khi class imbalance mạnh |
| E18 | [Gneiting & Raftery, Strictly Proper Scoring Rules](https://doi.org/10.1198/016214506000001437) | Brier/log score cho dự báo xác suất |
| E19 | [Taschuk & Wilson, Robust Research Software](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1005412) | code nghiên cứu chạy được ngoài máy tác giả |

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

