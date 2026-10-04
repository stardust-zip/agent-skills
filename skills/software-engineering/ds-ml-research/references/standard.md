# Tiêu chuẩn nghiên cứu Data Science và Machine Learning (SSOT)

**Phiên bản:** 2.8

**Trạng thái:** Normative

**Phạm vi:** nghiên cứu mô tả, classification, regression, forecasting và time-series anomaly detection

**Mục tiêu:** hai người hoặc hai AI đọc tài liệu này phải tạo cùng cấu trúc artifact, đi qua cùng stage gate và áp dụng cùng protocol lựa chọn

## 1. Quy ước và cách dùng

Tài liệu này là **single source of truth**. Không tạo một style guide khác trong cùng repository.

Chỉ dùng ba từ khóa:

- **MUST:** bắt buộc. Thiếu bằng chứng hoàn thành thì stage gate thất bại.
- **MUST NOT:** bị cấm.
- **CONDITIONAL:** bắt buộc khi trigger ghi trong decision table xảy ra.

Không dùng “NÊN”, “CÓ THỂ”, “phù hợp”, “khi cần” hoặc “khi khả thi” làm quy tắc. Mỗi ngoại lệ MUST có một Decision Record trong `research-log.md` gồm: rule ID, lý do, người duyệt, ngày hết hiệu lực và rủi ro được chấp nhận.

Mỗi quy tắc có mã `Sxx`. Mỗi cơ sở bên ngoài có mã `Exx`. Cú pháp:

```text
[S<rule-id> | E<evidence-id>,...]
```

Tên file, tên thư mục và schema artifact là **project convention**. Chúng không phải kết quả khoa học từ nguồn bên ngoài; chúng là cách repository thực thi yêu cầu truy vết/tái lập của nguồn được gắn bên cạnh.

## 2. Evidence policy

Evidence registry và ma trận truy vết được duy trì tại [`evidence.md`](evidence.md). Agent MUST NOT đọc file đó trong luồng thực thi thông thường. MUST đọc khi audit nguồn, sửa/thêm standard hoặc khi người dùng yêu cầu cơ sở bằng chứng cho một quy tắc.

## 3. Cấu trúc repository bắt buộc

[S01 | E02,E12,E13,E19]

Mỗi research topic MUST có đúng cấu trúc logic sau. File bổ sung được phép tồn tại; tên và vị trí của các artifact bắt buộc MUST NOT bị thay đổi.

```text
notebooks/<research-slug>/
├── research-plan.md
├── research-log.md
├── 00_data_inventory.ipynb
├── 01_data_quality.ipynb
├── 02_eda.ipynb
├── 03_build_dataset.ipynb
├── 04_baselines.ipynb
├── 05_candidates.ipynb
└── 06_evaluation.ipynb

data/<environment>/<domain>/
├── bronze/
├── silver/
├── gold/
└── manifests/
```

Quy tắc:

1. `research-plan.md` chứa trạng thái hiện hành: Problem Card, Data Contract, Evaluation Protocol và open decisions.
2. `research-log.md` là append-only; mỗi experiment/decision là một entry có ngày.
3. Notebook chỉ orchestration, inspection và narrative. Logic được dùng từ hai notebook trở lên MUST chuyển vào module Python của repository.
4. Raw data, model binary và output lớn MUST NOT commit vào Git.
5. Mỗi notebook MUST ghi artifact ra `data/...`, experiment tracker hoặc artifact store được khai báo trong Evaluation Protocol; notebook output không phải artifact chuẩn.
6. Toàn bộ file trong cây bắt buộc MUST được tạo khi khởi tạo research topic. Notebook của stage chưa chạy MUST chỉ chứa header chuẩn, trạng thái `NOT_STARTED` và skeleton section của mục 13.2 với placeholder `__NARRATIVE_REQUIRED__`; yêu cầu output của notebook bắt đầu áp dụng khi stage tương ứng chuyển sang `IN_PROGRESS`. Header của notebook có `**Status:**` khác `NOT_STARTED` MUST NOT còn placeholder `__REQUIRED__`. Khi gate của notebook (theo cột Stage/Gate của bảng dưới) là `PASS`, `**Status:**` của notebook MUST là `PASS`, `FAIL` hoặc `STOPPED`.
7. Ngôn ngữ prose của topic (`en` hoặc `vi`) MUST được chọn khi khởi tạo và ghi vào `language:` trong section 1 của `research-plan.md`. Mọi artifact prose của topic dùng ngôn ngữ đó; technical term và identifier giữ tiếng Anh theo [`writing.md`](writing.md).

Mục đích notebook là cố định:

| Notebook | Stage/Gate | Câu hỏi duy nhất | Output bắt buộc |
|---|---|---|---|
| `00_data_inventory.ipynb` | G1 | Có source, field, entity, time range và volume nào? | inventory table và draft Data Contract |
| `01_data_quality.ipynb` | G1 | Dữ liệu có đạt readiness threshold đã duyệt không? | data-quality report, manifest của snapshot đã kiểm tra và quyết định G1 |
| `02_eda.ipynb` | G2 | Population, target và candidate signal phân bố như thế nào trên train? | feature contract theo mục 8.5, rồi EDA report chỉ trên train theo split definition đã ghi trong Evaluation Protocol; không đọc validation/locked-test |
| `03_build_dataset.ipynb` | G2 | Làm thế nào tạo Silver/Gold snapshot tái lập được? | dataset, manifest, split assignment hiện thực hóa split definition và assertions |
| `04_baselines.ipynb` | G3 | Baseline bắt buộc đạt kết quả nào theo Evaluation Protocol? | baseline runs, comparison table và `strongest_baseline_id` |
| `05_candidates.ipynb` | G4 | Hypothesis nào vượt strongest baseline trên validation? | candidate runs, ablation và selected candidate |
| `06_evaluation.ipynb` | G5 | Selected run có PASS locked test và stress tests không? | locked-test report và quyết định G5 |

