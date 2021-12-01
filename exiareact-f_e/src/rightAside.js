import RightAsideItem from "./shared/rightAsideItem";
import StatusBarGradient from "./statusBarGradient";

export default function RightAside(props){

    return(
        <div className="rightAside">
          <div className="aside__container">
            <div className="aside__header">
              <p>Resumen de proyecto</p>
            </div>
            <div className="aside__body">
              <StatusBarGradient status = "40"/>
              <h3 className="asideSectionTitle">
                Datos Basicos del Proyecto
              </h3>
              <RightAsideItem itemTitle = "Proyecto: " value=" Proyect Name"/>
              <RightAsideItem itemTitle = "Coordenadas: " value=" Lat:105.2 | Lon:302"/>
              <RightAsideItem itemTitle = "Tipo de Proyecto: " value=" On-grid"/>
              <RightAsideItem itemTitle = "Estimación Detallada: " value=" Activado"/>
              <h3 className="asideSectionTitle">
                Datos Elécticos
              </h3>
              <RightAsideItem itemTitle = "Potencia Instalada: " value=" 335 kW"/>
              <RightAsideItem itemTitle = "Energía Consumida: " value=" 335 kWh"/>
              <RightAsideItem itemTitle = "Configuración: " value=" 230 V"/>
              <h3 className="asideSectionTitle">
                Resumen Generación
              </h3>
              <RightAsideItem itemTitle = "Horas Solar Pico: " value=" 4.3 HSP"/>
              <RightAsideItem itemTitle = "Energía Generada: " value=" 30kWh"/>
              <div className="asideButtonContainer">
                <button className="asideButton">
                  Estimar Proyecto
                </button>
              </div>
              
            </div>
          </div>
        </div>
        
        
    );
}