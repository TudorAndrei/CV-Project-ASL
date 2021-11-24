const arr =  ['mother', 'father', 'brother', 'sister', 'hi', 'maple', 'pear', 'you', 'one']
  
var i = 0;

function next() {
if (i != 8) {
    i++;
    return setNo();
} else {
    i = 0;
    return setNo();
}
}

function setNo() {
return document.getElementById("demo").innerHTML = arr[i];
}
