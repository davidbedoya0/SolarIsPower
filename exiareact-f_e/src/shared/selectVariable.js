import { useState } from "react";
import askLogo from "../img/ask.png"

export default function Selectvariable(props){

    const[state, setState] = useState(false);
    const enableHelp = ()=>{
        setState(true);
    }

    const disableHelp = ()=>{
        setState(false);
    }

    let amSels = props.selects;
    let selValue = props.selValues.split(",")
    let selOpt = props.selOpt.split(",")
    let selectData = [];
    
    if(selValue.length===selOpt.length){
        
        for(let i = 0; i < amSels; i++){
            selectData[i]={ valorSelect:null, opcionSelect:null}
            selectData[i].valorSelect = selValue[i]
            selectData[i].opcionSelect = selOpt[i];
        }
    }

    return(
        <div className= "selectContainer">
            <p className="textoInputs-Selects">
                {props.selTitle} <img src={askLogo} className="icon" onMouseOut={disableHelp} onMouseOver={enableHelp} />
                <div className={
                    state ? "ableInfoPop infoPop":"disableInfoPop infoPop"
                }>
                    {state ? props.children:""}
                </div>
            </p>
            
            <select className = "selectBox" >
                {selectData.map(dataSel =>
                    <option value = {dataSel.valorSelect}>{dataSel.opcionSelect}</option>
                    )
                }
            </select>
        </div>
    );
}