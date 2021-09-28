#import pandas as pd 

proteccionesAC = {
    "referencia":["ABN52C15A", "ABN52C20A","ABN52C30A","ABN52C40A","ABN52C50A",
    "ABN62C60A", "ABN102C75A", "ABN102C100A",
    "ABN202C125A", "ABN202C200A", 
    "ABN53C15A", "ABN53C20A", "ABN53C30A", "ABN53C40A", "ABN53C50A", 
    "ABN63C60A", 
    "ABN103D20A", "ABN103D30A", "ABN103D40A", "ABN103D50A", "ABN103D60A", "ABN103D75A", "ABN103D100A", 
    "ABN203C125A","ABN203C150A","ABN203C175A","ABN203C200A","ABN203C225A","ABN203C250A",
    "ABN403C250A", "ABN403C300A", "ABN403C350A", "ABN403C400A", 
    "ABN803C500A", "ABN803C630A", "ABN803C800A"],

    "corriente":[15, 20, 30, 40, 50, 
    60, 75, 100, 
    125, 200, 
    15, 20, 30, 40, 50, 
    60, 
    20, 30, 40, 50, 60, 75, 100, 
    125, 150, 175, 200, 225, 250, 
    250, 300, 350, 400, 
    500, 630, 800], 

    "polos":[2, 2, 2, 2, 2, 
    2, 2, 2, 
    2, 2, 
    3, 3, 3, 3, 3, 
    3, 
    3, 3, 3, 3, 3, 3, 3, 
    3, 3, 3, 3, 3, 3, 
    3, 3, 3, 3,
    3, 3, 3], 

    "capacidadRuptura":[ [30, 18, 14], [30, 18, 14], [30, 18, 14], [30, 18, 14], [30, 18, 14],
    [30, 18, 14], [35, 22, 18], [35, 22, 18],
    [65, 30, 25], [65, 30, 25],
    [30, 18, 14], [30, 18, 14], [30, 18, 14], [30, 18, 14], [30, 18, 14], 
    [30, 18, 14], 
    [50, 30, 26], [50, 30, 26], [50, 30, 26], [50, 30, 26], [50, 30, 26], [50, 30, 26], [50, 30, 26], 
    [65, 30, 25], [65, 30, 25], [65, 30, 25], [65, 30, 25], [65, 30, 25], [65, 30, 25],
    [50, 42, 37], [50, 42, 37], [50, 42, 37], [50, 42, 37], 
    [50, 45, 37], [50, 45, 37], [50, 45, 37]
    ],

    "dimensiones":[ [50, 130, 60], [50, 130, 60], [50, 130, 60], [50, 130, 60], [50, 130, 60],
    [50, 130, 60], [50, 130, 60], [50, 130, 60],
    [105, 165, 60], [105, 165, 60],
    [75, 130, 60], [75, 130, 60], [75, 130, 60], [75, 130, 60], [75, 130, 60], 
    [75, 130, 60], 
    [75, 130, 60], [75, 130, 60], [75, 130, 60], [75, 130, 60], [75, 130, 60], [75, 130, 60], [75, 130, 60], 
    [105, 165, 60], [105, 165, 60], [105, 165, 60], [105, 165, 60], [105, 165, 60], [105, 165, 60],
    [140, 257, 109], [140, 257, 109], [140, 257, 109], [140, 257, 109], 
    [210, 280, 109], [210, 280, 109], [210, 280, 109]
    ],

    "precios": [159000, 159000, 159000, 159000, 159000, 
    174000, 174000, 174000, 
    325400, 325400,
    177000, 177000, 177000, 177000, 177000, 
    198000, 
    215000, 215000, 215000, 215000, 215000, 215000, 215000, 
    396000, 396000, 396000, 396000, 396000, 422000, 
    1045000, 1045000, 1045000, 1045000, 
    1955000, 1955000, 2199500],

    "tension":[ 600, 600, 600, 600, 600, 
    600, 600, 600, 
    600, 600, 
    600, 600, 600, 600, 600, 
    600, 
    600, 600, 600, 600, 600, 600, 600, 
    600, 600, 600, 600, 600, 600, 
    600, 600, 600, 600, 
    600, 600, 600
    ]
}


