import { useState } from "react";

export default function Inputvariable(props){
    const [state, setState] = useState(0);
    const enableHelp = ()=>{
        setState(true);
    }

    const disableHelp = ()=>{
        setState(false);
    }

    return(
        <div className= "inputContainer">
            <p className = "inputTitle">
                {props.inptitle}
                <img src={props.imgsrc} className ="icon helpIcon" onMouseOver={enableHelp} onMouseOut={disableHelp}/>
                <div className={
                    state ? "ableInfoPop infoPop":"disableInfoPop infoPop"
                }>  
                    {state ? props.children:""}
                </div>
            </p>
            <input type = "text" className = "input_Box" placeholder = {props.plcholder}/>
        </div>
    );
}
