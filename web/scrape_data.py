# script to take links from styles page ugallery
# const links = [];
# for(let el of document.querySelectorAll(".card-img-link")) {
# 	const alinks = el.querySelectorAll("a")[1];
# 	if(alinks) {
# 		links = [...links, alinks.getAttribute("href")];
# 	}
# }

import os
import wget
import requests
from bs4 import BeautifulSoup
import random
import pytz
from datetime import datetime, timedelta
from django.utils.text import slugify
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from pages.models import Item, Category

base_url = "https://www.ugallery.com"
categories = {
    "Abstract": "1",
    "Classical": "2",
    "Contemporary": "3",
    "Expressionism": "4",
    "Impressionism": "5",
    "Minimalism": "6",
    "Modern": "7",
    "Pop": "8",
    "Primitive": "9",
    "Realism": "10",
    "Surrealism": "11",
}
links = {
    "Abstract": ["/art/acrylic-painting-fading-fast",   "/art/oil-painting-indigo-landscape-2",   "/art/oil-painting-indigo-stripes-3",   "/art/acrylic-painting-fragmentation-ii-rings",   "/art/acrylic-painting-fragmentation-ii-pieces",   "/art/acrylic-painting-joy-of-life",   "/art/ink-artwork-high-spirits",   "/art/ink-artwork-live-free",   "/art/ink-artwork-happy-abundance",   "/art/acrylic-painting-nothing-else-matters",   "/art/acrylic-painting-meet-the-light",   "/art/acrylic-painting-fragmentation-ii-spaces",   "/art/mixed-media-artwork-lily-pond-75401",   "/art/mixed-media-artwork-after-midnight",   "/art/oil-painting-indigo-beige-stripes",   "/art/mixed-media-artwork-where-the-sea-meets-the-sky",   "/art/mixed-media-artwork-opposites",   "/art/oil-painting-drifting-75081",   "/art/acrylic-painting-afloat",   "/art/oil-painting-crown-no-12",   "/art/oil-painting-crown-no-15",   "/art/oil-painting-crown-no-14",   "/art/mixed-media-artwork-always",   "/art/watercolor-painting-winter-landscape-75743",   "/art/watercolor-painting-steppe",   "/art/watercolor-painting-mountain-reverie-series-8",   "/art/watercolor-painting-mountain-reverie-series-5",   "/art/oil-painting-holy-realignment",   "/art/acrylic-painting-humble",   "/art/oil-painting-the-clearing-75862",   "/art/oil-painting-signs-of-spring",   "/art/oil-painting-break-of-day-75468",   "/art/ink-artwork-dreams-do-come-true",   "/art/acrylic-painting-the-love-story",   "/art/acrylic-painting-broken-heart",   "/art/acrylic-painting-breathing-silence",   "/art/acrylic-painting-struggle-with-life",   "/art/acrylic-painting-symbiosis",   "/art/oil-painting-triple-stripes-e",   "/art/oil-painting-triple-stripes-d",   "/art/mixed-media-artwork-apparition-75502",   "/art/ink-artwork-awakening",   "/art/acrylic-painting-awakening-75537",   "/art/acrylic-painting-the-never-ending-story",   "/art/mixed-media-artwork-bliss-75503",   "/art/acrylic-painting-aquatica",   "/art/oil-painting-crown-no-13",   "/art/mixed-media-artwork-primal",   "/art/acrylic-painting-batik",   "/art/acrylic-painting-white-balance",   "/art/acrylic-painting-finding-balance-v5",   "/art/mixed-media-artwork-subtle-complexities",   "/art/acrylic-painting-beyond-time",   "/art/acrylic-painting-deep-love-75540",   "/art/ink-artwork-passageway",   "/art/ink-artwork-euphoria",   "/art/ink-artwork-rebirth",   "/art/ink-artwork-thankful",   "/art/ink-artwork-the-true-path",   "/art/acrylic-painting-diving-in-teal-cloud"],
    "Classical": ["/art/oil-painting-extra-hot-snack",   "/art/oil-painting-theatre-in-the-sky",   "/art/oil-painting-poppy-path-36926",   "/art/oil-painting-a-little-south-of-marathon",   "/art/oil-painting-castle-vinne",   "/art/oil-painting-the-great-pumpkin",   "/art/oil-painting-montefioralle-italy",   "/art/oil-painting-morning-mist",   "/art/oil-painting-late-afternoon-at-the-river",   "/art/oil-painting-two-peas-in-a-pod",   "/art/oil-painting-crimson-s-edge-iii-waves-at-daybreak",   "/art/oil-painting-summer-bouquet-74995",   "/art/oil-painting-broken-75311",   "/art/oil-painting-an-apple-a-day",   "/art/oil-painting-bringing-back-memories",   "/art/oil-painting-clemence",   "/art/oil-painting-metamorphoses",   "/art/oil-painting-the-memory-of-autumn",   "/art/oil-painting-view-at-civita-castellana-no-2",   "/art/oil-painting-calla-lily-73073",   "/art/acrylic-painting-easter-again",   "/art/oil-painting-woman-at-mirror",   "/art/oil-painting-12-variations",   "/art/oil-painting-forest-encounter",   "/art/oil-painting-brilliant-wave",   "/art/oil-painting-weathertop",   "/art/oil-painting-the-genie",   "/art/oil-painting-gymnastics",   "/art/oil-painting-cupcake-with-orange-slice",   "/art/oil-painting-pink-cupcake-with-cranberries",   "/art/oil-painting-sunlight",   "/art/oil-painting-looking-back-57372",   "/art/oil-painting-the-afterlight",   "/art/oil-painting-in-solitude",   "/art/oil-painting-break-of-day",   "/art/oil-painting-twilight-interlude",   "/art/oil-painting-castles-in-the-air",   "/art/oil-painting-transition-crossroads",   "/art/oil-painting-summer-reminiscence",   "/art/oil-painting-orchard-in-spring",   "/art/oil-painting-morning-haze",   "/art/oil-painting-windmills",   "/art/oil-painting-japanese-elegance",   "/art/oil-painting-windmills-2",   "/art/oil-painting-concert-time",   "/art/oil-painting-bread-and-butter",   "/art/oil-painting-got-milk-ii",   "/art/oil-painting-dedication",   "/art/oil-painting-ravello",   "/art/oil-painting-purple-kimono",   "/art/oil-painting-red-kimono",   "/art/oil-painting-two-dancers",   "/art/oil-painting-woman-in-moroccan-costume",   "/art/oil-painting-clemence-in-the-garden",   "/art/oil-painting-woman-with-moths",   "/art/oil-painting-first-thaw",   "/art/oil-painting-ninon-gold-sash",   "/art/oil-painting-pause-69617",   "/art/oil-painting-woman-in-satin",   "/art/oil-painting-woman-with-cardinal"],
    "Contemporary": ["/art/oil-painting-the-blue-bird",   "/art/oil-painting-the-earth-3",   "/art/oil-painting-the-earth-2",   "/art/acrylic-painting-portrait-michael",   "/art/acrylic-painting-portrait-linsay",   "/art/acrylic-painting-ghost-in-the-city-city-tour",   "/art/mixed-media-artwork-every-day",   "/art/acrylic-painting-secrets-to-tell",   "/art/acrylic-painting-house-sparrows-about",   "/art/oil-painting-summer-in-pecos",   "/art/acrylic-painting-showing-up",   "/art/ink-artwork-friends-for-a-sobering-time-01-bunny",   "/art/ink-artwork-friends-for-a-sobering-time-04-cat",   "/art/ink-artwork-friends-for-a-sobering-time-05-bunny",   "/art/acrylic-painting-coastal-impressions-the-falls",   "/art/mixed-media-artwork-kintsugi-horse-the-beautiful-changes",   "/art/oil-painting-hug-me",   "/art/oil-painting-dogmocracy",   "/art/acrylic-painting-lying-2",   "/art/acrylic-painting-attachment",   "/art/mixed-media-artwork-with-orange-flowers",   "/art/oil-painting-mod-calculation",   "/art/oil-painting-finding-glamour",   "/art/oil-painting-bicycling-in-blue",   "/art/oil-painting-on-the-banks-of-the-indian-river",   "/art/acrylic-painting-the-classic",   "/art/mixed-media-artwork-neutral",   "/art/oil-painting-catcher",   "/art/mixed-media-artwork-here-today-gone-tomorrow",   "/art/mixed-media-artwork-searching-for-completion-in-my-garden",   "/art/mixed-media-artwork-i-am-woman",   "/art/oil-painting-the-earth",   "/art/acrylic-painting-joy-of-celebration-1",   "/art/mixed-media-artwork-on-top-of-the-world",   "/art/mixed-media-artwork-to-honor",   "/art/mixed-media-artwork-with-golden-clouds-raining-down",   "/art/mixed-media-artwork-expansion-set-of-2",   "/art/mixed-media-artwork-kintsugi-horses-alchemy",   "/art/acrylic-painting-asking-you",   "/art/oil-painting-fade-into-you-75403",   "/art/mixed-media-artwork-orkney-coast",   "/art/acrylic-painting-ghost-in-the-city-station",   "/art/acrylic-painting-ghost-in-the-city-cosplay",   "/art/acrylic-painting-pressure-point",   "/art/oil-painting-dogmocracy-ll",   "/art/mixed-media-artwork-he-finally-earned-his-tiara",   "/art/acrylic-painting-ghost-in-the-city-restaurant",   "/art/acrylic-painting-ghost-in-the-city-park",   "/art/acrylic-painting-ghost-in-the-city-crosswalk",   "/art/acrylic-painting-ghost-in-the-city-track-running",   "/art/oil-painting-inside-out-red",   "/art/oil-painting-inside-out-purple",   "/art/oil-painting-inside-out-grey",   "/art/oil-painting-all-that-is-golden",   "/art/oil-painting-pawsitive-energy",   "/art/acrylic-painting-ghost-in-the-city-police-2",   "/art/acrylic-painting-ghost-in-the-city-lunch-hour",   "/art/acrylic-painting-ghost-in-the-city-subway",   "/art/acrylic-painting-ghost-in-the-city-whole-foods",   "/art/acrylic-painting-ghost-in-the-city-lotte-world"],
    "Expressionism": ["/art/acrylic-painting-road-into-color",   "/art/acrylic-painting-a-day-on-monhegan-island",   "/art/acrylic-painting-summertime-rural-farm",   "/art/acrylic-painting-ways-of-the-city",   "/art/acrylic-painting-sunflowers-75831",   "/art/oil-painting-among-the-hidden",   "/art/acrylic-painting-study-in-blue-and-gold",   "/art/watercolor-painting-sunset-75846",   "/art/acrylic-painting-lake-house-with-two-boats",   "/art/mixed-media-artwork-max-and-sylvie",   "/art/mixed-media-artwork-duet-75699",   "/art/mixed-media-artwork-spin-75677",   "/art/acrylic-painting-ridgetop-flowers",   "/art/acrylic-painting-blue-eyes-75136",   "/art/oil-painting-autumn-s-light",   "/art/oil-painting-canyon-rock",   "/art/mixed-media-artwork-respite",   "/art/mixed-media-artwork-abstract-still-life",   "/art/oil-painting-quiet-embers",   "/art/watercolor-painting-path",   "/art/mixed-media-artwork-still-life-with-green-glass-jar",   "/art/watercolor-painting-the-soil",   "/art/acrylic-painting-blue-horse-with-crosses",   "/art/oil-painting-dreams-75467",   "/art/oil-painting-green-reflection",   "/art/acrylic-painting-reflection-girl-portrait",   "/art/acrylic-painting-soul-searching",   "/art/acrylic-painting-lady-america",   "/art/mixed-media-artwork-beach-dancers",   "/art/encaustic-artwork-stagecoach-road",   "/art/acrylic-painting-deep-love",   "/art/acrylic-painting-family-portrait-74611",   "/art/acrylic-painting-autumn-leaves-74354",   "/art/oil-painting-august-in-full-dress",   "/art/oil-painting-tryon-12",   "/art/oil-painting-the-wind",   "/art/oil-painting-morning-light-65031",   "/art/acrylic-painting-dawn-over-the-foliage",   "/art/acrylic-painting-beach-chair",   "/art/acrylic-painting-summer-coming-in",   "/art/acrylic-painting-the-old-curiosity-shop",   "/art/acrylic-painting-glow-74189",   "/art/acrylic-painting-on-a-clear-day-74625",   "/art/acrylic-painting-natural-bridge-74431",   "/art/acrylic-painting-path-through-the-forest",   "/art/acrylic-painting-saguaro-silhouettes",   "/art/mixed-media-artwork-my-best-friend",   "/art/oil-painting-glory-of-autumn",   "/art/acrylic-painting-times-square-ii",   "/art/oil-painting-turquoise-river",   "/art/acrylic-painting-another-day-ii",   "/art/encaustic-artwork-a-warm-interior",   "/art/acrylic-painting-intimate-impasse",   "/art/acrylic-painting-five-o-clock-somewhere",   "/art/acrylic-painting-woodlands",   "/art/acrylic-painting-view-of-the-bay",   "/art/acrylic-painting-farm-in-january",   "/art/acrylic-painting-midday-sun",   "/art/acrylic-painting-the-art-sellers",   "/art/acrylic-painting-moonbeams"],
    "Impressionism": ["/art/mixed-media-artwork-october-31",   "/art/mixed-media-artwork-modern-love",   "/art/acrylic-painting-prime-beachfront-property",   "/art/oil-painting-the-palm",   "/art/oil-painting-palms-75737",   "/art/oil-painting-cygnets-in-blue-and-white",   "/art/oil-painting-the-palm-trees",   "/art/oil-painting-all-you-need-is-a-puddle",   "/art/oil-painting-the-sleepover",   "/art/oil-painting-cyan-dusk",   "/art/oil-painting-blue-world",   "/art/oil-painting-coastal-elder-at-cayucos",   "/art/oil-painting-red-barn-off-grand-avenue",   "/art/mixed-media-artwork-still-dreaming",   "/art/oil-painting-after-the-rain-piazza-navona",   "/art/mixed-media-artwork-n-train-ninja",   "/art/oil-painting-rows-of-lavender-peach-light-above-the-hills",   "/art/acrylic-painting-costal-impressions-the-lone-cypress",   "/art/acrylic-painting-the-blue-swallow",   "/art/oil-painting-winging-it",   "/art/watercolor-painting-mt-diablo-spring-view",   "/art/oil-painting-diversity-is-a-beautiful-thing",   "/art/oil-painting-turning-of-the-tide",   "/art/oil-painting-misty-stream-in-yellowstone-park",   "/art/watercolor-painting-misty-morning-on-the-farm",   "/art/watercolor-painting-shoreline-trail",   "/art/oil-painting-california-calm",   "/art/oil-painting-emotion",   "/art/oil-painting-lofty-perch",   "/art/acrylic-painting-morning-field",   "/art/oil-painting-battle-of-the-grapes",   "/art/oil-painting-cookies-milk",   "/art/watercolor-painting-katowice-poland",   "/art/oil-painting-creekside",   "/art/mixed-media-artwork-small-butte-with-creosote",   "/art/oil-painting-canyon-scenery",   "/art/oil-painting-autumn-forest-75793",   "/art/oil-painting-big-sur-falls",   "/art/oil-painting-empty-nester",   "/art/oil-painting-a-square-in-aix-en-provence",   "/art/oil-painting-the-falls-at-boonton",   "/art/mixed-media-artwork-cold-one",   "/art/mixed-media-artwork-we-met-online",   "/art/oil-painting-the-swim",   "/art/oil-painting-bistro-du-midi",   "/art/oil-painting-stalling-and-waiting",   "/art/oil-painting-entering-the-swift-current",   "/art/acrylic-painting-house-with-red-door",   "/art/oil-painting-sunset-on-the-river-trail",   "/art/oil-painting-between-the-shadows-75281",   "/art/acrylic-painting-red-barn-reflections",   "/art/oil-painting-tangential-dreams",   "/art/mixed-media-artwork-a-good-book",   "/art/mixed-media-artwork-hockey-fan",   "/art/oil-painting-sunset-tulips",   "/art/oil-painting-path-in-the-garden",   "/art/acrylic-painting-forest-abstractions-chorus-line",   "/art/oil-painting-under-the-table-and-dreaming",   "/art/oil-painting-ascending-clouds",   "/art/oil-painting-end-of-an-era"],
    "Minimalism": ["/art/mixed-media-artwork-opposites",   "/art/sculpture-u-14-wavy-red",   "/art/sculpture-u-13-the-choice",   "/art/sculpture-u-climbers-on-red-iii",   "/art/acrylic-painting-pink-seasoning",   "/art/acrylic-painting-two-ladies",   "/art/acrylic-painting-come-together",   "/art/oil-painting-surrender-62726",   "/art/oil-painting-transference",   "/art/oil-painting-voyage",   "/art/oil-painting-restraint",   "/art/mixed-media-artwork-the-house-of-gratitude",   "/art/mixed-media-artwork-weighs-and-means",   "/art/mixed-media-artwork-in-the-stillness-66948",   "/art/acrylic-painting-essence",   "/art/gouache-painting-banana-blue-glaucus",   "/art/mixed-media-artwork-resolution",   "/art/oil-painting-in-the-stillness",   "/art/oil-painting-phenomenon-remnant",   "/art/oil-painting-settling-in",   "/art/acrylic-painting-baseball-horizon",   "/art/mixed-media-artwork-meerkat-coral-reef",   "/art/gouache-painting-fox-coral-reef",   "/art/oil-painting-gratification",   "/art/oil-painting-resistance",   "/art/oil-painting-breakthrough",   "/art/oil-painting-insight",   "/art/oil-painting-knowledge",   "/art/oil-painting-loneliness-aloneness",   "/art/oil-painting-letting-go-ii",   "/art/oil-painting-letting-go-i",   "/art/oil-painting-metamorphosis-i",   "/art/oil-painting-metamorphosis-ii",   "/art/oil-painting-interruption",   "/art/oil-painting-tune",   "/art/oil-painting-adaptation-ii",   "/art/oil-painting-adaptation-i",   "/art/oil-painting-whim",   "/art/oil-painting-enlightenment-i",   "/art/oil-painting-detachment",   "/art/oil-painting-attachment",   "/art/oil-painting-joy-63872",   "/art/oil-painting-peace-63870",   "/art/oil-painting-love-63871",   "/art/oil-painting-gravitas-ii",   "/art/oil-painting-gravitas-i",   "/art/oil-painting-chasm",   "/art/oil-painting-discourse",   "/art/oil-painting-epiphany-69637",   "/art/oil-painting-anima",   "/art/oil-painting-vanity",   "/art/oil-painting-ephemera",   "/art/oil-painting-clarity-61533",   "/art/oil-painting-duet",   "/art/oil-painting-boundary",   "/art/oil-painting-monologue",   "/art/oil-painting-dialogue",   "/art/oil-painting-forgiveness",   "/art/oil-painting-regret",   "/art/oil-painting-harmony-70421"],
    "Modern": ["/art/sculpture-u-14-wavy-red",   "/art/sculpture-u-13-the-choice",   "/art/oil-painting-out-of-the-wall",   "/art/acrylic-painting-window44",   "/art/acrylic-painting-window35",   "/art/acrylic-painting-gathered",   "/art/acrylic-painting-memory-s-echo",   "/art/acrylic-painting-peaceful-day",   "/art/acrylic-painting-coastal-impressions-the-cove",   "/art/oil-painting-mountain-colors",   "/art/mixed-media-artwork-small-beings-on-window-with-gold-curtain",   "/art/acrylic-painting-two-step-dance",   "/art/acrylic-painting-evening-in-a-bar",   "/art/acrylic-painting-sound-of-silence",   "/art/acrylic-painting-groove-35",   "/art/acrylic-painting-groove-30",   "/art/mixed-media-artwork-the-hidden-gem",   "/art/acrylic-painting-flirting-with-possibilities",   "/art/acrylic-painting-farmhouse-under-a-sunset-sky",   "/art/oil-painting-flower-and-bird-ii",   "/art/oil-painting-flower-and-bird-i",   "/art/acrylic-painting-in-the-quiet-of-the-mist",   "/art/acrylic-painting-diving-in-amber-rush",   "/art/acrylic-painting-fragmentation-breaking-point",   "/art/mixed-media-artwork-grid-light",   "/art/acrylic-painting-between-us",   "/art/mixed-media-artwork-all-the-people-at-this-party",   "/art/acrylic-painting-piazza-cafe",   "/art/acrylic-painting-empty-shell-to-past",   "/art/acrylic-painting-city-of-prague",   "/art/acrylic-painting-pink-seasoning",   "/art/acrylic-painting-two-ladies",   "/art/acrylic-painting-three-gourds",   "/art/mixed-media-artwork-tribute-to-mondrian-red-diamond-u-14",   "/art/mixed-media-artwork-tribute-to-mondrian-three-colors-u-15",   "/art/mixed-media-artwork-red-white-climbers",   "/art/mixed-media-artwork-small-beings-on-window-with-silver-curtain",   "/art/mixed-media-artwork-tribute-to-mondrian-four-colors-u-16",   "/art/mixed-media-artwork-red-bronze-small-beings",   "/art/acrylic-painting-fan-dancer",   "/art/acrylic-painting-enjoying-a-drink",   "/art/mixed-media-artwork-yellow-red-climbers",   "/art/mixed-media-artwork-white-blue-climbers",   "/art/sculpture-climber-on-green-hope-a",   "/art/sculpture-climber-on-green-hope-b",   "/art/mixed-media-artwork-small-beings-sitting-on-gray",   "/art/mixed-media-artwork-women-s-window",   "/art/mixed-media-artwork-the-circle-of-life-b",   "/art/mixed-media-artwork-white-black-and-red-with-climbers",   "/art/mixed-media-artwork-woman-in-red-circle",   "/art/mixed-media-artwork-woman-in-golden-circle",   "/art/mixed-media-artwork-yellow-and-red-square",   "/art/mixed-media-artwork-yellow-and-white-square",   "/art/acrylic-painting-woman-contemplating",   "/art/acrylic-painting-woman-with-attitude",   "/art/acrylic-painting-late-evening",   "/art/acrylic-painting-peach-n-peppers",   "/art/mixed-media-artwork-yellow-white-climbers",   "/art/sculpture-u-partners",   "/art/sculpture-u-love"],
    "Pop": ["/art/acrylic-painting-tea-and-flowers",   "/art/acrylic-painting-dazzle-me-twice",   "/art/mixed-media-artwork-a-masked-girl",   "/art/mixed-media-artwork-coffee-and-conundrums",   "/art/acrylic-painting-dazzle-me-once",   "/art/mixed-media-artwork-roger-that",   "/art/mixed-media-artwork-still-life-with-camper",   "/art/oil-painting-tic-tac-toe-75327",   "/art/oil-painting-canapes",   "/art/mixed-media-artwork-glory-kat",   "/art/mixed-media-artwork-culprits",   "/art/acrylic-painting-mouse-with-hot-chocolate",   "/art/oil-painting-fade-into-you",   "/art/oil-painting-flower-girl-68838",   "/art/oil-painting-sweet-disposition",   "/art/mixed-media-artwork-the-almost-perfect-day",   "/art/oil-painting-sushi-ii",   "/art/mixed-media-artwork-raining-color",   "/art/mixed-media-artwork-santa-fe-muse",   "/art/oil-painting-spring-into-summer",   "/art/oil-painting-sweet-favorites",   "/art/oil-painting-unity-makes-strength",   "/art/watercolor-painting-three-cars",   "/art/watercolor-painting-black-winged-stilts",   "/art/watercolor-painting-girls-with-coats",   "/art/oil-painting-four-ever-friends",   "/art/acrylic-painting-feliz-navidad",   "/art/oil-painting-yum-yum-funyuns",   "/art/oil-painting-silly-rabbit",   "/art/acrylic-painting-the-talk",   "/art/acrylic-painting-deep-in-my-bones",   "/art/acrylic-painting-back-to-you-68442",   "/art/acrylic-painting-bowl-of-grapes",   "/art/acrylic-painting-havana-dream",   "/art/acrylic-painting-well-stocked",   "/art/acrylic-painting-orchid-delight",   "/art/acrylic-painting-little-star",   "/art/acrylic-painting-mandarin-glide",   "/art/acrylic-painting-through-the-looking-glass",   "/art/mixed-media-artwork-to-creativity",   "/art/mixed-media-artwork-that-car-is-sooo",   "/art/mixed-media-artwork-tahoe",   "/art/mixed-media-artwork-penpals",   "/art/mixed-media-artwork-the-parrot",   "/art/oil-painting-blue-skirt-61547",   "/art/acrylic-painting-forest-abstractions-dance-of-nature",   "/art/oil-painting-my-sweet-valentine",   "/art/mixed-media-artwork-i-did-it-my-way",   "/art/mixed-media-artwork-all-cats-go-to-heaven",   "/art/acrylic-painting-midway-grill",   "/art/mixed-media-artwork-bot-descending-a-staircase",   "/art/mixed-media-artwork-alistair-gromit-spins-a-yarn",   "/art/oil-painting-antipasto",   "/art/oil-painting-surprise-party",   "/art/oil-painting-aye-aye-cap-n",   "/art/oil-painting-wonder",   "/art/oil-painting-sushi-plate",   "/art/mixed-media-artwork-big-chimpin",   "/art/mixed-media-artwork-a-boss-chimp",   "/art/oil-painting-princess-cake"],
    "Primitive": ["/art/acrylic-painting-never-again",   "/art/mixed-media-artwork-monica-and-dash",   "/art/mixed-media-artwork-girl-with-pearl-earring-and-her-dog",   "/art/acrylic-painting-shark-river-belmar-nj",   "/art/mixed-media-artwork-envy",   "/art/acrylic-painting-unlikely-friends",   "/art/mixed-media-artwork-great-plains-bison",   "/art/acrylic-painting-two-barn-owls",   "/art/acrylic-painting-house-finches-and-branches",   "/art/acrylic-painting-black-horse",   "/art/acrylic-painting-4-horses",   "/art/acrylic-painting-rider-and-crosses",   "/art/acrylic-painting-rebuff",   "/art/acrylic-painting-hill-country",   "/art/acrylic-painting-buildup",   "/art/acrylic-painting-obsession-5",   "/art/acrylic-painting-obsession-4",   "/art/acrylic-painting-obsession-3",   "/art/acrylic-painting-house-on-the-hill",   "/art/acrylic-painting-chipmunks",   "/art/mixed-media-artwork-the-older-couple",   "/art/acrylic-painting-many-medals",   "/art/acrylic-painting-cat-napping",   "/art/acrylic-painting-day-of-the-dead",   "/art/oil-painting-white-chrysanthemum",   "/art/mixed-media-artwork-thundering-bison",   "/art/acrylic-painting-three-dingo-night",   "/art/acrylic-painting-yellow-orange-and-blue",   "/art/acrylic-painting-acquiescence-73410",   "/art/acrylic-painting-morning-sun-bonsai",   "/art/mixed-media-artwork-the-getaway",   "/art/mixed-media-artwork-who-let-the-dogs-out",   "/art/acrylic-painting-water-is-life",   "/art/acrylic-painting-siblings-72862",   "/art/acrylic-painting-waters-edge-69552",   "/art/mixed-media-artwork-blue-74117",   "/art/acrylic-painting-smiling-faces-7",   "/art/acrylic-painting-smiling-faces-6",   "/art/acrylic-painting-smiling-faces-5",   "/art/acrylic-painting-blue-purple-and-orange",   "/art/acrylic-painting-orange-and-blue-9",   "/art/acrylic-painting-turquoise-runners",   "/art/acrylic-painting-se-orita",   "/art/acrylic-painting-moon-runner",   "/art/oil-painting-rainbow-horse",   "/art/acrylic-painting-painted-horse",   "/art/acrylic-painting-moon-runner-2",   "/art/mixed-media-artwork-steady-on",   "/art/acrylic-painting-howdy-ma-am",   "/art/acrylic-painting-fair-to-middlin",   "/art/acrylic-painting-obsession-6",   "/art/acrylic-painting-smiling-faces-4",   "/art/acrylic-painting-smiling-faces-3",   "/art/acrylic-painting-yellow-orange-and-blue-2",   "/art/acrylic-painting-red-black-horses",   "/art/acrylic-painting-pink-runners",   "/art/acrylic-painting-blue-horse",   "/art/acrylic-painting-male-gaze",   "/art/acrylic-painting-a-flutter-of-wings",   "/art/acrylic-painting-mimi-in-the-chair-smoking"],
    "Realism": ["/art/acrylic-painting-blue-teapot-and-roses",   "/art/acrylic-painting-three-houses",   "/art/mixed-media-artwork-east-village",   "/art/oil-painting-yellow-brick-road",   "/art/watercolor-painting-shadowed-hill-behind-the-barn",   "/art/acrylic-painting-can-egrets-forget",   "/art/watercolor-painting-point-lobos-succulents",   "/art/acrylic-painting-shaken",   "/art/gouache-painting-ranunculus-shindig",   "/art/gouache-painting-blushing-tones",   "/art/oil-painting-sunday-supper",   "/art/oil-painting-sunnyside-up",   "/art/oil-painting-staff-of-life",   "/art/watercolor-painting-blooming-succulents",   "/art/acrylic-painting-postcard-from-yellowstone",   "/art/acrylic-painting-of-rocks-and-colors-sulphur-shine",   "/art/oil-painting-tide-pools",   "/art/oil-painting-in-the-rain-75025",   "/art/oil-painting-the-escaping",   "/art/oil-painting-blooming-75112",   "/art/acrylic-painting-upgrade",   "/art/oil-painting-love-is-in-the-air",   "/art/acrylic-painting-speeding-crows",   "/art/acrylic-painting-raven-couple",   "/art/watercolor-painting-oasis",   "/art/oil-painting-shall-we-dance",   "/art/mixed-media-artwork-the-waffler",   "/art/oil-painting-atlantic-clam-shell",   "/art/acrylic-painting-of-rocks-and-colors-bg",   "/art/acrylic-painting-of-rocks-and-colors-s",   "/art/oil-painting-autumn-trees",   "/art/oil-painting-castle-vinne",   "/art/oil-painting-literary-delights",   "/art/oil-painting-carne-tagliata",   "/art/oil-painting-silent-hill",   "/art/oil-painting-a-glimpse-of-hope",   "/art/oil-painting-promised-land-water-lilies",   "/art/oil-painting-seabreeze-journey",   "/art/oil-painting-blt",   "/art/oil-painting-cheeseburger-fries",   "/art/oil-painting-saturday-morning-breakfast-of-champions",   "/art/oil-painting-vidalia-season",   "/art/oil-painting-margherita-pizza",   "/art/oil-painting-salsa",   "/art/watercolor-painting-rainbow-succulents",   "/art/watercolor-painting-succulent-stars",   "/art/oil-painting-rainbow-harvest",   "/art/oil-painting-pairs-well-with-wine",   "/art/oil-painting-sea-foam",   "/art/oil-painting-big-blue-72873",   "/art/oil-painting-check",   "/art/oil-painting-whimbrel-and-plover",   "/art/oil-painting-jetties",   "/art/acrylic-painting-blue-stones-in-water",   "/art/acrylic-painting-beach-patrol",   "/art/acrylic-painting-hidden-valley-ranch",   "/art/oil-painting-dreams-73405",   "/art/acrylic-painting-sunflower-medley-for-blues",   "/art/acrylic-painting-out-running-the-waves",   "/art/oil-painting-the-great-pumpkin"],
    "Surrealism": ["/art/mixed-media-artwork-the-souvenir",   "/art/mixed-media-artwork-coincidence",   "/art/mixed-media-artwork-sunday-in-the-burb",   "/art/oil-painting-roots",   "/art/oil-painting-relic",   "/art/mixed-media-artwork-black-cherry-n-vanilla",   "/art/oil-painting-these-boots",   "/art/oil-painting-venus-75199",   "/art/oil-painting-nebula",   "/art/oil-painting-time-ii",   "/art/oil-painting-time-i",   "/art/mixed-media-artwork-other-worlds",   "/art/mixed-media-artwork-the-waiting",   "/art/acrylic-painting-pressure-point",   "/art/mixed-media-artwork-study-for-the-hunter",   "/art/encaustic-artwork-glory-bee",   "/art/encaustic-artwork-her-friend-harvey",   "/art/encaustic-artwork-mystery-of-the-tell-tale-heart",   "/art/acrylic-painting-happiness-in-sorting",   "/art/acrylic-painting-play-room-2",   "/art/oil-painting-sensual-transcendence",   "/art/mixed-media-artwork-the-mountains-between-us",   "/art/oil-painting-ten-of-swords",   "/art/oil-painting-alchemic-kingdom",   "/art/oil-painting-windmills",   "/art/watercolor-painting-birch-wood",   "/art/mixed-media-artwork-old-growth-new-beginnings",   "/art/oil-painting-the-everlasting-folly-of-rose-and-abernathy",   "/art/oil-painting-one-blossom-one-world-peony-deer-i",   "/art/oil-painting-nine-of-swords",   "/art/oil-painting-eight-of-swords-ii",   "/art/oil-painting-rest-60880",   "/art/acrylic-painting-remembrance",   "/art/acrylic-painting-the-stroll",   "/art/acrylic-painting-yellowstone-with-lock-and-key",   "/art/acrylic-painting-water-of-life",   "/art/oil-painting-who-are-these-angels-cxlv",   "/art/acrylic-painting-luminous-stream",   "/art/mixed-media-artwork-desert-and-the-sea",   "/art/oil-painting-natura-naturans",   "/art/oil-painting-new-toy",   "/art/oil-painting-lines-upon-lines",   "/art/acrylic-painting-from-the-ashes",   "/art/encaustic-artwork-case-of-the-mythical-monkey",   "/art/encaustic-artwork-mystery-of-the-blue-velvet-mask",   "/art/acrylic-painting-prologue-of-a-cherry",   "/art/acrylic-painting-sorting-peaches",   "/art/oil-painting-out-of-this-world",   "/art/oil-painting-one-blossom-one-world-peony-deer-iii",   "/art/oil-painting-her-transformation",   "/art/oil-painting-isolation-iii",   "/art/acrylic-painting-don-t-be-sad-it-could-have-been-worse",   "/art/acrylic-painting-semaphore",   "/art/oil-painting-emptiness",   "/art/oil-painting-blue-green-cubist-cafe",   "/art/oil-painting-morning-joy",   "/art/oil-painting-nature-is-love",   "/art/oil-painting-tranquil-blue",   "/art/oil-painting-grateful",   "/art/oil-painting-dream-a-little-dream-of-me"],
}


