import asyncio
from pyppeteer import launch

import matplotlib.pyplot as plt
import numpy as np
from imageio import imread

def plot_hist(image_path):
    image = imread(image_path)
    image = image.reshape(image.shape[0]*image.shape[1], image.shape[2])
    colors, counts = np.unique(image, axis=0, return_counts=True)

    thresh = 20
    new_colors, new_counts = [], []
    for i in range(len(colors)):
        if counts[i]>thresh:
            new_colors.append(colors[i])
            new_counts.append(counts[i])
            
    for a,b in zip(new_colors, new_counts): print(a,b) 
    


async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()

    await page.goto('https://stackoverflow.com/questions/51000899/better-way-to-take-screenshot-of-a-url-in-python')
    await page.screenshot({'path': 'screen.png', 'fullPage': True})
    await browser.close()

    plot_hist('screen.png')

asyncio.get_event_loop().run_until_complete(main())