Thứ tự trong G2: (1) ghi split definition (timestamp/entity/filter của train, validation, locked test) vào Evaluation Protocol theo S09; (2) `02_eda.ipynb` lọc train bằng definition đó; (3) `03_build_dataset.ipynb` hiện thực hóa split assignment và manifest; (4) đóng băng phần còn lại của Evaluation Protocol. EDA MUST NOT dùng để chọn hoặc dịch ranh giới locked test.

`research-plan.md` MUST dùng đúng thứ tự section sau:

```text
1. Research status and target gate
2. Problem Card
3. Data Contracts
4. Dataset snapshots and manifests
5. Data Readiness Thresholds
6. Evaluation Protocol hoặc Analysis Protocol
7. Gate Status
8. Open Decisions
9. Approved Exceptions
```

`Gate Status` MUST là bảng có các cột `Gate`, `Status`, `Evidence/Artifact`, `Reviewer`, `Reviewed at UTC`. Giá trị `Status` chỉ được là `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL` hoặc `STOPPED`.

## 4. Chọn loại nghiên cứu

[S02 | E01,E03,E05,E08,E14]

Giai đoạn đầu MUST chọn đúng một `task_type` trong bảng. Nếu bài toán không thuộc bảng, nghiên cứu dừng tại Gate 0 cho tới khi SSOT được bổ sung protocol và evidence.

| `task_type` | Câu hỏi đầu ra |
|---|---|
| `descriptive` | Dữ liệu đã xảy ra như thế nào? |
| `classification` | Một entity/event thuộc lớp nào? |
| `regression` | Giá trị liên tục của entity/event là bao nhiêu? |
| `forecasting` | Giá trị chuỗi thời gian trong horizon tương lai là bao nhiêu? |
| `anomaly_detection` | Entity/time range nào lệch khỏi normal behavior? |

Chọn `task_type` bằng thứ tự đầu tiên khớp dưới đây:

1. Output chỉ mô tả population hoặc dữ liệu quá khứ, không tạo prediction/score cho từng unit → `descriptive`.
2. Target đã định nghĩa là category/class/event label → `classification`, kể cả khi dự đoán label ở thời điểm tương lai.
3. Target là giá trị số liên tục tại một horizon tương lai của chuỗi có thứ tự thời gian → `forecasting`.
4. Target là giá trị số liên tục nhưng không thuộc dòng 3 → `regression`.
5. Không có target label và output là độ lệch khỏi normal behavior → `anomaly_detection`.

Nếu nhiều dòng cùng khớp do problem statement chưa rõ, G0 MUST FAIL; owner MUST chốt output và target trước khi tiếp tục.

Clustering, ranking/recommendation, causal inference, reinforcement learning, computer vision foundation model và LLM evaluation chưa có protocol trong phiên bản hiện hành. Chúng MUST NOT dùng protocol classification mặc định; phải mở rộng SSOT trước khi bắt đầu.

## 5. Stage gates bắt buộc

[S03 | E01,E02,E03,E10,E15]

Không được bỏ stage. Khi nghiên cứu dừng trước gate mục tiêu, trạng thái MUST là `STOPPED` và lý do MUST được ghi trong research log.

| Gate | Input | Artifact bắt buộc | Điều kiện PASS |
|---|---|---|---|
| G0 Problem | yêu cầu nghiệp vụ | Problem Card trong `research-plan.md` | tất cả field có giá trị; owner duyệt target/action/metric |
| G1 Data | G0 PASS | Data Contract, manifest, data-quality report | mọi field bắt buộc của S05–S07 có giá trị; checksum khớp file; mọi readiness threshold đạt hoặc exception được duyệt |
| G2 Protocol | G1 PASS | Evaluation Protocol, feature contract | split, baseline, metric, slice, uncertainty, acceptance criteria, feature contract và locked test đã đóng băng |
| G3 Baseline | G2 PASS | baseline runs + report | tất cả baseline bắt buộc chạy cùng snapshot/split; failure analysis tồn tại |
| G4 Candidate | G3 PASS | approach-space record, candidate runs + comparison hoặc no-change decision | mỗi hypothesis đã đăng ký có kết quả; selected run so với strongest baseline; outcome được nêu rõ theo mục 10.3; không dùng locked test để tune |
| G5 Locked test | G4 PASS; selected run đã chọn | locked-test report | chạy một lần; đạt toàn bộ primary/guardrail/operational criteria |
| G6 Handoff | G5 PASS | model card, run/model URI, monitoring và rollback plan | reviewer kỹ thuật và owner nghiệp vụ ký duyệt |

`Discovery-only` research MUST hoàn thành G0–G2; tại G2, Evaluation Protocol được thay bằng Analysis Protocol ghi rõ population, sampling, estimand/statistic, uncertainty và giới hạn claim.

## 6. G0 — Problem Card

[S04 | E01,E03]

`research-plan.md` MUST chứa đúng các field:

