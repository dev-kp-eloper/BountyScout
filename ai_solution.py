```python
def format_bounty_results(bounty_list):
    formatted_results = []
    for item in bounty_list:
        lines = item.split('\n')
        id = lines[0].strip().split('.')[0].strip('[]')
        title = lines[0].split('### ')[1].strip()
        repository = lines[1].strip().split('**Repository:** ')[1].split(' (')[0].strip()
        comments = lines[2].strip().split('**Comments:** ')[1].strip()
        last_updated = lines[3].strip().split('**Last Updated:** ')[1].strip()
        formatted_results.append({
            'id': id,
            'title': title,
            'repository': repository,
            'comments': comments,
            'last_updated': last_updated
        })
    return formatted_results
```