function get_bnumber() {
  var dds = document.getElementsByTagName('dd');
  for (dd of dds) { 
    var matches = (dd.innerText).match(/NYPL catalog ID \(B-number\): (.*)/);
    if (matches) { return matches[1]} 
  }
}
var request = new XMLHttpRequest();
request.open('GET', 'https://127.0.0.1:8443/item/b12170768', false);
request.send(null);
var timeline = document.getElementById('timeline-container');
var child = document.createElement('div');
child.innerHTML = request.responseText;
timeline.appendChild(child);

// javascript:(function()%7Bfunction%20get_bnumber()%20%7Bvar%20dds%20%3D%20document.getElementsByTagName('dd')%3Bfor%20(dd%20of%20dds)%20%7Bvar%20matches%20%3D%20(dd.innerText).match(%2FNYPL%20catalog%20ID%20%5C(B-number%5C)%3A%20(.*)%2F)%3Bif%20(matches)%20%7B%20return%20matches%5B1%5D%7D%7D%7Dvar%20request%20%3D%20new%20XMLHttpRequest()%3Brequest.open('GET'%2C%20'https%3A%2F%2F127.0.0.1%3A8443%2Fitem%2Fb12170768'%2C%20false)%3Brequest.send(null)%3Bvar%20timeline%20%3D%20document.getElementById('timeline-container')%3Bvar%20child%20%3D%20document.createElement('div')%3Bchild.innerHTML%20%3D%20request.responseText%3Btimeline.appendChild(child)%7D)()
