import BasicDataProyect from "./basicDataProyect";
import Energyform from "./energyEntry";
import FacilityData_1 from "./facilityData_1";

export default function CenterView(props){
    const vistaSeleccionada = props.selectedView;
    if(vistaSeleccionada == 1){
        return <BasicDataProyect/>;
    }
    else if(vistaSeleccionada == 2){
        return <Energyform/>;
    }
    else if(vistaSeleccionada == 3){
        return <FacilityData_1/>;
    }
    return <BasicDataProyect/>;
}