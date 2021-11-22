export default function Inputvariable(props){

    return(
        <div className= "inputContainer">
            <p className = "inputTitle">
                {props.inptitle}
                <img src={props.imgsrc} className ="icon" />
            </p>
            <input type = "text" className = "input_Box" placeholder = {props.plcholder}/>
        </div>
    );
}
