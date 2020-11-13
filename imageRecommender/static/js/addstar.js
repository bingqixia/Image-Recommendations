
function addStar(obj) {
    if (obj.innerHTML == "取消关注") {
        obj.innerHTML = "添加关注";
        obj.setAttribute("class", "button2");
    } else {
        obj.innerHTML = "取消关注";
        obj.setAttribute("class", "button3");
    }      
}
