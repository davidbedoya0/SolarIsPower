import AsideLeft__Item from './asideItem';
export default function Leftaside(props){

    return(
        <div className="leftAside">
            <div className="leftAside__Header">
                <p>
                    Etapas
                </p>
            </div>
            <AsideLeft__Item title="Creacion del Proyecto" idit="creat"/>
            <AsideLeft__Item title="Generacion" idit="Gen"/>
            <AsideLeft__Item title="Datos instalación 1" idit="Other_1"/>
            <AsideLeft__Item title="Datos instalación 2" idit="Other_2"/>

        </div>
        
    );
}