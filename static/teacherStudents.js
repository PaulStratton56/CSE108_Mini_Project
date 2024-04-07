const MAINURL = "http://127.0.0.1:5000"

function setGrade(student_id, class_id, gradeInput){
    var request = new XMLHttpRequest();
    request.open("POST", MAINURL+"/setGrade/"+String(student_id)+"/"+String(class_id));
    request.setRequestHeader("Content-Type", "application/json");

    var body = JSON.stringify({"grade":gradeInput.value});
    request.send(body);
}