```yaml
problem_id:
title:
task_type:
research_deliverable:
business_owner:
technical_owner:
decision_user:
decision_or_action:
prediction_or_analysis_unit:
scoring_time:
feature_cutoff_time:
target_definition:
label_available_time:
prediction_horizon:
false_positive_cost:
false_negative_cost:
current_process_or_baseline:
primary_business_metric:
primary_model_metric:
guardrail_metrics:
operational_constraints:
supported_population:
excluded_population:
success_criteria:
stop_criteria:
approval:
```

Quy tắc PASS:

1. Mọi field MUST có giá trị; không dùng `TBD`.
2. `success_criteria` MUST là bất đẳng thức có số hoặc trạng thái `discovery_only`.
3. `target_definition` MUST mô tả đơn vị, điều kiện positive/value và timestamp.
4. `feature_cutoff_time` MUST nhỏ hơn hoặc bằng `scoring_time`.
5. `label_available_time` MUST được dùng để phát hiện feature không tồn tại khi score.
6. Owner MUST ghi tên và ngày duyệt trong `approval`.
7. `research_deliverable` MUST bắt đầu bằng đúng một trong ba giá trị, theo sau là một câu nêu sản phẩm đầu ra cụ thể:
   - `feasibility_poc`: kết luận nghiên cứu có khả thi hay không; không chọn model để triển khai.
   - `model_selection`: chọn một model và cấu hình, hoặc quyết định giữ reference hiện có, để đăng ký vào hệ thống tiêu thụ model.
   - `analysis_report`: báo cáo mô tả hoặc phân tích; không tạo model để triển khai.
8. Agent MUST NOT tự chọn `research_deliverable`. Giá trị này là quyết định của owner; thiếu thì trả `OWNER_DECISION_REQUIRED`.
9. Khi `research_deliverable` là `model_selection`: `operational_constraints` MUST nêu hệ thống tiêu thụ model cùng định dạng artifact và feature mà nó yêu cầu; `success_criteria` MUST trích tiêu chí nghiệm thu của hệ thống đó, hoặc ghi `OWNER_DECISION_REQUIRED` cho phần chưa có. Tiêu chí chỉ của nghiên cứu mà không có tiêu chí của hệ thống tiêu thụ không đủ để kết luận model dùng được.
10. Khi owner đổi `research_deliverable` sau G0 PASS, G0 MUST mở lại và gate sau đó MUST được đánh giá lại xem artifact đã có còn dùng được không.

## 7. G1 — Data Contract, manifest và readiness

### 7.1. Data Contract

[S05 | E04,E10,E16]

Mỗi source MUST có:

```yaml
source_name:
owner:
source_of_truth:
access_method:
schema:
field_semantics:
units:
entity_key:
event_key:
event_time:
processing_time:
timezone:
expected_cadence:
null_semantics:
zero_semantics:
duplicate_definition:
retention:
expected_arrival_lag:
late_data_policy:
sensitive_fields:
access_policy:
label_source:
known_limitations:
```

### 7.2. Dataset manifest

[S06 | E02,E04,E13]

Mỗi Bronze/Silver/Gold snapshot MUST có manifest:

```yaml
dataset_name:
snapshot_id:
layer: bronze|silver|gold
source_snapshot_ids:
created_at_utc:
created_by_code_commit:
extraction_query_or_job:
event_time_start:
event_time_end:
schema_version:
row_count:
entity_count:
label_count_by_class:
files:
checksums:
known_gaps:
filters:
transformations:
label_definition_version:
owner:
```

Bronze MUST bất biến. Silver/Gold đã được một experiment run tham chiếu MUST NOT bị ghi đè; tạo `snapshot_id` mới.

### 7.3. Data-quality report

[S07 | E04,E10]

`01_data_quality.ipynb` MUST xuất một bảng cho toàn dataset và từng slice được khai báo ở G0:

| Kiểm tra | Output bắt buộc |
|---|---|
| Coverage | min/max time, duration, row count, entity count theo period |
| Completeness | null/missing rate theo field, entity và period |
| Uniqueness | duplicate count theo `duplicate_definition` |
| Validity | count/rate ngoài range hoặc enum |
| Cadence | median, p05, p95 của inter-arrival time |
| Freshness | `processing_time - event_time` p50/p95/p99/max |
| Population stability | entity added/removed theo period |
| Label quality | class count, prevalence, ambiguous/unlabeled rate |
| Leakage inventory | thời điểm availability của từng candidate feature |

Readiness threshold MUST được khai báo trong Problem Card trước khi xem candidate model. Không có universal threshold. PASS nghĩa là mọi metric đạt threshold đã duyệt; nếu không đạt, G1 FAIL hoặc có exception theo mục 1.

### 7.4. Dữ liệu lớn, format và bảo mật

[S08 | E02,E04,E16,E19]

1. Nếu estimated in-memory size lớn hơn 50% RAM khả dụng, MUST scan theo column/filter/batch và aggregate trước pandas. Mốc 50% là project safety convention để chừa bộ nhớ cho runtime.
2. MUST giữ type-preserving format như Parquet khi source đã là Parquet; MUST NOT chuyển sang CSV chỉ để EDA.
3. MUST ghi row count trước/sau mỗi transformation.
4. Token, password, PII và URL chứa credential MUST NOT xuất hiện trong Git, notebook output, log hoặc screenshot.
5. Local data MUST nằm trong path được `.gitignore` bảo vệ. `data/<environment>/<domain>/` MUST bị Git ignore trước khi ghi dữ liệu.

