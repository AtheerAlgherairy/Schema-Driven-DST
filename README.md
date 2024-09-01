# The Effect of Different Schema-Driven Prompting for Dialogue State Tracking

To replicate the experiments from the paper "The Effect of Different Schema-Driven Prompting for Dialogue State Tracking," follow these steps:

- [Fork Convlab-3 and Add the Files](#fork-convlab-3-and-add-the-files)
- [Create Datasets for Different Scenarios](#create-datasets-for-different-scenarios)
- [T5 Training for DST](#t5-training-for-dst)
- [Evaluation](#evaluation)
- [Citing](#citing)
- [Source](#source)

## Fork Convlab-3 and Add the Files

1. Fork the following repository: [Convlab-3](https://github.com/ConvLab/ConvLab-3) (Many thanks to all contributors).
2. For more details on Convlab-3, refer to the [paper](https://aclanthology.org/2023.emnlp-demo.9/).
3. After forking Convlab-3:
   a. add `create_data_latest.py` to the `convlab/base_models/t5` directory.
   b. add `dst_metric_v2.py` and `merge_predict_res_v2.py` to the `convlab/base_models/t5/dst` directory.

## Create Datasets for Different Scenarios

To prepare different scenarios for the Schema Guided Dialogue (SGD) dataset and the MultiWOZ dataset:
Navigate to the convlab/base_models/t5 folder. Run the followings:

**Scenario 1: No Prompting**
(using create_data.py the original code in Convlab-3)
```bash
python create_data.py --tasks dst --datasets sgd --speaker user --context_window_size 50
python create_data.py --tasks dst --datasets mwoz --speaker user --context_window_size 50
```

**Scenario 2: Prompting with Slot Names Only**
```bash
python create_data_latest.py.py --tasks dstName --datasets sgd --speaker user --context_window_size 50
python create_data_latest.py.py --tasks dstName --datasets mwoz --speaker user --context_window_size 50
```
**Scenario 3: Prompting with Slot Names and Descriptions**
```bash
python create_data_latest.py.py --tasks dstNameDesc --datasets sgd --speaker user --context_window_size 50
python create_data_latest.py.py --tasks dstNameDesc --datasets mwoz --speaker user --context_window_size 50
```
**Scenario 4: Prompting with Slot IDs and Descriptions**

Adjust the URL for ontologyIDs.json (available in this repository for the SGD and MultiWOZ datasets).

```bash
python create_data_latest.py.py --tasks dstIDDesc --datasets sgd --speaker user --context_window_size 50
python create_data_latest.py.py --tasks dstIDDesc --datasets mwoz --speaker user --context_window_size 50
```
## T5 Training for DST
1. Navigate to the convlab/base_models/t5 folder.
2. Run run_seq2seq.py for training, specifying the URL of your dataset (train and validation files) and the name of model (model_name_or_path t5-small or t5-base):

```bash
python run_seq2seq.py \
    --task_name dst \
    --train_file PATH_TO_YOUR_TRAIN_FILE \
    --validation_file PATH_TO_YOUR_VALIDATION_FILE \
    --source_column context \
    --target_column state_seq \
    --max_source_length 1024 \
    --max_target_length 512 \
    --truncation_side left \
    --model_name_or_path t5-small \
    --do_train \
    --do_eval \
    --save_strategy epoch \
    --evaluation_strategy epoch \
    --save_total_limit 1 \
    --prediction_loss_only \
    --cache_dir PATH_TO_YOUR_CACHE_DIR \
    --output_dir PATH_TO_YOUR_OUTPUT_DIR \
    --logging_dir PATH_TO_YOUR_LOGGING_DIR \
    --overwrite_output_dir \
    --preprocessing_num_workers 4 \
    --per_device_train_batch_size 32 \
    --per_device_eval_batch_size 32 \
    --gradient_accumulation_steps 4 \
    --learning_rate 1e-4 \
    --num_train_epochs 10 \
    --optim adafactor \
    --gradient_checkpointing \
    --early_stopping_patience 5 \
    --load_best_model_at_end


```
## Evaluation

1. Navigate to the convlab/base_models/t5 folder.
2. Run run_seq2seq.py for evaluation, specifying the URL of your dataset (test file) and the model output from the previous step:
3. *Note:* When experimenting with IDs, use dst_metric_v2.py instead of dst_metric.py and merge_predict_res_v2.py instead of merge_predict_res.py. These updated scripts reverse the slot IDs back to names using ontologyID.json.
   
```bash
python run_seq2seq.py \
    --task_name dst \
    --test_file PATH_TO_YOUR_TEST_FILE \
    --source_column context \
    --target_column state_seq\
    --max_source_length 1024 \
    --max_target_length 512 \
    --truncation_side left \
    --model_name_or_path PATH_TO_YOUR_TRAINED_MODEL \
    --do_predict \
    --predict_with_generate \
    --metric_name_or_path dst_metric.py \
    --cache_dir ..\cache \
    --output_dir PATH_TO_YOUR_OUTPUT_DIR \
    --logging_dir PATH_TO_YOUR_LOGGING_DIR \
    --overwrite_output_dir \
    --preprocessing_num_workers 4 \
    --per_device_train_batch_size 32 \
    --per_device_eval_batch_size 32 \
    --gradient_accumulation_steps 4 \
    --learning_rate 1e-4 \
    --num_train_epochs 10 \
    --optim adafactor \
    --gradient_checkpointing


```

3. After evaluation, a *generated_predictions.json* will be generated in the output folder, use its path for PATH_TO_GENERATED_PREDICTIONS_JSON_FILE
4. Navigate to the convlab/base_models/t5/dst folder.
5. Run merge_predict_res.py a *predictions.json* will be generated in the output folder, use its path for PATH_TO_PREDICTIONS_JSON_FILE
7. Run evaluate_unified_datasets.py
   
```bash
python merge_predict_res.py -d multiwoz21 -s user -c 50 -p PATH_TO_GENERATED_PREDICTIONS_JSON_FILE

python evaluate_unified_datasets.py -p PATH_TO_PREDICTIONS_JSON_FILE

```
## Citing

