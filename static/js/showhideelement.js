var a;
function show_hide()
{
if(a==1)
{
document.getElementById("image").style.display="block";
document.getElementById("image2").style.display="block";
return a=0;
}
else 
{
document.getElementById("image").style.display="none";
document.getElementById("image2").style.display="none";
return a=1;
}
}