## 8. G2 — Evaluation Protocol

### 8.1. Chọn split bằng decision table

[S09 | E05,E06]

Áp dụng từ trên xuống; dòng đầu tiên khớp là protocol bắt buộc.

| Trigger production | Split bắt buộc |
|---|---|
| Dự đoán/đánh giá tương lai theo event time | chronological train → validation → locked test; forecasting dùng rolling-origin evaluation |
| Production gặp entity chưa từng thấy | group holdout theo entity; entity MUST không giao giữa split |
| Vừa dự đoán tương lai vừa cần tổng quát sang entity mới | hai test riêng: temporal test trên entity đã biết và temporal-group test trên entity mới |
| Dữ liệu i.i.d. classification, không có group/time dependency | stratified random split |
| Dữ liệu i.i.d. regression, không có group/time dependency | random split |
| `descriptive` | không train/test split; khóa population, sampling frame và analysis period |

Quy tắc:

1. Test set MUST được định nghĩa bằng timestamp/entity/filter cụ thể trong manifest.
2. Sau G2, test labels MUST NOT được dùng cho feature, threshold, model hoặc hyperparameter selection.
3. Locked test chỉ chạy sau khi chọn candidate. Nếu dùng kết quả test để thay đổi hệ thống, test đó mất trạng thái locked; nghiên cứu MUST tạo test period/snapshot mới và ghi invalidation.
4. Scaler, imputer, encoder, feature selector, resampling parameter và learned threshold MUST chỉ fit trên train rồi transform validation/test.

### 8.2. Baseline protocol theo task

[S10 | E07,E08,E09]

Tất cả baseline có dấu `MUST` phải chạy. `N/A` chỉ hợp lệ với Decision Record.

| Task | Baseline 0 | Baseline 1 | Baseline 2 |
|---|---|---|---|
| Classification | majority class và class-prior probability — MUST | rule hiện tại — MUST nếu production có rule | Logistic Regression — MUST |
| Regression | train mean và train median — MUST | công thức/rule hiện tại — MUST nếu tồn tại | Linear hoặc Ridge Regression — MUST |
| Forecasting | last-value naive — MUST | seasonal naive — MUST nếu train chứa ít nhất 2 chu kỳ đã định nghĩa | ETS hoặc ARIMA — MUST |
| Anomaly detection | all-normal và fixed alert-rate — MUST | rule/threshold hiện tại — MUST | rolling median + MAD — MUST |
| Descriptive | statistic hiện hành hoặc báo cáo cũ — MUST nếu tồn tại | không áp dụng model | không áp dụng model |

Isolation Forest là **candidate**, không phải statistical baseline. Rule-based baseline là deterministic logic. Statistical baseline ước lượng mức nền/phân bố/thời gian như median, MAD, EWMA, ETS hoặc ARIMA; nó không đồng nghĩa với xác suất.

### 8.3. Metric protocol theo task

[S11 | E03,E08,E14,E17,E18]

| Task/trigger | Primary report bắt buộc |
|---|---|
| Binary classification | confusion matrix tại threshold vận hành; precision, recall, F1; PR curve/AP; prevalence |
| Binary probability được dùng như risk score | toàn bộ dòng trên + Brier score + calibration curve |
| Multiclass | confusion matrix; per-class precision/recall/F1; macro average; support |
| Regression | MAE; RMSE; residual quantiles p50/p90/p95; error theo slice |
| Forecasting | MAE hoặc MASE; error theo horizon; so với naive/seasonal naive |
| Time-series anomaly có labels | event precision/recall/F1; detection delay; false alerts/entity/day; event coverage |
| Time-series anomaly không labels | alert rate; score stability; coverage; runtime; injected-anomaly sensitivity; MUST ghi “không đo chất lượng phát hiện thực tế” |
| Descriptive | estimand/statistic, sample size, sampling frame và uncertainty interval |

Primary metric MUST được chọn trong Problem Card theo chi phí quyết định:

- false positive bị giới hạn → primary là precision tại recall floor hoặc false alerts/entity/day;
- false negative bị giới hạn → primary là recall tại precision floor;
- xác suất được dùng trực tiếp → primary gồm proper scoring rule (Brier/log loss) và calibration;
- regression lỗi lớn có chi phí bình phương → RMSE; còn lại → MAE;
- anomaly kéo dài theo thời gian → event-level metric, MUST NOT chỉ dùng point-wise accuracy.

Accuracy MUST NOT là primary metric cho binary classification nếu majority-class baseline accuracy đã đạt success criterion hoặc positive class là lớp hành động hiếm; trong trường hợp đó dùng PR-based và operational metrics.

### 8.4. Slice, uncertainty và acceptance criteria

[S12 | E03,E11,E15]

Evaluation Protocol MUST ghi:

```yaml
primary_metric:
primary_acceptance_threshold:
guardrail_metrics_and_thresholds:
operational_metrics_and_thresholds:
slices:
uncertainty_method:
confidence_level: 0.95
stochastic_repetitions:
locked_test_snapshot:
experiment_tracker:
tracking_location:
artifact_location:
```

Quy tắc:

