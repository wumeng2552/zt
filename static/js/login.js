window.onload = () => {
    document.getElementById("password").onkeydown = (e) => {
        if(e.keyCode === 13) {
            console.log(e.keyCode)
            app_login()
        }
    }
}

function app_login () {
    // console.log(111111111111)
    var tenantcode = document.querySelectorAll('#tenantcode')[0].value,   //获得选中的值
        environment = document.querySelectorAll('#environment')[0].value,   //获得选中的值
    // var tenantcode = $("#tenantcode option:selected").val();   //获得选中的值
    //     console.log(tenantcode)
    // var environment = document.querySelectorAll("#environment")[0].value;  //获得选中的值
    // var environment = $("#environment option:selected").val();   //获得选中的值
    //     console.log(environment)
        user = document.getElementById("user").value,
        password = document.getElementById("password").value
    if (tenantcode != '' & environment != '' & user != '' & password != '') {
        setTimeout(function () {
            $.ajax({
                type: "post",
                url: "/tool/AutoAppLogin",
                dataType: "json",
                data: {
                    "tenantcode" : tenantcode,
                    "environment": environment,
                    "user": user,
                    "password": password,
                },
                success: function (data) {
                    const message=confirm("你需要打开移动端吗？" + data["data"]["returnMsg"]);
                    if(message==true)
                    {
                        // var  newTab=window.open('about:blank', 'height=5','width=5');
                        var  newTab=window.open('about:blank'); 
                        newTab.location.href = data["data"]["returnMsg"];
                        // window.open('"'+data["data"]["returnMsg"]+'"');
                    }
                   else if(message==false) {}
                    alert(data["data"]["returnMsg"]);

                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    document.getElementById("req").value = XMLHttpRequest.statusText + " " + XMLHttpRequest.status + ":\n" + XMLHttpRequest.responseText
                    layer.close(loading)
                }
            });
        });
    }
};





