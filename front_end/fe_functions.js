/*
    Funciones del frontend de la pagina de exia.
    
    Funciones:
        showTypeSystemInfographic: Cambia la imagen infografica de 
        acuerdo al proyecto seleccionado. Anade tambien la transicion 
        y modifica el texto

        validation coordinates data: valida las coordenadas introducidas
        en el formulario del proyecto

        energyDataStorage: Almacena la informacion de la energia

        loadEnergyDataStorage: Almacena la informacion del consumo 
        proveniente de la informacion de las cargas

        newLoad: Anade una nueva carga, modifica el frontend por medio
        de la adicion de una tabla de cargas

        energyLoadsComputation: calcula la energia demandada y la tarifa 
        estimada de acuerdo al precio de la factura

        aditionalInfoEnable: Habilita los campos de informacion adicional
        y modifica el front-end.

*/

// Query selectors
const typeSist = document.querySelector(".formularionuevoproyecto__tipodeproyecto--select")

const srcs = ["OnGrid.png","offGrid.png","hybrid.png"]
const syst_inf = ['Has seleccionado un sistema OnGrid, este es un sistema compuesto por paneles, tableros de proteccion, inversor, tablero de protecciones DC y contador bidireccional', 
    `Has seleccionado un sistema Off-Grid, este es un sistema compuesto por paneles, tablero de protecciones DC, inversor de onda pura, baterias y tablero de protecciones AC`,
    `Has seleccionado un sistema Off-Grid, este es un sistema compuesto por paneles, tablero de protecciones DC, inversor hibrido, baterias, tablero de protecciones AC y contador bidireccional`
]

function showTypeSystemInfographic(){

    // verificar si la seleccion es igual a la actual
    const edit_img = document.querySelector(".tipoProyecto__img");
    const var_select = document.querySelector("#selTypSyst");
    const infoPryct = document.querySelector(".tipoProyecto__info--p")
    var vardata= var_select.selectedIndex;
    if(vardata == 0){
        edit_img.src = srcs[0];
        infoPryct.innerHTML = syst_inf[0]
    }   
    else if(vardata == 1){
        edit_img.src = srcs[1];
        infoPryct.innerHTML = syst_inf[1]
    }
    else if(vardata == 2){
        edit_img.src = srcs[2];
        infoPryct.innerHTML = syst_inf[2]
    }

}

typeSist.addEventListener("change", (event)=>{
    showTypeSystemInfographic();
})