DPS_AC = {"referencia":["SPL220S2P_LS", "BKS_E_3PLS", "BKS_C_L4PS", 
            "CSH50120", "CSH50277","PSC1-12_120","PSC1-12_277",
            "PSC2-12_120TNS","PSC2-12_277TNS",
            "PSC3-12_230TNS","PSC3-12_480TNS",
            "PSC4-12_230TNS","PSC4-12_480TNS"], 

    "polos":[2, 3, 4,
        1, 1, 1, 1, 
        2, 2, 
        3, 3, 
        4, 4],
        
    "tension":[320, 460, 320, 
        208, 480, 208, 480, 
        208, 480, 
        208, 480, 
        208, 480],

    "ir":[80,70,40, 
        50, 50, 12.5, 12.5, 
        12.5, 12.5, 
        12.5, 12.5, 
        12.5, 12.5], 

    "precio":[1771000, 708500, 413100, 
        1333500, 1474900, 986500, 1097800, 
        1913900, 2235100, 
        3412500, 2939600, 
        3405000, 3901700
    ]
}


DPS_DC = {"referencia":["WorldSunlightn2P500VDC20_40kA","WorldSunlightn3P1000VDC20_40kA",
    "FEEO2P600V20_40kA", "FEEO3P1000V20_40kA", "Clamper3P300VDC40kA","Clamper1P275VDC20kA"], 

    "polos":[2, 3, 
        2, 3, 3, 1],

    "tension":[500, 1000, 600, 1000, 300, 275, 
    320],

    "ir":[40, 40, 40, 40, 40, 20]

}


proteccionesDC = {"referencia":["Siemens16ADC72V1P", "Weg20ADC120V1P",
    "Weg32ADC120V1P","Weg50ADC120V1P","Weg63ADC120V1P","Siemens50ADC120V1P",
    "Siemens40ADC72V1P","Siemens63ADC72V1P","Worldsunlight16ADC250V1P","Worldsunlight32ADC250V1P",
    "Worldsunlight63ADC250V1P","Worldsunlight16ADC500V2P","Worldsunlight32ADC500V2P","Worldsunlight63ADC500V2P",
    "Worldsunlight16ADC750V3P","Worldsunlight32ADC750V3P","Worldsunlight63ADC750V3P","Worldsunlight16ADC1000V4P",
    "Worldsunlight32ADC1000V4P","Worldsunlight63ADC1000V4P","FEEO16ADC1000V4P","FEEO32ADC1000V4P",
    "FEEO63ADC1000V4P","FEEO16ADC250V1P","FEEO32ADC250V1P","FEEO40ADC250V1P",
    "FEEO63ADC250V1P","FEEO16ADC500V2P","FEEO32ADC500V2P","FEEO63ADC500V2P"
    ], 

    #Precio sin IVA
    "precio":[ 28500, 28500, 
    31500, 34900, 39900, 31900, 
    34900, 39900, 64000, 64000, 
    64000, 114000, 114000, 114000, 
    159000, 159000, 159000, 179000,
    179000, 179000, 199000, 199000,
    199000, 69000, 69000, 69000, 
    69000, 129000, 129000, 129000],

    "corriente":[16, 20,
    32, 50, 63, 50, 
    40, 63, 16, 32, 
    63, 16, 32, 63, 
    16, 32, 63, 16,
    32, 63, 16, 32,
    63, 16, 32, 40, 
    63, 16, 32, 63],

    "tension":[72, 120,
    120, 120, 120, 120, 
    72, 72, 250, 250, 
    250, 500, 500, 500, 
    750, 750, 750, 1000, 
    1000, 1000, 1000, 1000, 
    1000, 250, 250, 250, 
    250, 500, 500, 500],

    "polos":[1, 1,
    1, 1, 1, 1, 
    1, 1, 1, 1, 
    1, 2, 2, 2, 
    3, 3, 3, 4, 
    4, 4, 4, 4, 
    4, 1, 1, 1, 
    1, 2, 2, 2],

    "marca":["Siemens", "Weg",
    "Weg","Weg","Weg","Siemens",
    "Siemens","Siemens","Worldsunlight","Worldsunlight",
    "Worldsunlight","Worldsunlight","Worldsunlight","Worldsunlight",
    "Worldsunlight","Worldsunlight","Worldsunlight","Worldsunlight",
    "Worldsunlight","Worldsunlight","FEEO","FEEO",
    "FEEO","FEEO","FEEO","FEEO",
    "FEEO","FEEO","FEEO","FEEO"
    ]
}

