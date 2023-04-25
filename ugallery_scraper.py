# script to take links from styles page ugallery
# const links = [];
# for(let el of document.querySelectorAll(".card-img-link")) {
# 	const alinks = el.querySelectorAll("a")[1];
# 	if(alinks) {
# 		links = [...links, alinks.getAttribute("href")];
# 	}
# }

import requests
from bs4 import BeautifulSoup

base_url = "https://www.ugallery.com"
categories = {
    "Abstract": "https://www.ugallery.com/abstract-artwork",
    "Classical": "https://www.ugallery.com/classical-artwork",
    "Contemporary": "https://www.ugallery.com/Contemporary-artwork",
    "Expressionism": "https://www.ugallery.com/expressionism-artwork",
    "Impressionism": "https://www.ugallery.com/impressionism-artwork",
    "Minimalism": "https://www.ugallery.com/minimalism-artwork",
    "Modern": "https://www.ugallery.com/modern-artwork",
    "Pop": "https://www.ugallery.com/pop-culture-artwork",
    "Primitive": "https://www.ugallery.com/primitive-artwork",
    "Realism": "https://www.ugallery.com/realism-artwork",
    "Surrealism": "https://www.ugallery.com/surrealism-artwork"
}

s = requests.Session()

links = ["/art/acrylic-painting-fading-fast",   "/art/oil-painting-indigo-landscape-2",   "/art/oil-painting-indigo-stripes-3",   "/art/acrylic-painting-fragmentation-ii-rings",   "/art/acrylic-painting-fragmentation-ii-pieces",   "/art/acrylic-painting-joy-of-life",   "/art/ink-artwork-high-spirits",   "/art/ink-artwork-live-free",   "/art/ink-artwork-happy-abundance",   "/art/acrylic-painting-nothing-else-matters",   "/art/acrylic-painting-meet-the-light",   "/art/acrylic-painting-fragmentation-ii-spaces",   "/art/mixed-media-artwork-lily-pond-75401",   "/art/mixed-media-artwork-after-midnight",   "/art/oil-painting-indigo-beige-stripes",   "/art/mixed-media-artwork-where-the-sea-meets-the-sky",   "/art/mixed-media-artwork-opposites",   "/art/oil-painting-drifting-75081",   "/art/acrylic-painting-afloat",   "/art/oil-painting-crown-no-12",   "/art/oil-painting-crown-no-15",   "/art/oil-painting-crown-no-14",   "/art/mixed-media-artwork-always",   "/art/watercolor-painting-winter-landscape-75743",   "/art/watercolor-painting-steppe",   "/art/watercolor-painting-mountain-reverie-series-8",   "/art/watercolor-painting-mountain-reverie-series-5",   "/art/oil-painting-holy-realignment",   "/art/acrylic-painting-humble",   "/art/oil-painting-the-clearing-75862",   "/art/oil-painting-signs-of-spring",   "/art/oil-painting-break-of-day-75468",   "/art/ink-artwork-dreams-do-come-true",   "/art/acrylic-painting-the-love-story",   "/art/acrylic-painting-broken-heart",   "/art/acrylic-painting-breathing-silence",   "/art/acrylic-painting-struggle-with-life",   "/art/acrylic-painting-symbiosis",   "/art/oil-painting-triple-stripes-e",   "/art/oil-painting-triple-stripes-d",   "/art/mixed-media-artwork-apparition-75502",   "/art/ink-artwork-awakening",   "/art/acrylic-painting-awakening-75537",   "/art/acrylic-painting-the-never-ending-story",   "/art/mixed-media-artwork-bliss-75503",   "/art/acrylic-painting-aquatica",   "/art/oil-painting-crown-no-13",   "/art/mixed-media-artwork-primal",   "/art/acrylic-painting-batik",   "/art/acrylic-painting-white-balance",   "/art/acrylic-painting-finding-balance-v5",   "/art/mixed-media-artwork-subtle-complexities",   "/art/acrylic-painting-beyond-time",   "/art/acrylic-painting-deep-love-75540",   "/art/ink-artwork-passageway",   "/art/ink-artwork-euphoria",   "/art/ink-artwork-rebirth",   "/art/ink-artwork-thankful",   "/art/ink-artwork-the-true-path",   "/art/acrylic-painting-diving-in-teal-cloud"]

for link in links:
    r = s.get(base_url+link)
    soup = BeautifulSoup(r.text, "lxml")
    title = soup.select("h2[itemprop='name']")[0].get_text()
    description = soup.select("[class='artwork-description']")[0].get_text()
    category = "Abstract"
    print(description)
