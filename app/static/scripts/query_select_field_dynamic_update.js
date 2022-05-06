function create_request()
{
    let request = false;
    if (window.XMLHttpRequest)
    {
        request = new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        try
        {
             request = new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch (CatchException)
        {
             request = new ActiveXObject("Msxml2.XMLHTTP");
        }
    }
    return request;
}


function new_student_suggest_class()
{
    request = create_request();
    request.onreadystatechange = function();
    {
        if (request.readyState == 4)
        {
            let class_id = document.getElementById('class_id');
            class_id.parentNode.replaceChild(class_id, request.responseText);
        }
    }
    request.open("GET", url, true);
    request.send(null);
}


