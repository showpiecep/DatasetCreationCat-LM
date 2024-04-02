input="./data/teco_config_paths_t0.2_n10.txt"
while IFS= read -r file
do
  echo "Processing $file"
  sudo cp $file ./configs/
  sudo python3 ./deepy.py generate.py -d configs 2-7B.yml local_setup.yml text_generation_teco_t0.2_n10.yml 
done < "$input"


# unbuffer ./generate_tests_teco_t0.2.sh  | sudo tee output_generation_teco_t0.2_n10.txt