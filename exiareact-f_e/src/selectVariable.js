export default function Selectvariable(props){

    let amSels = props.selects;
    let params = "<select className=\"formularionuevoproyecto__tipodeproyecto--select\" id=\"selTypSyst\">"
    let selValue = props.selValues.split(",")
    let selOpt = props.selOpt.split(",")

    if(selValue.length==selOpt.length){
        for(let i = 0; i < amSels; i++){
            params = params + "<option value=\"" + selValue[i] + "\">" + selOpt[i] + "</option>"
        }
        params = params + "</selec>"
    }

    return(
        <div className= "selectContainer">
            <p className="textoInputs-Selects">
                {props.selTitle} <img src="img/ask.png" className="icon" />
            </p>
            
            <div dangerouslySetInnerHTML={{__html:params}}></div>
            
        </div>
    );
}