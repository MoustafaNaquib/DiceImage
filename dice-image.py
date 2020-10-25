from PIL import Image, ImageOps  
import requests
from io import BytesIO
dice_size = 10

dice_images = {
    num: Image.open(f"images/dice-real/{str(num)}.jpg").resize((10,10)) for num in [1,2,3,4,5,6]
}

def crop(image, x, y, w, h):
    box = (x, y, x+w, y+h)
    cropped_area = image.crop(box)
    return cropped_area

def get_average_color_val(image):
    image_data = list(image.getdata())
    return sum(image_data) / len(image_data)

def get_dice_image(val):
    if val >= 212.5:
        return dice_images[1]
    elif val >= 170:
        return dice_images[2]
    elif val >= 127.5:
        return dice_images[3]
    elif val >= 85:
        return dice_images[4]
    elif val >= 42.5:
        return dice_images[5]
    else:
        return dice_images[6]

def build_dice_image(image):
    print(image.size)
    image = ImageOps.grayscale(image)
    dice_image = Image.new(mode = "RGB", size = (image.size), color=(255, 255, 255))
    for y in range(0, image.size[1], dice_size):
        for x in range(0, image.size[0], dice_size):
            image_chunk = crop(image, x, y, dice_size, dice_size)
            color_val = get_average_color_val(image_chunk)
            print(color_val)
            dice = get_dice_image(color_val)
            dice_image.paste(dice, (x, y))
    return dice_image


if __name__ == "__main__":
    url = 'https://www.teahub.io/photos/full/60-607490_kanye-west-portrait-uhd-4k-wallpaper-kanye-west.jpg'
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    dice_image = build_dice_image(image)
    dice_image.save('test-out.jpg')
