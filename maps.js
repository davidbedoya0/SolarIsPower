function initMaps(){
    var coord = {
        lat : 4.615,
        lng:-74.069
    };
    var map = new google.maps.Map(document.getElementById("map"),{
        zoom:10,
        center:coord
    });
}