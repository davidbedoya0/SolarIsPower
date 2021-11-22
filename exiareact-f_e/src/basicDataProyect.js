import SectionSubtitle from "./subTitleSec";
import Inputvariable from './inputvariable';

export default function BasicDataProyect(props){

    return(
        <div className="ProyectBasicData">
              <SectionSubtitle content="Datos Básicos"/>
              <div className="ProyectBasicData__form">
                <Inputvariable inptitle = "Nombre del Proyecto" imgsrc = "img/ask.png" plcholder = "  Nombre del proyecto"/>
                <p className="textoInputs-Selects">
                  Tipo de Sistema <img src="img/ask.png" className="icon" />
                </p>
                <select className="selectBox" id="selTypSyst">
                  <option value="0">Sistema On-grid</option>
                  <option value="1">Sistema Off-grid</option>
                  <option value="2">Sistema Hibrido</option>
                </select>
              </div>
              <div className="ProyectBasicData__info">
                <div className="ProyectBasicData__container--img">
                  <img src="img/SistemaOnGrid.png" className="tipoProyecto__img" />
                </div>
                <p>
                  *Sistema OnGrid, sistema compuesto por paneles,
                  tableros de proteccion, inversor, tablero de protecciones DC y contador bidireccional
                </p>
              </div>
              <div className="">
                <button className="centralButton">Guardar Entrada</button>
              </div>
              
        </div>
        
    );
}