test_json="/code/teco/_work/setup/CSNm/split/test.json"
data_dir="/code/teco/_work/data"
downloads_dir="/code/teco/_work/downloads"
model_json="/code/teco/_work/setup/CSNm/split/test_model.json"
teco_json="/code/teco/_work/setup/CSNm/split/test_teco.json"

python3 dataset_to_context_json.py $test_json $data_dir $downloads_dir $model_json $teco_json