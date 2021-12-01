import SubSubSectionTitle from "./subSubSectionTitle";
export default function SubSection(props){
    
    return(
        <div className="SubSubSec">
            <SubSubSectionTitle content = {props.subsubsectiontitle}/>
            <div className = {props.SectionContentStyles}>
                {props.children}
            </div>            
        </div>
        
    );
}