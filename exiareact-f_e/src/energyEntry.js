import Selectvariable from "./shared/selectVariable";
import InfoDisplay from "./shared/displayInfo";
import Inputvariable from "./shared/inputvariable";
import SubSection from "./shared/subSection";
import SectionSubtitle from "./shared/subTitleSec";
import askLogo from "./img/ask.png";
import SetRadioInput from "./shared/setRadioInput";

export default function Energyform(){

    return(
        <div className="formularionuevoproyecto__entradaEnergia">
            <SectionSubtitle content ="Demanda de energia"/>
            <Inputvariable inptitle = "Costo Unitario" imgsrc = {askLogo} plcholder = " precio kWh [$COP]">
                    Este es el cobro por unidad de energía en su instalación. Esta información esta disponible es 
                    su factura de energía eléctrica.
            </Inputvariable>
            <SetRadioInput selTitle = "Entrada de consumo" amount = "2" 
                options = " Consolidado de consumo, Construir consumo por conjunto de cargas" values = "0,1">
                Sí se selecciona la opción consolidado de consumo se ingresa un único valor de consumo de la instalación. La opción
                construir consumo por conjunto de cargas permite definir el consumo para cada carga en la instalación. La segunda opción requiere
                un conocimiento detallado de las cargas.
            </SetRadioInput>
            <SubSection subsubsectiontitle = "Consumo">
                <Selectvariable selects="3" selValues="0,1,2" selOpt="kWh/dia,kWh/mes,kWh/año" selTitle="Seleccion de Magnitud">
                    Esta selección nos permite conocer la unidad de energía empleada para desarrollar la estimación de tu 
                    sistema de generación.
                </Selectvariable>
                <Inputvariable inptitle = "Entrada de consumo de Energía" imgsrc = {askLogo} plcholder = "Unidades de energía">
                    Estas son las unidades de energía que consume su instalación. Esta información esta disponible en la factura 
                    de energía eléctrica.
                </Inputvariable>

                <InfoDisplay infoTitle = "Consumo de Energía: " infoData=""/>
                <InfoDisplay infoTitle = "Tarifa de Energía Estimada [COP $]: " infoData=""/>
                <div className="container_centralButton">
                    <button className="centralButton">Usar datos de consumo</button>
                </div>
            </SubSection>
            <SubSection subsubsectiontitle = "Calculo por cargas Conectadas">
                <Inputvariable inptitle = "Nombre" imgsrc = {askLogo} plcholder = "# Tag de Carga">
                    Este es el nombre que le asignara al equipo, dispositivo o electrodomestico que desea 
                    tener en cuenta en su consumo.
                </Inputvariable>
                    
                <Inputvariable inptitle = "Potencia Nominal" imgsrc = {askLogo} plcholder = "Potencia de la Carga [kW]">
                    Esta es la potencia de la carga que acaba de nombrar. Esta información esta disponible en adesibles o placas 
                    en el respaldo o base de la carga y se expresa como un valor numerico seguido por las unidades kW. 
                </Inputvariable>
                <Inputvariable inptitle = "Horas de Uso" imgsrc = {askLogo} plcholder = "Horas de Uso [h]">
                    Esta es la cantidad de tiempo que usted o los otros usuarios de la instalación utilizan esta carga.
                </Inputvariable>
                <div className="container_centralButton">
                    <button className="centralButton">Agregar Carga</button>
                </div>
                {/* Espacio para renderizar botones condicionales de la subseccion cargas especificas */}
                <InfoDisplay infoTitle = "Consumo de Energía: " infoData=""/>
                <InfoDisplay infoTitle = "Tarifa de Energía Estimada [COP $]: " infoData=""/>
            </SubSection>
        </div>
    );
}
