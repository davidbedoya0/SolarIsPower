export default function AsideLeft__Item(props){
    
    return(
        <div className="leftAside__Item" id={props.idit} onClick={()=>{props.setPaginaActualState(props.opt)}}>
            <p>
                {props.title}
            </p>
        </div>
        
    );
}