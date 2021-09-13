import pandas as pd 

proteccionesAC = [
    "referencia"["worldsunlight B110A 4P XM1 - 125PV", "referencia2"]
]

proteccionesDC = {"referencia":["Siemens16ADC72V1P", "Weg20ADC120V1P",
    "Weg32ADC120V1P","Weg50ADC120V1P","Weg63ADC120V1P","Siemens50ADC120V1P",
    "Siemens40ADC72V1P","Siemens63ADC72V1P","Worldsunlight16ADC250V1P","Worldsunlight32ADC250V1P",
    "Worldsunlight63ADC250V1P","Worldsunlight16ADC500V2P","Worldsunlight32ADC500V2P","Worldsunlight63ADC500V2P",
    "Worldsunlight16ADC750V3P","Worldsunlight32ADC750V3P","Worldsunlight63ADC750V3P","Worldsunlight16ADC1000V4P",
    "Worldsunlight32ADC1000V4P","Worldsunlight63ADC1000V4P","FEEO16ADC1000V4P","FEEO32ADC1000V4P",
    "FEEO63ADC1000V4P","FEEO16ADC250V1P","FEEO32ADC250V1P","FEEO40ADC250V1P",
    "FEEO63ADC250V1P","FEEO16ADC500V2P","FEEO32ADC500V2P","FEEO63ADC500V2P"
    ], 

    "corriente":[16, 20,
    32, 50, 63, 50, 
    40, 63, 16, 32, 
    63, 16, 32, 63, 
    16, 32, 63, 16, 
    63, 16, 32, 40, 
    63, 16, 32, 63],

    "Tension":[72, 120,
    120, 120, 120, 120, 
    72, 72, 250, 250, 
    250, 500, 500, 500, 
    750, 750, 750, 1000, 
    1000, 250, 250, 250, 
    250, 500, 500, 500],

    "Polos":[1, 1,
    1, 1, 1, 1, 
    1, 1, 1, 1, 
    1, 2, 2, 2, 
    3, 3, 3, 4, 
    4, 1, 1, 1, 
    1, 2, 2, 2],

    "Polos":["Siemens", "Weg",
    "Weg","Weg","Weg","Siemens",
    "Siemens","Siemens","Worldsunlight","Worldsunlight",
    "Worldsunlight","Worldsunlight","Worldsunlight","Worldsunlight",
    "Worldsunlight","Worldsunlight","Worldsunlight","Worldsunlight",
    "Worldsunlight","Worldsunlight","FEEO","FEEO",
    "FEEO","FEEO","FEEO","FEEO",
    "FEEO","FEEO","FEEO","FEEO"
    ]

    }
