import './App.css';
import React, {useEffect, useState} from "react";
import HeaderWebPage from './header';
import Leftaside from './leftAside';
import AsideLeft__Item from './asideItem';
import CenterView from "./centerView";
import RightAside from './rightAside';
import Button from '@mui/material/Button'
import {AppBar} from '@mui/material/AppBar'


function App() {

  const [paginaActual, setPaginaActual] = useState(1);
  
  
  return (
      <div>
        <HeaderWebPage Title="Nuevo Proyecto"/>
        <div className="Main">
          
          <Leftaside>
            <AsideLeft__Item title="Creacion del Proyecto" idit="creat" opt="1" setPaginaActualState={setPaginaActual}/>
            <AsideLeft__Item title="Generacion" idit="Gen" opt="2" setPaginaActualState={setPaginaActual}/>
            <AsideLeft__Item title="Datos instalación 1" idit="Other_1" opt="3" setPaginaActualState={setPaginaActual}/>
            <AsideLeft__Item title="Datos instalación 2" idit="Other_2" opt="4" setPaginaActualState={setPaginaActual}/>
          </Leftaside>

          <div className="centerview">
            <CenterView selectedView = {paginaActual}/>
          </div>
          <RightAside/>

        </div> {/* End of centerview section */}
        <Button>Este es mi boton</Button>
        <div className="Footer">
          <p className="p_left">EXIA</p>
          <p className="p_left">Tutoriales</p>
          <p className="p_left">Data</p>
        </div>
      </div>
  );
}

export default App;


