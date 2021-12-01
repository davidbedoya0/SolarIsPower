export default function InfoDisplay(props){
    /* InfoDisplay render a display that show info.
    It have 2 props,  */
    return(
        <div className = "InfoDisplay">
            <p>{props.infoTitle}</p>
            <p>{props.infoData}</p>
        </div>
    );
}