let i=0;
let arr=[];
// document.getElementById("search").addEventListener("onchange",function(){
//   for(let i=0;i<video.length;i++)
//     {
      
//         var v=video[i].getElementsByTagName("video");
//         var tags=video[i].getElementsByTagName("h3");
//         for(let j=0;j<v.length;j++)
//         {
//             if(arr[j]!=1)
//             {
//               v[j].style.display="block";
//               tags[j].style.display="block";
//             }
            
//         }   
//     }




// });
document.getElementById("btn").addEventListener("click",function(){

let text="manu";
let heading="jay";

text=document.getElementById("search").value;
let video=document.getElementsByClassName("c2");

for(let j=0;j<video.length;j++)
{
var tags=video[j].getElementsByTagName("h3");

for(let i=0;i<tags.length;i++)
{
heading=tags[i].textContent;
result=heading.includes(text);

if(result)
  arr[i]=1;
else
  arr[i]=0;
}
}

for(let i=0;i<video.length;i++)
{
  
    var v=video[i].getElementsByTagName("video");
    var tags=video[i].getElementsByTagName("h3");
    for(let j=0;j<v.length;j++)
    {
        if(arr[j]!=1)
        {
          v[j].style.display="None";
          tags[j].style.display="None";
        }
        else
          {
            v[j].style.display="block";
            tags[j].style.display="block";
          }
    }   
}
textl=document.createElement("li");
text1=document.createTextNode(document.getElementById("search").value);
textl.appendChild(text1);
document.getElementById("hlist").appendChild(textl);
console.log(arr);
});
