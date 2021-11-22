import './App.css';
import BasicDataProyect from './basicDataProyect';
import HeaderWebPage from './header';
import Inputvariable from './inputvariable';
import Leftaside from './leftAside';
import Selectvariable from './selectVariable';

function App() {

  return (
      <div>
        <HeaderWebPage Title="Nuevo Proyecto"/>
        <div className="Main">
          <Leftaside/>
          <div className="centerview">
            <BasicDataProyect/>
            
            <div className="formularionuevoproyecto__seleccionUbicacion">
              <div className="formularionuevoproyecto__tituloseccion">
                <h1 className="formularionuevoproyecto__titulosubseccion--highlight">
                  <p>
                    Ubicacion
                  </p>
                </h1>
              </div>
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
            <div className="formularionuevoproyecto__entradaEnergia">
              <div className="formularionuevoproyecto__tituloseccion">
                <h1 className="formularionuevoproyecto__titulosubseccion--highlight">
                  <p>
                    Demanda de energia
                  </p>
                </h1>
                <p className="p_left">Costo Unitario
                  <img src="img/ask.png" className="icon" /></p>
                <input type="text" className="inputForm_right" placeholder="Precio kWh [COP]" id="kwhprice" />
              </div>
              <div className="entradaEnergia__consumo">
                <h2 className="formularionuevoproyecto__titulosubsubseccion--highlight">
                  Consumo
                </h2>
                <p className="p_left">
                  Seleccion de Magnitud <img src="img/ask.png" className="icon" />
                </p>
                <select className="Selects_left">
                  <option value="0">kWh/dia</option>
                  <option value="1">kWh/mes</option>
                  <option value="2">kWh/anio</option>
                </select>
                <p className="p_left">
                  Entrada de energia <img src="img/ask.png" className="icon" />
                </p>
                <input type="text" className="inputForm" placeholder="Inserte el valor de Energia" />
                <button className="button_left"> Usar datos de consumo</button>
              </div>
              <div className="entradaEnergia__cargas">
                <h2 className="formularionuevoproyecto__titulosubsubseccion--highlight">
                  Cargas Especificas - Agregar cargas
                </h2>
                <div className="container__loadInputs">
                  <div className="container__formLoads">
                    <p className="p_left">Nombre <img src="img/ask.png" className="icon" /></p>
                    <input type="text" className="inputForm" placeholder="#Tag carga" id="loadName" />
                    <p className="p_left">Potencia Nominal <img src="img/ask.png" className="icon" /></p>
                    <input type="text" className="inputForm" placeholder="Potencia de carga [kw]" id="loadPower" />
                    <p className="p_left">Horas de uso <img src="img/ask.png" className="icon" /></p>
                    <input type="text" className="inputForm" placeholder="Horas de uso [h]" id="loadHours" />
                  </div>
                  <div className="container_rightButton">
                    <button className="button_right newLoad">Nueva Carga</button>
                  </div>
                </div>
                <div className="loadTables" id="#loadTables"></div>
                <div className="loadConsumptionOutput">
                  <div className="container__loadInputs">
                    <p className="p_left">
                      Energia demandada [kWh]
                    </p>
                    <div className="result" id="energydemand"></div>
                  </div>
                  <div className="container__loadInputs">
                    <p className="p_left">
                      Tarifa Estimada [COP $]
                    </p>
                    <div className="result" id="tarifaEstimada"></div>
                  </div>
                </div>
                <div className="buttonContainers">
                  <button className="buttonload" id="deleteButton"> Borrar Cargas</button>
                  <button className="buttonload"> Usar datos de Cargas</button>
                </div>
              </div>
            </div>

            <div className="formularionuevoproyecto__datosInstalacion" />
            <h1 className="formularionuevoproyecto__titulosubseccion--highlight">
              Otros datos de la instalacion
            </h1>
            <div className="datosInstalacion__configuracionAC">
              <p className="p_left">
                Configuracion AC <img src="img/ask.png" className="icon" />
              </p>
              <select className="Selects_left">
                <option value="0">MONOFASICO 1F+N</option>
                <option value="1">BIFASICO 2F</option>
                <option value="2">TRIFASICO 3F</option>
                <option value="3">TRIFASICO 4 HILOS 3F+N</option>
              </select>
              <p className="p_left">
                Nivel de tension Linea-Neutro <img src="img/ask.png" className="icon" />
              </p>
              <select className="Selects_left">
                <option value="0">110 V</option>
                <option value="1">120 V</option>
                <option value="2">127 V</option>
                <option value="3">230 V</option>
              </select>
              <p className="p_left">
                Area Disponible (*opcional) <img src="img/ask.png" className="icon" />
              </p>
              <input type="text" className="inputForm" />
            </div>
            <div className="datosInstalacion__areadisponible">
              <p className="p_left">
                Informacion Adicional en la instalacion <img src="img/ask.png" className="icon" />
              </p>
              <input type="radio" value="0" />
              <label>Habilitar informacion Adicional</label>
              <br />
              <input type="radio" value="0" />
              <label>Deshabilitar informacion Adicional</label>
            </div>
            <div className="seleccionUbicacion__botonBusqueda">
              <button>Crear Proyecto</button>
            </div>
          </div>
          <div className="rightAside">
            <div className="aside__container">
              <div className="aside__header">
                <p>Resumen de proyecto</p>
              </div>
              <div className="aside__body">
                <div className="aside__status">
                  <p> Datos necesarios</p>
                  <div className="perc">25%</div>
                  <div className="perc">50%</div>
                  <div className="perc">75%</div>
                  <div className="perc">100%</div>
                </div>
                <div className="aside__proyectTitle"></div>
                <div className="aside__placeinfo"></div>
                <div className="aside__consumption"></div>
                <div className="aside__electricFeats"></div>
              </div>
            </div>
          </div>
        </div>
        <div className="Footer">
          <p className="p_left">EXIA</p>
          <p className="p_left">Tutoriales</p>
          <p className="p_left">Data</p>
        </div>
      </div>
  );
}

export default App;


