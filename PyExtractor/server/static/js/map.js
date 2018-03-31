
var map, marker,map2,marker2,gl, gl2, myarr=[];

window.onload=function () {
    
    function initialize(){

        map = L.map('map',{ 
            maxBounds:[ [0, 30], [60,120] ],
            minZoom: 1
        });

        // map2 = L.map('map2',{ 
        //     maxBounds:[ [5, 60], [40,100] ],
        //     minZoom: 1
        // });

        gl = L.mapboxGL({
            accessToken: '{token}',
            // style: 'https://openmaptiles.github.io/osm-bright-gl-style/style-cdn.json'
            // style: 'js/style-cdn.json'
            style:'http://localhost:8080/styles/klokantech-basic/style.json'
        
        }).addTo(map);

        // gl2 = L.mapboxGL({
        //     accessToken: '{token}',
        //     // style: 'https://openmaptiles.github.io/osm-bright-gl-style/style-cdn.json'
        //     // style: 'js/style-cdn.json'
        //     style:'http://localhost:8080/styles/klokantech-basic/style.json'        
        // }).addTo(map2);

        // map = map.fitWorld();    
        map = map.locate({setView: true, maxZoom: 5}); 
        marker = L.marker([13.0108, 74.7943]).addTo(map);
        
    }
    initialize();
    
    
    //map.panTo(new L.LatLng(40.737, -73.923));
    //map.setView(new L.LatLng(40.737, -73.923), 8);
    //map.setView(latlng, map.getZoom(), { animation: true });
    // var popup = L.popup()
    //         .setLatLng([23.0225, 72.5714])
    //         .setContent("Hello Ahmedabad")
    //         .openOn(map);
    
    // Get Latitude and longitude
    map.on('click', function(e) {
        // alert("Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng)
        onLocationfound(e);
    });
    
    // var marker = L.marker([13.0108, 74.7943]).addTo(map);
    onLocationfound = function(e){
        marker.setLatLng(e.latlng);
        map.setView(marker.getLatLng(),map.getZoom(), { animation: true });
        // map2.setView(marker.getLatLng(),map.getZoom(), { animation: true });
        // alert('Marker has been set to position :' + marker.getLatLng().toString());
        console.log(e.latlng)
        document.getElementById('id_latitude').value = e.latlng.lat;
        document.getElementById('id_longitude').value = e.latlng.lng;
    };
    
    map.on('locationfound', onLocationfound);    
    marker.bindPopup("Your Location.").openPopup();  


};



function add(query){
    console.log((query));    
    myarr.push((query))
    // var mark = L.marker([myarr[3], myarr[4]]).addTo(map2);
    // mark.bindPopup(myarr[0]).openPopup();
    // marker = L.marker([13.0108, 74.7943]).addTo(map);
    // marker.bindPopup("Your Location.").openPopup(); 

}

function locate(){
    console.log(myarr);
    for(var i=0; i<myarr.length ;++i){
        console.log(myarr[i].latitude);

    var mark = L.marker([myarr[i].latitude, myarr[i].longitude]).addTo(map);
    // mark.bindPopup(myarr[0]).openPopup();
    // marker = L.marker([13.0108, 74.7943]).addTo(map);
    mark.bindPopup(myarr[i].img_name).openPopup(); 
    } 
}
    