1. Slice MUST gồm mọi population được G0 liệt kê và mọi nhóm có semantics/source khác nhau.
2. Metric MUST kèm sample size/support.
3. Model stochastic MUST chạy tối thiểu 5 seed; báo mean, standard deviation và từng seed. `5` là project convention nhằm thực thi yêu cầu error bars của E15.
4. Deterministic model chạy một lần; MUST ghi `stochastic_repetitions: 1` và lý do deterministic.
5. So sánh candidate-baseline MUST báo 95% interval của delta trên evaluation unit độc lập. Time series MUST dùng block/entity/event resampling thay vì bootstrap từng row nếu row có autocorrelation.
6. Candidate chỉ được tuyên bố “tốt hơn” nếu interval của delta không chứa giá trị không-cải-thiện và toàn bộ guardrail đạt ngưỡng.

### 8.5. Feature contract

Mục này mở rộng S12: feature là một phần của Evaluation Protocol và MUST được đóng băng cùng nó tại G2. Hoãn tới handoff thì không còn ai nhớ vì sao một feature được chọn.

Mỗi feature MUST có một dòng:

```yaml
feature:
definition:            # công thức trên window, khớp với code tạo feature
unit:
definition_source:     # protocol section và code triển khai; không thay cho lý do chọn
targets_behaviour:     # hành vi hoặc lỗi mà feature nhằm đo; hoặc "data sufficiency" nếu chỉ là kiểm soát chất lượng
behaviour_basis:       # recorded decision hoặc inference from definition; không coi inference là lịch sử lựa chọn
used_by:               # model dùng để score, eligibility, hoặc diagnostic only; ghi rõ từng vai trò
decision_source:       # nơi ghi lý do chọn, owner + ngày nếu có; thiếu thì OWNER_DECISION_REQUIRED
```

Quy tắc:

1. `definition` MUST khớp với code tạo feature; khác nhau là FAIL G2.
2. `decision_source` MUST trỏ tới nơi lý do chọn được ghi lại. Định nghĩa đã được duyệt không chứng minh lý do chọn đã được ghi nhận. Nếu không có, ghi `OWNER_DECISION_REQUIRED`; agent MUST NOT tự đặt lý do. Agent có thể giải thích hành vi suy ra từ công thức, nhưng MUST ghi `behaviour_basis` là inference và không coi đó là bằng chứng về hiệu quả phát hiện.
3. Mọi candidate feature từng được cân nhắc (trong plan cũ, notebook cũ hoặc nghiên cứu trước) nhưng không vào protocol MUST được liệt kê với lý do loại hoặc `OWNER_DECISION_REQUIRED`. Phân biệt feature bị loại, đổi tên, đổi định nghĩa và metadata; không gọi alias là feature bị loại. Alternative window lengths được ghi riêng.
4. Feature được tính nhưng không model nào dùng để score MUST được ghi rõ trong `used_by`, kèm vai trò eligibility/diagnostic nếu có và lý do giữ. Model chỉ dùng một subset MUST có danh sách subset khớp code và nguồn lý do lựa chọn subset, hoặc `OWNER_DECISION_REQUIRED`.
5. `02_eda.ipynb` MUST trình bày feature contract trước khi mô tả phân phối feature, và lưu nó thành artifact.
6. Khi bổ sung giải thích vào protocol đã đóng băng, giữ nguyên artifact và hash cũ; dùng sidecar có version, tham chiếu protocol hash và ghi trạng thái decision chưa giải quyết. Approval cho việc cập nhật tài liệu không phải approval cho lý do lựa chọn chưa được cung cấp. G2 chưa được reaffirm PASS khi thiếu lý do bắt buộc.

## 9. G3 — Baseline implementation

[S13 | E01,E07,E08,E09]

`04_baselines.ipynb` MUST:

1. Load đúng Gold snapshot và split manifest đã khóa ở G2.
2. Chạy toàn bộ baseline bắt buộc ở S10.
3. Log mỗi baseline thành một experiment run riêng trong tracker đã chọn ở G2.
4. Dùng cùng feature availability, metric implementation và evaluation unit với candidate.
5. Xuất comparison table có metric, interval, runtime, artifact size và failure examples.
6. Chọn `strongest_baseline_id` theo primary metric trong tập baseline PASS toàn bộ guardrail threshold của S12.

Nếu rule-based hoặc statistical baseline đạt success criteria, candidate experiment vẫn được phép thực hiện và MUST dùng baseline đó làm chuẩn so sánh. Nếu không đăng ký candidate hypothesis, G4 MUST ghi `no-change decision` và chọn strongest baseline làm selected run. Nếu candidate không vượt baseline theo S12.6, quyết định MUST là giữ baseline, trừ khi có Decision Record được duyệt.

## 10. G4 — Candidate experiments

[S14 | E02,E13,E15]

### 10.1. Candidate là gì

Candidate là một hypothesis đã đăng ký: một thay đổi có kiểm soát so với reference run. Thay đổi đó có thể là họ model, tập feature, cách tính score, chính sách threshold hoặc preprocessing.

Candidate không nhất thiết là ML model. Một rule hoặc phương pháp thống kê khác với reference cũng là candidate khi nó được đăng ký như một hypothesis. ML model không bắt buộc ở G4; xem mục 10.3 về kết quả hợp lệ khi không candidate nào vượt reference.

### 10.2. Approach-space record

Trước khi đăng ký hypothesis, researcher MUST ghi một Decision Record trong `research-log.md` liệt kê các họ approach đã được cân nhắc. Mỗi họ có đúng một trạng thái:

