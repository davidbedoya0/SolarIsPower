import SectionSubtitle from "./subTitleSec";
import Inputvariable from './inputvariable';

export default function BasicDataProyect(props){

    return(
        <div className="formularionuevoproyecto__seleccionUbicacion">
            <SectionSubtitle content="Datos Básicos"/>
            <div className="seleccionUbicacion__formulario">

            <Inputvariable inptitle = "Dirección" imgsrc = "img/ask.png" plcholder = "  Inserte dirección"/>
            <Inputvariable inptitle = "Latitud" imgsrc = "img/ask.png" plcholder = "  Inserte latitud"/>
            <Inputvariable inptitle = "Longitud" imgsrc = "img/ask.png" plcholder = "  Inserte longitud"/>
          
        </div>
        <div className="seleccionUbicacion__ubicacion">
        </div>
        <div className="seleccionUbicacion__botonBusqueda">
          <button><img src="img/magnifying-glass.png" className="icon" />Buscar Seleccion</button>
        </div>
      </div>
        
    );
}