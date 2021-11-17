/*

Crear un sistema que permita visualizar los datos de los alumnos, 
y cuando pueden ser asignados.

Interfaz agradable y atractiva
Debe contener los datos de manera estructurada
El profesor puede seleccionar en cual de las 2 semanas agenda al  alumno
Si el profesor confirma, los datos se deben actualizar y reemplazar
el espacio asignado por el profeso.

*/

const alumnosBar = document.querySelector(".barraAlumnos")
const calendario = document.querySelector(".contenedor__Horario")
const boton = document.querySelector(".boton");


const alumnosName = ["maria", "tomas", "daniel", "camila", "pedro"];
const dias = ["Lunes","Martes","Miercoles","Jueves","Viernes",]
const alumnos = [];
const calendarioArr = [];
const vectClass = [];
let counter = 0;

function comprobarSeleccion(){
    for(let i = 0; i < alumnos.length; i++){
        vectClass[i] = alumnos[i].classList.contains("Alumnos_Box_select");
    }
    let index = vectClass.indexOf(true);
    return [vectClass.reduce((a, b) => a | b), index];
}


function alumnosBox(alumnos){
    for(let i = 0; i < alumnosName.length; i++){
        alumnos[i] = document.createElement("DIV");
        alumnosBar.appendChild(alumnos[i]);
        alumnos[i].classList.add("Alumnos_Box");
        alumnos[i].innerHTML = alumnosName[i];
        alumnos[i].addEventListener("click",(event)=>{
            let ot;
            let flag;
            [flag, ot] = comprobarSeleccion();
            if(!flag){
                alumnos[i].classList.add("Alumnos_Box_select");
            }
        })
        
    }
}

function calendar(){
    let i = 0;
    let j = 1;
    let k = 1;
    while( i < 40){
        calendarioArr[i] = document.createElement("DIV");
        calendario.appendChild(calendarioArr[i]);
        calendarioArr[i].style.gridColumn = `${j} / ${j + 1}`;
        calendarioArr[i].style.gridRow = `${k} / ${k + 1}`;
        
        if(k == 1){
            calendarioArr[i].innerHTML = dias[j - 1];
            calendarioArr[i].classList.add('horario__Header');
        }
        else{
            calendarioArr[i].classList.add('horario_Box');
            calendarioArr[i].addEventListener("click",(event)=>{
                let ot;
                let flag;
                [flag, ot] = comprobarSeleccion();
                if(flag){
                    event.currentTarget.style.backgroundColor = '#090';
                    event.currentTarget.innerHTML = alumnos[ot].innerHTML;
                    alumnos[ot].classList.remove("Alumnos_Box_select");
                    alumnosBar.removeChild(alumnos[ot]);
                    counter += 1;
                    if(counter==alumnos.length){
                        boton.style.visibility = "initial";
                    }
                }
            })
        }
        i++;
        k++;        
        if(k == 9){
            k = 1;
            j++;    
        }
    }
        
}

boton.addEventListener("click", (event)=>{
    alert("Envio de datos exitoso");
})

alumnosBox(alumnos);
calendar();