| Họ approach | Trạng thái |
|---|---|
| Rule-based | `tried: <hypothesis_id>`, `not_tried: <lý do>` hoặc `OWNER_DECISION_REQUIRED` |
| Statistical | như trên |
| Unsupervised ML | như trên |
| Supervised ML | như trên; `not_tried: no labels` là lý do hợp lệ khi không có nhãn |
| Họ khác phù hợp với task | như trên |

Quy tắc:

1. Agent MUST NOT tự đặt lý do cho `not_tried`. Lý do phải là sự thật kiểm chứng được (ví dụ không có nhãn) hoặc đã được owner ghi lại; ngược lại ghi `OWNER_DECISION_REQUIRED`.
2. Họ approach mà hệ thống tiêu thụ model hỗ trợ (theo `operational_constraints` của Problem Card) MUST được liệt kê, kể cả khi chưa thử.
3. Họ ở trạng thái `OWNER_DECISION_REQUIRED` không chặn G4 PASS, nhưng MUST xuất hiện trong báo cáo G4 như một mục mở. Khi `research_deliverable` là `model_selection`, mọi họ MUST có trạng thái khác `OWNER_DECISION_REQUIRED` trước khi G5 bắt đầu.

### 10.3. Kết quả G4

Báo cáo G4 MUST nêu đúng một outcome bên cạnh trạng thái gate:

| Outcome | Nghĩa |
|---|---|
| `IMPROVEMENT_FOUND` | Có candidate vượt reference theo S12.6 và đạt mọi guardrail; selected run là candidate đó |
| `NO_CHANGE` | Mọi hypothesis đã đăng ký đều có kết quả và không candidate nào vượt reference theo S12.6; selected run là reference hoặc strongest baseline |
| `NO_CANDIDATE_REGISTERED` | Không có hypothesis nào được đăng ký; cần Decision Record nêu lý do, selected run là strongest baseline |

`G4: PASS` chỉ nghĩa là mọi hypothesis đã đăng ký có kết quả. Nó không nghĩa là đã tìm được model tốt hơn. `NO_CHANGE` là kết quả hợp lệ, không phải thất bại, nhưng MUST được báo cáo là "đã thử và không candidate nào vượt baseline", không được diễn đạt như một cải tiến.

### 10.4. Đăng ký hypothesis

Mỗi experiment MUST có `hypothesis_id` và chỉ thay đổi một nhóm yếu tố:

```yaml
hypothesis_id:
question:
expected_mechanism:
change_from_reference_run:
fixed_components:
dataset_snapshot:
split_version:
primary_expected_effect:
falsification_condition:
```

Mỗi experiment run dùng trong báo cáo MUST log:

```text
problem_id, hypothesis_id, research_stage
git_commit, branch
dataset_snapshot_id, manifest_hash
schema_version, feature_version, split_version
model_class, all hyperparameters, seed
package/environment reference
train/validation metrics
slice metrics and support
threshold
runtime and principal compute resource
model, preprocessing pipeline, plots, eval table
run status and conclusion
```

`experiment_tracker` MUST là một backend được project cho phép và lưu được toàn bộ field/artifact ở trên. Nếu dùng MLflow, experiment name MUST là `<domain>-<task>-<environment>`. Với mọi backend, run ID MUST ổn định và run name MUST là `<stage>-<model>-<feature_version>-<yyyymmdd-hhmm>`.

Researcher MUST NOT xem locked-test metric ở G4.

## 11. G5 — Locked-test evaluation

[S15 | E03,E10,E11,E15]

`06_evaluation.ipynb` MUST chạy selected run và strongest baseline trên cùng locked test đúng một lần.

PASS chỉ khi đồng thời:

1. primary metric đạt `primary_acceptance_threshold`;
2. mọi guardrail đạt threshold;
3. mọi operational metric đạt threshold;
4. metric và support được báo cho mọi slice;
5. uncertainty report chứa đủ `uncertainty_method`, `confidence_level`, evaluation unit, interval của từng metric bắt buộc và delta candidate-baseline theo S12;
6. candidate-baseline claim tuân theo S12.6;
7. failure analysis có ít nhất false-positive và false-negative examples nếu có labels;
8. limitation và unsupported population được ghi.

Nếu không có ground truth, kết luận G5 MUST giới hạn ở technical readiness hoặc score stability. MUST NOT dùng từ Precision, Recall, accuracy thực tế hoặc “model tốt” cho unlabeled test.

## 12. Robustness và stress-test matrix

[S16 | E03,E10,E16]

Áp dụng mọi dòng có trigger đúng; không có danh sách tùy chọn.

| Trigger | Test bắt buộc |
|---|---|
| Có event time/streaming | missing window, delayed/late data, out-of-order event, duplicate event |
| Có categorical ID/category | unseen category và category bị thiếu |
| Có external dependency | timeout, error response, stale response và fallback |
| Có real-time SLA | p50/p95/p99 latency, throughput và load tại capacity đã khai báo |
| Có class imbalance | prevalence shift và threshold sensitivity |
| Có entity/site/profile slices | metric và coverage theo từng slice |
| Có rolling/lag feature | boundary test để chứng minh không đọc tương lai |
| Có retraining | schema drift, feature drift, label delay và empty training window |
| Có model stochastic | seed variability theo S12 |

Stress result MUST được log thành artifact và link trong locked-test report.

## 13. Notebook specification

[S17 | E02,E12,E19]

### 13.1. Header chuẩn

Cell đầu tiên của mọi notebook MUST có đúng các mục, mỗi mục là một đoạn riêng (cách nhau bằng dòng trống). Label theo ngôn ngữ của topic; bảng dưới là bản `vi`, bản `en` nằm trong `assets/en/notebook-header.md`.

