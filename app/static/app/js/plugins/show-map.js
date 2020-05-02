function set(img) {
    console.log("hello");
    console.log(img)
    document.getElementById('map-img').src = img;
}
function restoreMap() {
    console.log("hlooo");
    document.getElementById('map-img').src = "{% static 'app/images/map.png' %}";
}
function goMainPage(cityCode) {

    //alert(url);
    console.log("HELOO");
    var langType = '0';
    var url = '/Sodai/V2Main/' + cityCode + '/0';

    //url = '/Sodai/V2RecMail/13121/' + langType +'/0/0/-';
    window.location.href = url;
}