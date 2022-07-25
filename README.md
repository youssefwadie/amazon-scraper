# Amazon Scraper

ِWeb scraper for [Amazon](https://www.amazon.com) products with Scrapy

<p>
    Scrape <a href="https://www.amazon.com">amazon</a> products details, output them in json format
    <br>
    <strong>amazon may block your IP, or returns 503 service unavailable error. So, consider using a proxy for better results</strong>
</p>

# Installation

1. Install scrapy with [pip](#pip_install), [conda](#conda_install) or [micromamba](#mamba_install)
2. `git clone https://github.com/youssefwadie/amazon-scraper.git`
3. `cd amazon-scraper`
4. Edit the [query list](/amazon_scraper/spiders/amazon.py#L6)
5. `scrapy crawl amazon -o outfile.json`

```bash
scrapy crawl amazon -o outfile.json
```

pip installation <a name="pip_install"></a>
MacOS/Linux

```bash
python3 -m pip install --user virtualenv
python3 -m venv test
source test/bin/activate
pip install scrapy
```

Windows

```bash
py -m pip install --user virtualenv
py -m venv test
.\test\Scripts\activate
pip install scrapy
```

---
conda installation <a name="conda_install"></a>

```bash
conda create -n test -c conda-forge python scrapy
conda activate test
```

---
micromamba installation<a name="mamba_install"></a>

```bash
micromamba create -n test -c conda-forge python scrapy
micromamba activate test
```

---
Sample output

```json
 {
  "asin": "B08NWCT6SK",
  "title": "Moto G Stylus | 2021 | 2-Day Battery | Unlocked | Made for US by Motorola | 4/128GB | 48MP Camera | White",
  "main_image": "https://m.media-amazon.com/images/I/414X4yF8zcL._AC_.jpg",
  "price": "199",
  "sizes": [
    "128GB",
    "256GB"
  ],
  "colors": [
    "Black",
    "Metallic Rose",
    "Twilight Blue",
    "White",
    "Emerald",
    "Seafoam Green"
  ],
  "features": [
    "Unlocked for the freedom to choose your carrier. Compatible with AT&T, Sprint, T-Mobile, and Verizon networks. Sim card not included. Customers may need to contact Sprint for activation on Sprints network.",
    "Built-in stylus. Retouch photos, jot notes, sketch artwork, and control a growing number of games and all apps with pinpoint precision.",
    "48 MP quad camera system. Showcase your creativity from every perspective, from ultra-wide angle shots to detailed close-ups and everything in between.",
    "Faster, smoother performance. Feel the instant response with every touch and tap of the stylus thanks to the Qualcomm Snapdragon 678 processor.",
    "128 GB of storage. Carry more photos, songs, games, and movies and never give storage a second thought.",
    "6.8\" Max Vision FHD, display. Watch your photos, movies, and video chats come to life on the biggest moto g display ever.",
    "Up to 2 days battery life. Go longer on a single charge with a 4000 mAh battery.",
    "Operating System: Android 10",
    "Wi-Fi Hotspot Ready: Moto G Power (2021) offers Wi-fi hotspot connectivity in 2.4 GHz , 5 GHz for the best experience.",
    "In-box: Moto G Stylus (2021), 10W rapid Charger, USB Cable, Guides, SIM tool"
  ],
  "list_price": "$299.99",
  "images": [
    "https://m.media-amazon.com/images/I/41kNnMYElKL._AC_US40_.jpg",
    "https://m.media-amazon.com/images/I/61wo4NtXXWL.SS40_BG85,85,85_BR-120_PKdp-play-icon-overlay__.jpg",
    "https://m.media-amazon.com/images/I/41KLxfKjR2L._AC_US40_.jpg",
    "https://m.media-amazon.com/images/I/31M4u0EvKoL._AC_US40_.jpg",
    "https://m.media-amazon.com/images/I/414X4yF8zcL._AC_US40_.jpg",
    "https://m.media-amazon.com/images/I/31wy+smU1uL._AC_US40_.jpg",
    "https://m.media-amazon.com/images/I/41dWTCmUQGL._AC_US40_.jpg"
  ],
  "dimensions": {
    "length": 6.6,
    "width": 1.84,
    "height": 3.09
  },
  "weight": 13.8
}
```