```markdown
# <Số> — <Tên notebook>

**Problem ID:**

**Stage/Gate:**

**Câu hỏi duy nhất:**

**Ngoài phạm vi:**

**Input snapshot/manifest:**

**Output artifact:**

**Config:**

**Git commit:**

**Cách chạy:**

**Ngày chạy UTC:**

**Status:** NOT_STARTED|IN_PROGRESS|PASS|FAIL|STOPPED
```

### 13.2. Thứ tự section

Notebook được tổ chức theo câu hỏi, không theo các bước thực thi. Tên section theo ngôn ngữ của topic (`en` / `vi`):

```text
1. Questions / Câu hỏi
2. Setup
3. Analysis / Phân tích
   3.1. <câu hỏi 1>
   3.2. <câu hỏi 2>
   ...
4. Output checks and artifacts / Output assertions và artifacts
5. Findings / Kết luận
```

1. **Câu hỏi** liệt kê các câu hỏi được đánh số `1.`..`n.`, mỗi câu kèm lý do nó quan trọng cho quyết định của gate. Câu hỏi duy nhất trong header được chia nhỏ thành các câu hỏi này.
2. **Setup** gồm configuration, import, environment capture, input loading và input assertions. Setup MUST NOT hiển thị table/figure.
3. **Phân tích** có đúng một block `### 3.k.` cho mỗi câu hỏi k, theo cùng thứ tự. Mọi table/figure MUST nằm trong một block.
4. **Output assertions và artifacts** kiểm tra output và lưu artifact.
5. **Kết luận** có findings table với đúng một dòng cho mỗi câu hỏi, sau đó là not proven, limitations và next decision.

### 13.3. Execution rules

1. Notebook MUST chạy thành công bằng `Restart Kernel and Run All`.
2. Seed, paths và parameters MUST nằm ở đầu Setup; cell sau MUST NOT gán lại.
3. Input loading MUST dùng snapshot/manifest, không dùng “file mới nhất”.
4. Input assertions MUST kiểm tra schema, time range, row count so với threshold trong S07 và duplicate rule.
5. Notebook MUST NOT chứa credential hoặc sửa Bronze data.
6. Cell lỗi, code chết và output debug MUST được xóa trước review.
7. Shared/production logic MUST nằm trong module có test; notebook chỉ gọi module. Module MUST expose một function cho mỗi câu hỏi phân tích, để mỗi block 3.k gọi đúng phần tính toán của nó; MUST NOT gom toàn bộ phân tích vào một lời gọi duy nhất.
8. Mọi bảng/figure được dùng trong claim MUST được lưu bằng tên ổn định và log vào run/artifact.

### 13.4. Figure/table rules

Mỗi figure MUST có title, axis name, unit, timezone/time range, sample size/support, legend và filter/aggregation note. Màu MUST NOT là kênh duy nhất phân biệt series/class.

Mỗi metric table MUST có dataset/split, metric definition/version, threshold nếu có, support và uncertainty.

### 13.5. Narrative

Notebook MUST đọc hiểu được mà không cần cuộc hội thoại đã tạo ra nó. Người đọc là một đồng nghiệp hiểu domain nhưng không biết standard này: họ phải biết notebook trả lời câu hỏi nào, mỗi câu hỏi được trả lời ra sao và câu trả lời thay đổi quyết định thế nào. Lập luận chỉ nằm trong hội thoại được coi là không tồn tại.

Khi `**Status:**` khác `NOT_STARTED`:

1. Mỗi block `### 3.k.` MUST có ba phần theo thứ tự: **What to look for** trước code cell đầu tiên, code cell, và **Answer** sau code cell cuối cùng.
2. **What to look for** MUST nêu table/figure sắp xuất hiện, cột hoặc vùng cần nhìn, và kết quả nào nghĩa là ổn, kết quả nào nghĩa là có vấn đề. Đây là tiêu chí; nó MUST được viết trước khi chạy code. Khi viết lại notebook mà kết quả đã được biết từ run trước, tiêu chí MUST lấy từ protocol, threshold hoặc Data Contract đã duyệt, và `research-log.md` MUST ghi rằng tiêu chí không được đăng ký trước.
3. **Answer** MUST trả lời câu hỏi ngay ở câu đầu tiên (có số), nói rõ đạt hay không đạt tiêu chí trong **What to look for**, và nêu hệ quả cho bước tiếp theo.
4. Mỗi code cell hiển thị tối đa một table/figure và MUST được theo sau bởi markdown.
5. Rule ID, evidence ID và gate code (`S05`, `E12`, `G1`) MUST NOT xuất hiện trong câu hỏi, **What to look for** hoặc **Answer**. Chúng nằm trong một dòng **Trace** ở cuối block.
6. Mọi vấn đề được nhắc tới trong prose MUST là một câu hỏi có block riêng hoặc được ghi trong **Not proven**. Không để vấn đề được nêu ra rồi bỏ lửng.
7. Findings table MUST có một dòng cho mỗi câu hỏi với verdict `Met` / `Not met` / `Partly met` / `Undetermined` (`vi`: `Đạt` / `Không đạt` / `Đạt một phần` / `Chưa xác định`). **Not proven** MUST NOT rỗng.
8. Notebook mô tả dữ liệu và kết quả, không mô tả lịch sử tạo ra chính nó (rerun, replay, sửa narrative). Lịch sử đó thuộc `research-log.md`.
9. Mọi placeholder `__NARRATIVE_REQUIRED__` MUST được thay bằng nội dung.

