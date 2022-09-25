# utf-8
import eyed3

def embed_image_on_mp3(audiopath:str, imagepath:str, imagemime:str):
    '''
    (既に保存されたファイルを想定)
    mp3ファイルのパス、画像ファイルのパス、画像ファイルのmimetypeを送ると、
    mp3ファイルに対して画像ファイルを埋め込む。

    Eng:
    (condition:files are already saved.)
    This function needs filepaths(str) and mimetype(str)
    '''
    audio_eyed3 = eyed3.load(audiopath)
    if not audio_eyed3.tag : audio_eyed3.initTag()
    with open(imagepath, 'rb') as cover_art :
        audio_eyed3.tag.images.set(3, cover_art.read(), imagemime)
    audio_eyed3.tag.save(max_padding=64)

    return
