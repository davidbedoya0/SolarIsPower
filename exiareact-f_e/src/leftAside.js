export default function Leftaside(props){
    

    return(
        <div className="leftAside">
            <div className="leftAside__Header">
                <p>
                    Etapas
                </p>
            </div>
            {props.children}
        </div>
    );
}