Label theo ngôn ngữ của topic, số từ tối thiểu và ví dụ nằm trong [`writing.md`](writing.md) section 3. Validator kiểm tra cấu trúc; việc câu trả lời có thực sự trả lời câu hỏi được kiểm tra khi review.

### 13.6. Layout prose

Markdown cell, `research-plan.md`, `research-log.md` và gate report MUST tuân theo [`writing.md`](writing.md) section 2: không ngắt dòng giữa câu, mỗi đoạn một ý, các dòng `**Label:**` cách nhau bằng dòng trống, mỗi bullet một ý.

## 14. Research plan và research log

[S18 | E02,E15]

`research-plan.md` là current state và được phép cập nhật. `research-log.md` là append-only và MUST NOT xóa negative result.

Mỗi log entry MUST dùng template dưới đây (bản `vi`; bản `en` nằm trong `assets/en/research-log.md`). Mỗi label là một đoạn riêng, cách nhau bằng dòng trống.

```markdown
## YYYY-MM-DD — <Experiment/Decision ID> — <Tên>

**Stage/Gate:**

**Câu hỏi:**

**Giả thuyết:**

**Dữ liệu/snapshot:**

**Phương pháp/config:**

**Run/artifact:**

**Kết quả định lượng:**

**Uncertainty/support:**

**Giới hạn:**

**Kết luận:**

**Decision:**

**Bước tiếp theo:**
```

Claim MUST có population, period/split, baseline, metric delta, uncertainty và limitation. Ví dụ đạt chuẩn:

```text
Trên locked test 01–07/09 gồm 412 sự kiện của 2130 thiết bị, candidate giảm false alerts/device/day từ 0.42 xuống 0.31 so với baseline (delta -0.11; 95% CI [-0.14; -0.08]) trong khi event recall giảm từ 0.78 xuống 0.77.

Chưa đánh giá trên site khác.
```

## 15. G6 — Handoff

[S19 | E03,E10,E11,E13,E16]

Trước production MUST có:

```text
model card
dataset/manifest card
feature contract (từ G2, mục 8.5, cập nhật nếu thay đổi)
locked-test report
experiment/run/model URI hoặc catalog identifier
inference interface and example
training-serving parity test
monitoring metric and threshold
data/model drift response
fallback and rollback procedure
owner and review date
```

Model Card MUST ghi intended use, unsupported use, supported/excluded population, train/eval snapshots, metric theo slice, operational constraints, failure modes, ethical/privacy concerns và expiry/review condition.

## 16. Definition of Done

[S20 | E02,E03,E10,E11,E15]

Nghiên cứu có trạng thái `COMPLETE` chỉ khi:

1. Gate mục tiêu đã PASS và artifact của mọi gate trước tồn tại.
2. Mọi claim truy được tới snapshot, code commit, run và artifact.
3. Baseline và candidate dùng cùng Evaluation Protocol.
4. Locked test không bị dùng để tune.
5. Metric đáp ứng S11; uncertainty và support đáp ứng S12; mọi slice trong Evaluation Protocol có kết quả; failure analysis đáp ứng S15.7.
6. Notebook chạy lại từ kernel sạch.
7. Kết luận ghi điều đã chứng minh, chưa chứng minh và population được hỗ trợ.
8. Nếu mục tiêu là production, G6 PASS.

Model phức tạp không phải điều kiện hoàn thành. Các trạng thái kết luận hợp lệ gồm “rule/statistical baseline đạt success criteria”, “dữ liệu không đạt readiness threshold”, “không tìm thấy signal dự báo theo Evaluation Protocol” hoặc “candidate đạt gate”.

## 17. Anti-patterns — tự động FAIL gate

[S21 | E01,E02,E06,E10,E15,E16]

- Thiếu Problem Card hoặc field còn `TBD`.
- Chọn thuật toán trước khi G0 PASS.
- Không có manifest/snapshot ID.
- Sửa Bronze hoặc ghi đè snapshot đã dùng.
- Fit preprocessing/threshold trên validation+test hoặc toàn bộ dữ liệu.
- Random split khi có time/group dependency.
- Dùng test để chọn feature/model/threshold rồi vẫn gọi là locked test.
- Candidate và baseline dùng dataset/split/metric code khác nhau.
- Bỏ baseline bắt buộc mà không có Decision Record.
- Dùng accuracy duy nhất cho positive class hiếm.
- Báo point-wise metric duy nhất cho range anomaly.
- Gọi weak/proxy/synthetic label là ground truth.
- Báo Precision/Recall khi không có label.
- Không báo support/slice/uncertainty theo protocol.
- Chọn champion bằng cách sort một metric mà bỏ guardrail/operational gate.
- Logic production chỉ tồn tại trong notebook.
- Notebook đã chạy nhưng thiếu narrative theo mục 13.5, hoặc lập luận chỉ nằm trong hội thoại.
- Xóa run thất bại hoặc negative result.
- Credential hoặc dữ liệu nhạy cảm xuất hiện trong Git/notebook/log.

## 18. Evidence traceability

Canonical registry và ma trận `Sxx → Exx` nằm tại [`evidence.md`](evidence.md). Mọi thay đổi rule ID hoặc evidence ID MUST cập nhật file đó trong cùng change.