# add categories to db first
# for category in categories.keys():
#     Category.objects.create(id=categories[category], name=category)

s = requests.Session()

for category in links.keys():
    for link in links[category]:
        r = s.get(base_url+link)
        soup = BeautifulSoup(r.text, "lxml")
        title = soup.select("h2[itemprop='name']")[0].get_text()
        description = soup.select("[class='artwork-description']")[0].get_text().replace("'", "''")
        image = soup.select("img[itemprop='image']")[0]["src"]
        image_url = os.path.basename(image)
        if not os.path.exists("/mnt/sda2/home/bl4ck/Documents/Code/Study/minor_project/imperium/web/uploads/" + image_url):
            wget.download(image, out="/mnt/sda2/home/bl4ck/Documents/Code/Study/minor_project/imperium/web/uploads")
        category_id = categories[category]
        price = random.randint(500, 10000)
        seller = 1
        current_time = datetime.now(pytz.timezone('Asia/Kathmandu'))
        random_future = timedelta(days=random.randint(0, 30))
        one_week = timedelta(weeks=1)
        added_at = current_time
        if random.randint(0, 1):
            starts_at = current_time
        else:
            starts_at = current_time + random_future
        deadline_at = current_time + one_week
        slug = slugify(title)
        Item.objects.create(title=title, description=description, image=image_url, price=price, added_at=added_at, starts_at=starts_at, deadline_at=deadline_at, slug=slug, category_id=category_id, seller_id=seller)

        # print(f"'{id}', '{title}', '{description}', '1.png', '{price}', '{added_at}', '{starts_at}', '{deadline_at}', '{slug}', '{category_id}', '{seller}'")
