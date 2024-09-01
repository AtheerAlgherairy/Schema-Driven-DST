# The effect of different schema-driven prompting for dialogue state tracking

First, forke the following repo: 
## Convlab-3  (Many thanks to all contributors)
For more details on ConvLab-3, see [paper](https://aclanthology.org/2023.emnlp-demo.9/).

To duplicate the code in paper: The effect of different schema-driven prompting for dialogue state tracking, follow the steps:

- [Create datasets for different scenarios](#create-datasets)
- [T5 training for DST ](#t5-training)
- [Evaluation ](#evaluation)
- [Citing](#citing)



## Create datasets for different scenarios

First, you need to fork the Convlab-3 and add "create_data_latest.py" under "convlab/base_models/t5"

Then, to prepare the different scenarios for the Schema Guided Dialogue (SGD) dataset and the MultiWOZ dataset, 


Scenario 1: No prompting
`
python create_data.py --tasks dst --datasets sgd --speaker user --context_window_size 50
`

`
python create_data.py --tasks dst --datasets mwoz --speaker user --context_window_size 50
`

Scenario 2: Prompting with slot names only
`
python create_data_latest.py --tasks dstName --datasets sgd --speaker user --context_window_size 50
`

`
python create_data_latest.py --tasks dstName --datasets mwoz --speaker user --context_window_size 50
`

Scenario 3: Prompting with slot names and descriptions:


`
python create_data_latest.py --tasks dstNameDesc --datasets sgd --speaker user --context_window_size 50
`

`
python create_data_latest.py --tasks dstNameDesc --datasets mwoz --speaker user --context_window_size 50
`

Scenario 4: Prompting with slot IDs and descriptions:
`
python create_data_latest.py --tasks dstIDDesc --datasets sgd --speaker user --context_window_size 50
`

`
python create_data_latest.py --tasks dstIDDesc --datasets mwoz --speaker user --context_window_size 50
`

## T5 Training for DST 

Go to `convlab/base_models/t5` folder and run "run_seq2seq.py" for each dataset, specify the URL of your dataset, the model (T5-base or T5-small):.

`
python run_seq2seq.py 
`

## Evaluation




## Citing
