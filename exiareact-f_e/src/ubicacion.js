import SectionSubtitle from "./subTitleSec";
import Inputvariable from './inputvariable';

export default function LocationDataProyect(props){

    return(
        <div className="locationData">
            <SectionSubtitle content="Ubicación"/>
            <div className="locationData__form">
                <Inputvariable inptitle = "Dirección" imgsrc = "img/ask.png" plcholder = "  Inserte dirección"/>
                <Inputvariable inptitle = "Latitud" imgsrc = "img/ask.png" plcholder = "  Inserte latitud"/>
                <Inputvariable inptitle = "Longitud" imgsrc = "img/ask.png" plcholder = "  Inserte longitud"/>
            </div>
            <div className="locationData__map">
            </div>
            <div className="seleccionUbicacion__botonBusqueda">
                <button className="centralButton"><img src="img/magnifying-glass.png" className="icon" />Buscar Seleccion</button>
            </div>
      </div>
        
    );
}