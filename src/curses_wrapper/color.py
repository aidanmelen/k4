from typing import Type, List, Dict, Tuple, Iterator, ItemsView
import curses
import os

class CursesColor:
    """A wrapper around the curses color functionality.

    This class provides a higher-level interface to the curses color
    functionality, allowing the user to work with color names and
    RGB values instead of low-level color numbers.

    Attributes:
        COLOR_DEFAULT (int): The default color number.
    """

    COLOR_DEFAULT: int = -1

    def __init__(self) -> None:
        """Initializes a new CursesColorPair object."""
        self._color_name_to_number: Dict[str, int] = {}
        self._used_color_numbers: set = set()

        # Colors sourced from https://www.colorhexa.com/color-names
        self._color_name_to_rgb: Dict[str, Tuple[int, int, int]] = {
            "WHITE": (1000, 1000, 1000),
            "BLACK": (0, 0, 0),
            "RED": (1000, 0, 0),
            "GREEN": (0, 1000, 0),
            "BLUE": (0, 0, 1000),
            "AIR_FORCE_BLUE": (364, 541, 658),
            "ALICE_BLUE": (941, 972, 1000),
            "ALIZARIN_CRIMSON": (890, 149, 211),
            "ALMOND": (937, 870, 803),
            "AMARANTH": (898, 168, 313),
            "AMBER": (1000, 749, 0),
            "AMERICAN_ROSE": (1000, 11, 243),
            "AMETHYST": (600, 400, 800),
            "ANDROID_GREEN": (643, 776, 223),
            "ANTI_FLASH_WHITE": (949, 952, 956),
            "ANTIQUE_BRASS": (803, 584, 458),
            "ANTIQUE_FUCHSIA": (568, 360, 513),
            "ANTIQUE_WHITE": (980, 921, 843),
            "AO": (0, 501, 0),
            "APPLE_GREEN": (552, 713, 0),
            "APRICOT": (984, 807, 694),
            "AQUA": (0, 1000, 1000),
            "AQUAMARINE": (498, 1000, 831),
            "ARMY_GREEN": (294, 325, 125),
            "ARYLIDE_YELLOW": (913, 839, 419),
            "ASH_GREY": (698, 745, 709),
            "ASPARAGUS": (529, 662, 419),
            "ATOMIC_TANGERINE": (1000, 600, 400),
            "AUBURN": (647, 164, 164),
            "AUREOLIN": (992, 933, 0),
            "AUROMETALSAURUS": (431, 498, 501),
            "AWESOME": (1000, 125, 321),
            "AZURE": (0, 498, 1000),
            "AZURE_MIST_WEB": (941, 1000, 1000),
            "BABY_BLUE": (537, 811, 941),
            "BABY_BLUE_EYES": (631, 792, 945),
            "BABY_PINK": (956, 760, 760),
            "BALL_BLUE": (129, 670, 803),
            "BANANA_MANIA": (980, 905, 709),
            "BANANA_YELLOW": (1000, 882, 207),
            "BATTLESHIP_GREY": (517, 517, 509),
            "BAZAAR": (596, 466, 482),
            "BEAU_BLUE": (737, 831, 901),
            "BEAVER": (623, 505, 439),
            "BEIGE": (960, 960, 862),
            "BISQUE": (1000, 894, 768),
            "BISTRE": (239, 168, 121),
            "BITTERSWEET": (996, 435, 368),
            "BLACK": (0, 0, 0),
            "BLANCHED_ALMOND": (1000, 921, 803),
            "BLEU_DE_FRANCE": (192, 549, 905),
            "BLIZZARD_BLUE": (674, 898, 933),
            "BLOND": (980, 941, 745),
            "BLUE": (0, 0, 1000),
            "BLUE_BELL": (635, 635, 815),
            "BLUE_GRAY": (400, 600, 800),
            "BLUE_GREEN": (50, 596, 729),
            "BLUE_PURPLE": (541, 168, 886),
            "BLUE_VIOLET": (541, 168, 886),
            "BLUSH": (870, 364, 513),
            "BOLE": (474, 266, 231),
            "BONDI_BLUE": (0, 584, 713),
            "BONE": (890, 854, 788),
            "BOSTON_UNIVERSITY_RED": (800, 0, 0),
            "BOTTLE_GREEN": (0, 415, 305),
            "BOYSENBERRY": (529, 196, 376),
            "BRANDEIS_BLUE": (0, 439, 1000),
            "BRASS": (709, 650, 258),
            "BRICK_RED": (796, 254, 329),
            "BRIGHT_CERULEAN": (113, 674, 839),
            "BRIGHT_GREEN": (400, 1000, 0),
            "BRIGHT_LAVENDER": (749, 580, 894),
            "BRIGHT_MAROON": (764, 129, 282),
            "BRIGHT_PINK": (1000, 0, 498),
            "BRIGHT_TURQUOISE": (31, 909, 870),
            "BRIGHT_UBE": (819, 623, 909),
            "BRILLIANT_LAVENDER": (956, 733, 1000),
            "BRILLIANT_ROSE": (1000, 333, 639),
            "BRINK_PINK": (984, 376, 498),
            "BRITISH_RACING_GREEN": (0, 258, 145),
            "BRONZE": (803, 498, 196),
            "BROWN": (647, 164, 164),
            "BUBBLE_GUM": (1000, 756, 800),
            "BUBBLES": (905, 996, 1000),
            "BUFF": (941, 862, 509),
            "BULGARIAN_ROSE": (282, 23, 27),
            "BURGUNDY": (501, 0, 125),
            "BURLYWOOD": (870, 721, 529),
            "BURNT_ORANGE": (800, 333, 0),
            "BURNT_SIENNA": (913, 454, 317),
            "BURNT_UMBER": (541, 200, 141),
            "BYZANTINE": (741, 200, 643),
            "BYZANTIUM": (439, 160, 388),
            "CG_BLUE": (0, 478, 647),
            "CG_RED": (878, 235, 192),
            "CADET": (325, 407, 447),
            "CADET_BLUE": (372, 619, 627),
            "CADET_GREY": (568, 639, 690),
            "CADMIUM_GREEN": (0, 419, 235),
            "CADMIUM_ORANGE": (929, 529, 176),
            "CADMIUM_RED": (890, 0, 133),
            "CADMIUM_YELLOW": (1000, 964, 0),
            "CAFÉ_AU_LAIT": (650, 482, 356),
            "CAFÉ_NOIR": (294, 211, 129),
            "CAL_POLY_POMONA_GREEN": (117, 301, 168),
            "CAMBRIDGE_BLUE": (639, 756, 678),
            "CAMEL": (756, 603, 419),
            "CAMOUFLAGE_GREEN": (470, 525, 419),
            "CANARY": (1000, 1000, 600),
            "CANARY_YELLOW": (1000, 937, 0),
            "CANDY_APPLE_RED": (1000, 31, 0),
            "CANDY_PINK": (894, 443, 478),
            "CAPRI": (0, 749, 1000),
            "CAPUT_MORTUUM": (349, 152, 125),
            "CARDINAL": (768, 117, 227),
            "CARIBBEAN_GREEN": (0, 800, 600),
            "CARMINE": (1000, 0, 250),
            "CARMINE_PINK": (921, 298, 258),
            "CARMINE_RED": (1000, 0, 219),
            "CARNATION_PINK": (1000, 650, 788),
            "CARNELIAN": (701, 105, 105),
            "CAROLINA_BLUE": (600, 729, 866),
            "CARROT_ORANGE": (929, 568, 129),
            "CELADON": (674, 882, 686),
            "CELESTE": (698, 1000, 1000),
            "CELESTIAL_BLUE": (286, 592, 815),
            "CERISE": (870, 192, 388),
            "CERISE_PINK": (925, 231, 513),
            "CERULEAN": (0, 482, 654),
            "CERULEAN_BLUE": (164, 321, 745),
            "CHAMOISEE": (627, 470, 352),
            "CHAMPAGNE": (980, 839, 647),
            "CHARCOAL": (211, 270, 309),
            "CHARTREUSE": (498, 1000, 0),
            "CHERRY": (870, 192, 388),
            "CHERRY_BLOSSOM_PINK": (1000, 717, 772),
            "CHESTNUT": (803, 360, 360),
            "CHOCOLATE": (823, 411, 117),
            "CHROME_YELLOW": (1000, 654, 0),
            "CINEREOUS": (596, 505, 482),
            "CINNABAR": (890, 258, 203),
            "CINNAMON": (823, 411, 117),
            "CITRINE": (894, 815, 39),
            "CLASSIC_ROSE": (984, 800, 905),
            "COBALT": (0, 278, 670),
            "COCOA_BROWN": (823, 411, 117),
            "COFFEE": (435, 305, 215),
            "COLUMBIA_BLUE": (607, 866, 1000),
            "COOL_BLACK": (0, 180, 388),
            "COOL_GREY": (549, 572, 674),
            "COPPER": (721, 450, 200),
            "COPPER_ROSE": (600, 400, 400),
            "COQUELICOT": (1000, 219, 0),
            "CORAL": (1000, 498, 313),
            "CORAL_PINK": (972, 513, 474),
            "CORAL_RED": (1000, 250, 250),
            "CORDOVAN": (537, 247, 270),
            "CORN": (984, 925, 364),
            "CORNELL_RED": (701, 105, 105),
            "CORNFLOWER": (603, 807, 921),
            "CORNFLOWER_BLUE": (392, 584, 929),
            "CORNSILK": (1000, 972, 862),
            "COSMIC_LATTE": (1000, 972, 905),
            "COTTON_CANDY": (1000, 737, 850),
            "CREAM": (1000, 992, 815),
            "CRIMSON": (862, 78, 235),
            "CRIMSON_RED": (600, 0, 0),
            "CRIMSON_GLORY": (745, 0, 196),
            "CYAN": (0, 1000, 1000),
            "DAFFODIL": (1000, 1000, 192),
            "DANDELION": (941, 882, 188),
            "DARK_BLUE": (0, 0, 545),
            "DARK_BROWN": (396, 262, 129),
            "DARK_BYZANTIUM": (364, 223, 329),
            "DARK_CANDY_APPLE_RED": (643, 0, 0),
            "DARK_CERULEAN": (31, 270, 494),
            "DARK_CHESTNUT": (596, 411, 376),
            "DARK_CORAL": (803, 356, 270),
            "DARK_CYAN": (0, 545, 545),
            "DARK_ELECTRIC_BLUE": (325, 407, 470),
            "DARK_ORANGE": (721, 525, 43),
            "DARK_GRAY": (662, 662, 662),
            "DARK_GREEN": (3, 196, 125),
            "DARK_JUNGLE_GREEN": (101, 141, 129),
            "DARK_KHAKI": (741, 717, 419),
            "DARK_LAVA": (282, 235, 196),
            "DARK_LAVENDER": (450, 309, 588),
            "DARK_MAGENTA": (545, 0, 545),
            "DARK_MIDNIGHT_BLUE": (0, 200, 400),
            "DARK_OLIVE_GREEN": (333, 419, 184),
            "DARK_ORANGE": (1000, 549, 0),
            "DARK_ORCHID": (600, 196, 800),
            "DARK_PASTEL_BLUE": (466, 619, 796),
            "DARK_PASTEL_GREEN": (11, 752, 235),
            "DARK_PASTEL_PURPLE": (588, 435, 839),
            "DARK_PASTEL_RED": (760, 231, 133),
            "DARK_PINK": (905, 329, 501),
            "DARK_POWDER_BLUE": (0, 200, 600),
            "DARK_RASPBERRY": (529, 149, 341),
            "DARK_RED": (545, 0, 0),
            "DARK_SALMON": (913, 588, 478),
            "DARK_SCARLET": (337, 11, 98),
            "DARK_SEA_GREEN": (560, 737, 560),
            "DARK_SIENNA": (235, 78, 78),
            "DARK_SLATE_BLUE": (282, 239, 545),
            "DARK_SLATE_GRAY": (184, 309, 309),
            "DARK_SPRING_GREEN": (90, 447, 270),
            "DARK_TAN": (568, 505, 317),
            "DARK_TANGERINE": (1000, 658, 70),
            "DARK_TAUPE": (282, 235, 196),
            "DARK_TERRA_COTTA": (800, 305, 360),
            "DARK_TURQUOISE": (0, 807, 819),
            "DARK_VIOLET": (580, 0, 827),
            "DARTMOUTH_GREEN": (0, 411, 243),
            "DAVY_GREY": (333, 333, 333),
            "DEBIAN_RED": (843, 39, 325),
            "DEEP_CARMINE": (662, 125, 243),
            "DEEP_CARMINE_PINK": (937, 188, 219),
            "DEEP_CARROT_ORANGE": (913, 411, 172),
            "DEEP_CERISE": (854, 196, 529),
            "DEEP_CHAMPAGNE": (980, 839, 647),
            "DEEP_CHESTNUT": (725, 305, 282),
            "DEEP_COFFEE": (439, 258, 254),
            "DEEP_FUCHSIA": (756, 329, 756),
            "DEEP_JUNGLE_GREEN": (0, 294, 286),
            "DEEP_LILAC": (600, 333, 733),
            "DEEP_MAGENTA": (800, 0, 800),
            "DEEP_PEACH": (1000, 796, 643),
            "DEEP_PINK": (1000, 78, 576),
            "DEEP_SAFFRON": (1000, 600, 200),
            "DEEP_SKY_BLUE": (0, 749, 1000),
            "DENIM": (82, 376, 741),
            "DESERT": (756, 603, 419),
            "DESERT_SAND": (929, 788, 686),
            "DIM_GRAY": (411, 411, 411),
            "DODGER_BLUE": (117, 564, 1000),
            "DOGWOOD_ROSE": (843, 94, 407),
            "DOLLAR_BILL": (521, 733, 396),
            "DRAB": (588, 443, 90),
            "DUKE_BLUE": (0, 0, 611),
            "EARTH_YELLOW": (882, 662, 372),
            "ECRU": (760, 698, 501),
            "EGGPLANT": (380, 250, 317),
            "EGGSHELL": (941, 917, 839),
            "EGYPTIAN_BLUE": (62, 203, 650),
            "ELECTRIC_BLUE": (490, 976, 1000),
            "ELECTRIC_CRIMSON": (1000, 0, 247),
            "ELECTRIC_CYAN": (0, 1000, 1000),
            "ELECTRIC_GREEN": (0, 1000, 0),
            "ELECTRIC_INDIGO": (435, 0, 1000),
            "ELECTRIC_LAVENDER": (956, 733, 1000),
            "ELECTRIC_LIME": (800, 1000, 0),
            "ELECTRIC_PURPLE": (749, 0, 1000),
            "ELECTRIC_ULTRAMARINE": (247, 0, 1000),
            "ELECTRIC_VIOLET": (560, 0, 1000),
            "ELECTRIC_YELLOW": (1000, 1000, 0),
            "EMERALD": (313, 784, 470),
            "ETON_BLUE": (588, 784, 635),
            "FALLOW": (756, 603, 419),
            "FALU_RED": (501, 94, 94),
            "FAMOUS": (1000, 0, 1000),
            "FANDANGO": (709, 200, 537),
            "FASHION_FUCHSIA": (956, 0, 631),
            "FAWN": (898, 666, 439),
            "FELDGRAU": (301, 364, 325),
            "FERN": (443, 737, 470),
            "FERN_GREEN": (309, 474, 258),
            "FERRARI_RED": (1000, 156, 0),
            "FIELD_DRAB": (423, 329, 117),
            "FIRE_ENGINE_RED": (807, 125, 160),
            "FIREBRICK": (698, 133, 133),
            "FLAME": (886, 345, 133),
            "FLAMINGO_PINK": (988, 556, 674),
            "FLAVESCENT": (968, 913, 556),
            "FLAX": (933, 862, 509),
            "FLORAL_WHITE": (1000, 980, 941),
            "FLUORESCENT_ORANGE": (1000, 749, 0),
            "FLUORESCENT_PINK": (1000, 78, 576),
            "FLUORESCENT_YELLOW": (800, 1000, 0),
            "FOLLY": (1000, 0, 309),
            "FOREST_GREEN": (133, 545, 133),
            "FRENCH_BEIGE": (650, 482, 356),
            "FRENCH_BLUE": (0, 447, 733),
            "FRENCH_LILAC": (525, 376, 556),
            "FRENCH_ROSE": (964, 290, 541),
            "FUCHSIA": (1000, 0, 1000),
            "FUCHSIA_PINK": (1000, 466, 1000),
            "FULVOUS": (894, 517, 0),
            "FUZZY_WUZZY": (800, 400, 400),
            "GAINSBORO": (862, 862, 862),
            "GAMBOGE": (894, 607, 58),
            "GHOST_WHITE": (972, 972, 1000),
            "GINGER": (690, 396, 0),
            "GLAUCOUS": (376, 509, 713),
            "GLITTER": (901, 909, 980),
            "GOLD": (1000, 843, 0),
            "GOLDEN_BROWN": (600, 396, 82),
            "GOLDEN_POPPY": (988, 760, 0),
            "GOLDEN_YELLOW": (1000, 874, 0),
            "ORANGE": (854, 647, 125),
            "GRANNY_SMITH_APPLE": (658, 894, 627),
            "GRAY": (501, 501, 501),
            "GRAY_ASPARAGUS": (274, 349, 270),
            "GREEN": (0, 1000, 0),
            "GREEN_BLUE": (66, 392, 705),
            "GREEN_YELLOW": (678, 1000, 184),
            "GRULLO": (662, 603, 525),
            "GUPPIE_GREEN": (0, 1000, 498),
            "HALAYÀ_ÚBE": (400, 219, 329),
            "HAN_BLUE": (266, 423, 811),
            "HAN_PURPLE": (321, 94, 980),
            "HANSA_YELLOW": (913, 839, 419),
            "HARLEQUIN": (247, 1000, 0),
            "HARVARD_CRIMSON": (788, 0, 86),
            "HARVEST_GOLD": (854, 568, 0),
            "HEART_GOLD": (501, 501, 0),
            "HELIOTROPE": (874, 450, 1000),
            "HOLLYWOOD_CERISE": (956, 0, 631),
            "HONEYDEW": (941, 1000, 941),
            "HOOKER_GREEN": (286, 474, 419),
            "HOT_MAGENTA": (1000, 113, 807),
            "HOT_PINK": (1000, 411, 705),
            "HUNTER_GREEN": (207, 368, 231),
            "ICTERINE": (988, 968, 368),
            "INCHWORM": (698, 925, 364),
            "INDIA_GREEN": (74, 533, 31),
            "INDIAN_RED": (803, 360, 360),
            "INDIAN_YELLOW": (890, 658, 341),
            "INDIGO": (294, 0, 509),
            "INTERNATIONAL_KLEIN_BLUE": (0, 184, 654),
            "INTERNATIONAL_ORANGE": (1000, 309, 0),
            "IRIS": (352, 309, 811),
            "ISABELLINE": (956, 941, 925),
            "ISLAMIC_GREEN": (0, 564, 0),
            "IVORY": (1000, 1000, 941),
            "JADE": (0, 658, 419),
            "JASMINE": (972, 870, 494),
            "JASPER": (843, 231, 243),
            "JAZZBERRY_JAM": (647, 43, 368),
            "JONQUIL": (980, 854, 368),
            "JUNE_BUD": (741, 854, 341),
            "JUNGLE_GREEN": (160, 670, 529),
            "KU_CRIMSON": (909, 0, 50),
            "KELLY_GREEN": (298, 733, 90),
            "KHAKI": (764, 690, 568),
            "LA_SALLE_GREEN": (31, 470, 188),
            "LANGUID_LAVENDER": (839, 792, 866),
            "LAPIS_LAZULI": (149, 380, 611),
            "LASER_LEMON": (996, 996, 133),
            "LAUREL_GREEN": (662, 729, 615),
            "LAVA": (811, 62, 125),
            "LAVENDER": (901, 901, 980),
            "LAVENDER_BLUE": (800, 800, 1000),
            "LAVENDER_BLUSH": (1000, 941, 960),
            "LAVENDER_GRAY": (768, 764, 815),
            "LAVENDER_INDIGO": (580, 341, 921),
            "LAVENDER_MAGENTA": (933, 509, 933),
            "LAVENDER_MIST": (901, 901, 980),
            "LAVENDER_PINK": (984, 682, 823),
            "LAVENDER_PURPLE": (588, 482, 713),
            "LAVENDER_ROSE": (984, 627, 890),
            "LAWN_GREEN": (486, 988, 0),
            "LEMON": (1000, 968, 0),
            "LEMON_YELLOW": (1000, 956, 309),
            "LEMON_CHIFFON": (1000, 980, 803),
            "LEMON_LIME": (749, 1000, 0),
            "LIGHT_CRIMSON": (960, 411, 568),
            "LIGHT_THULIAN_PINK": (901, 560, 674),
            "LIGHT_APRICOT": (992, 835, 694),
            "LIGHT_BLUE": (678, 847, 901),
            "LIGHT_BROWN": (709, 396, 113),
            "LIGHT_CARMINE_PINK": (901, 403, 443),
            "LIGHT_CORAL": (941, 501, 501),
            "LIGHT_CORNFLOWER_BLUE": (576, 800, 917),
            "LIGHT_CYAN": (878, 1000, 1000),
            "LIGHT_FUCHSIA_PINK": (976, 517, 937),
            "LIGHT_ORANGE_YELLOW": (980, 980, 823),
            "LIGHT_GRAY": (827, 827, 827),
            "LIGHT_GREEN": (564, 933, 564),
            "LIGHT_KHAKI": (941, 901, 549),
            "LIGHT_PASTEL_PURPLE": (694, 611, 850),
            "LIGHT_PINK": (1000, 713, 756),
            "LIGHT_SALMON": (1000, 627, 478),
            "LIGHT_SALMON_PINK": (1000, 600, 600),
            "LIGHT_SEA_GREEN": (125, 698, 666),
            "LIGHT_SKY_BLUE": (529, 807, 980),
            "LIGHT_SLATE_GRAY": (466, 533, 600),
            "LIGHT_TAUPE": (701, 545, 427),
            "LIGHT_YELLOW": (1000, 1000, 929),
            "LILAC": (784, 635, 784),
            "LIME": (749, 1000, 0),
            "LIME_GREEN": (196, 803, 196),
            "LINCOLN_GREEN": (98, 349, 19),
            "LINEN": (980, 941, 901),
            "LION": (756, 603, 419),
            "LIVER": (325, 294, 309),
            "LUST": (901, 125, 125),
            "MSU_GREEN": (94, 270, 231),
            "MACARONI_AND_CHEESE": (1000, 741, 533),
            "MAGENTA": (1000, 0, 1000),
            "MAGIC_MINT": (666, 941, 819),
            "MAGNOLIA": (972, 956, 1000),
            "MAHOGANY": (752, 250, 0),
            "MAIZE": (984, 925, 364),
            "MAJORELLE_BLUE": (376, 313, 862),
            "MALACHITE": (43, 854, 317),
            "MANATEE": (592, 603, 666),
            "MANGO_TANGO": (1000, 509, 262),
            "MANTIS": (454, 764, 396),
            "MAROON": (501, 0, 0),
            "MAUVE": (878, 690, 1000),
            "MAUVE_TAUPE": (568, 372, 427),
            "MAUVELOUS": (937, 596, 666),
            "MAYA_BLUE": (450, 760, 984),
            "MEAT_BROWN": (898, 717, 231),
            "MEDIUM_PERSIAN_BLUE": (0, 403, 647),
            "MEDIUM_AQUAMARINE": (400, 866, 666),
            "MEDIUM_BLUE": (0, 0, 803),
            "MEDIUM_CANDY_APPLE_RED": (886, 23, 172),
            "MEDIUM_CARMINE": (686, 250, 207),
            "MEDIUM_CHAMPAGNE": (952, 898, 670),
            "MEDIUM_ELECTRIC_BLUE": (11, 313, 588),
            "MEDIUM_JUNGLE_GREEN": (109, 207, 176),
            "MEDIUM_LAVENDER_MAGENTA": (866, 627, 866),
            "MEDIUM_ORCHID": (729, 333, 827),
            "MEDIUM_PURPLE": (576, 439, 858),
            "MEDIUM_RED_VIOLET": (733, 200, 521),
            "MEDIUM_SEA_GREEN": (235, 701, 443),
            "MEDIUM_SLATE_BLUE": (482, 407, 933),
            "MEDIUM_SPRING_BUD": (788, 862, 529),
            "MEDIUM_SPRING_GREEN": (0, 980, 603),
            "MEDIUM_TAUPE": (403, 298, 278),
            "MEDIUM_TEAL_BLUE": (0, 329, 705),
            "MEDIUM_TURQUOISE": (282, 819, 800),
            "MEDIUM_VIOLET_RED": (780, 82, 521),
            "MELON": (992, 737, 705),
            "MIDNIGHT_BLUE": (98, 98, 439),
            "MIDNIGHT_GREEN": (0, 286, 325),
            "MIKADO_YELLOW": (1000, 768, 47),
            "MINT": (243, 705, 537),
            "MINT_CREAM": (960, 1000, 980),
            "MINT_GREEN": (596, 1000, 596),
            "MISTY_ROSE": (1000, 894, 882),
            "MOCCASIN": (980, 921, 843),
            "MODE_BEIGE": (588, 443, 90),
            "MOONSTONE_BLUE": (450, 662, 760),
            "MORDANT_RED_19": (682, 47, 0),
            "MOSS_GREEN": (678, 874, 678),
            "MOUNTAIN_MEADOW": (188, 729, 560),
            "MOUNTBATTEN_PINK": (600, 478, 552),
            "MULBERRY": (772, 294, 549),
            "MUNSELL": (949, 952, 956),
            "MUSTARD": (1000, 858, 345),
            "MYRTLE": (129, 258, 117),
            "NADESHIKO_PINK": (964, 678, 776),
            "NAPIER_GREEN": (164, 501, 0),
            "NAPLES_YELLOW": (980, 854, 368),
            "NAVAJO_WHITE": (1000, 870, 678),
            "NAVY_BLUE": (0, 0, 501),
            "NEON_CARROT": (1000, 639, 262),
            "NEON_FUCHSIA": (996, 349, 760),
            "NEON_GREEN": (223, 1000, 78),
            "NON_PHOTO_BLUE": (643, 866, 929),
            "NORTH_TEXAS_GREEN": (19, 564, 200),
            "OCEAN_BOAT_BLUE": (0, 466, 745),
            "OCHRE": (800, 466, 133),
            "OFFICE_GREEN": (0, 501, 0),
            "OLD_GOLD": (811, 709, 231),
            "OLD_LACE": (992, 960, 901),
            "OLD_LAVENDER": (474, 407, 470),
            "OLD_MAUVE": (403, 192, 278),
            "OLD_ROSE": (752, 501, 505),
            "OLIVE": (501, 501, 0),
            "OLIVE_DRAB": (419, 556, 137),
            "OLIVE_GREEN": (729, 721, 423),
            "OLIVINE": (603, 725, 450),
            "ONYX": (58, 58, 58),
            "OPERA_MAUVE": (717, 517, 654),
            "ORANGE": (1000, 647, 0),
            "ORANGE_YELLOW": (972, 835, 407),
            "ORANGE_PEEL": (1000, 623, 0),
            "ORANGE_RED": (1000, 270, 0),
            "ORCHID": (854, 439, 839),
            "OTTER_BROWN": (396, 262, 129),
            "OUTER_SPACE": (254, 290, 298),
            "OUTRAGEOUS_ORANGE": (1000, 431, 290),
            "OXFORD_BLUE": (0, 129, 278),
            "PACIFIC_BLUE": (109, 662, 788),
            "PAKISTAN_GREEN": (0, 400, 0),
            "PALATINATE_BLUE": (152, 231, 886),
            "PALATINATE_PURPLE": (407, 156, 376),
            "PALE_AQUA": (737, 831, 901),
            "PALE_BLUE": (686, 933, 933),
            "PALE_BROWN": (596, 462, 329),
            "PALE_CARMINE": (686, 250, 207),
            "PALE_CERULEAN": (607, 768, 886),
            "PALE_CHESTNUT": (866, 678, 686),
            "PALE_COPPER": (854, 541, 403),
            "PALE_CORNFLOWER_BLUE": (670, 803, 937),
            "PALE_GOLD": (901, 745, 541),
            "PALE_ORANGE": (933, 909, 666),
            "PALE_GREEN": (596, 984, 596),
            "PALE_LAVENDER": (862, 815, 1000),
            "PALE_MAGENTA": (976, 517, 898),
            "PALE_PINK": (980, 854, 866),
            "PALE_PLUM": (866, 627, 866),
            "PALE_RED_VIOLET": (858, 439, 576),
            "PALE_ROBIN_EGG_BLUE": (588, 870, 819),
            "PALE_SILVER": (788, 752, 733),
            "PALE_SPRING_BUD": (925, 921, 741),
            "PALE_TAUPE": (737, 596, 494),
            "PALE_VIOLET_RED": (858, 439, 576),
            "PANSY_PURPLE": (470, 94, 290),
            "PAPAYA_WHIP": (1000, 937, 835),
            "PARIS_GREEN": (313, 784, 470),
            "PASTEL_BLUE": (682, 776, 811),
            "PASTEL_BROWN": (513, 411, 325),
            "PASTEL_GRAY": (811, 811, 768),
            "PASTEL_GREEN": (466, 866, 466),
            "PASTEL_MAGENTA": (956, 603, 760),
            "PASTEL_ORANGE": (1000, 701, 278),
            "PASTEL_PINK": (1000, 819, 862),
            "PASTEL_PURPLE": (701, 619, 709),
            "PASTEL_RED": (1000, 411, 380),
            "PASTEL_VIOLET": (796, 600, 788),
            "PASTEL_YELLOW": (992, 992, 588),
            "PATRIARCH": (501, 0, 501),
            "PAYNE_GREY": (325, 407, 470),
            "PEACH": (1000, 898, 705),
            "PEACH_PUFF": (1000, 854, 725),
            "PEACH_YELLOW": (980, 874, 678),
            "PEAR": (819, 886, 192),
            "PEARL": (917, 878, 784),
            "PEARL_AQUA": (533, 847, 752),
            "PERIDOT": (901, 886, 0),
            "PERIWINKLE": (800, 800, 1000),
            "PERSIAN_BLUE": (109, 223, 733),
            "PERSIAN_INDIGO": (196, 70, 478),
            "PERSIAN_ORANGE": (850, 564, 345),
            "PERSIAN_PINK": (968, 498, 745),
            "PERSIAN_PLUM": (439, 109, 109),
            "PERSIAN_RED": (800, 200, 200),
            "PERSIAN_ROSE": (996, 156, 635),
            "PHLOX": (874, 0, 1000),
            "PHTHALO_BLUE": (0, 58, 537),
            "PHTHALO_GREEN": (70, 207, 141),
            "PIGGY_PINK": (992, 866, 901),
            "PINE_GREEN": (3, 474, 435),
            "PINK": (1000, 752, 796),
            "PINK_FLAMINGO": (988, 454, 992),
            "PINK_SHERBET": (968, 560, 654),
            "PINK_PEARL": (905, 674, 811),
            "PISTACHIO": (576, 772, 447),
            "PLATINUM": (898, 894, 886),
            "PLUM": (866, 627, 866),
            "PORTLAND_ORANGE": (1000, 352, 211),
            "POWDER_BLUE": (690, 878, 901),
            "PRINCETON_ORANGE": (1000, 560, 0),
            "PRUSSIAN_BLUE": (0, 192, 325),
            "PSYCHEDELIC_PURPLE": (874, 0, 1000),
            "PUCE": (800, 533, 600),
            "PUMPKIN": (1000, 458, 94),
            "PURPLE": (501, 0, 501),
            "PURPLE_HEART": (411, 207, 611),
            "PURPLE_MOUNTAINS_MAJESTY": (615, 505, 729),
            "PURPLE_MOUNTAIN_MAJESTY": (588, 470, 713),
            "PURPLE_PIZZAZZ": (996, 305, 854),
            "PURPLE_TAUPE": (313, 250, 301),
            "RACKLEY": (364, 541, 658),
            "RADICAL_RED": (1000, 207, 368),
            "RASPBERRY": (890, 43, 364),
            "RASPBERRY_GLACE": (568, 372, 427),
            "RASPBERRY_PINK": (886, 313, 596),
            "RASPBERRY_ROSE": (701, 266, 423),
            "RAW_SIENNA": (839, 541, 349),
            "RAZZLE_DAZZLE_ROSE": (1000, 200, 800),
            "RAZZMATAZZ": (890, 145, 419),
            "RED": (1000, 0, 0),
            "RED_ORANGE": (1000, 325, 286),
            "RED_BROWN": (647, 164, 164),
            "RED_VIOLET": (780, 82, 521),
            "RICH_BLACK": (0, 250, 250),
            "RICH_CARMINE": (843, 0, 250),
            "RICH_ELECTRIC_BLUE": (31, 572, 815),
            "RICH_LILAC": (713, 400, 823),
            "RICH_MAROON": (690, 188, 376),
            "RIFLE_GREEN": (254, 282, 200),
            "ROBINS_EGG_BLUE": (121, 807, 796),
            "ROSE": (1000, 0, 498),
            "ROSE_BONBON": (976, 258, 619),
            "ROSE_EBONY": (403, 282, 274),
            "ROSE_GOLD": (717, 431, 474),
            "ROSE_MADDER": (890, 149, 211),
            "ROSE_PINK": (1000, 400, 800),
            "ROSE_QUARTZ": (666, 596, 662),
            "ROSE_TAUPE": (564, 364, 364),
            "ROSE_VALE": (670, 305, 321),
            "ROSEWOOD": (396, 0, 43),
            "ROSSO_CORSA": (831, 0, 0),
            "ROSY_BROWN": (737, 560, 560),
            "ROYAL_AZURE": (0, 219, 658),
            "ROYAL_BLUE": (254, 411, 882),
            "ROYAL_FUCHSIA": (792, 172, 572),
            "ROYAL_PURPLE": (470, 317, 662),
            "RUBY": (878, 66, 372),
            "RUDDY": (1000, 0, 156),
            "RUDDY_BROWN": (733, 396, 156),
            "RUDDY_PINK": (882, 556, 588),
            "RUFOUS": (658, 109, 27),
            "RUSSET": (501, 274, 105),
            "RUST": (717, 254, 54),
            "SACRAMENTO_STATE_GREEN": (0, 337, 247),
            "SADDLE_BROWN": (545, 270, 74),
            "SAFETY_ORANGE": (1000, 403, 0),
            "SAFFRON": (956, 768, 188),
            "SAINT_PATRICK_BLUE": (137, 160, 478),
            "SALMON": (1000, 549, 411),
            "SALMON_PINK": (1000, 568, 643),
            "SAND": (760, 698, 501),
            "SAND_DUNE": (588, 443, 90),
            "SANDSTORM": (925, 835, 250),
            "SANDY_BROWN": (956, 643, 376),
            "SANDY_TAUPE": (588, 443, 90),
            "SAP_GREEN": (313, 490, 164),
            "SAPPHIRE": (58, 321, 729),
            "SATIN_SHEEN_GOLD": (796, 631, 207),
            "SCARLET": (1000, 141, 0),
            "SCHOOL_BUS_YELLOW": (1000, 847, 0),
            "SCREAMIN_GREEN": (462, 1000, 478),
            "SEA_BLUE": (0, 411, 580),
            "SEA_GREEN": (180, 545, 341),
            "SEAL_BROWN": (196, 78, 78),
            "SEASHELL": (1000, 960, 933),
            "SELECTIVE_YELLOW": (1000, 729, 0),
            "SEPIA": (439, 258, 78),
            "SHADOW": (541, 474, 364),
            "SHAMROCK": (270, 807, 635),
            "SHAMROCK_GREEN": (0, 619, 376),
            "SHOCKING_PINK": (988, 58, 752),
            "SIENNA": (533, 176, 90),
            "SILVER": (752, 752, 752),
            "SINOPIA": (796, 254, 43),
            "SKOBELOFF": (0, 454, 454),
            "SKY_BLUE": (529, 807, 921),
            "SKY_MAGENTA": (811, 443, 686),
            "SLATE_BLUE": (415, 352, 803),
            "SLATE_GRAY": (439, 501, 564),
            "SMALT": (0, 200, 600),
            "SMOKEY_TOPAZ": (576, 239, 254),
            "SMOKY_BLACK": (62, 47, 31),
            "SNOW": (1000, 980, 980),
            "SPIRO_DISCO_BALL": (58, 752, 988),
            "SPRING_BUD": (654, 988, 0),
            "SPRING_GREEN": (0, 1000, 498),
            "STEEL_BLUE": (274, 509, 705),
            "STIL_DE_GRAIN_YELLOW": (980, 854, 368),
            "STIZZA": (600, 0, 0),
            "STORMCLOUD": (0, 501, 501),
            "STRAW": (894, 850, 435),
            "SUNGLOW": (1000, 800, 200),
            "SUNSET": (980, 839, 647),
            "SUNSET_ORANGE": (992, 368, 325),
            "TAN": (823, 705, 549),
            "TANGELO": (976, 301, 0),
            "TANGERINE": (949, 521, 0),
            "TANGERINE_YELLOW": (1000, 800, 0),
            "TAUPE": (282, 235, 196),
            "TAUPE_GRAY": (545, 521, 537),
            "TAWNY": (803, 341, 0),
            "TEA_GREEN": (815, 941, 752),
            "TEA_ROSE": (956, 760, 760),
            "TEAL": (0, 501, 501),
            "TEAL_BLUE": (211, 458, 533),
            "TEAL_GREEN": (0, 427, 356),
            "TERRA_COTTA": (886, 447, 356),
            "THISTLE": (847, 749, 847),
            "THULIAN_PINK": (870, 435, 631),
            "TICKLE_ME_PINK": (988, 537, 674),
            "TIFFANY_BLUE": (39, 729, 709),
            "TIGER_EYE": (878, 552, 235),
            "TIMBERWOLF": (858, 843, 823),
            "TITANIUM_YELLOW": (933, 901, 0),
            "TOMATO": (1000, 388, 278),
            "TOOLBOX": (454, 423, 752),
            "TOPAZ": (1000, 784, 486),
            "TRACTOR_RED": (992, 54, 207),
            "TROLLEY_GREY": (501, 501, 501),
            "TROPICAL_RAIN_FOREST": (0, 458, 368),
            "TRUE_BLUE": (0, 450, 811),
            "TUFTS_BLUE": (254, 490, 756),
            "TUMBLEWEED": (870, 666, 533),
            "TURKISH_ROSE": (709, 447, 505),
            "TURQUOISE": (188, 835, 784),
            "TURQUOISE_BLUE": (0, 1000, 937),
            "TURQUOISE_GREEN": (627, 839, 705),
            "TUSCAN_RED": (400, 258, 301),
            "TWILIGHT_LAVENDER": (541, 286, 419),
            "TYRIAN_PURPLE": (400, 7, 235),
            "UA_BLUE": (0, 200, 666),
            "UA_RED": (850, 0, 298),
            "UCLA_BLUE": (325, 407, 584),
            "UCLA_GOLD": (1000, 701, 0),
            "UFO_GREEN": (235, 815, 439),
            "UP_FOREST_GREEN": (3, 266, 129),
            "UP_MAROON": (482, 66, 74),
            "USC_CARDINAL": (600, 0, 0),
            "USC_GOLD": (1000, 800, 0),
            "UBE": (533, 470, 764),
            "ULTRA_PINK": (1000, 435, 1000),
            "ULTRAMARINE": (70, 39, 560),
            "ULTRAMARINE_BLUE": (254, 400, 960),
            "UMBER": (388, 317, 278),
            "UNITED_NATIONS_BLUE": (356, 572, 898),
            "UNIVERSITY_OF_CALIFORNIA_GOLD": (717, 529, 152),
            "UNMELLOW_YELLOW": (1000, 1000, 400),
            "UPSDELL_RED": (682, 125, 160),
            "UROBILIN": (882, 678, 129),
            "UTAH_CRIMSON": (827, 0, 247),
            "VANILLA": (952, 898, 670),
            "VEGAS_GOLD": (772, 701, 345),
            "VENETIAN_RED": (784, 31, 82),
            "VERDIGRIS": (262, 701, 682),
            "VERMILION": (890, 258, 203),
            "VERONICA": (627, 125, 941),
            "VIOLET": (933, 509, 933),
            "VIOLET_BLUE": (196, 290, 698),
            "VIOLET_RED": (968, 325, 580),
            "VIRIDIAN": (250, 509, 427),
            "VIVID_AUBURN": (572, 152, 141),
            "VIVID_BURGUNDY": (623, 113, 207),
            "VIVID_CERISE": (854, 113, 505),
            "VIVID_TANGERINE": (1000, 627, 537),
            "VIVID_VIOLET": (623, 0, 1000),
            "WARM_BLACK": (0, 258, 258),
            "WATERSPOUT": (0, 1000, 1000),
            "WENGE": (392, 329, 321),
            "WHEAT": (960, 870, 701),
            "WHITE": (1000, 1000, 1000),
            "WHITE_SMOKE": (960, 960, 960),
            "WILD_STRAWBERRY": (1000, 262, 643),
            "WILD_WATERMELON": (988, 423, 521),
            "WILD_BLUE_YONDER": (635, 678, 815),
            "WINE": (447, 184, 215),
            "WISTERIA": (788, 627, 862),
            "XANADU": (450, 525, 470),
            "YALE_BLUE": (58, 301, 572),
            "YELLOW": (1000, 1000, 0),
            "YELLOW_ORANGE": (1000, 682, 258),
            "YELLOW_GREEN": (603, 803, 196),
            "ZAFFRE": (0, 78, 658),
            "ZINNWALDITE_BROWN": (172, 86, 31),
        }

        self.__has_colors: bool = False

    def start_color(self) -> None:
        """Initializes curses colors and ensures that the terminal support 256 colors."""
        curses.start_color()

        if not curses.can_change_color():
            raise Exception("Cannot change colors displayed by the terminal.")

        if os.environ.get("TERM") != "xterm-256color":
            raise Exception("No extended color support found.")

        curses.use_default_colors()
        self.__has_colors = True

    def init_colors(self, color_names: List[str]) -> None:
        """Initializes the extended colors."""
        for color_name in color_names:
            self[color_name] = self._color_name_to_rgb[color_name]

    @property
    def has_colors(self) -> bool:
        """Returns True if the terminal supports colors."""
        return self.__has_colors

    @property
    def color_names(self) -> Dict[str, int]:
        """Returns a list of color names."""
        return self._color_name_to_rgb.keys()

    @property
    def color_name_to_number(self) -> Dict[str, int]:
        """Returns a dictionary mapping color names to their corresponding color numbers."""
        return self._color_name_to_number

    @property
    def color_name_to_rgb(self) -> Dict[str, Tuple[int, int, int]]:
        """Returns a dictionary mapping color names to their corresponding RGB color 3 Tuple (base 1000)."""
        return self._color_name_to_rgb

    def color_content_by_name(self, color_name: str) -> Tuple[int, int, int]:
        """Returns the RGB values of the color with the given name."""
        return curses.color_content(self._color_name_to_number[color_name])

    def color_content_by_number(self, color_number: int) -> Tuple[int, int, int]:
        """Returns the RGB values of the color with the given number."""
        return curses.color_content(color_number)

    def is_color_initialized(self, color_number: int) -> bool:
        """Returns True if the color with the given number has been initialized."""
        return color_number in self._color_name_to_number.values()

    def next_color_number(self) -> int:
        """Returns the next available color number from highest to lowest."""
        for color_number in range(curses.COLORS - 1, -1, -1):
            if color_number not in self._used_color_numbers:
                return color_number
        else:
            raise Exception(f"All {curses.COLORS} colors are set.")

    def __setitem__(self, color_name: str, rgb: Tuple[int, int, int]) -> None:
        """Sets a color by name and its corresponding RGB values."""
        color_name = str(color_name).upper()

        if color_name in self._color_name_to_number:
            # update existing color
            color_number = self[color_name]
            self._color_name_to_rgb[color_name] = rgb
            curses.init_color(color_number, *rgb)

        else:
            # create new color
            color_number = self.next_color_number()
            self._color_name_to_number[color_name] = color_number
            self._used_color_numbers.add(color_number)
            curses.init_color(color_number, *rgb)

    def __getitem__(self, color_name: str) -> int:
        """Returns the color number of a given color name."""
        return self._color_name_to_number[color_name]

    def get(self, color_name: str, default_color_number: int = COLOR_DEFAULT) -> int:
        """Returns the color number of a given color name, or a default value if the color name does not exist."""
        if color_name == "DEFAULT":
            return self.COLOR_DEFAULT
        return self._color_name_to_number.get(color_name, default_color_number)

    def __iter__(self) -> Iterator[Tuple[str, int]]:
        """Returns an iterator over the color name to color number mapping."""
        return iter(self._color_name_to_number.items())

    def items(self) -> ItemsView[str, int]:
        """Returns a view object containing the color name to color number mapping."""
        return self._color_name_to_number.items()


