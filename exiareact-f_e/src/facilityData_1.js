import React, {useEffect, useState} from "react";
import Selectvariable from "./shared/selectVariable";
import Inputvariable from "./shared/inputvariable";
import SectionSubtitle from "./shared/subTitleSec";
import SetRadioInput from "./shared/setRadioInput";
import askLogo from "./img/ask.png";
import SubTitleInfo from "./shared/subTitlewInfo";

export default function FacilityData_1(){


    return(
        <div className="formularionuevoproyecto__entradaEnergia">
            <SectionSubtitle content ="Datos de Electricos de la Instalación"/>
            <Selectvariable selects="4" selValues="0,1,2,3" selOpt="MONOFASICO F+N,BIFASICO 2F,TRIFASICO 3F,TRIFASICO 3F+N" 
                selTitle="Configuración AC">
                Aquí debes ingresar la configuración AC de tu instalación, este dato es crucial para seleccionar los equipos que se adapten 
                especificamente para tu instalación.
            </Selectvariable>
            <Selectvariable selects="5" selValues="0,1,2,3,4" selOpt="110V, 120V, 127V, 230V, 254V" selTitle="Voltaje Linea-Neutro">    
                Aquí debes ingresar el nivel de tensión al cual estan conectados tus equipos, este dato es crucial para seleccionar los equipos
                que se adapaten especificamente para tu instalación.
            </Selectvariable>
            <Inputvariable inptitle = "Área Disponible" imgsrc = {askLogo} plcholder = "Area en m^2">
                Aquí tomaremos la información del área disponible en tu instalación. Este dato nos permitira establecer la cantidad de equipos 
                que pueden ser instalados en tu proyecto, este dato es crucial para estimar la generación y el máximo valor de ahorro al que puedes 
                aspirar.
            </Inputvariable>
            <SubTitleInfo selTitle = "Información Adicional de la Instalación">
                Sí seleccionas la opción habilitar información adicional te preguntaremos detalles adicionales sobre
                el sitio de instalación. Estos datos nos permitiran hacer una estimación aun más precisa de los equipos y
                el costo del sistema
            </SubTitleInfo>
            
        </div>
    );
}
