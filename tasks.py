# tasks.py
import json
import execjs
import random
from utils.constants import *
from utils.mongo import *
from utils.generation import *


class Sampler:
    def __init__(self, traits):
        self.traits = traits

    def sample(self, n):
        output = []
        for i in range(n):
            trait_args = []
            for trait_type, values in self.traits.items():
                trait_args.append({'traitType': trait_type, 'value': random.choice(values)})
            output.append(trait_args)
        return output

def create_collection_if_not_exists(collection_name, db_name="experimentPlatform"):
    db = get_db(db_name)

    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

    # Access the collection
    coll = db[collection_name]

    # Step 4: Create Index
    # This creates an index on the 'prompt' field
    coll.create_index([('prompt', 1)])  # 1 for ascending order

def get_samples(traits_file, sampleNum):
    sampler = Sampler(traits_file)
    samples = sampler.sample(sampleNum)
    return samples

def store_mongo(dataEntry, collection_name):
    db = get_db("experimentPlatform")
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

    collection = get_collection(db, collection_name)

    insert(collection, dataEntry.__dict__)
    

def generate_images(config_file, traits_file, js_file, sampleNum, submitter_name, experiment_details, experiment_id, submittedDate):
    # Your long-running task logic here
    print("generate_images is called here")
    samples = get_samples(json.loads(traits_file), sampleNum)

    # with open(js_file, 'r') as js_file:
    #     js_code = js_file.read()
    #     print(js_code)
    js_code = js_file

    # Load config and trait arguments from JSON files
    # with open(config_file, 'r') as f:
    #     config = json.load(f)
    config = json.loads(config_file)

    # Create an ExecJS context
    ctx = execjs.compile(js_code)
    prompts = []
    for sample in samples:
        prompt = ctx.call('createPrompt', config, sample)
        prompts.append(prompt)
    
    base64images = []
    for prompt in prompts:
        base64image, revised_prompt = generate_one_sample(prompt)
        base64images.append(base64image)
        dataEntry = DataEntry(
            description= experiment_details,
            submitter=submitter_name,
            create_date=submittedDate,
            status="Success",
            imageResult=base64image,
            prompt=prompt,
            revised_prompt=revised_prompt
            )
        collection_name = f"experiment_{experiment_id}"
        store_mongo(dataEntry, collection_name)
    

    

    # print(query(collection_name))

    return base64images

if __name__ == '__main__':
    config_file = '{"id":"xibos-selected-6","version":"1","prefix":"I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: A simple pixel art image of a Chartreux cat in a natural sitting pose with 4 legs visible, facing directly at the viewer,","suffix":""}'
    traits_file = '{"Hat":["Alpine Hat","Ascot Cap","Aviator Hat"],"Eyes":["Has Angelic eyes","Has Bewitching eyes","Has Bold eyes"],"Mouth":["Angelic Savor","Belching","Blissful Munch "],"Clothes":["Anime School Uniform","Bandolier","Baseball Tee"],"Pet":["Alpaca Cria","Baby Albatross","Baby Albino Peacock"],"Necklace":["Beaded Necklace","Bib Necklace","Butterfly necklace"]}'
    js_file = "function _extractBreedGroup(traitType,value){var isBreedGroup=traitType.toLowerCase().trim()=='breed';if(isBreedGroup){return{traitType:traitType,value:value,group:'breed',extracted:value.trim()}}else{return null}}function _extractPetGroup(traitType,value){var isPetGroup=traitType.toLowerCase().trim()=='pet';if(isPetGroup){return{traitType:traitType,value:value,group:'pet',extracted:value.trim()}}else{return null}}function _extractBackgroundGroup(traitType,value){var isBackgroundGroup=traitType.toLowerCase().trim()=='background';if(isBackgroundGroup){return{traitType:traitType,value:value,group:'background',extracted:value.trim()}}else{return null}}function _extractIsGroup(traitType,value){var tokens=value.trim().split(' ');var matching_the_target_pattern=tokens.length==2&&tokens[0]=='is';if(matching_the_target_pattern){return{traitType:traitType,value:value,group:'is',extracted:tokens[tokens.length-1].trim()}}else{return null}}function _extractWithGroup(traitType,value){return{traitType:traitType,value:value,group:'with',extracted:value.trim().replace('wears','').replace('wearing','').replace('is wearing','').replace('has','').replace('Wears','').replace('Wearing','').replace('Is Wearing','').replace('Has','')}}function _extract(trait_arg){var handlers=[_extractBreedGroup,_extractBackgroundGroup,_extractPetGroup,_extractIsGroup,_extractWithGroup];for(let i=0;i<handlers.length;i++){var obj=handlers[i](trait_arg.traitType,trait_arg.value);if(obj!=null){return obj}}}function _makeGroups(traits_identified){return traits_identified.reduce((accumulator,currentItem)=>{const g=currentItem.group;if(!accumulator[g]){accumulator[g]=[]}accumulator[g].push(currentItem);return accumulator},{})}function _joinWithCommasAndAnd(values){if(values.length===0){return''}else if(values.length===1){return values[0]}else{const last=values.pop();const joined=values.join(', ');return`${joined},and ${last}`}}function _formatGroup(groups,groupName){if(!groups.hasOwnProperty(groupName)){return''}return _joinWithCommasAndAnd(groups[groupName].map(x=>x.extracted))}function createPrompt(config,trait_args){prompt=config.prefix;var traits_identified=trait_args.map(_extract);var groups=_makeGroups(traits_identified);var groupBreed=_formatGroup(groups,'breed');var groupIs=_formatGroup(groups,'is');var groupWith=_formatGroup(groups,'with');if(groupBreed!=''){prompt=prompt.replace(/image of a [\\w\\s]*[Cc]at/,'image of a '+groupBreed+' cat')}if(groupIs!=''&&groupWith!=''){prompt=prompt+' that is '+groupIs+' and with '+groupWith+'.'}else if(groupIs!=''){prompt=prompt+' that is '+groupIs+'.'}else if(groupWith!=''){prompt=prompt+' with '+groupWith+'.'}else{prompt=prompt+'.'}var groupPet=_formatGroup(groups,'pet');if(groupPet!=''){prompt=prompt+' It is accompanied by a pet '+groupPet+'.'}var groupBackground=_formatGroup(groups,'background');if(groupBackground!=''){prompt=prompt+' The image has a '+groupBackground+' background.'}else{' The image has a solid background.'}return prompt}"
    sampleNum = 2
    generate_images(config_file, traits_file, js_file, sampleNum,"xibo","Test",155,"20240314")