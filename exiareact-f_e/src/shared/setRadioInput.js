import { useState } from "react";
import askLogo from "../img/ask.png"

export default function SetRadioInput(props){

    const[state, infoShow] = useState(false);
    const[radState, radToggle] = useState(false);

    const activeInfo = ()=>{
        infoShow(true);
    }
    const disableInfo = ()=>{
        infoShow(false);
    }

    let amSels = props.amount;
    let selOpt = props.options.split(",")
    let selVal = props.values.split(",")
    let selectData = [];
    
    if(selVal.length===selOpt.length){
        
        for(let i = 0; i < amSels; i++){
            selectData[i]={ opcionValue:null, opcionSelect:null}
            selectData[i].opcionSelect = selOpt[i];
            selectData[i].opcionValue = selVal[i];
        }
    }

    return(
        <div className= "radioContainer">
            <p className="textoInputs-Selects">
                {props.selTitle} <img src={askLogo} className="icon" onMouseOver={activeInfo} onMouseOut={disableInfo}/>
                <div className={
                    state ? "ableInfoPop infoPop":"disableInfoPop infoPop"
                }>  
                    {state ? props.children:""}
                </div>
            </p>
            <div className= "radioInputContainer">
                {props.children}
            </div>
        </div>
    );
}