import urllib.parse
import urllib.request
import json


__all__ = ['jsearch', 'jprint']


def jsearch(string, clean_up=True):
    '''
    The top level search request function
    '''
    s=f'https://jisho.org/api/v1/search/words?keyword={urllib.parse.quote(string)}'
    data = operUrl = urllib.request.urlopen(s)
    if data.getcode() != 200:
    	raise LookupError(f'Bad HTTP request: Code {data.getcode()}.')
    data = data.read()
    data = json.loads(data)['data']
    return [jclean(i) for i in data] if clean_up else data

def jclean(d):
    '''
    Strip the jsho.org json dict of unnecessary entries
    '''
    ret   = {}
    jap   = d['japanese']
    trans = d['senses']
    ret['Kanji'] 	= set([i['word']    if 'word'    in i else '' for i in jap])
    ret['Reading'] 	= set([i['reading'] if 'reading' in i else '' for i in jap])
    ret['Meaning'] 	= [ {k:i[k] for k in ['parts_of_speech','english_definitions', 'tags', 'antonyms', 'info']} for i in trans ]
    ret['Tags']		= d['tags']
    if 'is_common' in d and d['is_common']:
        ret['Tags'].append('common')
    return ret

def jprint(d):
    '''
    Print the dict niceley to screen
    '''
    print(f'Kanji:    {", ".join(d["Kanji"]):<20}')
    for num,i in enumerate(d['Reading'],1):
        if num == 1: print(f'Reading:  {num}. {i}')
        else:	  	 print(f'          {num}. {i}')
    if d['Tags']:
        print(f'Tags:     {", ".join(d["Tags"]):<20}')
    print()
    cnt = 1
    for i in d['Meaning']:
        print(', '.join(j for j in i['parts_of_speech']))
        for j in i['english_definitions']:
            print(f'  {cnt}. {j}')
            cnt += 1
        if i['info']:
            print(f'  Info: {"; ".join(ii for ii in i["info"])}')
        if i["tags"]:
            print(f'  Tags: {", ".join(tag for tag in i["tags"])}')
    print('---')
# %%
# raw = jsearch('helo', False)
# jclean(raw[4])
# jprint(raw[0])
