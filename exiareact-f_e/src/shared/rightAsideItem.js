

export default function RightAsideItem(props){
    return(
        <div className= "righAsideItemContainer">
            <p className="rightAsideItemTitle">
                {props.itemTitle}
            </p>
            <p className="rightAsideItemValue">
                {props.value}
            </p>
        </div>
    );
}
