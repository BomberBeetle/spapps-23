from PIL import Image
import numpy as np
from pydub import AudioSegment
import json

objects = {}

with open("objects.json", 'r') as file:
    objects = json.loads(file.read())


for idx in objects.keys():
    imagem = Image.open("object{}.png".format(idx))
    dados_numericos = np.array(imagem)

    # Defina o número de canais, a largura da amostra e a taxa de quadros
    numero_de_canais = 1  # Para áudio mono
    largura_da_amostra = imagem.dtype.itemsize
    frame_rate = 44100  # Você pode ajustar isso conforme necessário

    # Crie o objeto de áudio
    audio = AudioSegment(
        data=imagem_audio.tobytes(),
        sample_width=largura_da_amostra,
        frame_rate=frame_rate,
        channels=numero_de_canais
    )

    audio.export('object{}.wav'.format(idx), format='wav')
