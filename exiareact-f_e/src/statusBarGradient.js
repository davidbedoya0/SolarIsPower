

export default function StatusBarGradient(props){
    return(
        <div className= "statusBarContainer">
            <p>
                Avance del Proyecto
            </p>
            <div className="statusBarGradientContainer">
                <div className="statusColor" style={{width:props.status + "%"}}>
                    <p className = "statusBar_info">
                        {props.status}%
                    </p>
                </div>
            </div>
        </div>
    );
}
