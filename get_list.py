import os  


def get_list(path):
    result = []
    dirs = []
    images = []
    jsons = {}
    with os.scandir(path) as iter_dir:
        for entry in iter_dir:
            if entry.is_dir():
                dirs.append(entry.name)
                continue
            name, ext = os.path.splitext(entry.name)
            if ext.lower() in ('.png', '.jpeg', '.jpg'):
                images.append(entry.name)
            elif ext.lower() in ('.json'):
                jsons[name] = entry.name
    for dir in dirs:
        dir_entry = get_list('/'.join((path, dir)))
        if dir_entry:
            result.append({dir: dir_entry})
    for image in images:
        json = jsons.get(image.partition('.')[0], False)
        if json:
            result.append(
                ['/'.join((path, image)), '/'.join((path, json))]
            )
    return result

if __name__ == '__main__':
    labels_dir = '/tmp/labels'
    print(get_list(labels_dir))
