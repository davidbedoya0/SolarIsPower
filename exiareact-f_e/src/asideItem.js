export default function AsideLeft__Item(props){

    return(
        <div className="leftAside__Item" id={props.idit}>
            <p>
                {props.title}
            </p>
        </div>
        
    );
}