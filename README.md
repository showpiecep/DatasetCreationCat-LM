# CAT-LM_artifacts

## Training CAT-LM

We provide all scripts to reproduce our results for training CAT-LM.

### Data Collection and Preprocessing

**Mining data from GitHub (Training/GitHubMining)**
1. Run `python3 gh_crawler.py` to get a list of all the python and java repositories that have a minimum of 10 stars.
2. Run `mine_code_test_pairs_java.sh` and `mine_code_test_pairs_python.sh` to mine data and extract the code-test file pairs for python and java.
3. Run `mine_testdata.sh` to mine test data for python and java.

**Data Preprocessing (Training/DataPrep)**
1. Run `deduplicate_data_java.sh` and `deduplicate_data_python.sh` to deduplicate data.
2. Run `concatenate_pairs.sh` to prepare the file pairs by concatenating the code and test files with the separator.
3. Run `make_train_test.sh` to prepare the final training and test dataset.
4. Run `get_updated_metadata_java.sh` and `get_updated_metadata_python.sh` to get the metadata after preprocessing.

**Perform Data Analysis (Training/DataAnalysis)**
1. Run `compute_all_corpus_stats.sh` to get the summary statistics for the entire data.
2. Run `python3 data_analysis.py` to get the visualizations and to analyse the data distributions.

**Train SentencePiece tokenizer (Training/SentencePieceTokenizer)**
1. Run `train_sentencepiece_model.sh` to train the SentencePiece tokenizer.

**Training CAT-LM (gpt-neox)**
1. Run `pip3 install  -r gpt-neox/requirements/requirements.txt` in the directory to install all requirements.
2. Run `python3 -u gpt-neox/deepy.py gpt-neox/train.py -d gpt-neox/configs 2-7B.yml local_setup.yml | tee train-log.txt` to tokenize and prepare the training data.
3. Run `python3 -u gpt-neox/deepy.py gpt-neox/train.py -d gpt-neox/configs 2-7B.yml local_setup.yml | tee train-log.txt` to train the CAT-LM model.
4. Run `python3 gpt-neox/deepy.py gpt-neox/generate.py -d gpt-neox/configs 2-7B.yml local_setup.yml text_generation.yml` to run inference with CAT-LM.

## Evaluation

We provide all evaluation scripts to reproduce our results for comparing with TeCo on Test Completion and with CodeGen on Test Generation.

### Test Completion (Evaluation/Test Completion)
In order to reproduce the results we obtained for comparing with TeCo, one must follow the steps below:

**First you need to setup TeCo (Evaluation/Test Completion/TeCo)**
1. Clone the [TeCo](https://github.com/EngineeringSoftware/teco/tree/main) repository.
2. Follow all requirements and installation steps from the TeCo repository, stop at the step "inv data.eval-setup". This will give the TeCo test set used in their evaluation.
3. Run `dataset_to_context.sh` in the "Test Completion" subdirectory.
4. Run `enforce_teco_sample.sh` to take the ids chosen for our new test set and create a split for TeCo.
5. Replace your old TeCo setup directory with the new one created in the previous step.
6. Run the following command to compute lexical metrics on TeCo.

`inv exp.eval-single --setup CSNm --overwrite --suffix teco-norr --trained CodeT5-teco-norr --decoding bs10 --eval-set eval-any-stmt/test --args "--seed_everything=4197"`

7. Lexical metrics for TeCo are available at: `teco/_work/exp/CSNm/eval-any-stmt/test/SingleEvaluator-teco-norr/bs10-last/metrics_summary.json`

**To compute predictions for CAT-LM run the following commands (Evaluation/Test Completion)**

1. Run the script `json_to_contexts.sh`. This generates the input contexts for CAT-LM.
2. Once you have prompted CAT-LM, postprocess the generated tests by running `postprocess_generated_tests.sh`.

**Finally to compute lexical metrics on CAT-LM run the following commands (Evaluation/Analysis)**

1. In Analysis/TextMetrics run `compute_metrics_teco.sh` to compute lexical metrics on TeCo's postprocessed statement generations.
2. Run `aggregate_metrics_teco.sh `to aggregate the metrics computed in the previous step, this will output a JSON file with all lexical metrics.

### Test Generation (Evaluation/Test Generation)

In order to reproduce the results we obtained for comparing with CodeGen, one must follow the steps below:

**First you need to setup all runnable projects (Evaluation/Test Generation/TestFiltering)**
1. Build all docker images for the TestingFramework by running `build_images.sh` in the Dockerfiles subdirectory.
2. Run `filter_test_set_fp.sh` to filter the test set to only contain repositories with filepairs.
3. Run `get_all_java_logs.sh` to get a list of java filepairs we can execute.
4. Run `get_all_python_logs.sh` to get a list of python filepairs we can execute.
5. Run `aggregate_data.py` to aggregate all the data from the previous steps into a file with all the projects we can execute.

**Then you need to prompt CAT-LM (Evaluation/Test Generation/TestDataPrep)**
1. Run `input_context_generation_java.sh` to generate the input contexts for CAT-LM for java.
2. Run `input_context_generation_python.sh` to generate the input contexts for CAT-LM for python.
3. Run `input_config_generation.sh` to generate the configuration files required for CAT-LM for both java and python.
4. Run `write_test_baselines_files.py` to generate the baseline files for the test generation task.
5. Update config `gpt-neox/configs/local_setup.yml` config file to point to the model weights.
4. Run `generate_tests_java_t0.2.sh` and `generate_tests_python_t0.2.sh` to prompt CAT-LM and get the generations for java and python.
4. Once you prompt CAT-LM, run `postprocess_generated_tests.sh` to postprocess the generated tests.

**You now need to run the Testing Framework on the generated tests (Evaluation/Test Generation/TestFramework)**
1. In "TestingFramework" run `main_framework_filepairs_testing_llm.sh` to run all java and python filepairs and ensure we can get coverage.
2. Run `aggregate_data_filepairs_testing_llm.sh` to get a list of all the filepairs we can run.
3. Run `diff_and_resample_filepairs.sh` to sample 10 filepairs for each project in Python.
4. Also run `golds_to_json.sh` to generate the golds for the Testing Framework.
5. Now you are read to run the testing framework. To do this, run `main_framework_filepairs_testing_llm.sh`.
6. Finally you need to aggregate all the results, run `aggregate_data_testing_llm.sh`. This will output a CSV with all the tests generated and whether they could run or not and coverage statistics.

**Finally you need to compute lexical and runtime metrics (Evaluation/Analysis)**
1. To compute lexical metrics, run `compute_metrics_test_framework.sh` in Analysis/TextMetrics.
2. Aggregate these metrics with `aggregate_metrics_test_framework.sh`.
3. For runtime metrics run `compute_generation_stats_testing_llm.sh` in Analysis/TestDataAnalysis, this will output a JSON file with all the runtime metrics for each model and mode run.
