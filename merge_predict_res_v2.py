import json
import os
from convlab.util import load_dataset, load_dst_data
from convlab.base_models.t5.dst.serialization import deserialize_dialogue_state


def reverse_back(state_seq):
    #from numbers to slot names and pv numbers to pv values
    #schema_path= "SGD/ontologyIDs.json"
    schema_path= "multiwoz/ontologyIDs.json"
    schema =json.load(open(schema_path))
    
    decoded_dic={}
    domains=list(state_seq.keys())
    for domain in domains:
        new_item={}
        for item in state_seq[domain].items():
            slot_id=item[0]
            
            for slot in schema["domains"][domain]["slots"]:
                if int(slot_id)== schema["domains"][domain]["slots"][slot]['slot_ID']:
                    new_item[slot]=item[1]
                if schema["domains"][domain]["slots"][slot]['is_categorical']:
                    for pv in schema["domains"][domain]["slots"][slot]["possible_values"]:
                        result_string = pv.split(":")[0]
                        if item[1].strip() == result_string.strip():
                            new_item[slot]=pv.split(":")[1].strip()



        decoded_dic[domain]=new_item

    return decoded_dic

def merge(dataset_names, speaker, save_dir, context_window_size, predict_result):
    assert os.path.exists(predict_result)
    
    if save_dir is None:
        save_dir = os.path.dirname(predict_result)
    else:
        os.makedirs(save_dir, exist_ok=True)
    predict_result = [reverse_back(deserialize_dialogue_state(json.loads(x)['predictions'].strip())) for x in open(predict_result)]

    merged = []
    i = 0
    for dataset_name in dataset_names.split('+'):
        print(dataset_name)
        dataset = load_dataset(dataset_name, args.dial_ids_order)
        data = load_dst_data(dataset, data_split='test', speaker=speaker, use_context=context_window_size>0, context_window_size=context_window_size)['test']
    
        for sample in data:
            sample['predictions'] = {'state': predict_result[i]}
            i += 1
            merged.append(sample)

    json.dump(merged, open(os.path.join(save_dir, 'predictions.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="merge predict results with original data for unified NLU evaluation")
    parser.add_argument('--dataset', '-d', metavar='dataset_name', type=str, help='name of the unified dataset')
    parser.add_argument('--speaker', '-s', type=str, choices=['user', 'system', 'all'], help='speaker(s) of utterances')
    parser.add_argument('--save_dir', type=str, help='merged data will be saved as $save_dir/predictions.json. default: on the same directory as predict_result')
    parser.add_argument('--context_window_size', '-c', type=int, default=0, help='how many contextual utterances are considered')
    parser.add_argument('--predict_result', '-p', type=str, required=True, help='path to the output file generated_predictions.json')
    parser.add_argument('--dial_ids_order', '-o', type=int, default=None, help='which data order is used for experiments')
    args = parser.parse_args()
    print(args)
    merge(args.dataset, args.speaker, args.save_dir, args.context_window_size, args.predict_result)
