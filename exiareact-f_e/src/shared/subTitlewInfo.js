import { useState } from "react";
import askLogo from "../img/ask.png"

export default function SubTitleInfo(props){

    const[infostate, infoShow] = useState(false);

    const activeInfo = ()=>{
        infoShow(true);
    }
    const disableInfo = ()=>{
        infoShow(false);
    }

    return(
        
        <h3 className="textoInputs-Selects">
            {props.selTitle} <img src={askLogo} className="icon" onMouseOver={activeInfo} onMouseOut={disableInfo}/>
            <div className={
                infostate ? "ableInfoPop infoPop":"disableInfoPop infoPop"
            }>  
                {infostate ? props.children:""}
            </div>
        </h3>
        
    );
}