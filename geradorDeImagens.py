from PIL import Image, ImageDraw

# Tamanho da imagem em pixels
tamanho = 100

# Criar imagens para as peças numeradas
for numero in range(1, 9):
    imagem = Image.new("RGB", (tamanho, tamanho), color="white")
    draw = ImageDraw.Draw(imagem)
    draw.text((tamanho // 2 - 10, tamanho // 2 - 10),
              str(numero), fill="black")
    imagem.save(f"{numero}.png")

imagem_vazia = Image.new("RGB", (tamanho, tamanho), color="white")
imagem_vazia.save("vazio.png")
