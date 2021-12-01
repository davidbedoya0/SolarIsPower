import SectionSubtitle from "./shared/subTitleSec";
import Inputvariable from './shared/inputvariable';
import Selectvariable from "./shared/selectVariable";
import askLogo from "./img/ask.png";
import systemImg from "./img/SistemaHibrido.png"
import Lupa from "./img/magnifying-glass.png"

export default function BasicDataProyect(props){

    return(
        <>
          <div className="ProyectBasicData">
                <SectionSubtitle content="Datos Básicos"/>
                <div className="ProyectBasicData__form">
                  <Inputvariable inptitle = "Nombre del Proyecto" imgsrc = {askLogo} plcholder = "  Nombre del proyecto">
                    Escriba el Nombre que desea asignarle a su nuevo proyecto
                  </Inputvariable>
                  <Selectvariable selects = "3" selValues = "0,1,2" selOpt = "Sistema On-Grid,Sistema Off-grid,Sistema Hibrido" selTitle = "Tipo de Sistema">
                    Aquí seleccionara el tipo de proyecto solar que desea estimar. A la derecha puede visualizar una descripción breve
                    de la selección del proyecto.
                  </Selectvariable>
                </div>
                <div className="ProyectBasicData__info">
                  <div className="ProyectBasicData__container--img">
                    <img src={systemImg} className="tipoProyecto__img" />
                  </div>
                  <p>
                    *Sistema OnGrid, sistema compuesto por paneles,
                    tableros de proteccion, inversor, tablero de protecciones DC y contador bidireccional.
                  </p>
                </div>
          </div>
          <div className="locationData">
              <SectionSubtitle content="Ubicación"/>
              <div className="locationData__form">
                  <Inputvariable inptitle = "Dirección" imgsrc = {askLogo} plcholder = "  Inserte dirección">
                    Esto nos ayudara a obtener los valores de irradiación de la ubicación de su proyecto
                  </Inputvariable>
                  <Inputvariable inptitle = "Latitud" imgsrc = {askLogo} plcholder = "  Inserte latitud">
                    Sí conoce la latitud de su instalación ingresela, esta información nos permitira obtener una estimación más
                    precisa de la irradiación en su proyecto.
                  </Inputvariable>
                  <Inputvariable inptitle = "Longitud" imgsrc = {askLogo} plcholder = "  Inserte longitud">
                  Sí conoce la longitud de su instalación ingresela, esta información nos permitira obtener una estimación más
                    precisa de la irradiación en su proyecto.
                  </Inputvariable>
              </div>
              <div className="locationData__map">
              </div>
              <div className="seleccionUbicacion__botonBusqueda">
                  <button className="centralButton"><img src={Lupa} className="icon" />Crear Proyecto</button>
              </div>
        </div>
      </>
        
    );
}