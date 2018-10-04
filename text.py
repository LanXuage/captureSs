from urllib import request
import ssl
import re
import pytesseract
from PIL import Image


def add_edge(pic, edge):
    pw, ph = pic.size
    ow = pw + 2 * edge
    oh = ph + 2 * edge
    img2 = Image.new("RGBA", (ow, oh), "white")
    img2.paste(image, (edge, edge, pw + edge, ph + edge), mask=pic.split()[3])
    return img2


if __name__ == '__main__':
    # the url
    url = "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    # setting the ssl
    context = ssl._create_unverified_context()
    # open the url
    with request.urlopen(url, context=context) as response:
        html = response.read()          # fetch the source of HTML
    # setting the decode
    html = html.decode("utf-8")
    pattern = re.compile(r'<img src="(\S+?\.PNG)"', re.I)
    imgList = pattern.findall(html)
    x = 0
    code = ""
    for img_url in imgList:
        x = x + 1
        filename = 'ss' + str(x) + '.png'
        with request.urlopen(img_url, context=context) as res, open(filename, 'wb') as fp:
            fp.write(res.read())
        image = Image.open(filename)
        image = add_edge(image, 4)
        image.save(filename)
        code = code + "\n" + pytesseract.image_to_string(image)
        image.close()
        print(code)
    print('end')
