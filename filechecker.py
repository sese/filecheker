import os
import hashlib
from dbs3 import Db


def md5sum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def readFolder(folderName):
    files = {}
    # r=root, d=directories, f = files
    for r, d, f in os.walk(folderName):
        for file in f:
            fileName = os.path.join(r, file)
            try:
                md5 = md5sum(fileName)
            except OSError:
                # print("Ignore file {} cannot be opened".format(fileName))
                continue
            files[fileName] = md5

    return files


exit(0)

folderName = "/etc"
files = readFolder(folderName)


db = Db()
# db.saveFiles(files)

stats = {
    "new": 0,
    "mod": 0,
    "total": 0
}

for fileName, md5 in files.items():
    result = db.test_file(fileName, md5)
    stats["total"] += 1
    if result == -1:
        stats["new"] += 1
        print("New File: {}".format(fileName))
    elif result == 0:
        stats["mod"] += 1
        print("Modified File: {}".format(fileName))

print("=" * 80)
print("Total files: {:>6}".format(stats["total"]))
print("New files  : {:>6}".format(stats["new"]))
print("Mod files  : {:>6}".format(stats["mod"]))