WiresISO = {
    "REF":["ALTHHN_N18","ALTHHN_N16","ALTHHN_N14","ALTHHN_N12","ALTHHN_N10","ALTHHN_N8","ALTHHNEXTDZL_N3x12",
    "ALTHHNEXTDZL_N14","ALTHHNEXTDZL_N12","ALTHHNEXTDZL_N10","ALTHHNEXTDZL_N8","ALTHHNEXTDZL_N6",
    "ALTHHNEXTDZL_N4","ALTHHNEXTDZL_N2","ALTHHNEXTDZL_N1_0","ALTHHNEXTDZL_N2_0","ALTHHNEXTDZL_N3_0",
    "ALTHHNEXTDZL_N4_0","ALTHHNEXTDZL_N250","ALTHHNEXTDZL_N300","ALTHHNEXTDZL_N350","ALTHHNEXTDZL_N400",
    "ALTHHNEXTDZL_N500","ALTHHN_SINTOXHF_N3X12","ALTHHN_SINTOXHF_N14"
    "ALTHHN_SINTOXHF_N12","ALTHHN_SINTOXHF_N10","ALTHHN_SINTOXHF_N8","ALTHHN_SINTOXHF_N6",
    "ALTHHN_SINTOXHF_N4","ALTHHN_SINTOXHF_N2","ALTHHN_SINTOXHF_N1_0","ALTHHN_SINTOXHF_N2_0",
    "ALTHHN_SINTOXHF_N4_0","ALTHHN_AL_SINTOXHF_N6","ALTHHN_AL_SINTOXHF_N4","ALTHHN_AL_SINTOXHF_N2",
    "ALTHHN_AL_SINTOXHF_N1_0","ALTHHN_AL_SINTOXHF_N2_0","ALTHHN_AL_SINTOXHF_N3_0","ALTHHN_AL_SINTOXHF_N4_0",
    "ALTHHN_AL_SINTOXHF_N250","ALTHHN_AL_SINTOXHF_N300","ALTHHN_AL_SINTOXHF_N350",
    "ALTHHN_AL_SINTOXHF_N400","ALTHHN_AL_SINTOXHF_N500"],

    "CALIBRE":[18, 16, 14, 12, 10, 8, 36, 
    14, 12, 10, 8, 6, 
    4, 2, 100, 200, 300, 
    400, 2500, 3000, 3500, 4000, 
    5000, 36, 14, 
    12, 10, 8, 6, 
    4, 2, 100, 200, 
    400, 6, 4, 2, 
    100, 200, 300, 400, 
    2500, 3000, 3500, 
    4000, 5000],

    "CAPCurr":[10, 13, 25, 30, 40, 55, 30, 
    25, 30, 40, 55, 75, 
    95, 130, 170, 195, 225, 
    260, 290, 320, 350, 380, 
    430, 30, 20, 
    25, 35, 50, 65, 
    85, 115, 150, 175, 
    230, 60, 75, 100, 
    135, 150, 175, 205, 
    230, 255, 280, 
    305, 350],

    "Precio":[925, 1239, 1499, 2157, 3474, 5506, 8889, 
    1950, 2787, 4032, 5979, 9243, 
    14262, 22118, 36141, 45164, 59892, 
    70750, 85447, 101485, 119147, 137400, 
    176915, 9787, 2147, 
    3064, 4435, 6578, 10166, 
    15687, 24329, 39753, 49681, 
    77824, 2906, 3906, 5716, 
    9431, 12289, 13813, 14537, 
    19630, 22006, 24150, 
    28084, 32873
    ]

}


"WirNakedCu"={
    "referencia":[]

}