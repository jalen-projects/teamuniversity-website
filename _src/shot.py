"""
SCREENSHOT THE BUILT SITE
=========================
Four passes were spent guessing what "the colours are too deep" referred to,
because the page was never looked at. This looks at it.

    python _src/shot.py                     # desktop + phone of the home page
    python _src/shot.py programmes.html     # any page

Note the viewport is set through CDP rather than --window-size. Headless
Chrome silently clamps --window-size to about 512px, so every "it fits on a
phone" check made that way is really a check on a small tablet. CDP is not
clamped; the script asserts the width it actually got.
"""

import os
import subprocess
import sys
import time

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, "_src", "shots")
PORT = 8123


def serve():
    """A local server for the duration, so file:// quirks never confuse this."""
    process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
        cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    return process


def shoot(page="index.html", width=1440, height=2600, tag="desktop"):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--force-device-scale-factor=1")
    driver = webdriver.Chrome(options=options)
    try:
        # Navigate FIRST. The viewport of about:blank has no <meta viewport>,
        # so a mobile override measured there reports 980 and the assert fires
        # on a page that was never the one being tested.
        driver.get(f"http://127.0.0.1:{PORT}/{page}")
        driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": height, "deviceScaleFactor": 1,
            "mobile": width < 700})
        time.sleep(.4)
        got = driver.execute_script("return window.innerWidth")
        assert abs(got - width) < 40, f"viewport is {got}, asked for {width}"
        # Let the fonts, the reveal-on-scroll and the first video frame settle.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1.4)

        os.makedirs(OUT, exist_ok=True)
        name = os.path.join(OUT, f"{page.replace('.html', '')}-{tag}.png")
        driver.save_screenshot(name)
        print(f"  {name}  ({got}px wide)")
        return name
    finally:
        driver.quit()


def main():
    page = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    server = serve()
    try:
        shoot(page, 1440, 3000, "desktop")
        shoot(page, 390, 2400, "phone")
    finally:
        server.terminate()


if __name__ == "__main__":
    main()
