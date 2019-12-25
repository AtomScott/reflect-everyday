from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError 
from bs4 import BeautifulSoup

from collections import Counter

import re, colorsys
import matplotlib.pyplot as plt

def get_hsv(hexrgb):
    hexrgb = hexrgb.lstrip("#")   # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in range(0,5,2))
    return colorsys.rgb_to_hsv(r, g, b)

def rgb_to_hex(rgb_color):
    rgb_color = re.search('\(.*\)', rgb_color).group(0).replace(' ', '').lstrip('(').rstrip(')')
    [r, g, b, *_] = [int(x) for x in rgb_color.split(',') if float(x)==float(x)//1]

    # check if in range 0~255
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255
 
    r = hex(r).lstrip('0x')
    g = hex(g).lstrip('0x')
    b = hex(b).lstrip('0x')

    # re-write '7' to '07'
    r = (2 - len(r)) * '0' + r
    g = (2 - len(g)) * '0' + g
    b = (2 - len(b)) * '0' + b
 
    hex_color = '#' + r + g + b
    assert len(hex_color) == 7
    return hex_color


def main():
    url = input("Enter URL:\n")
    try:
        html = urlopen(url)
    
    except HTTPError as e: 
        print(e)
    
    except URLError:
        print("Server down or incorrect domain")
    
    else:
        res = BeautifulSoup(html.read(),"html5lib")

        with open('./res.txt', 'w+') as f:
            p = r'#(?:[a-f\d]{3}){1,2}\b|rgb\((?:(?:\s*0*(?:25[0-5]|2[0-4]\d|1?\d?\d)\s*,){2}\s*0*(?:25[0-5]|2[0-4]\d|1?\d?\d)|\s*0*(?:100(?:\.0+)?|\d?\d(?:\.\d+)?)%(?:\s*,\s*0*(?:100(?:\.0+)?|\d?\d(?:\.\d+)?)%){2})\s*\)|hsl\(\s*0*(?:360|3[0-5]\d|[12]?\d?\d)\s*(?:,\s*0*(?:100(?:\.0+)?|\d?\d(?:\.\d+)?)%\s*){2}\)|(?:rgba\((?:(?:\s*0*(?:25[0-5]|2[0-4]\d|1?\d?\d)\s*,){3}|(?:\s*0*(?:100(?:\.0+)?|\d?\d(?:\.\d+)?)%\s*,){3})|hsla\(\s*0*(?:360|3[0-5]\d|[12]?\d?\d)\s*(?:,\s*0*(?:100(?:\.0+)?|\d?\d(?:\.\d+)?)%\s*){2},)\s*0*(?:1|0(?:\.\d+)?)\s*\)'

            colors = re.findall(p, res.decode())
            
            # convert rgba to hex
            for i, c in enumerate(colors):
                if c.startswith('rgb'):
                    colors[i] = rgb_to_hex(c)
                elif c == '#fff':
                    colors[i] = '#ffffff'
                elif c == '#000':
                    colors[i] = '#000000'

            colors.sort(key=get_hsv)
            c_dct = Counter(colors)
            for key, values in c_dct.items():
                f.write(f'{key}, {values}\n')

    xs = [1] * len(colors)
    y_pos = range(len(colors))
    plt.bar(y_pos, xs, color=colors, align='center', alpha=0.5)
    plt.xticks(y_pos, colors)
    plt.ylabel('Usage')
    plt.title('Programming language usage')
    plt.savefig('fig.png')

if __name__ == "__main__":
    main()