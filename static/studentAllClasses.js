const MAINURL = "http://127.0.0.1:5000"

function editEnrollment(student_id, class_id, changeType, className){
    var request = new XMLHttpRequest();
    request.open("POST", MAINURL+"/"+changeType+"Class", true);
    request.setRequestHeader("Content-Type", "application/json");

    var requestBody = {
        "student_id":Number(student_id),
        "class_id":Number(class_id)
    };

    request.send(JSON.stringify(requestBody));

    request.onload = function(){
        if(changeType == "drop"){
            alert("Dropped class: " + className);
        }
        else if(changeType == "join"){
            alert("Joined class: " + className);
        }
        location.reload();
    }

}