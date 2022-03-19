<script
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA2wZe6-CgWyeoEJha5aeZLQp-cpn4kb8k&libraries=places&callback=initMap">
</script>


//CREATES AND EMBEDS MAP
var mylatlng = {
    lat: 1.3343,
    lng: 103.8563,
}

var mapOptions = {
    center: mylatlng,
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP
}

var map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);

//Creating a Directions Service Object to use the route method
var directionsService = new google.maps.DirectionsService();

//Creating a DirectionsRenderer object
var directionsDisplay = new google.maps.DirectionsRenderer();

//binding the directionDisplay to the Map
directionsDisplay.setMap(map)
