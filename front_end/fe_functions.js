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

        ? Tasks 
        cmplt Agregar cambio de nombre de proyecto
        todo agregar logica consulta PVGIS json
        todo Agregar Aside en pagina Web
        todo arreglar posicion costo unitario
        todo arreglar espaciamiento cargas especificas botones
        todo arreglar apariencia radius input informacion adicional
        todo agregar campos adicionales
        todo almacenar todos los valores y configurar json final
        todo arreglar header y footer
        todo arreglar imagenes tipo de sistema
        todo agregar iconos de ayuda y ayudas de cada input
        cmplt
*/

// Query selectors Inicio del proyecto
const typeSist = document.querySelector(".formularionuevoproyecto__tipodeproyecto--select")
const titleInput = document.querySelector(".formularionuevoproyecto__tipodeproyecto--input")
const siteTitle = document.querySelector(".formularionuevoproyecto__tituloseccion--Large")

// Query selectors Ubicacion

const newLoadButton = document.querySelector(".newLoad")
const energydemand = document.querySelector("#energydemand")
const tarifaestimada = document.querySelector("#tarifaEstimada")
const loadoutput = document.querySelector(".loadConsumptionOutput")
const uninkwhprice = document.querySelector("#kwhprice")
const deletButton = document.querySelector("#deleteButton")
const specificLoads = document.querySelector(".loadTables")
const loadName = document.getElementById("loadName")
const loadPower = document.getElementById("loadPower")
const loadHours = document.getElementById("loadHours")

const srcs = ["OnGrid.png","offGrid.png","hybrid.png"]
const syst_inf = ['*Sistema OnGrid, sistema compuesto por paneles, tableros de proteccion, inversor, tablero de protecciones DC y contador bidireccional', 
    `*Sistema Off-Grid, sistema compuesto por paneles, tablero de protecciones DC, inversor de onda pura, baterias y tablero de protecciones AC`,
    `*Sistema Off-Grid, sistema compuesto por paneles, tablero de protecciones DC, inversor hibrido, baterias, tablero de protecciones AC y contador bidireccional`
]

function showTypeSystemInfographic(){

    // verificar si la seleccion es igual a la actual
    const edit_img = document.querySelector(".tipoProyecto__img");
    const var_select = document.querySelector("#selTypSyst");
    const infoPryct = document.querySelector(".tipoProyecto__info--p")
    var vardata= var_select.selectedIndex;
    
    edit_img.classList.add("transimg")
    setTimeout(function(){}, 5000)
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
    };
    setTimeout(function(){edit_img.classList.remove("transimg")}, 1000)
    //edit_img.classList.add("endtransimg")
    
};


function crearTabla(){

    if(loadName.value == ""|loadPower.value == ""|loadHours.value == ""){
        alert("Debe completar todos los datos")
        return 0
    }

    // Verifica si la tabla ya ha sido creada
    if (document.querySelector(".headloadTables") == null){
        var headerCargas = document.createElement("div")
        var tituloTablaCargas = document.createElement("div")
        tituloTablaCargas.innerHTML="Listado de cargas"
        var headerNames = document.createElement("div")
        headerNames.innerHTML="Nombre"
        var headerHoras = document.createElement("div")
        headerHoras.innerHTML="Horas <br> [h]"
        var headerPotencia = document.createElement("div")
        headerPotencia.innerHTML="Potencia <br> [kW]"
        var headerEnergia = document.createElement("div")
        headerEnergia.innerHTML="Energia <br> [kWh]"
        headerCargas.appendChild(tituloTablaCargas)
        headerCargas.appendChild(headerNames)
        headerCargas.appendChild(headerHoras)
        headerCargas.appendChild(headerPotencia)
        headerCargas.appendChild(headerEnergia)

        headerCargas.setAttribute("class","headloadTables")
        headerNames.setAttribute("class","headloadTables_headers_name")
        headerHoras.setAttribute("class","headloadTables_headers_others")
        headerPotencia.setAttribute("class","headloadTables_headers_others")
        headerEnergia.setAttribute("class","headloadTables_headers_others")
        tituloTablaCargas.setAttribute("class","headloadTables_headers_title")
        
        specificLoads.appendChild(headerCargas)

    }
    // Crea la casilla
    var carga = document.createElement("div")
    var loName = document.createElement("div")
    var lousHor = document.createElement("div")
    var loPow = document.createElement("div")
    var loEnr = document.createElement("div")
    

    // Obtiene datos de la carga
    var ld_pwr = loadPower.value
    var ld_hrs = loadHours.value
    var ld_enrg = ld_pwr * ld_hrs

    // Agregar contenido
    loName.innerHTML = loadName.value
    loPow.innerHTML = ld_pwr
    lousHor.innerHTML = ld_hrs
    loEnr.innerHTML = Math.round(ld_enrg)
    carga.setAttribute("class","carga_row")
    loEnr.setAttribute("class","loadcell_stl")
    lousHor.setAttribute("class","loadcell_stl")
    loPow.setAttribute("class","loadcell_stl")
    loName.setAttribute("class","loadName_stl")

    // ordena las casillas
    carga.appendChild(loName)
    carga.appendChild(lousHor)
    carga.appendChild(loPow)
    carga.appendChild(loEnr)
    specificLoads.appendChild(carga)

    // actualizar resultado general
    if(energydemand.innerText== ""){
        loadoutput.style.visibility = "visible"
        energydemand.innerHTML = Math.round(ld_enrg)
        tarifaestimada.innerHTML = Math.round(ld_enrg * Number(uninkwhprice.value) * 30)
    }
    else{
        energydemand.innerText = Math.round(Number(energydemand.innerText) + ld_enrg)
        tarifaestimada.innerHTML = Math.round(Number(energydemand.innerText) * Number(uninkwhprice.value) * 30)
    }
}

function changeTitle(){
    siteTitle.innerText = "Nuevo Proyecto" + ": " + titleInput.value
}

/*
function getIrradiationData(){

    
    var lati = 70;
    var long = 10;
    var params = "lat=" + lati + "&lon=" + long + "&horirrad=" + 1 + "&outputformat=" + "json";
    var urlTarget ="https://re.jrc.ec.europa.eu/api/MRcalc" + "?" + params;
    console.log(urlTarget)
    request = fetch(urlTarget)
    
}



getIrradiationData()
*/



// ! Event listeners

typeSist.addEventListener("change", (event)=>{
    showTypeSystemInfographic();
})

newLoadButton.addEventListener("click", (event)=>{
    crearTabla();
})

deletButton.addEventListener("click", (event)=>{
    specificLoads.innerHTML=""
    loadoutput.style.visibility = "hidden"
})

titleInput.addEventListener("change",(event)=>{
    changeTitle()
})

