const arr =  ['MOTHER', 'FATHER', 'BROTHER', 'SISTER', 'HI', 'BYE']
  
var i = 0;

function next() {
if (i != 5) {
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
