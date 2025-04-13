import asyncio
import nodriver as uc

async def main():
    browser = await uc.start(headless=True)
    page = await browser.get('https://github.com/ultrafunkamsterdam/nodriver')

    await page.save_screenshot()
    await page.get_content()
    await page.scroll_down(150)
    elems = await page.select_all('*[src]')
    for elem in elems:
        await elem.flash()

    for p in (page):
       await p.bring_to_front()
       await p.scroll_down(200)
       await p   # wait for events to be processed
       await p.reload()


if __name__ == '__main__':

    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())