class CursesColorPair:
    """A wrapper around the curses color pair functionality.

    This class provides a higher-level interface to the curses color
    pair functionality, allowing the user to work with color pair names
    and low-level color pair numbers.

    Attributes:
        COLOR_PAIR_DEFAULT (int): The default color pair number.
    """

    COLOR_PAIR_DEFAULT: int = 0

    def __init__(self, curses_color: Type[CursesColor]) -> None:
        """
        Initializes a new CursesColorPair object.

        Args:
            curses_color (Type[CursesColor]): A CursesColor object representing the color palette.
        """
        if not isinstance(curses_color, CursesColor):
            raise TypeError("curses_color must be a CursesColor type.")

        self._curses_color = curses_color
        self._pair_name_to_number = {}
        self._used_pair_numbers = set()

    def init_pairs(self, bg_color_name: str = "DEFAULT") -> None:
        """Initializes color pairs for all possible foreground/background color permutations."""
        if not self._curses_color.has_colors:
            raise RuntimeError(
                "must call CursesColor().init_colors() before initializing the extended color pairs."
            )

        bg_color_name = str(bg_color_name).upper()
        bg_color_number = self._curses_color.get(bg_color_name)

        for fg_color_name, fg_color_number in self._curses_color:
            self.init_pair(fg_color_name, bg_color_name)

    def init_pair(self, fg_color_name: str, bg_color_name: str = "DEFAULT") -> None:
        """Initializes a color pair with the specified foreground and background colors."""
        pair_name = f"{fg_color_name}_ON_{bg_color_name}".upper()

        fg_color_number = self._curses_color.get(fg_color_name)
        bg_color_number = self._curses_color.get(bg_color_name)

        if not bg_color_number:
            raise Exception(f"The background color name {bg_color_name} has not been initialized.")

        self[pair_name] = (fg_color_name, bg_color_name)

    def next_pair_number(self) -> int:
        """Returns the next available color pair number from lowest to highest."""
        for pair_number in range(1, curses.COLOR_PAIRS - 1):
            if pair_number not in self._used_pair_numbers:
                return pair_number
        else:
            raise Exception("Color pair is greater than 32765 (curses.COLOR_PAIRS - 1).")

    @property
    def pair_name_to_number(self) -> Dict[str, int]:
        """Returns a dictionary mapping pair names to pair numbers."""
        return self._pair_name_to_number

    def __setitem__(self, pair_name: str, color_pair_names) -> None:
        """Sets a color pair with the specified name and color pair."""
        if len(color_pair_names) != 2:
            raise ValueError("color_pair_names must be a 2-tuple of color names.")

        fg_color_name = str(color_pair_names[0]).upper()
        bg_color_name = str(color_pair_names[1]).upper()
        pair_number = self.next_pair_number()
        curses.init_pair(
            pair_number,
            self._curses_color.get(fg_color_name),
            self._curses_color.get(bg_color_name),
        )
        self._pair_name_to_number[pair_name] = curses.color_pair(pair_number)
        self._used_pair_numbers.add(pair_number)

    def __getitem__(self, name: str) -> int:
        """Get the color pair number associated with the specified color pair name."""
        return self._pair_name_to_number[name]

    def get(self, pair_name: str, default: int = COLOR_PAIR_DEFAULT) -> int:
        """Get the color pair number associated with the specified color pair name, or the default value if not found."""
        return self._pair_name_to_number.get(pair_name, default)

    def __iter__(self) -> Iterator[Tuple[str, int]]:
        """Get an iterator over the color pairs."""
        return iter(self._pair_name_to_number.items())

    def items(self) -> ItemsView[str, int]:
        """Get an iterator over the color pairs."""
        return self._pair_name_to_number.items()