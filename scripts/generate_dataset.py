import json
import os

def main():
    input_file = 'data/hotpot_dev_distractor_v1.json'
    output_file = 'data/evaluation_100.json'
    
    if not os.path.exists(input_file):
        print(f'Input file {input_file} not found.')
        return
        
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    res = []
    for item in data[:100]:
        context = []
        for ctx_item in item.get('context', []):
            title = ctx_item[0]
            text = ' '.join(ctx_item[1])
            context.append({
                'title': title,
                'text': text
            })
            
        new_item = {
            'qid': item['_id'],
            'difficulty': item.get('level', 'medium'),
            'question': item['question'],
            'gold_answer': item['answer'],
            'context': context
        }
        res.append(new_item)
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=2)
        
    print(f'Generated {len(res)} items to {output_file}')

if __name__ == '__main__':
    main()

