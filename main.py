import argparse, json, os, random, shutil, uuid, zipfile

parser = argparse.ArgumentParser(description='Convert Minecraft PC .zip resource packs to PE/Win10 .mcpack resource packs.')
parser.add_argument('input', help='Input .zip file')
parser.add_argument('output', help='Output .mcpack file')
parser.add_argument('--name', help='Recource pack name', required=True)
parser.add_argument('--version', help='Recource pack version', required=True)
parser.add_argument('--description', help='Recource pack description (default: copy from pack.mcmeta)')
parser.add_argument('--pack_id', help='Pack UUID')
parser.add_argument('--uuid', help='Module UUID')
args = parser.parse_args()

in_dir = 'tempin' + str(random.randint(0, 1000000))
in_zip = zipfile.ZipFile(args.input)
in_zip.extractall(in_dir)
in_zip.close()

if args.description == None:
    with open(in_dir + '/pack.mcmeta') as mcmeta_json:
        mcmeta = json.loads(mcmeta_json.read())
        args.description = mcmeta['pack']['description']

if args.pack_id == None:
    args.pack_id = str(uuid.uuid4())
    print('Using Pack UUID ' + args.pack_id + '.')

if args.uuid == None:
    args.uuid = str(uuid.uuid4())
    print('Using Module UUID ' + args.uuid + '.')

out_dir = 'tempout' + str(random.randint(0, 1000000))
shutil.copytree(in_dir + '/assets/minecraft/', out_dir) # textures
shutil.copyfile(in_dir + '/pack.png', out_dir + '/pack_icon.png') # icon

pack_manifest = {
    'header': {
        'pack_id': args.pack_id,
        'name': args.name,
        'packs_version': args.version,
        'description': args.description,
        'modules': [
            {
                'description': args.description,
                'version': args.version,
                'uuid': args.uuid,
                'type': 'resources'
            }
        ]
    }
}

json.dump(pack_manifest, open(out_dir + '/pack_manifest.json', 'w')) # pack manifest

out_zip = zipfile.ZipFile(args.output, 'w', zipfile.ZIP_DEFLATED)
os.chdir(out_dir)

for root, dirs, files in os.walk('.'):
    for file in files:
        out_zip.write(os.path.join(root, file))

os.chdir('..')
out_zip.close()

shutil.rmtree(in_dir)
shutil.rmtree(out_dir)
